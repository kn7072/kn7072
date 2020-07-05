# -*-coding:utf-8 -*-

path_temp = "temp.txt"

def get_prepare_data(path_file, start_num):
    temp= [("%s.  %s" % (ind + start_num, examp_i)).replace("\n", "") for ind, examp_i in enumerate(open(path_file, encoding="utf-8"))]
    for i in temp:
        print(i)

get_prepare_data(path_temp, 50)

