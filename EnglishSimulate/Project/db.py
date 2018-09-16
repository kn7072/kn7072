# coding="utf-8"
import sqlite3
import os
import shutil


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
        """

    with sqlite3.connect("work_db.db") as db:
        cur = db.cursor()
        cur.executescript(sql)
        db.commit()

if __name__ == "__main__":
    creata_work_base("core_word_base.db")


