# coding="utf-8"
import sqlite3
import os
import shutil
from datetime import datetime
COUNT_REPEAT = 5


def creata_work_base(path_base):
    """
    Если существует work_db.db, значит обучение начато - выходим
    Если базы work_db.db нет, значит копируем базу path_base и расширяем таблицу
    :param path_base:
    :return:
    """

    if os.path.isfile("work_db.db"):
        return
    if os.path.isfile(path_base):
        shutil.copyfile(path_base, "work_db.db")
    else:
        raise Exception("Не удалось скопировать базу %s" % path_base)
    # На данном этапе база скопирована и необходимо расширить таблицу полями: состояние
    sql = """
        ALTER TABLE core_word_base ADD COLUMN know INTEGER DEFAULT 0;

        ALTER TABLE core_word_base ADD COLUMN repeat INTEGER DEFAULT 5;

        ALTER TABLE core_word_base ADD COLUMN data TEXT DEFAULT NONE;

        ALTER TABLE core_word_base ADD COLUMN count INTEGER DEFAULT 0;
        """

    with sqlite3.connect("work_db.db") as db:
        cur = db.cursor()
        cur.executescript(sql)
        db.commit()


def query_sql(sql):
    with sqlite3.connect("work_db.db") as db:
        cur = db.cursor()
        res = cur.execute(sql)
        return res.fetchall()


def my_factory(c, r):
    d = {}
    for i, nаme in enumerate(c.description):
        d[nаme[0]] = r[i]  # Ключи в  виде названий полей
        d[i] = r[i]  # Ключи в  виде индексов полей
    return d


def updata_base(res):
    """
    https://stackoverflow.com/questions/7831371/is-there-a-way-to-get-a-list-of-column-names-in-sqlite
    cur.execute("SELECT * FROM core_word_base")
    col_name_list = [tuple[0] for tuple in cur.description]

    :param res:
    :return:
    """

    know = 0
    res = {key: value[0].decode() for key, value in res.items()}
    sql_info_word = """
    SELECT * FROM core_word_base WHERE word='{word}'
    """.format(word=res["word"])

    data_now = datetime.strftime(datetime.now().date(), '%d.%m.%Y')
    sql_updata = """
    UPDATE core_word_base SET know='{know}', repeat='{repeat}', data='{data}', count='{count}' WHERE word='{word}'
    """

    with sqlite3.connect("work_db.db") as db:
        db.row_factory = my_factory
        cur = db.cursor()
        info_word_db = cur.execute(sql_info_word).fetchone()
        count = info_word_db["count"]
        if int(res["know"]):
            if count == 0:
                know = 1
                repeat = 0
                count = 1
            else:
                # слово написано(переведено или услышано) верно
                repeat = info_word_db["repeat"] - 1
                repeat = repeat if repeat > 0 else 0
                count += 1
                if repeat == 0:
                    know = 1
        else:
            repeat = info_word_db["repeat"] + 1
            count += 1
            repeat = repeat if repeat <= COUNT_REPEAT else COUNT_REPEAT
        sql_updata = sql_updata.format(know=know, repeat=repeat, data=data_now, word=res["word"], count=count)
        cur.execute(sql_updata)

def crate_file_base(name_db, name_table):
    sql = "SELECT id, num_word_garibyan, word, translate, transcription FROM {name_table}".format(name_table=name_table)
    with sqlite3.connect(name_db) as db:
        cur = db.cursor()
        res = cur.execute(sql)
        with open("bakap.csv", "w", encoding="utf-8") as f:
            for i in res.fetchall():
                f.write(";".join(map(str, i))+";\n")
                #print()
        #return res.fetchall()

if True:
    crate_file_base("core_word_base.db", "core_word_base")

if __name__ == "__main__":
    creata_work_base("core_word_base.db")


