# coding="utf-8"

import sqlite3 as sq
import os


def create_base(path_base):
    list_table = ["words_of_day", "words_of_template"]
    if os.path.isfile(path_base):
        return
    else:
        with sq.connect(path_base) as db:
            for table_name in list_table:
                sql = f"""
                    CREATE TABLE IF NOT EXISTS {table_name} (first_line TEXT, mnemo_text TEXT, examples TEXT, error TEXT)
                """
                cursor = db.cursor()
                cursor.executescript(sql)
                db.commit()


def into_table(path_base, data, table_name="words_of_day"):
    sgl = f"INSERT INTO {table_name} (first_line, mnemo_text, examples, error) VALUES (?, ?, ?, ?)"
    try:
        with sq.connect(path_base) as db_con:
            for data_i in data:
                cur = db_con.cursor()
                cur.execute(sgl, data_i)
    except sq.DatabaseError as err:
        print("Ошибка:", err)   

def fetchall(path_base, table_name="words_of_day"):
    sql = f"""
    SELECT first_line, mnemo_text, examples, error FROM {table_name}"""
    with sq.connect(path_base) as db:
        cur = db.cursor()
        res = cur.execute(sql)       
        return res.fetchall()

def clear_table(path_base, table_name="words_of_day"):
    sql = f"""
    DELETE FROM {table_name}"""
    with sq.connect(path_base) as db:
        cur = db.cursor()
        res = cur.execute(sql) 


