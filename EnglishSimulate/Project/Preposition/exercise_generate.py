# -*- coding: utf-8 -*-
import re
import os
import random

temp_text = """
1. Расскажи мне о своей семье. — Tell me about your family.
2. Он рассказал детям о своих приключениях. — Не told the children about his adventures.
3. О чем вы говорите? — What are you talking about?
4. Как насчет обеда? — What about dinner?
5. В этом нет сомнения. — There is no doubt about it.
6. Давайте погуляем по городу. — Let's walk about the town.
7. Дети разбросали игрушки по комнате. — The children left the toys about the room.
8. Дети танцевали вокруг ёлки. — The children were dancing about the New Year tree.
9. Вокруг него было много друзей. — There were a lot of friends about him.
10.	Там было приблизительно 100 человек. — There were about 100 persons there.
11.	Это стоит около 50 рублей. — It costs about 50 roubles.
12.	Я буду около 5 часов. — I'll be at about 5 o' clock.
13.	Я хочу жить около Москвы. — I want to live about Moscow.
14.	Он всегда носит с собой словарь. — Не has always his dictionary about him.

"""

pattern = r"(?P<num>\d{1,2})\.(?P<rus>.+?)\—(?P<eng>.+)"
temp_com = re.compile(pattern, re.S | re.M)
search_one = temp_com.search(temp_text)
findall = temp_com.findall(temp_text)

path_dir_for_exercise = r"Exercise"

def get_data_file(path_file):
    temp_list = []
    for str_i in open(path_file, encoding="utf-8", mode="r"):
        findall = temp_com.findall(str_i)
        if findall and len(findall[0]) == 3 :
            findall = findall[0]
            findall = [i.strip() for i in findall]
            temp_list.append(findall)
        else:
            print("Что-то не так")
            raise Exception("Что-то не так")
    return temp_list


def create_files(data_exersises, name_file):
    with open(name_file, encoding="utf-8", mode="w") as f:
        f.write(data_exersises)


temp_dict = {}
list_exersises = []
for file_i in os.listdir(path_dir_for_exercise):
    path_file = os.path.join(path_dir_for_exercise, file_i)
    name_preposition = file_i.split(".")[0]
    print("Предлог %s" % name_preposition)
    data_i = get_data_file(path_file)
    list_exersises.extend(data_i)
    temp_dict[name_preposition] = data_i

count = sum([len(val_i) for key_i, val_i in temp_dict.items()])
# перемешаем список
random.shuffle(list_exersises)
list_rus = []
list_eng = []
for i in list_exersises:
    list_rus.append(i[1])
    list_eng.append(i[2])


name_rus = "EXERCISE_RUS.txt"
name_eng = "EXERCISE_ENG.txt"

create_files("\n".join(list_rus), name_rus)
create_files("\n".join(list_eng), name_eng)
print()