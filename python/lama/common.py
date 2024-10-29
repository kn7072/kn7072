# -*-coding:utf-8 -*-
import json
import os
import time
from config import get_path_file, Direction, COMMON_REQUEST_ENG, COMMON_REQUEST_RUS
from client import OllamaClient


encoding = "utf-8"


def get_list_lines_file(path_to_file: str):
    temp = []
    with open(path_to_file, mode="r", encoding=encoding) as f:
        for row in f:
            temp.append(row.rstrip("\n"))
    return temp

class Storage:

    def __init__(self, name: str):
        self.response_path_file = f"{name}_response.json"
        self.content = {}
        if os.path.isfile(self.response_path_file):
            with open(self.response_path_file, mode="r", encoding=encoding) as f:
                self.content = json.loads(f.read())

    def insert(self, number: str, request: str, response: str):
        if not self.content.get(number):
           self.content[number] = {}
        self.content[number][request] = response
        

    def save(self):

        if not os.path.isfile(self.response_path_file):
            with open(self.response_path_file, mode="w", encoding=encoding) as f:
                f.write("{}")

        with open(self.response_path_file, mode="r", encoding=encoding) as f:
            backup = f.read()
            with open("backup", mode="w", encoding=encoding) as f2:
                f2.write(backup)

        try:
            with open(self.response_path_file, mode="w", encoding=encoding) as f:
                f.write(json.dumps(self.content, ensure_ascii=False, indent=4, sort_keys=True))
        except:
            with open(self.response_path_file, mode="w", encoding=encoding) as f:
                f.write(backup)
            


class InitRequests:
    
    def __init__(self, form_verb:str, count_request: int = 5, time_out_between_requests:int = 7):
        self.file_name = "checkpoint"
        self.form_verb = form_verb
        self.count_request = count_request
        self.time_time_out_between_requests = time_out_between_requests
        self.check_checkpoint_file()
        self.start_request = self.get_start_number_sentence()
        #TODO прекратить выполнение есть достигли конца файла
        self._data = self._prepare_data()
        # if len(self._data) ==
        self.lama_client = OllamaClient()
        self.storage = Storage(form_verb)
                
    
    def get_start_number_sentence(self) -> int:
        with open(self.file_name, mode="r", encoding=encoding) as f:
            json_data = json.loads(f.read())
            start_request = json_data.get(self.form_verb, 0)
        return start_request

    def check_checkpoint_file(self):
        """создает файла checkpoint если его нет"""
        if not os.path.isfile(self.file_name):
            with open(self.file_name, mode="w", encoding=encoding) as f:
                f.write("{}")


    def _prepare_data(self) -> tuple[tuple[str, str]]:
        pathes = (get_path_file(self.form_verb, directon_i) for directon_i in Direction.get_directions())
        temp = []
        for path_i in pathes:
            temp.append(get_list_lines_file(path_i))

        return tuple(zip(temp[0], temp[1]))

    def save_checkpoint(self, next_index):
        with open(self.file_name, mode="r", encoding=encoding) as f:
            json_data = json.loads(f.read())
            json_data[self.form_verb] = next_index
        
        with open(self.file_name, mode="w", encoding=encoding) as f:
            f.write(json.dumps(json_data, ensure_ascii=False, indent=4, sort_keys=True))
        pass

    def send_request(self):
        # last_index = (end_index := (self.start_request + self.count_request)) if end_index < len(self._data) else len(self._data)
        max_index = len(self._data)
        if max_index == self.start_request:
            print(f"Запросов для {self.form_verb} не осталось")
            return
            
        last_index = end_index if (end_index := (self.start_request + self.count_request)) <= max_index else max_index

        for i in range(self.start_request, last_index):
            eng_sentence = self._data[i][0]
            rus_sentence = self._data[i][1]
            request_eng = COMMON_REQUEST_ENG % eng_sentence
            request_rus = COMMON_REQUEST_RUS % rus_sentence

            res_eng = self.lama_client.get_response(request_eng)
            res_rus = self.lama_client.get_response(request_rus)
            
            str_i = str(i)
            self.storage.insert(str_i, request_eng, res_eng)
            time.sleep(self.time_time_out_between_requests)
            self.storage.insert(str_i, request_rus, res_rus)

        self.storage.save()
        self.save_checkpoint(last_index)
