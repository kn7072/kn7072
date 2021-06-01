# coding="utf-8"

import sqlite3 as sq
import os


def create_base(path_base):
    if os.path.isfile(path_base):
        return
    else:
        with sq.connect(path_base) as db:
            sql = """
                CREATE TABLE IF NOT EXISTS words_of_day (first_line TEXT, mnemo_text TEXT, examples TEXT, error TEXT)
            """
            cursor = db.cursor()
            cursor.executescript(sql)
            db.commit()


def into_table(path_base, data):
    sgl = "INSERT INTO words_of_day (first_line, mnemo_text, examples, error) VALUES (?, ?, ?, ?)"
    try:
        with sq.connect(path_base) as db_con:
            for data_i in data:
                cur = db_con.cursor()
                cur.execute(sgl, data_i)
    except sq.DatabaseError as err:
        print("Ошибка:", err)   

def fetchall(path_base):
    sql = """
    SELECT first_line, mnemo_text, examples, error FROM words_of_day"""
    with sq.connect(path_base) as db:
        cur = db.cursor()
        res = cur.execute(sql)       
        return res.fetchall()

def clear_table(path_base):
    sql = """
    DELETE FROM words_of_day"""
    with sq.connect(path_base) as db:
        cur = db.cursor()
        res = cur.execute(sql) 


