#=======================================================================================================================
# Скрипт служит для запуска набора тестов Jmeter записанных в списов scenarios (пусть указывать полный до проекта).
# Действия:
# 1) Создает директорию с текущей датой и временем, копирует в неё необходимые данные для запуска.
# 2) Запускает поочердно все проекты по два раза с задержкой 600 сек между запусками.
# 3) Строит все необходимые отчеты и графики.
# 4) Архивирует все содержимое папки в zip архив.
# 5) Удаляет все данные полученные в ходе тестирования: jtl, log, txt.
#=======================================================================================================================
# -*- coding: utf-8 -*-

import subprocess
import os
import time
import shutil
import csv
from xlsxwriter.workbook import Workbook

#Список проектов для запуска

scenarios = [
             #r'c:\inetpub\load_tests\Классификаторы\Классификаторы.Выборка\test.jmx',
             #r'c:\inetpub\load_tests\Классификаторы\Классификаторы.ЗаписьПоКоду\test.jmx',
             r'c:\inetpub\load_tests\Классификаторы\Классификаторы.НайтиМаксимальноПохожийОкато\test.jmx',
             #r'c:\inetpub\load_tests\Классификаторы\Классификаторы.Список\test.jmx',
             #r'c:\inetpub\load_tests\Классификаторы\Классификаторы.СписокДляАвтодополнения\test.jmx',
             #r'c:\inetpub\load_tests\Классификаторы\Классификаторы.СписокПоПолномуКоду\test.jmx',
             #r'c:\inetpub\load_tests\Классификаторы\Классификаторы.СписокРегионов\test.jmx',
             #r'c:\inetpub\load_tests\Классификаторы\Классификаторы.СписокРегионовСГородами\test.jmx',
             #r'c:\inetpub\load_tests\Классификаторы\Классификаторы.ПолучитьСправочникЦеликом\test.jmx',	 
            ]

#Время простоя между тестами
time_delay = 1

#Путь к Jmeter
Jmeter_path = r'c:\JMeter\bin\ApacheJMeter.jar'
#Путь к плагину для построения отчетов
CMDRunner_path = r'c:\JMeter\lib\ext\CMDRunner.jar'
#Путь к архиватору 7-zip
Arch_path = r'c:\7-Zip\7z.exe'

new_scenarios = []
filter_file = []

def run_and_copy(scenarios):
    '''Копирует файлы проекта
    
    Создает директорию в папке с проектом с текущей датой и временем. 
    Копирует в неё все необходимые файлы для запуска.
    Запускает тест.
    Задержка между запусками 600 сек.
    Возвращает новый список с путями для запуска тестов.
    
    '''
    
    for i in range(1):
        for scenario in scenarios:
            filter_file = []
            os.chdir(os.path.dirname(scenario))                      
            files = os.listdir(os.path.dirname(scenario))
            for file in files:
                if (file.endswith('.jtl') == file.endswith('.txt') == file.endswith('.log') == False and os.path.isfile(file) == True):
                    filter_file.append(file) 
            dir_name = time.strftime("%d%m%y_%H%M%S", time.localtime())
            os.mkdir(dir_name)      
            for file in filter_file:
                shutil.copyfile(os.path.join(os.path.dirname(scenario), file), os.path.join(os.path.dirname(scenario), dir_name, file))
            (folder, file_name) = os.path.split(scenario)
            new_scenarios.append(os.path.join(folder, dir_name, file_name))
            os.chdir(os.path.join(folder, dir_name))
            mon = subprocess.Popen(['python','test_monitor.py'])
            subprocess.call(['java', '-jar', Jmeter_path, '-n', '-t', os.path.join(folder, dir_name, file_name)])
            subprocess.Popen.terminate(mon)
            time.sleep(time_delay)
    return new_scenarios     
    
