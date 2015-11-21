# -*- coding: utf-8 -*-
import os
import json
from copy import deepcopy
import sys
import assert_that


path_json = "REDACTION_TEST2_RESPONSE.txt"
path_json_responce = "REDACTION_TEST2_RESPONSE__NEW.txt"

def get_list_names(list_dicts):
    temp = []
    if list_dicts:
        for elm in list_dicts:
            name = elm.get('Название')
            if name:
                temp.append(name)
    return temp

def sort_event_and_investing(obj_json, responce, sub_attr = 'Событие'):
    """Сортирует Вложение и Событие чтобы гарантировать одинаковй порядок следования"""
    if obj_json.get(sub_attr) and responce.get(sub_attr):
        list_event_template = obj_json[sub_attr]
        list_event_responce = responce[sub_attr]
        copy_responce = deepcopy(list_event_responce)
        if type(list_event_template) is list:
            list_arrt = get_list_names(list_event_template)
            if list_arrt:
                delete_elements = []
                for index, val in enumerate(copy_responce):
                    name = val.get('Название')
                    if name not in list_arrt:
                        delete_elements.append(index)
                        print("###### DEL %s - %s ######" % (sub_attr, name))
                if delete_elements:
                    delete_elements.sort(reverse=True)
                    for i in delete_elements:
                        list_event_responce.pop(i)
                list_event_template.sort(key=lambda i: i['Название'])
                list_event_responce.sort(key=lambda i: i['Название'])
        else:
            list_event_responce = 'ignore'

    return obj_json, responce

def delete_tags():
    pass

def get_json(path):
    list_line = [line.strip() for line in open(path) if line]  # , encoding='ascii' utf-8
    tmp_str = ''.join(list_line)
    tmp_response = json.loads(tmp_str)
    return tmp_response['result']

events = get_json(path_json)  # path_json = "REDACTION_TEST2_RESPONSE.txt"
events_responce = get_json(path_json_responce)  # path_json_responce = "REDACTION_TEST2_RESPONSE__NEW.txt"

def print_event(elm_dict, sub_attr = 'Событие'):
    try:
        for index, event in enumerate(elm_dict['result']['Событие']):
            print(event['Название'], index)
            if tmp_response['result']['Событие'][index].get('Вложение'):
                sub_event_all = tmp_response['result']['Событие'][index]['Вложение']
                for i, sub_event in enumerate(sub_event_all):
                    print("    ", sub_event['Название'], i)
    except Exception as e:
        print()

def delete_ignore_elm_in_dict(dict1):
        tmp_dict = deepcopy(dict1)
        print(dict1.keys())
        for key, value in tmp_dict.items(): #tmp_dict.items()
            print(key)
            dict1.pop(key, None)
#print_event(tmp_response)
test_dict = {'a':4, 'b':5, 'c':6, 'k':7}
delete_ignore_elm_in_dict(test_dict)

def print_elm(list_event_responce, sub_attr = 'Событие'):
    list_event = list_event_responce[sub_attr]
    count = len(list_event_responce[sub_attr])
    for j in range(count):
        print(list_event[j]['Название'])
        if list_event[j].get("Вложение") and type(list_event[j].get("Вложение")) is list:
            for k in range(len(list_event[j].get("Вложение"))):
                print("      %s" % list_event[j]["Вложение"][k]['Название'])
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
events, events_responce = sort_event_and_investing(events, events_responce, sub_attr = 'Вложение')#, sub_attr = 'Вложение'

print_elm(events_responce, sub_attr = 'Вложение')
print_elm(events, sub_attr = 'Вложение')
print_event(events)
print()