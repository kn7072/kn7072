# coding="utf-8"
import sqlite3
import requests
import re
from lxml import etree


temp_all_word_page = r"wordlist-oxford3000 list-plain\">(?P<all_word_page>.*?)<\/ul>"
coml_all_word_page = re.compile(temp_all_word_page, flags=re.DOTALL)#re.VERBOSE |

temp_word = r"definition\">(?P<word>.+?)</a>"
compl_word = re.compile(temp_word)


db_name = "oxford.db"


def create_table():
    sgl_crate_table = """
    CREATE TABLE IF NOT EXISTS oxford (word TEXT ) -- UNIQUE
    """
    with sqlite3.connect(db_name) as db_con:
        cur = db_con.cursor()
        cur.executescript(sgl_crate_table)
        db_con.commit()

create_table()


def into_table(path_base, table_name, data):
    sgl = "INSERT INTO {name_table} VALUES (?)".format(name_table=table_name)
    try:
        with sqlite3.connect(path_base) as db_con:
            for data_i in data:
                cur = db_con.cursor()
                cur.execute(sgl, (data_i, ))
    except sqlite3.DatabaseError as err:
        print("Ошибка:", err)

list_temp = ["_A-B", "_C-D", "_E-G", "_H-K", "_L-N", "_O-P", "_Q-R", "_S", "_T", "_U-Z"]
url_oxford = r"https://www.oxfordlearnersdictionaries.com/wordlist/american_english/oxford3000/Oxford3000"
s = requests.Session()
s.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36'})

for i in list_temp:
    for j in range(1, 7):
        temp_link = url_oxford + i + "/?page=%s" % j
        all_html = s.get(temp_link).text
        search_all_words = coml_all_word_page.search(all_html)
        all_word_page_html = search_all_words.group("all_word_page")
        tr = all_word_page_html.replace("\n", "").replace(" ", "")
        if tr:
            print(temp_link)
            word_all = compl_word.findall(all_word_page_html)
            into_table(db_name, "oxford", word_all)
        else:
            print(j)
            break
    print()
print()




