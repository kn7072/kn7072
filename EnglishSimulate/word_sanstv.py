# coding="utf-8"
import requests
import sqlite3
import re


def crate_table(path_db, table):
    with sqlite3.connect(path_db) as db:
        sql = """
        CREATE TABLE IF NOT EXISTS {table} (word TEXT)
        """.format(table=table)
        cur = db.cursor()
        cur.execute(sql)


def into_table(path_db, name_table, data):
    with sqlite3.connect(path_db) as db:
        sql = """
        INSERT INTO {name_table} VALUES (?)
        """.format(name_table=name_table)
        try:
            for data_i in data:
                cur = db.cursor()
                cur.execute(sql, (data_i,))
        except sqlite3.DatabaseError as err:
            print("Ошибка:", err)


db_name = "sanstv.db"
crate_table(db_name, "sanstv")

all_text = r"<tr>(?P<info_word>.+?)<\/tr>"
compile_all_test = re.compile(all_text, re.DOTALL)

word_one = r"target='_blamk' tabindex='-1'>(?P<word>.+?)<"
complite_word = re.compile(word_one, re.DOTALL)

url = r"https://sanstv.ru/english_words"
s = requests.Session()
s.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36'})
all_html = s.get(url).text

search_all = compile_all_test.findall(all_html)


list_word = []
if search_all:
    for word_i in search_all:
        search_word = complite_word.search(word_i)
        if search_word:
            word = search_word.group("word")
            if word:
                list_word.append(word)
                # print("#"*30)
                # print(word_i)

into_table(db_name, "sanstv", list_word)
print()