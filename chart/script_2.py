# -*- coding:utf-8 -*-
import requests
import logging
import sys
import lxml.html as html
import json
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import re
import os
import my_sql

dict_os_sysmem = {'W864':'MS Windows 8, 64-разрядная версия',
                  'W764': 'MS Windows 7, 64-разрядная версия',
                  'BIOSA':'BIOS',
                  'LNUX':'Linux',
                  'LN70':'Red Hat Linux 7.0',
                  'LN62':'Red Hat Linux 6.2',
                  'W98':'MS Windows 98',
                  'OS2':'IBM OS/2',
                  'WNT5':'MS Windows 2000',
                  'W95':'MS Windows 95',
                  'WNT3':'MS Windows NT 3.5x',
                  'WME':'MS Windows Me',
                  'W31':'MS Windows 3.x',
                  'WNT4':'MS Windows NT 4.0',
                  'NW':'Novell Netware',
                  'W832':'MS Windows 8, 32-разрядная версия',
                  'WB32A':'MS Windows 8.1 32-bit',
                  'WB64A':'MS Windows 8.1 64-bit',
                  'RH64':'Red Hat Ent Linux 6.4',
                  'WLH':'MS Windows Vista, 32-разрядная версия',
                  'WXPX':'MS Windows XP x64',
                  'WW1':'MS Windows XP',
                  'WV64':'MS Windows Vista, 64-разрядная версия',
                  'FRDOS':'FreeDOS',
                  'RH60':'Red Hat Enterprise Linux 6',
                  'WN104':'Ubuntu 10.10',
                  'W732':'MS Windows 7, 32-разрядная версия',
                  'UB10':'Ubuntu 10.04',
                  'MYV':'Microsoft Hyper-V',
                  'RHEL5':'Red Hat Enterprise Linux 5',
                  'UMB':'Ubuntu Moblin',
                  'RL51':'Red Hat Enterprise Linux 5.1',
                  'U1104':'Ubuntu 11.04 - ALL',
                  'WXPEM':'MS Windows XP Embedded',
                  'UB14A':'Ubuntu 14.04',
                  'U1110':'Ubuntu 11.10',
                  'UD94':'Ubuntu Desktop 9.04',
                  'DOS':'Microsoft MS-DOS',
                  '1204A':'Ubuntu 12.04',
                  'NAA':'Не применимо'}

ditectoty_work = os.getcwd()  # путь к катологу от куда запущен скрипт

h1 = '<h1>Скачать драйверы {model} [{system}]</h1>\n'
cat_drivers =     '<div class="driver_block_header">{category}</div>\n'
template_driver = '<div class="driver_block_description">\n'\
                  '    <span class="driver_block_description_td">Название</span><span class="driver_block_description_name">%(driver_name)s</span><span class="driver_block_download_link"><a href="%(HttpFileLocation_cur)s">Скачать</a></span>\n'\
                  '    <span class="driver_block_description_td">Версия: </span><span class="driver_block_description_version">%(DellVer)s</span>\n'\
                  '    <span class="driver_block_description_td">Дата выпуска: </span><span class="driver_block_description_date">%(LUPDDate)s</span>\n'\
                  '    <span class="driver_block_description_td">Размер (Мб): </span><span class="driver_block_description_size">%(file_size)s</span>\n'\
                  '    <span class="driver_block_description_td">Имя файла: </span><span class="driver_block_description_file_name">%(file_name)s</span>\n'\
                  '    %(other_drivers_blok)s'\
                  '</div>\n'\
###############################################################################################################
other_driver =    '<span class="driver_block_description_td">Другие версии:</span>\n'\
	              '<div class="driver_block_description_other_version">\n'\
		          '      <ul>\n'\
			      '          %s'\
		          '      </ul>\n'\
	              '</div>'
elm_li_temp = '<li><a href="%(HttpFileLocation)s">%(file_name)s</a>, %(file_size)s</li>\n'

other_driver_2 =    '   <div class="driver_block_description_other_version">\n' \
                  '      <span class="driver_block_description_size">%(file_size)s</span>\n' \
                  '      <span class="driver_block_description_file_name">%(file_name)s</span>\n' \
                  '   </div>\n' \
                  '   <div class="driver_block_download_link">\n' \
                  '      <a href="%(HttpFileLocation)s" rel="external">Скачать</a>\n' \
                  '   </div>\n'
