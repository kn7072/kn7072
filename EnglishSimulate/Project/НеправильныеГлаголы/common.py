# -*- coding: utf-8 -*-
import json
import os

def get_all_exercise():
    # with open("exercise_answer.json", mode="r", encoding="utf-8") as f:
    #     return json.loads(f.read())
    my_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(my_path, "exercise_answer.json")

    with open(path, mode="r", encoding="utf-8") as f:
        return json.loads(f.read())

    # path.relpath("2091/data.txt")    

def get_exercise_type(name_group, type_exercises):
    all_exercise = get_all_exercise()
    list_temp = []
    for num_exercise_i, val_i in all_exercise.items():
        if name_group == val_i["group"]:

            if type_exercises in ["rus_eng", "bracket"] and type_exercises==val_i["type"]:
                list_temp.extend(val_i["content"])
            elif type_exercises == "eng_rus" and val_i["type"]=="rus_eng":
                revers = [[eng_i, rus_i] for rus_i, eng_i in val_i["content"]]
                list_temp.extend(revers)
    return list_temp
