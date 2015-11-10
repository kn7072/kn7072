# -*- coding:utf-8 -*-
import os
#import markdown
base_path = r'D:\git_hub_new\kn7072\exp_md_2\doc'
path_modules = base_path.replace('\doc', "")

text_menu = []
text_menu.append(['*    [doc](/doc/)\n', 0, 'doc'])#*    [&nbsp;](/doc/){: .menu_one }
local_text_menu = []
#path_doc = r'/doc/TEST/dir_1/dir_1_1/dir_1_1_1/doc_first/'  #three
path_doc =    r'/doc/TEST/'#dir_1/dir_1_1/dir_1_1_1/three/'
parent_menu = r'/doc/TEST/'  #TEST/dir_1/dir_1_1/dir_1_1_1dir_1_1//three/  r'/doc/TEST/'
open_menu_list = [
                   r'/doc/api/',
                  #r'/doc/TEST/',
                  #r'/doc/TEST/dir_1/',
                  r'/doc/TEST/dir_1/dir_1_2/',
                  #r'/doc/TEST/dir_1/dir_1_1/',
                  #r'/doc/TEST/dir_1/dir_1_1/dir_1_1_1/',
                  r'/doc/TEST/dir_1/dir_1_1/dir_1_1_1/three/']

def fun(row, clas='.menu_one'):
    split_row = row.split("*")
    split_row[1] = split_row[1].replace("\n", "").replace("\t", "")
    split_row[1] = split_row[1].strip()
    real_path = split_row[1].split("(/")[1].replace("/)", "")
    return real_path

def add_class(row):
    row_text = row[0].replace("\n", "").replace("\t", "").split("*")[1]
    row_path = row[2]
    real_path_dir = os.path.normpath(os.path.join(path_modules, row_path))
    # menu_open   menu_one
    if os.path.isdir(real_path_dir):
        real_path = "/%s/" % row[2]
        if real_path in open_menu_list:
            string = row[1]*"    " + '*    [&nbsp;](%s){: %s } ' % (real_path, '.menu_open') + row_text + "\n"
        else:
            string = row[1]*"    " + '*    [&nbsp;](%s){: %s } ' % (real_path, '.menu_one') + row_text + "\n"
    else:
        string = row[1]*"    " + '*    [&nbsp;](#){: .document }' + row_text + "\n"
    return string

def active_doc(doc_or_dir):
    xxx = os.path.join(path_modules, os.path.normpath(doc_or_dir))
    list_dirs = xxx.split("\\")
    count_dirs = len(list_dirs)
    index_doc = list_dirs.index('doc')
    count = len(doc_or_dir.split("/"))
    for i in reversed(range(count)):
        current_path = xxx.rsplit("\\", i)[0]
        parent_menu_relative = '(%s)' % parent_menu
        if os.path.isdir(current_path):
            # если текущий путь указывает на католог то читаем его меню и берем из него нужную информицию
            menu_for_cat = current_path + "\menu.md"
            local_text_menu = [x for x in open(menu_for_cat, encoding='utf-8') if x != '\n']
            # если сдедующий елемент пути тоже указывает на католог - то из меню текущего каталога берем только одну строчку
            # указывающую на каталог ниже
            index_next = i - 1
            if index_next >= 0:
                next_path = xxx.rsplit("\\", i-1)[0]
                if os.path.isdir(next_path):
                    # если следующий элемент католог
                    search_path = '(/%s/)' % doc_or_dir.rsplit('/', i-1)[0]
                    # находим теперь строку содержащую search_path в меню текущего каталога current_path
                    # берем только одну строку
                    for s in local_text_menu:
                        if search_path in s:
                            # строка s указывает на каталог - вешаем нужные стили
                            # если index_next = 0 значит это последний элемент пути и одновременно католог - значит нужен
                            # отступ
                            if index_next == 0:
                                #open_dir = "    " + fun(s, '.menu_open')
                                text_menu.append([s, 1, fun(s)])
                                # читаем содержимое меню(последнего меню index_next = 0) и добавляем еще отступы
                                last_path_menu = next_path + "\menu.md"
                                last_text_menu = [x for x in open(last_path_menu, encoding='utf-8') if x != '\n']
                                for j in last_text_menu:
                                    #string_menu = "        " + j#fun(j)
                                    text_menu.append([j, 2, fun(j)])
                            else:
                                text_menu.append([s, 0, fun(s)])
                else:
                    # если следующий элемент файл - значит нужно забирать из меню по адресу - current_path все сожержимое
                    # правило таково, если путь указывает на документ - то раскрывается содержимое меню - описывающее
                    # все содержимое каталога в котором находится файл (если документ находится в каталоге dir_1 то нужно
                    # найти menu.md в этом каталоге и забрать все содержимое файла menu.md)
                    # добавим последниму элементу отспуп - если текущий путь указывает на файл, то предыдущий на каталог
                    text_menu[-1][0] = 1
                    for j in local_text_menu:
                        #string_menu = "        " + j#fun(j)
                        text_menu.append([j, 2, fun(j)])
