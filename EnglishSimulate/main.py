# coding="utf-8"
import sqlite3


def create_table(name_db, name_table):
    try:
        con = sqlite3.connect(name_db)
        cur = con.cursor()
        sql = "CREATE TABLE IF NOT EXISTS {name_table} (word TEXT, num INTEGEG);"\
            .format(name_table=name_table)
        cur.execute(sql)
    finally:
        con.close()


def insert_database(path_to_base, name_table, data):
    try:
        con = sqlite3.connect(path_to_base)
        cur = con.cursor()
        sql = "INSERT INTO {name_table} VALUES (?, ?)".format(name_table=name_table)
        for data_i in data:
            cur.execute(sql, data_i)
    except sqlite3.DatabaseError as err:
        print("Ошибка:", err)
    else:
        con.commit()
    con.close()


def get_data(name_file):
    with open(name_file, encoding="utf-8") as f:
        data = f.read()
        list_ = data.split("\n")
        list_all = list(zip(list_[::2], list_[1::2]))
    return list_all


def get_data_2(name_file):

    def xxx(i):
        res = i.rsplit("\t", 1)
        if len(res) == 1:
            # значит разделитель не \t а пробел
            word, num = i.rsplit(" ", 1)
            word = word.strip()
            num = num.strip()
        else:
            word, num = res
            word = word.replace("\t", "").replace(" ", "")
            num = num.replace("\t", "").replace(" ", "")
        return word, num

    with open(name_file, encoding="utf-8") as f:
        data = f.read()
        list_ = data.split("\n")
        list_all = [xxx(i) for i in list_]
        # list_index = []
        # for ind, data_i in enumerate(list_all):
        #     try:
        #         i, j = data_i
        #     except:
        #         list_index.append(ind)
        #         continue
        # for i in list_index:
        #     data_i = list_all[i]
        #     list_all[i] = data_i[0].rsplit(" ", 1)
        # for i in list_all:
        #     print(i)
        # print()
    return list_all


def print_words(name_db, name_table):
    try:
        con = sqlite3.connect(name_db)
        sql = "SELECT word FROM {name_table}".format(name_table=name_table)
        cur = con.cursor()
        cur.execute(sql)
        res = cur.fetchall()
        for i in res:
            print(i[0])
    except sqlite3.DatabaseError as err:
        print("Ошибка:", err)
    else:
        con.commit()
    con.close()


name_db = "test.db"
if False:
    table_name = "WORDS_GARIBAN"
    create_table(name_db, table_name)
    data = get_data("test.txt")

table_name = "WORDS_GARIBAN_ALL"
create_table(name_db, table_name)
data = get_data_2("test_2.txt")

insert_database(name_db, table_name, data)
# print_words(name_db, table_name)

if __name__ == "__main__":
    print_words(name_db, table_name)



