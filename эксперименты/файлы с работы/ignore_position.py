# -*- coding: utf-8 -*-
import os
import json
from copy import deepcopy
import sys

path_json = "test-files\ignore_position_2.txt"
def home_version():
    list_line = [line.strip() for line in open(path_json) if line]  # , encoding='ascii' utf-8
    tmp_str = ''.join(list_line)
    tmp_response = json.loads(tmp_str)
    count_investing = len(tmp_response['result']['Вложение'])
    #json.dumps(item1_copy, indent=3, sort_keys=True, ensure_ascii=False)

    list_investing = tmp_response['result']['Вложение']
    list_investing.sort(key=lambda i: i['Название'])
    list_event = tmp_response['result']['Событие']
    list_event.sort(key=lambda i: i['Название'])

    for x in range(count_investing):
        print(tmp_response['result']['Вложение'][x]['Название'])
    print('/////////////////////////')
    list_investing.sort(key=lambda i: i['Название'])
    for x in range(count_investing):
        print(tmp_response['result']['Вложение'][x]['Название'])
# for i in range(5):
#     for x in range(count_investing):
#         print(tmp_response['result']['Вложение'][x]['Название'])
#     print("/////////////////////////////////")
# tmp_response['result']['Вложение'][0]['Название']
# tmp_response['result']['Событие']
# tmp_response['result']['Событие'][2]['Название']
# dict1.pop(key, None)
# list1.pop(index)

def sort_event_and_investing(obj_json):
    """Сортирует Вложение и Событие чтобы гарантировать одинаковй порядок следования"""
    ignoge_elements = []  #'Утверждение', 'Подтверждение отправки электронного документа оператором',
                          #'Товарная накладная (титул покупателя)' 'Утверждение',
    print("######### Вложение ##########")
    if type(obj_json.get('result')) is dict:
        if obj_json['result'].get('Вложение'):
            list_investing = obj_json['result']['Вложение']
            if type(list_investing) is list:
                list_investing.sort(key=lambda i: i['Название'])
                for i in range(len(list_investing)):
                    print(list_investing[i]['Название'])
        print("######### События ##########")
        if obj_json['result'].get('Событие'):
            list_event = obj_json['result']['Событие']
            if type(list_event) is list:
                copy_list_event = deepcopy(list_event)
                # проверим - событие входит в список ignoge_elements
                count_event = len(copy_list_event)
                index_for_delete = []
                for event_i in range(count_event):
                    if copy_list_event[event_i]['Название'] in ignoge_elements:
                        index_for_delete.append(event_i)
                if index_for_delete:
                    index_for_delete.sort(reverse=True)
                    for index in index_for_delete:
                        copy_list_event.pop(index)
                copy_list_event.sort(key=lambda i: i['Название'])
                obj_json['result']['Событие'] = copy_list_event
                count_event = len(list_event)
                for event_i in range(count_event):  # проходим по всем событиям
                    investing_event = obj_json['result']['Событие'][event_i].get("Вложение")
                    if investing_event:  # если  у события есть вложение и объект список (не ignore)
                        if type(investing_event) is list:
                            investing_event.sort(key=lambda i: i['Название'])  # отсортировали вложения в событии
                            # проверим вложения события на предмет игнорируемых
                            count_event_investing = len(investing_event)
                            # создаем копию списка вложений для события - из которого будут удалены некоторые вложения
                            delete_index_investing_event = []
                            for x in range(count_event_investing):
                                if investing_event[x]['Название'] in ignoge_elements:
                                    delete_index_investing_event.append(x)
                            if delete_index_investing_event:
                                delete_index_investing_event.sort(reverse=True)
                                for i in delete_index_investing_event:
                                    investing_event.pop(i)

                list_event = obj_json['result']['Событие']
                for j in range(count_event):
                    print(list_event[j]['Название'])
                    if list_event[j].get("Вложение") and type(list_event[j].get("Вложение")) is list:
                        for k in range(len(list_event[j].get("Вложение"))):
                            print("      %s" % list_event[j]["Вложение"][k]['Название'])
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")


list_line = [line.strip() for line in open(path_json) if line]  # , encoding='ascii' utf-8
tmp_str = ''.join(list_line)
tmp_response = json.loads(tmp_str)
def print_event(elm_dict):
    try:
        for index, event in enumerate(elm_dict['result']['Событие']):
            print(event['Название'], index)
            if tmp_response['result']['Событие'][index].get('Вложение'):
                sub_event_all = tmp_response['result']['Событие'][index]['Вложение']
                for i, sub_event in enumerate(sub_event_all):
                    print("    ", sub_event['Название'], i)
    except Exception as e:
        print()


#print_event(tmp_response)
sort_event_and_investing(tmp_response)
print_event(tmp_response)
print()