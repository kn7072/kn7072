# coding=utf-8
import os
import re

number = "(?P<num>\d{1,2})\."
compl_number = re.compile(number)

path_to_file = "./Упражнения/50/2"

def get_text_exercise(path_to_file: str) -> str: 
    all_text = ""
    for str_i in open(path_to_file, encoding="utf-8"):
        str_i = str_i.replace("\n", " ")
        if str_i.endswith("-"):
            str_i = str_i[0: -1]
        all_text += str_i
        
    return all_text

def get_list_sentance(text_exercise: str) -> list:
    res = compl_number.split(text_exercise)
    if not res[0]:
        res = res[1:]
    list_sentance = list(num + text for num, text in zip(res[0::2], res[1::2]))
    return list_sentance

def print_list_sentance(list_sentance):
    for i in list_sentance:
        print(i)

text_exerсise = get_text_exercise(path_to_file)
print(text_exerсise)
list_sentance = get_list_sentance(text_exerсise)
print_list_sentance(list_sentance)
pass