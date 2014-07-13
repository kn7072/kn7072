# -*- coding: utf-8 -*-

# import atf
# from atf.helper import wait
# import unittest
from datetime import datetime
import time
# import string
# from pages.test_online.login import LoginPage
# from pages.test_online.main import MainPage
# from pages.test_online.kontragents.main import KontragentMainPage
# from pages.test_online.documents.index import DocsPage
# from pages.test_online.reports.fns import ReportsFNS
from matplotlib import numpy as np
# from pages.test_online.kontragents import main
# from pages.test_online.kontragents import card

def performance(name, count=30):
    """Реализует декоратор для измерения времени отработки кода тестового метода"""

    def decorator(f):

        def wrapper(*args):
            results = []
            file = open('./templates/sampler.template', 'r', encoding='utf-8')
            sampler = file.read()
            file.close()
            #число неудавшихся измерений
            failure = 0
            for i in range(count):
                results_file = open('results.jtl', 'a', encoding='utf-8')
                time.sleep(2)
                start_time = datetime.now()
                success = True
                try:
                    f(*args)
                except Exception as e:
                    print(e)
                    success = False
                if success:
                    finish_time = datetime.now()
                    duration = int((finish_time - start_time).total_seconds() * 1000)
                    sampler_success = 'true'
                else:
                    duration = 1000
                    sampler_success = 'false'
                    failure += 1
                results.append(duration)
                print(name)
                results_file.write(sampler.format(str(duration), name, str(int(time.time() * 1000)), sampler_success))
                results_file.close()
                print(duration)
            avg = sum(results) / len(results)
            print(avg)
            if failure*100/count < 3:
                file = open(name + '_trends.csv', 'a', encoding='utf-8')
                dt = datetime.strftime(datetime.now(), '%y/%m/%d %H:%M:%S')
                file.write('\n{0};{1};{2};{3}'.format(dt, str(np.median(results)), min(results), max(results)))
                file.close()
        return wrapper
    return decorator

class TestPagesPerfomance(atf.ATFSuite):
    """Данный набор тестов предназначен для тестирования времени открытия остновных страниц сайтов"""

    @classmethod
    def setUpClass(cls):
        file = open('./templates/header.template', 'r', encoding='utf-8')
        header = file.read()
        file.close()
        file = open('results.jtl', 'w', encoding="utf-8")
        file.write(header)
        file.close()

    def setUp(self):
        atf.ATFSuite.setUp(self)
        page = LoginPage(self)
        self.browser.open(self.config.SITE)
        page.login_as(self.config.USER_NAME, self.config.PASSWORD)
        time.sleep(25)

    @classmethod
    def tearDownClass(cla):
        file = open('./templates/bottom.template', 'r', encoding='utf-8')
        bottom = file.read()
        file.close()
        file = open("results.jtl", 'a', encoding='utf-8')
        file.write(bottom)
        file.close()

    @performance("MainPage")
    def test_online_main_page(self):
        """Тест на время открытия разводящей страницы"""

        page = MainPage(self)
        self.browser.refresh()
        self.assertTrue(wait(lambda: page.org_table.size[0] > 0),
                        "Не загрузилась таблица с организациями")


    @performance("KontragentsPage")
    def test_online_kontragents_page(self):
        """Тест на время открытия контрагентов"""

        page = KontragentMainPage(self)
        self.browser.open(self.config.SITE + "/contragents.html")
        self.assertTrue(wait(lambda: page.regions_tbl.rows_number == 10),
                        "Не дождались загрузки таблицы")
        self.assertTrue(wait(lambda: page.companies_top_tbl.rows_number == 15),
                        "Не дождались загрузки таблицы")
        self.assertTrue(wait(lambda: page.owners_tbl.rows_number == 15),
                        "Не дождались загрузки таблицы")

    @performance("DocsPage")
    def test_online_documents_page(self):
        """Тест на время открытия страницы документооборота"""

        page = DocsPage(self)
        self.browser.open(self.config.SITE + "/edo.html")
        self.assertTrue(wait(lambda: page.out_link.is_present),
                        "Не дождались загрузки таблицы")

    @unittest.skip('Сейчас отдел отчётности не фурычит')
    @performance("ReportsPage")
    def test_online_reports_page(self):
        """Тест на время открытия страницы отчётности"""

        page = ReportsFNS(self)
        self.browser.open(self.config.SITE + "/ereport.html#list=ОтчетФНС")
        self.assertTrue(wait(lambda: page.reports_tbl.is_present),
                        "Не дождались загрузки таблицы")

    def open_card(self):
        page = main.KontragentMainPage(self)
        page.all_kontrag_tbl.cell(contains_text='Компания "Тензор"').click()
        page = card.common.KontragentCardCommonPage(self)
        #page.data_tab.click()

        page = card.general.CardGeneralPage(self)
        #self.assertTrue(wait(lambda: page.name_txt.inner_html == 'Общество с ограниченной ответственностью  "Компания "Тензор"'),
        #                "Отсутствует или не верно название организации")
        self.assertTrue(wait(lambda: page.telephone_tbl.rows_number >= 1),
                        "Отсутствуют телефоны на странице")
        self.assertTrue(wait(lambda: page.telephone_add_btn.is_present),
                        "Отсутствует кнопка добавления телефона")
        page = card.common.KontragentCardCommonPage(self)
        page.close_btn.click()


    @performance("OpenCard")
    def test_online_open_card(self):
        """Тест на время открытия карточки контрагента"""
        page = main.KontragentMainPage(self)
        self.browser.open(self.config.SITE + "/contragents.html")
        page.search_inp.type_in("7605016030")
        page.search_btn.click()
        wait(lambda: 'Тензор' in page.all_kontrag_tbl)
        self.open_card()

if __name__ == '__main__':
    unittest.main(testRunner=atf.XMLTestRunner(output='test-reports'))