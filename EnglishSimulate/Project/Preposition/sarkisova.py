# -*- coding: utf-8 -*-
import re
import os

pat_negative = r"(?![\.,\*0-9\)])"  # данных симполов быть не должно
pattern = r"^{num_start}{pat_negative}(?P<text_page>.+?)^{num_end}{pat_negative}"

temp_text = """
dddddddddddddddddddddddddddd
0   dddd
Л.Г. Саркисова
ПРЕДЛОГИ
на каждый день
Teach Yourself
Обучи себя сам
1
Издательство «Менеджер»
0. sdfsdfsdf
dsfsdfsd
1. sdfsdfsdf

"""
pattern_search = pattern.format(num_start=1, pat_negative=pat_negative, num_end=2)
temp_com = re.compile(pattern_search, re.S | re.M)
search_one = temp_com.search(temp_text)

findall = temp_com.findall(temp_text)

if search_one:
    print(search_one.group("text_page"))

path_flle_csv = r"Саркисова\Саркисова Л.Г.csv"
path_dir_for_pages = r"TEMP_PAGES"

def get_data_file(path_file):
    with open(path_file, encoding="utf-8", newline="\r\n", mode="r") as f:  # newline="\r\n",   mode="rb"
        return f.read()  # .decode("utf-8")

def create_page(file_name, data_page):
    path_temp = os.path.join(path_dir_for_pages, file_name)
    with open(path_temp, encoding="utf-8", mode="w") as f:
        f.write(data_page)

def create_pages(data_file, count_pages=334):
    for i in range(count_pages):
        next_num = i+1
        if next_num == 102:
            print()
        pattern_i = pattern.format(num_start=i, pat_negative=pat_negative, num_end=next_num)
        temp_com = re.compile(pattern_i,  re.S |re.M | re.A)  #
        findall = temp_com.findall(data_file)  # data_file
        if findall and len(findall) == 1:
            print(next_num)
            name_file_page = "%s.txt" % next_num
            data_i = findall[0].replace("\r", "")
            data_rows_not_empty = [row for row in data_i.split("\n") if row]
            data_rows_ind = [(row, row.endswith("-"), ind) for ind, row in enumerate(data_rows_not_empty)]

            temp = []
            list_ignore_ind = []
            count_list = len(data_rows_ind)
            for row, endswith_, ind in data_rows_ind:
                if ind not in list_ignore_ind:
                    if endswith_:
                        row_temp = row[:-1]
                        for j in range(ind+1, count_list):
                            row_j, endswith_j, ind_j = data_rows_ind[j]
                            if endswith_j:
                                row_temp += row_j[:-1]
                            else:
                                row_temp += row_j
                            list_ignore_ind.append(j)
                            if not endswith_j:
                                break
                        temp.append(row_temp)
                    else:
                        temp.append(row)
                else:
                    continue
            data_old = "\n".join(data_rows_not_empty)
            data_i = "\n".join(temp)
            create_page(name_file_page, data_i)
            create_page("%s_OLD.txt" % next_num, data_old)
        else:
            for i in findall:
                print(i)
                print("#"*50)
            print("Всего найдено - %s, страница %s" % (len(findall), next_num))
            raise Exception("Не обнаружили страницу %s" % next_num)


data_file = get_data_file(path_flle_csv)
create_pages(data_file)
