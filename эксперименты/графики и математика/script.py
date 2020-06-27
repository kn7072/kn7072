# coding:utf8
import requests
import logging
import sys
import lxml.html as html
import json
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import re
import sys
import os

ditectoty_work = os.getcwd()  # путь к катологу от куда запущен скрипт
template_driver = '<div class="driver_block_header">%(category)s</div>' \
                  '   <div class="driver_block_description">\n' \
                  '      <span class="driver_block_description_name">%(driver_name)s</span>\n' \
                  '      <span class="driver_block_description_date">%(LUPDDate)s</span>\n' \
                  '      <span class="driver_block_description_version">%(DellVer)s</span>\n' \
                  '      <span class="driver_block_description_size">%(file_size)s</span>\n' \
                  '      <span class="driver_block_description_file_name">%(file_name)s</span>\n' \
                  '   </div>\n   ' \
                  '   <div class="driver_block_download_link">\n' \
                  '      <a href="%(HttpFileLocation_cur)s" rel="external">Скачать</a>\n' \
                  '   </div>\n'

other_driver =    '   <div class="driver_block_description_other_version">\n' \
                  '      <span class="driver_block_description_size">%(file_size)s</span>\n' \
                  '      <span class="driver_block_description_file_name">%(file_name)s</span>\n' \
                  '   </div>\n' \
                  '   <div class="driver_block_download_link">\n' \
                  '      <a href="%(HttpFileLocation)s" rel="external">Скачать</a>\n' \
                  '   </div>\n'
class ParserDELL:
    """забираем ссылку с сайта dell"""
    def request(self, url):
        """метод получает код страницы по адресу url"""
        auth = requests.auth.HTTPProxyAuth('sg.chernov', 'QWEqwe123')
        headers0 = {'Content-Type': 'application/json; charset=UTF-8'}
        r = requests.get(url, headers=headers0, verify=False, auth=auth)
        #r = requests.get(url)
        text = r.text  # код страницы
        table = html.fromstring(text)  # объект html
        obj = table.get_element_by_id('tagDrivers')  # объект содержащий все информацию о драйверах
        j = json.loads(obj.attrib['value'])
        list_json = j['GroupItem']  # список джейсонов их количесто соответствует количеству категорий
        return list_json

    def parser_json_driver(self, list_json, file_name_to_save):
        """метод получает на вход список джейсонов и парсит их"""
        count_json = len(list_json)  # сколько джейсонов пришло
        file_to_save = r'%s.txt' % file_name_to_save
        with open(file_to_save, encoding='utf-8', mode='w') as f:  # открыли файл для записи w - запись, если файла нет
            # то он будет создан, если существует то будет перезаписан
            for json_driver in list_json:
                f.write('<div class="driver_block">\n')
                count_driver_cat = len(json_driver['Drivers'])
                category = json_driver['GroupItemName']  # общая категория X1
                for i in range(count_driver_cat):
                    temp = {}  # словарь для удобства хранения информации
                    temp['category'] = category
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
                    temp['file_size'] = file_size  # X5
                    file_name = drivers['FileFrmtInfo']['FileName']
                    temp['file_name'] = file_name  # X6
                    HttpFileLocation_cur = drivers['FileFrmtInfo']['HttpFileLocation']  # ссылка на скачивание
                    temp['HttpFileLocation_cur'] = HttpFileLocation_cur  # X7
                    # другие доступные форматы файлов
                    OthFileFrmts = drivers['OthFileFrmts']  # список словарей с доступными версиями
                    write_templete = template_driver % temp
                    f.write(write_templete)
                    count_OthFileFrmts = len(OthFileFrmts)
                    # если count_OthFileFrmts то значит других драйверов нет
                    for j in range(1, count_OthFileFrmts):
                        temp_other_driver = {}
                        file_size = OthFileFrmts[j]['FileSize']
                        temp_other_driver['file_size'] = file_size  # размер файла
                        filename = OthFileFrmts[j]['FileName']
                        temp_other_driver['file_name'] = filename  # имея файла
                        HttpFileLocation = OthFileFrmts[j]['HttpFileLocation']
                        temp_other_driver['HttpFileLocation'] = HttpFileLocation  # ссылка для скачивания
                        write_templete_other_driver = other_driver % temp_other_driver
                        f.write(write_templete_other_driver)
                    f.write("################ NEW DRIVER ################\n")

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
        all_models = self.temp_dict
        for cat, dict_molel in all_models.items():
            # на каждую категорию подобную egacylp
            path = ditectoty_work +'\\DRIVERS\\' + cat  # в директории где запущен скрипт будет создан
            # общий католог DRIVERS а в нем дочерние каталоги по категориям
            if not os.path.isdir(path):
                try:
                    os.makedirs(path)
                except OSError:
                    print("каталог уже существует или католог не может быть создан")
            # каталоги созданы - теперь начинается самое интересное
            for model, link in dict_molel.items():
                list_json = self.request(link)
                path_to_save = path + "\\%s" % model
                self.parser_json_driver(list_json, file_name_to_save = path_to_save)

if __name__ == "__main__":
    instance = ParserDELL()
    instance.craate()


    serial_model_list = instance.serial_model()
    dict_all_models = instance.selenium_parser(serial_model_list)#('http://www.dell.com/support/home/ru/ru/rudhs1/Products/laptop/inspiron_laptop')
    instance.link_notebook(serial_model_list)
    url = r'http://www.dell.com/support/home/ru/ru/rudhs1/product-support/product/inspiron-1000/drivers'
    json_drivers = instance.request(url)
    instance.parser_json_driver(json_drivers)