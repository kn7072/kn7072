# -*- coding: utf-8 -*-
import unittest
from atf import *
from atf.config import Config
from pages.left_panel import *
from pages import design_area_demo
from atf import logfactory

class TestEventPanel(ATFSuite):
    """Тестирование событий кнопки"""
    
    LIST_OF_TESTS_FOR_RUN = Config().LIST_OF_TESTS_FOR_RUN
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.run_browser(cls)
        cls.open(cls, Config().SITE)
        # включаем отображение тестовой страницы
        left_pnl = LeftPanel(cls)
        left_pnl.open_page('genie-test-cloud > Основной сервис > Стенд > Page_for_tests > Page2 > Page2.module.js')
        left_pnl.open_page('Page2.xhtml')
        palette = design_area_demo.PalettePanel(cls)
        palette.tab.click()
                
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        
    @unittest.skipIf(LIST_OF_TESTS_FOR_RUN!='' and "01" not in LIST_OF_TESTS_FOR_RUN, "Пропустить тест")
    def test_01_drag_and_drop_button(self):
        "01. перетаскивание кнопки для тестирования"

        message = "hello world"
        logfactory.Log().WriteEvent(report(self.driver, message), "message", [None, "errors"])
        logfactory.log('комент', "action")
        #logfactory.Log(report(self.driver,message))

        print(self.browser.get_window_position())
        area = design_area_demo.AreaPanel(self)
        palette = design_area_demo.PalettePanel(self)
        properties = design_area_demo.PropertiesPanel(self)
        events = design_area_demo.EventsPanel(self)
        self.browser.switch_to_parent_frame()
        palette.tab.click()
        overlay_x = area.overlay.position[0]
        overlay_y = area.overlay.position[1]
        palette.search.clear()
        palette.search.add_text("Button")
        # определение координат элемента  Button в palette
        btn_x = palette.btn.position[0]
        btn_y = palette.btn.position[1]
        # перетаскиваем первую Button
        palette.btn.drag_and_drop_by_offset(overlay_x - btn_x , overlay_y - btn_y )
        self.browser.switch_to_frame(0)
        # кликаем по тестируемой кнопке 
        area.button_in_event_panel.click()
        self.browser.switch_to_parent_frame()
        events.events_panel.click()
        events.on_activated_create.click()
        edition = Editor(self.driver, "xpath", "//div[@class ='ace_layer ace_text-layer']")
        #находим текущее положение курсора
        num_line = edition.cursor().row_number
        q= edition.line(num_line-1).text
        q2 = edition.line(contains_text='onActivated').text
        #проверяем что строка находящаяся выше курсора содержит в себе название созданного события
        self.assertTrue(self.wait(lambda: 'onActivated' in edition.line(num_line-1).text),
                        "строка идущая выше курсора не содежит текст 'onActivated'")
        events.page2_xhtml.click()
        # закрываю вкладку Page2.module.js 
        events.close_page2_module_js.click()
        # проверяем что вкладка закрылась
        self.assertTrue(self.wait(lambda: not events.close_page2_module_js.is_present()),
                        "вкладка не закрылась")
        # кликаем по названию события on_activated и должен снова открыться ранее закрытый файл(вкладка) Page2.module.js
        events.on_activated.click()
        
        self.assertTrue(self.wait(lambda: events.close_page2_module_js.is_present()),
                        "вкладка не открылась")
        num_line = edition.cursor().row_number
        self.assertTrue(self.wait(lambda: 'onActivated' in edition.line(num_line-1).text),
                        "строка идущая выше курсора не содежит текст 'onActivated'")

        w = ['hallo world', 'sting', 'batman']
        edition.cursor().add_code(2, w)
        text = edition.line().text_all()
        pass
   
if __name__ == '__main__':
    unittest.main(testRunner=XMLTestRunner(output='test-reports'))