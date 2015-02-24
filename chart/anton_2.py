# -*- coding:utf-8 -*-
import requests
import logging
import sys
from requests.exceptions import RequestException, ConnectionError, HTTPError, URLRequired, TooManyRedirects, Timeout
import json
from subprocess import Popen, PIPE
#from gitlab import Gitlab
# http://doc.gitlab.com/ce/api/merge_requests.html
first_logger = logging.getLogger('first_log')
log_formatter = logging.Formatter("%(asctime)s  %(message)s\n", datefmt="%d.%m.%y %H:%M:%S")  # формат сообщения
first_logger.setLevel(logging.INFO)  # уровень важности
logfile = 'log_merge_requests.log'
file_handler = logging.FileHandler(logfile)  # обработчик для вывода в файл
file_handler.setFormatter(log_formatter)  # подключение форматера к обработчику
first_logger.addHandler(file_handler)  # добавление обработчика в регистр
# вывод в консоль
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(log_formatter)
first_logger.addHandler(console_handler)  # выводим в консоль
message = '%s%s%s' % (2, 3, 6)
first_logger.info(message)  # пишим в файл


###################################################################
url = r'http://www.dell.com/support/home/ru/ru/rudhs1/product-support/product/inspiron-1000/drivers'
# req = requests.Request('GET', url)
# req = req.prepare()
# s = requests.Session()
# r = s.send(req)
# t.text
#################################################################
import lxml.html as html
import json
from lxml.html import parse
from requests.auth import HTTPBasicAuth, HTTPProxyAuth
# auth = requests.auth.HTTPProxyAuth('sg.chernov', 'QWEqwe123')
#headers0 = {'Content-Type': 'application/json; charset=UTF-8'}
r = requests.get(url)  #headers=headers0, verify=False, auth=auth
text = r.text  #.decode('utf-8')   encode
#text_2 = text.encode('cp1251')
#unicode_text = text.decode('utf-8')
#text_in_1251 = text.encode('cp1251')
table = html.fromstring(r.text)
# iter_ = html.iterlinks(r.text)
#hrefs_ = table.cssselect('a.pointerCursor')
#table.body.find_class('pointerCursor')
#s = text.encode('latin1').decode('cp1251')
t = table.get_element_by_id('tagDrivers')
j = json.loads(t.attrib['value'])
list_ = j['GroupItem']  # 11
################################################################################
bios = j['GroupItem'][0]  # bios
count_driver = len(bios['Drivers'])
category = bios['GroupItemName'] # общая категория
drivers = bios['Drivers'][0] # пока для биоса 0 bios['Drivers'][0].keys()
driver_name = drivers['DriverName']
ReleaseDate = drivers['ReleaseDate']  # дата выпуска
LUPDDate = drivers['LUPDDate']  #  Последнее обновление 03 ноя 2011
DellVer = drivers['DellVer']  # версия драйвера
# текущая версия драйвера
FileFrmtInfo = drivers['FileFrmtInfo']  # словарь
file_name = drivers['FileFrmtInfo']['FileName']
file_size = drivers['FileFrmtInfo']['FileSize']
HttpFileLocation = drivers['FileFrmtInfo']['HttpFileLocation']
# другие доступные форматы файлов
OthFileFrmts = drivers['OthFileFrmts']  # список словарей
count_OthFileFrmts = len(OthFileFrmts)
FileName = OthFileFrmts[0]['FileName']
filesize = OthFileFrmts[0]['FileSize']
HttpFileLocation = OthFileFrmts[0]['HttpFileLocation']
################################################################################

################################################################################
bios = j['GroupItem'][2]  # модем связь
count_driver_cat = len(bios['Drivers'])
category = bios['GroupItemName'] # общая категория
for i in range(count_driver_cat):
    drivers = bios['Drivers'][i]
    driver_name = drivers['DriverName']
    ReleaseDate = drivers['ReleaseDate']  # дата выпуска
    LUPDDate = drivers['LUPDDate']  #  Последнее обновление 03 ноя 2011
    DellVer = drivers['DellVer']  # версия драйвера
    # текущая версия драйвера
    FileFrmtInfo = drivers['FileFrmtInfo']  # словарь
    file_name = drivers['FileFrmtInfo']['FileName']
    file_size = drivers['FileFrmtInfo']['FileSize']
    HttpFileLocation_cur = drivers['FileFrmtInfo']['HttpFileLocation']
    # другие доступные форматы файлов
    print("#############    другие доступные форматы файлов    #############")
    OthFileFrmts = drivers['OthFileFrmts']  # список словарей с доступными версиями
    count_OthFileFrmts = len(OthFileFrmts)
    for j in range(count_OthFileFrmts):
        FileName = OthFileFrmts[j]['FileName']
        filesize = OthFileFrmts[j]['FileSize']
        HttpFileLocation = OthFileFrmts[j]['HttpFileLocation']
################################################################################

########
VI = j['GroupItem'][1]  # VI
print(VI['GroupItemName'])
########
DIAG = j['GroupItem'][2] # диагностика
print(DIAG['GroupItemName'])
########
DRVR = j['GroupItem'][3] # звук
print(DRVR['GroupItemName'])
########
UTIL = j['GroupItem'][10] # Съемные накопители
print(UTIL['GroupItemName'])
# for x in iter_:
#     print(x.get
for x in range(11):
    print(j['GroupItem'][x]['GroupItemName'])
links = html.resolve_base_href(r.text)
# http://downloads.dell.com/comm/R85670.EXE  'R80894.EXE'  "input#tagDrivers")
for x in iter_:
    try:
        print(x[0].attrib['href'])  # , "----", x[1], "---", x[2]
        if 'http://downloads' in x[0].attrib['href']:  # 'http://downloads.dell.com/comm/R85670.EXE':
            print()
    except:
        pass
print()
###################################################################


