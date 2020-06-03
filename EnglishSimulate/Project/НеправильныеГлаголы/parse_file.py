# -*- coding: utf-8 -*-
import os
import re
# https://regex101.com/
# https://habr.com/ru/post/349860/

temp_re = "(?P<text>[0-9]+?\..+?[\.|\?|\!])"  # (?P<text>[0-9]+?\..+?)(?=[0-9])
compl_1 = re.compile(temp_re, flags=re.DOTALL)
path_dir = "files_source"
path_file = os.path.join(path_dir, "group_1")

def get_data_file(path_file):
    with open(path_file, mode="r", encoding="utf-8") as f:
        return f.read()

def parse_data(data):
    search = re.findall(compl_1, data)
    search_mod = [i.replace("-\n", "").replace("\n", " ") for i in search]
    assert len(search_mod) % 2 == 0, "Должно быть четным"
    return search_mod

data = get_data_file(path_file)
res = parse_data(data)