# находим минимальный путь - от него будем отталкиваться
def sort_path (j):
    return j[1]

sort_open_menu_list = [[x, len(x.split("\\"))] for x in open_menu_list]
sort_open_menu_list = sorted(sort_open_menu_list, key=sort_path)
sort_open_menu_list = [r[0] for r in sort_open_menu_list]

first_path = sort_open_menu_list[0][1:-1]
active_doc(first_path)

for path in sort_open_menu_list[1:]:
    #path = '/doc/TEST/dir_1/dir_1_1/dir_1_1_1/three/'
    print(path)
    doc_or_dir = path[1:-1]
    count = len(doc_or_dir.split("/"))

    path_menu = os.path.join(path_modules, os.path.normpath(doc_or_dir)) + "\menu.md"
    for j in range(count):
        # ищем максимально близкий путь из меню text_menu который сооветствует пути меню которое необходимо добавить
        # к существующему меню
        f = False
        max_path = doc_or_dir.rsplit("/", j)[0]
        for row in text_menu:
            if max_path == row[2]:
                # запоминаем индекс строки после которой нужно добавлять меню по адресу
                f = True
                index = text_menu.index(row)
                if j == 0:
                    # оказалось что меню которую нужно развернуть совпадает с строкой из меню созданного ранее
                    # значит найденой строке нужно увеличить отступ на единицу, а ниже к списку добавить все содержание
                    # этого меню с отступом на два больше отступа найденой строки из ранее постороенного меню
                    if os.path.isfile(path_menu):
                        local_menu_list = [x for x in open(path_menu, encoding='utf-8') if x != '\n']
                        indent_row = text_menu[index][1]
                        #text_menu[index][1] = text_menu[index][1] + 1
                        # присоединяем содержимое меню local_menu_list ниже
                        index = index + 1
                        count_add_element = len(local_menu_list)
                        for t in range(count_add_element):
                            text_menu.insert(index + t, [local_menu_list[t], indent_row+1, fun(local_menu_list[t])])
                        break
                else:
                    # сюда мы попадаем когда между уже постороенным меню и меню которое нужно добавить существуют
                    #  несколько дополнительных элементов(каталог)
                    # для начала разберемся на кого укззывает путь path_menu если файл существует то то это каталог

                    def super_(x, y):
                        xxx = os.path.join(path_modules, os.path.normpath(x))
                        text_menu = []
                        z = x.replace(y, "")
                        ii = 1
                        l = [i for i in z.split("/") if i]
                        count = len(l) + 1
                        for i in reversed(range(count)):
                            current_path = xxx.rsplit("\\", i)[0]
                            if os.path.isdir(current_path):
                                # если текущий путь указывает на католог то читаем его меню и берем из него нужную информицию
                                menu_for_cat = current_path + "\menu.md"
                                local_text_menu = [x for x in open(menu_for_cat, encoding='utf-8') if x != '\n']
                                # если сдедующий елемент пути тоже указывает на католог - то из меню текущего каталога берем только одну строчку
                                # указывающую на каталог ниже
                                index_next = i - 1
                                if index_next >= 0:
                                    next_path = xxx.rsplit("\\", i-1)[0]
                                    if os.path.isdir(next_path):
                                        # если следующий элемент католог
                                        search_path = '(/%s/)' % doc_or_dir.rsplit('/', i-1)[0]
                                        for s in local_text_menu:
                                            if search_path in s:
                                                # строка s указывает на каталог
                                                # если index_next = 0 значит это последний элемент пути и одновременно католог - значит нужен
                                                # отступ
                                                if index_next == 0:
                                                    #open_dir = "    " + fun(s, '.menu_open')
                                                    text_menu.append([s, ii, fun(s)])
                                                    # читаем содержимое меню(последнего меню index_next = 0) и добавляем еще отступы
                                                    last_path_menu = next_path + "\menu.md"
                                                    last_text_menu = [x for x in open(last_path_menu, encoding='utf-8') if x != '\n']
                                                    for j in last_text_menu:
                                                        #string_menu = "        " + j#fun(j)
                                                        text_menu.append([j, ii+1, fun(j)])
                                                else:
                                                    text_menu.append([s, ii, fun(s)])
                                                    ii+=1
                        return text_menu
                    if os.path.isfile(path_menu):
                        local_menu_list = [x for x in open(path_menu, encoding='utf-8') if x != '\n']
                        indent_row = text_menu[index][1]
                        index = index + 1
                        # прежде чем добавлять меню path_menu необходимо достроить необходимое количество родителей
                        create_menu = super_(doc_or_dir, max_path)
                        count_add_element = len(create_menu)
                        for t in range(count_add_element):
                            add_row = create_menu[t][0]
                            add_indent = create_menu[t][1]
                            text_menu.insert(index + t, [add_row, indent_row+add_indent, fun(add_row)])
                    break
        if f:
            break

# собираем меню - волнующий момент
#www = [f[1]*"    " + f[0] for f in text_menu]
www = [add_class(f) for f in text_menu]
print()
#              text_menu