def build_report(scenarios):
    "Строит отчеты из полученных данных"
    
    for scenario in scenarios:
        os.chdir(os.path.dirname(scenario))
        
        subprocess.call(['java', '-jar', CMDRunner_path, "--tool", "Reporter"                       
                         ,"--generate-png", "response_times_vs_threads.png", '--input-jtl', r"{0}\response_times_vs_threads.jtl"
                         .format(os.path.dirname(scenario)),
                         '--plugin-type', 'TimesVsThreads', '--exclude-labels', 'Авторизация на сайте','--width', '1200', '--height', '900'])

        subprocess.call(['java', '-jar', CMDRunner_path, "--tool", "Reporter"
                         ,"--generate-png", "response_times_over_time.png", '--input-jtl', r"{0}\response_times_vs_threads.jtl"
                         .format(os.path.dirname(scenario)),
                         '--plugin-type', 'ResponseTimesOverTime', '--exclude-labels', 'Авторизация на сайте', '--width', '1200', '--height', '900'])            
                                     
        subprocess.call(['java', '-jar', CMDRunner_path, "--tool", "Reporter"                       
                         ,"--generate-png", "response_codes_per_second.png", '--exclude-labels', 'Авторизация на сайте', '--input-jtl', r"{0}\response_times_vs_threads.jtl"
                         .format(os.path.dirname(scenario)),
                         '--plugin-type', 'ResponseCodesPerSecond', '--width', '1200', '--height', '900'])
        
        subprocess.call(['java', '-jar', CMDRunner_path, "--tool", "Reporter"                       
                         ,"--generate-csv", "summary.csv", '--input-jtl', r"{0}\response_times_vs_threads.jtl"
                         .format(os.path.dirname(scenario)),
                         '--plugin-type', 'AggregateReport'])
         
        
def archive_data(scenarios):
    "Архивирует все содержимое папки в архив с название директории"
    
    for scenario in scenarios:
        os.chdir(os.path.dirname(scenario))
        path = scenario.split(os.sep)
        zip_dir = path[len(path)-2]
        zip_path = os.path.join(os.path.dirname(scenario), zip_dir + '.zip')
        subprocess.check_call([Arch_path, "a", "-tzip", "-ssw", "-mx4", zip_path, os.path.dirname(scenario)])

def delete_data(scenarios):
    "Удаляет все .jtl, .log, .txt из папки"
    
    for scenario in scenarios:
        os.chdir(os.path.dirname(scenario))
        files = os.listdir(os.path.dirname(scenario))
        for file in files:
            if (file.endswith('.jtl') == True or file.endswith('.txt') == True or file.endswith('.log') == True):
                os.remove(file)
				
def export_exel(scenarios):
    "Строит exel отчет по тесту"
    
    metrics = [
               'Общее кол-во запросов',
               'Среднее время отклика, мс',
               'median',
               '90% line',
               'Минимальное время отклика, мс',
               'Максимальное время отклика, мс',
               'Процент ошибок',
               'Кол-во запросов в секунду',
               'Пропускная способность, Kb/sev',
               'Сред.квадратичное отклонение'
               ]                         
    
    reports = ([
               'response_codes_per_second.png',
               'response_times_over_time.png',
               'response_times_vs_threads.png'
               ],
               [
                'Изменение количества кодов в секунду в ходе испытания',
                'Изменение времени ответа в ходе испытания',
                'Изменение времени ответа в зависимости от кол-ва пользователей',
                ])
    i = 0
    test_number = 1
    work_doc = Workbook('report.xlsx')
    sheet = work_doc.add_worksheet(time.strftime("%d%m%y", time.localtime()))
    sheet.set_column(0, 0, 35)
    sheet.set_column(1, 1, 15)
    for scenario in scenarios:
        os.chdir(os.path.dirname(scenario))
        with open ('summary.csv','r') as f:
            reader = csv.reader(f, delimiter = ',')
            parameters = list(reader)        
        
        sheet.write(i, 0, 'Тест №%s. %s' % (test_number, parameters[2][0]))
        sheet.write(i+2, 0, 'Метрика')
        sheet.write(i+2, 1, 'Результат')       
        
        for a in range(len(metrics)):
            sheet.write(i+a+3, 0, metrics[a])
            sheet.write(i+a+3, 1, parameters[2][a+1])
        
        i += 16
        
        for a in range(len(reports[0])):
            sheet.insert_image(i, 0, reports[0][a], {'x_scale': 0.5, 'y_scale': 0.5})
            sheet.write(i+23, 0, 'Рис.%s.%s. %s' % (test_number, a+1, reports[1][a]))
            i += 28    
        test_number +=1
        
    sheet.write(i, 0, 'Выводы')
    work_doc.close()
      
new_scenarios = run_and_copy(scenarios)
build_report(new_scenarios)
archive_data(new_scenarios)
delete_data(new_scenarios)
export_exel(new_scenarios)