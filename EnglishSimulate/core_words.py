# coding="utf-8"
import sqlite3


def get_data(path_base, table_name, column_name):
    try:
        with sqlite3.connect(path_base) as con:
            cur = con.cursor()
            sql = """
            SELECT {column_name} FROM {table_name};
            """.format(column_name=column_name, table_name=table_name)
            res = cur.execute(sql)
            all = res.fetchall()
            if all:
                all = [i[0] for i in all]
            return all
    except sqlite3.DatabaseError as err:
        print("Ошибка ", err)


word_oxford = set(get_data("oxford.db", "oxford", "word"))
word_garib = set(get_data("test.db", "WORDS_GARIBAN_ALL", "word"))
word_sanstv = set(get_data("sanstv.db", "sanstv", "word"))


diff_garib_xford = word_garib - word_oxford
diff_garib_sanstv = word_garib - word_sanstv
union_sanstv_oxford = word_sanstv | word_oxford | word_garib

intersection_sanstv_oxford_gari = word_sanstv & word_oxford & word_garib
print(len(intersection_sanstv_oxford_gari))
print()
