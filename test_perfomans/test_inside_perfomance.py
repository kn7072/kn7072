# -*- coding: utf-8 -*-

import atf
import unittest
from datetime import datetime
import time
from pages.test_online.login import LoginPage
from pages.test_online.main import MainPage
from pages.test_online.kontragents.main import KontragentMainPage
from pages.test_online.documents.index import DocsPage
from pages.test_online.reports.fns import ReportsFNS
import numpy as np
from atf.helper import performance


class TestPagesPerfomance(atf.ATFSuite):
    """Данный набор тестов предназначен для тестирования времени открытия остновных страниц сайтов"""

    @classmethod
    def setUpClass(cls):
        file = open('./templates/header.template', 'r', encoding='utf-8')
        header = file.read()
        file.close()
        file = open('results_inside.jtl', 'w', encoding="utf-8")
        file.write(header)
        file.close()

    def setUp(self):
        atf.ATFSuite.setUp(self)
        page = LoginPage(self)
        self.browser.open("http://test-insidexxx")
        page.login_as("Демо", "Демо123")
        time.sleep(5)

    @classmethod
    def tearDownClass(cla):
        file = open('./templates/bottom.template', 'r', encoding='utf-8')
        bottom = file.read()
        file.close()
        file = open("results_inside.jtl", 'a', encoding='utf-8')
        file.write(bottom)
        file.close()

    @performance("MainPage")
    def test_online_main_page(self):
        """Тест на время открытия разводящей страницы"""

        page = MainPage(self)
        self.browser.refresh()
        self.assertTrue(wait(lambda: page.events_table.size() > 5),
                        "Не загрузилась таблица с извещениямми")


    @performance("KontragentsPage")
    def test_online_kontragents_page(self):
        """Тест на время открытия контрагентов"""

        page = KontragentMainPage(self)
        self.browser.open("http://test-insidexxx" + "/contragents.html")
        self.assertTrue(wait(lambda: page.regions_tbl.rows_number == 10),
                        "Не дождались загрузки таблицы")
        self.assertTrue(wait(lambda: page.companies_top_tbl.rows_number == 10),
                        "Не дождались загрузки таблицы")
        self.assertTrue(wait(lambda: page.owners_tbl.rows_number == 10),
                        "Не дождались загрузки таблицы")

    @performance("DocsPage")
    def test_online_documents_page(self):
        """Тест на время открытия страницы документооборота"""

        page = DocsPage(self)
        self.browser.open("http://test-insidexxx" + "/edo.html")
        self.assertTrue(wait(lambda: page.out_link.is_present),
                        "Не дождались загрузки таблицы")

    @performance("ReportsPage")
    def test_online_reports_page(self):
        """Тест на время открытия страницы отчётности"""

        page = ReportsFNS(self)
        self.browser.open("http://test-insidexxx" + "/ereport.html#list=ОтчетФНС")
        self.assertTrue(wait(lambda: page.reports_tbl.is_present),
                        "Не дождались загрузки таблицы")


if __name__ == '__main__':
    unittest.main(testRunner=atf.XMLTestRunner(output='test-reports'))