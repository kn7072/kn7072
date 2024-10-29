# -*- coding:utf-8 -*-
from enum import Enum
from dataclasses import dataclass
import os

PATH_DIR_FILES = '/home/stepan/GIT/kn7072/EnglishSimulate/Project/VERB_NON_FINITE_FORMS'
HOST='http://192.168.1.71'
PORT = '11434'
COMMON_REQUEST_ENG = "Переведи на русский язык предложение - %s"
COMMON_REQUEST_RUS = "Переведи на английский язык предложение - %s"

MODEL = 'llama3.1:70b'
# MODEL='llama3.1'

request_time_out = 30

class VerbForm:
    INFINITIVE = "INFINITIVE"
    GERUND = "GERUND"
    PARTICIPLE = "PARTICIPLE"

# @dataclass(frozen=True)
# class VerbForm:
#     title: str
#     author: str

class Direction:
    ENG = "ENG"
    RUS = "RUS"
    
    @classmethod
    def get_directions(cls):
        return (cls.ENG, cls.RUS)

def get_path_file(verb_form: str, direction: str) -> str:
    path = os.path.join(PATH_DIR_FILES, f"{verb_form}_{direction}_PRINT.txt")
    return path