temp_os = {}
class ParserDELL:
    """забираем ссылку с сайта dell"""

    def request(self, model, url):
        """метод получает код страницы по адресу url"""
        #url = 'http://www.dell.com/support/home/ru/ru/rudhs1/product-support/product/latitude-110l/drivers'
        #GET http://www.dell.com/support/home/ru/ru/rudhs1/Drivers/DriversList/GetDriverListOnLanguageAndOSCode?languageCode=&productCode=latitude-110l&serviceTag=&osCode=NAA HTTP/1.1
        r = requests.get(url)
        # auth = requests.auth.HTTPProxyAuth('sg.chernov', 'QWEqwe123')
        # headers0 = {'Content-Type': 'application/json; charset=UTF-8'}
        # r = requests.get(url, headers=headers0, verify=False, auth=auth)

        text = r.text  # код страницы
        table = html.fromstring(text)  # объект html
        obj = table.get_element_by_id('DriverList')  #DriverList tagDrivers объект содержащий все информацию о драйверах
        text_element = obj.text_content()
        j = self.search_json(text_element)
        # com = re.compile('masterDriversData = (?P<model_json>(.*))\;\nvar', re.MULTILINE|re.DOTALL)
        # XX = re.findall(com, text_element)
        # model = re.search('masterCmsData = (?P<model_json>(.*))\;', text_element).group('model_json')# masterCmsData = (?P<model>.*)\;\nvar
        # j = json.loads(obj.attrib['value'])
        # вытаскиваем список возможных драйверов
        list_dict_os = j['FilterData']['OSFilter']  # список словарей
        os_code = [dict_os['OSCode'] for dict_os in list_dict_os]  # все доступные коды OS для данной модели
        for osys in os_code:
            if osys not in dict_os_sysmem.keys() and osys not in temp_os.keys():
                temp_os[osys] = url
            if osys == 'WN104':
                print()
            link = 'http://www.dell.com/support/home/ru/ru/rudhs1/Drivers/DriversList/GetDriverListOnLanguageAndOSCode?languageCode=&productCode={0}&serviceTag=&osCode={1}'.format(model, osys)
            req = requests.get(link) # requests.get(link, headers=headers0, verify=False, auth=auth)  # requests.get(link)
            js = req.json()
            json_drivers_model = json.loads(js['driversdata']['DriverListData'])['GroupItem']  # список джейсонов их количесто соответствует количеству категорий
            yield (osys, json_drivers_model)  # создали функцию генератор

    def parser_json_driver(self, list_json, model, osys, cat, file_name_to_save):
        """метод получает на вход список джейсонов и парсит их"""
        #count_json = len(list_json)  # сколько джейсонов пришло
        file_to_save = r'%s.txt' % file_name_to_save
        # 'D:\\git_hub_new\\kn7072\\chart\\DRIVERS\\inspiron_laptop\\inspiron-15r-5537\\BIOSA_inspiron-15r-5537.txt'
        with open(file_to_save, encoding='utf-8', mode='w') as f:  # открыли файл для записи w - запись, если файла нет
            # то он будет создан, если существует то будет перезаписан
            # Фомрируем данные для отправки в базу
            dict_for_base = {}
            split_model = model.split('-', 1)
            system = dict_os_sysmem[osys]
            name_for_title = split_model[0].capitalize() +' '+ split_model[1].replace('-', ' ')
            dict_for_base['meta_k'] = "скачать,драйверы,бесплатно,на высокой скорости,Dell,%s,%s,%s" % (split_model[0], split_model[1].replace('-', ' '), system)
            dict_for_base['meta_d'] = "Скачать бесплатно драйверы на высокой скорости для Dell %s [%s]" % (name_for_title, system)
            dict_for_base['title'] = "Скачать драйверы Dell %s [%s]" % (name_for_title, system)
            dict_for_base['text'] = '<h1>Скачать драйверы Dell {model} [{system}]</h1>\n'.format(model=name_for_title, system=system)  # строка с заголовком для модели
            dict_for_base['category'] = cat
            ############################################################
            for json_driver in list_json:
                #f.write('<div class="driver_block">\n')
                count_driver_cat = len(json_driver['Drivers'])
                category = json_driver['GroupItemName']  # общая категория X1
                dict_for_base['text'] += cat_drivers.format(category=category)  # на каждую категорию один заголовок
                for i in range(count_driver_cat):
                    temp = {}  # словарь для удобства хранения информации
                    temp['category'] = category  # название группы драйверов
                    drivers = json_driver['Drivers'][i]
                    driver_name = drivers['DriverName']  # X2
                    temp['driver_name'] = driver_name
                    ReleaseDate = drivers['ReleaseDate']  # дата выпуска
                    LUPDDate = drivers['LUPDDate']  #  Последнее обновление 03 ноя 2011
                    temp['LUPDDate'] = LUPDDate  # X3
                    DellVer = drivers['DellVer']  # версия драйвера
                    temp['DellVer'] = DellVer  # X4
                    # текущая версия драйвера
                    FileFrmtInfo = drivers['FileFrmtInfo']  # словарь
                    file_size = drivers['FileFrmtInfo']['FileSize']
                    file_size = int(file_size)/1024000  # певод в Mb
                    file_size = str(round(file_size, 1))
                    temp['file_size'] = file_size  # X5
                    file_name = drivers['FileFrmtInfo']['FileName']
                    temp['file_name'] = file_name  # X6
                    HttpFileLocation_cur = drivers['FileFrmtInfo']['HttpFileLocation']  # ссылка на скачивание
                    temp['HttpFileLocation_cur'] = HttpFileLocation_cur  # X7
                    temp['model_laptop'] = model
                    temp['os_system'] = system
                    # другие доступные форматы файлов
                    OthFileFrmts = drivers['OthFileFrmts']  # список словарей с доступными версиями
                    # write_templete = template_driver % temp
                    # f.write(write_templete)
                    count_OthFileFrmts = len(OthFileFrmts)
                    temp['other_drivers_blok'] = ''
                    # если count_OthFileFrmts то значит других драйверов нет
                    string_li = ''
                    for j in range(1, count_OthFileFrmts):
                        temp_other_driver = {}
                        file_size = OthFileFrmts[j]['FileSize']
                        file_size = int(file_size)/1024000  # певод в Mb
                        file_size = str(round(file_size, 1))
                        temp_other_driver['file_size'] = file_size  # размер файла
                        filename = OthFileFrmts[j]['FileName']
                        temp_other_driver['file_name'] = filename  # имея файла
                        HttpFileLocation = OthFileFrmts[j]['HttpFileLocation']
                        temp_other_driver['HttpFileLocation'] = HttpFileLocation  # ссылка для скачивания
                        li = elm_li_temp % temp_other_driver
                        string_li = string_li + li  # конкатинируем другие доступние драйвера
                        #write_templete_other_driver = other_driver % temp_other_driver
                    if string_li:  # если что-то нашлось
                        other_driver_temp = other_driver % string_li
                        temp['other_drivers_blok'] = other_driver_temp
                        good_templete = template_driver % temp
                        dict_for_base['text'] += good_templete
                    else:
                        good_templete = template_driver % temp
                        dict_for_base['text'] += good_templete
                    f.write(good_templete)
                    f.write("################ NEW DRIVER ################\n")
            self.sql_query(dict_for_base)

    i = 1  # сщетчик для проверки
    def sql_query(self, data_for_sql):
        my_sql.insert_book(data_for_sql)
        print("запись N %s" % self.i)
        self.i += 1
        # self.i -=1
        # if self.i > 0:
        #     my_sql.insert_book(data_for_sql)
        # print()

    def serial_model(self):
        """метод возвращает список на модельные ряды - например adamo_laptop """
        url_cat = r'http://www.dell.com/support/home/ru/ru/rudhs1/ProductSelector/PS/laptop'
        req = requests.Request('GET', url_cat)
        req = req.prepare()
        s = requests.Session()
        r = s.send(req)
        iter_ = html.iterlinks(r.text)
        # 'http://www.dell.com/support/home/ru/ru/rudhs1/Products/laptop/adamo_laptop'
        list_serial = {}
        for x in iter_:
            try:
                model_category = x[0].attrib['href']
                category = model_category.split('/')[-1]
                print(model_category)
                link = r'http://www.dell.com'+model_category
                list_serial[category] = link
            except:
                pass
        return list_serial

    def link_notebook(self, links):
        for link in links:
            req = requests.Request('GET', link)
            req = req.prepare()
            s = requests.Session()
            r = s.send(req)
            text = r.text
            table = html.fromstring(text)
            obj = table.get_element_by_id('parent')
            # http://www.dell.com/support/home/ru/ru/rudhs1/Products/laptop/adamo_laptop
            # http://www.dell.com/support/home/ru/ru/rudhs1/Products/laptop/inspiron_laptop'

    def selenium_parser(self, url_dict):

        all_model = {}
        for cat, url in url_dict.items():
            driver = webdriver.Firefox()
            driver.get(url)  # открываем страницу чтобы прогрузилась
            time.sleep(5)  # пока так
            # найдем все модели на на странице
            print(url)
            model_list_category = {}
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, ".panel-body-bordered .text-left li a")
                elements_2 = driver.find_elements(By.CSS_SELECTOR, '.row span a')
                if elements:
                    for i in elements:
                        temp = i.get_attribute('href')
                        model = re.search('\'(?P<model>[\S]*)\'', temp).group('model')
                        model_list_category[model] = r'http://www.dell.com/support/home/ru/ru/rudhs1/product-support/product/%s/drivers' % model
                else:
                    for i in elements_2:
                        temp = i.get_attribute('href')
                        model = re.search('\'(?P<model>[\S]*)\'', temp).group('model')
                        model_list_category[model] = r'http://www.dell.com/support/home/ru/ru/rudhs1/product-support/product/%s/drivers' % model
            finally:
                all_model[cat] = model_list_category
                driver.quit()
        return all_model

    temp_dict = {'legacylp': {'oth-386-320n-plus': 'http://www.dell.com/support/home/ru/ru/rudhs1/product-support/product/oth-386-320n-plus/drivers',
                          'dell-smart-250n': 'http://www.dell.com/support/home/ru/ru/rudhs1/product-support/product/dell-smart-250n/drivers',
                          'oth-386-320n': 'http://www.dell.com/support/home/ru/ru/rudhs1/product-support/product/oth-386-320n/drivers'},
                 'studio_laptop': {'studio-1745': 'http://www.dell.com/support/home/ru/ru/rudhs1/product-support/product/studio-1745/drivers',
                               'studio-1747': 'http://www.dell.com/support/home/ru/ru/rudhs1/product-support/product/studio-1747/drivers',
                               'studio-1749': 'http://www.dell.com/support/home/ru/ru/rudhs1/product-support/product/studio-1749/drivers'}
                 }

    def craate(self, all_models = None):
        """буферный метод"""
        #all_models = self.temp_dict
        error_drivers = ditectoty_work +'\\error_drivers.txt'  # сюда пишим ссылки по которым произошли ошибки
        with open(error_drivers, encoding='utf-8', mode='w') as f:
            for cat, dict_molel in all_models.items():

                for model, link in dict_molel.items():  # модель и ссылка к ней ведущая
                    try:
                        print(model+" --> "+link)
                        generator_os_driver = self.request(model, link)
                        for osys, json_drivers_for_os in generator_os_driver:
                            try:
                                # на каждую категорию подобную egacylp
                                path = ditectoty_work +'\\DRIVERS\\%s\\%s' % (cat, model) # в директории где запущен скрипт будет создан
                                # общий католог DRIVERS а в нем дочерние каталоги по категориям
                                if not os.path.isdir(path):
                                    try:
                                        os.makedirs(path)
                                    except OSError:
                                        print("каталог уже существует или католог не может быть создан")
                                # каталоги созданы - теперь начинается самое интересное
                                file_name = "%s_%s" % (osys, model)
                                path_to_save = path + "\\%s" % file_name
                                if not json_drivers_for_os:
                                    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
                                self.parser_json_driver(json_drivers_for_os, model=model, osys=osys, cat=cat, file_name_to_save = path_to_save)
                            except:
                                print("Exception !!!  "+str(cat) + "  "+osys +" --> " + link)
                                massage = "Error model - %s to %s\n" % (model, link)
                                sys.exc_info()  # af
                                f.write(massage)
                    except:
                        print("Exception !!!  "+str(cat) + " --> " + link)
                        massage = "Error model - %s to %s \n" % (model, link)
                        f.write(massage)

    def search_json(self, text=None):
        # url = 'http://www.dell.com/support/home/ru/ru/rudhs1/Drivers/DriversList/GetDriverListOnLanguageAndOSCode?languageCode=&productCode=latitude-d505&serviceTag=&osCode=WW1'
        # #url = 'http://www.dell.com/support/home/ru/ru/rudhs1/product-support/product/latitude-d505/drivers'
        # auth = requests.auth.HTTPProxyAuth('sg.chernov', 'QWEqwe123')
        # headers0 = {'Content-Type': 'application/json; charset=UTF-8'}
        # r = requests.get(url, headers=headers0, verify=False, auth=auth)
        # # jj = json.loads(r.text)
        # j = r.json()
        # jj = json.loads(j['driversdata']['DriverListData'])  # ['DriversThresholdCount', 'GroupItem', 'NoDriversFound', 'systemModel', 'DefaultLWPLanguage', 'FilterData']
        # js = json.loads(j['driversdata']['DriverListData'])['GroupItem'][2]['Drivers'][0]['OthFileFrmts'][1]  # Другие доступные форматы файлов
        text_element = text
        com = re.compile('masterDriversData = (?P<model_json>(.*))var masterCmsData', re.DOTALL)
        line = com.findall(text_element)[0][0].replace(';\r\n', '')
        json_obj = json.loads(line)  # , encoding='utf-8'
        return json_obj
        # masterCmsData = (?P<model>.*)\;\nvar
        # with open('templ_json.txt', encoding='utf-8', mode='r') as f:  # html_text.txt
        #     text_element = f.read()
        #     line = com.findall(text_element)[0][0].replace(';\\r\\n    ', '')
        #     json_obj = json.loads(line)
        #     pass
        #print()
