import unittest
from unittest_data_provider import data_provider
from atf import logfactory
from atf.reporter import *
from atf import *
from atf.config import Config
from atf.config import Config
from pages.left_panel import *
from pages.elements import buttons

def data_provider(fn_data_provider):
    """Data provider decorator, allows another callable to provide the data for the test"""
    def test_decorator(fn):
        def repl(self, *args):
            for i in fn_data_provider():
                try:
                    fn(self, *i)
                except AssertionError:
                    print("Assertion error caught with data set ", i)
                    raise
        return repl
    return test_decorator

class TestEle(ATFSuite):
    "Тестирование элементов > кнопки > стандартные"

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        #ATFSuite.setUp(self)
        cls.run_browser(cls)
        cls.open(cls, Config().SITE)
        # включаем отображение тестовой страницы
        left_pnl = LeftPanel(cls)
        left_pnl.open_page('genie-test-cloud > Основной сервис > Стенд > demoControls > Buttons > Standart.xhtml')
        cls.browser.maximize_window()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    itemIds = lambda: (('q42',), ('Q42',), ('Q1', ), ('Q1000',), ('Q31337',),)
    #itemIds = (('q42',), ('Q42',), ('Q1', ), ('Q1000',), ('Q31337',),)


    @data_provider(itemIds)
    def test_01_menu_btn_properties(self, itemString):
        "03. Проверяем свойства кнопки-меню"
        area = buttons.ButtonsStandartPage(self)
        properties = buttons.PropertiesPanel(self)
        area.menu_btn.click()
        self.browser.switch_to_parent_frame()
        self.assertTrue(self.wait(lambda: 'button with' in properties.caption.text()),
                        "В свойствах кнопки-меню не верный caption")
        self.assertTrue(self.wait(lambda: properties.enabled.state == True),
                        "В свойствах кнопки-меню не верно выставлен чекбокс enabled")
        logfactory.log("qqq"+itemString)

if __name__ == '__main__':
    unittest.main(testRunner=XMLTestRunner(output='test-reports'))