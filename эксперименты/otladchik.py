# -*- coding: utf-8 -*-
import unittest
from atf import *
import pack
from atf.config import Config
from pages import design_area_demo
from pages.left_panel import LeftPanel
import codecs

class TestTextTemplate(ATFSuite):
    """Проверка идентичности кода страницы шаблону"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.run_browser(cls)
        cls.browser.open(Config().SITE)
        # включаем отображение тестовой страницы
        # left_pnl = LeftPanel(cls)
        # left_pnl.open_page('genie-test-cloud > Основной сервис > Стенд > Page_for_tests >  PageInner > PageInner.module.js')

        # palette = design_area_demo.PalettePanel(cls)
        # palette.tab.click()

    def tearDown(self):
        super().tearDown()
        self.browser.switch_to_parent_frame()

    def test_01_dialog_tab_control(self):
        """01. перетаскивание диалога и TabControl в поле диалога"""

        area = design_area_demo.XXX(self)
        self.browser.switch_to_frame(0)
        self.browser.switch_to_parent_frame()






if __name__ == '__main__':
    unittest.main(testRunner=XMLTestRunner(output='test-reports'))
