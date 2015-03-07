# -*- coding:utf-8 -*-
from datetime import datetime
def convert_date(line):
    line = line.split(',')
    line_data_time = " ".join(line[0:2])
    time_ = datetime.strptime(line_data_time, "%Y.%m.%d %H:%M") #  '%y/%m/%d %H:%M
    time_format = time_.strftime('%Y%m%d %I:%M') # H для часов
    print(time_, time_format)
    # date = line[0].replace("." ,"")
    # time_hour = line[0][0:2]
    # time_min = line[1][:2]
    # if int(time_hour)>12:
    #     time_hour = str(int(time_hour)-12)
    # convert_time
    forex = 1
    if forex:
        # умножим все котировки на 100
        new_quote = [str(float(x)*100) for x in line[2:]]
        date = ','.join(new_quote) + '\n'
    else:
        date = ",".join(line[2:])
    string = time_format + "," + date
    return string
def convetr_dey():
    with open('EURUSD240.csv', encoding='utf-8', mode='r') as f:
        with open('EURUSD240_conv.csv', encoding='utf-8', mode='w') as f2:
            #lins = f.readline()
            lins = [f2.write(convert_date(x)) for x in f]  #  open('qqq.txt', encoding='utf-8', mode='r')
    return lins

lin = convetr_dey()
print()