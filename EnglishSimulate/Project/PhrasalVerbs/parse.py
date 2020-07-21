# -*- coding: utf-8 -*-
import json
import os
import re

path_answer = r"files_source\answer"
path_exercise = r"files_source\exercise"

temp_all_exercise = "Упражнение\s*?(?P<num_exercise>[0-9]+)(?P<exercise>.+?)(?=Упражнение)"
compl_1 = re.compile(temp_all_exercise, flags=re.DOTALL)

temp_exercise = "(?P<text>[0-9]+?\..+?)(?=\s[0-9]{,2}?\.)"
compl_2 = re.compile(temp_exercise, flags=re.DOTALL)


def get_data_file(path_file):
    with open(path_file, mode="r", encoding="utf-8") as f:
        return f.read()

type_eng = "Переведите предложения на русский язык"
type_rus = "Переведите предложения на английский язык"

def parse_data(data, use_type=False):
    dict_temp = {}
    search = re.findall(compl_1, data)
    for num_exercise_i, exercise_i in search:
        # чтобы шаблон работал правильно - добавим в конец строки 99.
        exercise_i += " 99."
        search_exercise = re.findall(compl_2, exercise_i)
        search_mod = [i.replace("\n", " ").strip() for i in search_exercise]

        if use_type:
            if type_eng in exercise_i:
                dict_temp[num_exercise_i] = {"data": search_mod, "type": "eng"}
            elif type_rus in exercise_i:
                dict_temp[num_exercise_i] = {"data": search_mod, "type": "rus"}
            else:
                raise Exception("Не удалось определить тип")
        else:
            dict_temp[num_exercise_i] = search_mod
    return dict_temp


def assert_exercise_answers(data_exercise, data_answers):
    list_error = []
    for num_exercise_i, value_i in data_exercise.items():
        data_answer_i = data_answers[num_exercise_i]
        if len(value_i["data"]) != len(data_answer_i):
            list_error.append([num_exercise_i, len(value_i["data"]), len(data_answer_i)])
    if list_error:
        for i in list_error:
            print(i)

def create_json(data_exercise, data_answers):
    obj = {}
    for num_exercise_i, value_i in data_exercise.items():
        data_answer_i = data_answers[num_exercise_i]
        if value_i["type"] == "rus":
            content = list(zip(value_i["data"], data_answer_i))
        else:
            content = list(zip(data_answer_i, value_i["data"]))
        obj[num_exercise_i] = content
    return obj

def create_json_file(data):
    data_json = json.dumps(data, ensure_ascii=False, indent=4)
    with open("exercise_answer.json", mode="w", encoding="utf-8") as f:
        f.write(data_json)

data_exercise = get_data_file(path_exercise)
data_answer = get_data_file(path_answer)

exercise_data_dict = parse_data(data_exercise, use_type=True)
answer_data_dict = parse_data(data_answer)

assert_exercise_answers(exercise_data_dict, answer_data_dict)
obj = create_json(exercise_data_dict, answer_data_dict)
create_json_file(obj)
print()





