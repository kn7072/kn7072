# -*- coding: utf-8 -*-
import os
import re
import json
# https://regex101.com/
# https://habr.com/ru/post/349860/

temp_all_exercise = "Упражнение\s*?(?P<num_exercise>[0-9]+)(?P<exercise>.+?)(?=Упражнение)"
compl_1 = re.compile(temp_all_exercise, flags=re.DOTALL)

temp_exercise = "(?P<text>[0-9]+?\..+?)(?=\s[0-9]{,2}?\.)"
compl_2 = re.compile(temp_exercise, flags=re.DOTALL)

path_dir = "files_source"
path_file_exercise = os.path.join(path_dir, "exercise")
path_file_answer = os.path.join(path_dir, "answer")
list_bracket = [1, 2, 5, 6, 9, 10, 13, 14, 18, 19, 22, 23, 27, 28, 31, 32, 36, 37, 40, 41, 45, 46, 50, 51, 55, 56, 60,
                61, 65, 66, 69, 70]
list_rus_eng = [4, 8, 12, 16, 21, 25, 30, 34, 39, 43, 48, 53, 58, 63, 68, 72]
list_eng_rus = [3, 7, 11, 15, 20, 24, 29, 33, 38, 42, 47, 52, 57, 62, 67, 71]

def get_data_file(path_file):
    with open(path_file, mode="r", encoding="utf-8") as f:
        return f.read()

def parse_data(data):
    dict_temp = {}
    search = re.findall(compl_1, data)
    for num_exercise_i, exercise_i in search:
        # чтобы шаблон работал правильно - добавим в конец строки 99.
        exercise_i += " 99."
        search_exercise = re.findall(compl_2, exercise_i)
        search_mod = [i.replace("-\n", "").replace("\n", " ").strip() for i in search_exercise]
        dict_temp[num_exercise_i] = search_mod
    return dict_temp
    # assert len(search_mod) % 2 == 0, "Должно быть четным"
    # return search_mod

def assert_exercise_answers(data_exercise, data_answers):
    list_error = []
    for num_exercise_i, value_i in data_exercise.items():
        data_answer_i = data_answers[num_exercise_i]
        if len(value_i) != len(data_answer_i):
            list_error.append([num_exercise_i, len(value_i), len(data_answer_i)])
    if list_error:
        for i in list_error:
            print(i)

def join_objects(data_exercise, data_answers):
    obj = {}
    for num_exercise_i, value_i in data_exercise.items():
        data_answer_i = data_answers[num_exercise_i]
        num = int(num_exercise_i)
        if num in list_rus_eng:
            type_exercise = "rus_eng"
            temp_list = list(zip(value_i, data_answer_i))
        elif num in list_eng_rus:
            type_exercise = "rus_eng"
            temp_list = list(zip(data_answer_i, value_i))
        elif num in list_bracket:
            type_exercise = "bracket"
            temp_list = list(zip(value_i, data_answer_i))
        else:
            raise Exception("Что-то не так с номером упражнения %s" % num)

        obj[num_exercise_i] = {"type": type_exercise, "content": temp_list}
    return obj

def create_json_file(data):
    data_json = json.dumps(data, ensure_ascii=False, indent=4)
    with open("exercise_answer.json", mode="w", encoding="utf-8") as f:
        f.write(data_json)

data_exercise = get_data_file(path_file_exercise)
dict_exercise = parse_data(data_exercise)

data_answer = get_data_file(path_file_answer)
dict_answer = parse_data(data_answer)

assert_exercise_answers(dict_exercise, dict_answer)
obj = join_objects(dict_exercise, dict_answer)
create_json_file(obj)
print()