if __name__ == "__main__":
    instance = ParserDELL()
    #instance.search_json()
    # req = instance.request(model='latitude-110l', url='')
    # for os, j in req:
    #     print(os)
    #instance.craate()
    # Exception !!!  alienware_laptops  WB64A --> http://www.dell.com/support/home/ru/ru/rudhs1/product-support/product/alienware-13/drivers
    # x = my_sql.conect
    # globals()['my_sql'].__dict__['conect']
    # my_sql.conect = 10
    # my_sql.yy()
    # my_sql.xx()
    # y = my_sql.conect
    # trmf= {'meta_k': 'скачать,драйверы,бесплатно,на высокой скорости,dell,inspiron,3521,windows 7,64 bit',
    #         'title': 'adamo-xps W764',
    #         'text': '<h1>Скачать драйверы adamo-xps [W764]</h1>\n<div class="driver_block_header">BIOS</div>\n<div class="driver_block_description">\n    <span class="driver_block_description_td">Название</span><span class="driver_block_description_name">Phoenix Pheonix Bios, A04</span><span class="driver_block_download_link"><a href="http://downloads.dell.com/bios/AdamoXPS_A04.exe">Скачать</a></span>\n    <span class="driver_block_description_td">Версия: </span><span class="driver_block_description_version">A04</span>\n    <span class="driver_block_description_td">Дата выпуска: </span><span class="driver_block_description_date">03 ноя 2011</span>\n    <span class="driver_block_description_td">Размер (Мб): </span><span class="driver_block_description_size">5.2</span>\n    <span class="driver_block_description_td">Имя файла: </span><span class="driver_block_description_file_name">AdamoXPS_A04.exe</span>\n    </div>\n',
    #         'meta_d': 'Скачать бесплатно драйверы на высокой скорости для Dell adamo-xps [MS Windows 7, 64-разрядная версия]'}
    # my_sql.insert_book(trmf)


    serial_model_list = instance.serial_model()
    #serial_model_list = {'latitude_laptop': 'http://www.dell.com/support/home/ru/ru/rudhs1/Products/laptop/latitude_laptop'}
    dict_all_models = instance.selenium_parser(serial_model_list)#('http://www.dell.com/support/home/ru/ru/rudhs1/Products/laptop/inspiron_laptop')
    instance.craate(all_models=dict_all_models)



    instance.link_notebook(serial_model_list)
    url = r'http://www.dell.com/support/home/ru/ru/rudhs1/product-support/product/inspiron-1000/drivers'
    json_drivers = instance.request(url)
    instance.parser_json_driver(json_drivers)