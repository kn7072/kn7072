# -*- coding: utf-8 -*-

import json

def get_json(path):
    list_line = [line.strip() for line in open(path) if line]  # , encoding='ascii' utf-8
    tmp_str = ''.join(list_line)
    tmp_response = json.loads(tmp_str)
    return tmp_response#['result']
path_json = 'event2.txt'
events = get_json(path_json)
print()