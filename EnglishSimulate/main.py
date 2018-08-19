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
table_name = "WORDS_GARIBAN"
create_table(name_db, table_name)
data = get_data("test.txt")
insert_database(name_db, table_name, data)
print_words(name_db, table_name)

if __name__ == "__main__":
    print_words(name_db, table_name)



