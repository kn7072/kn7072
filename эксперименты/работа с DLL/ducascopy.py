# -*- coding:utf-8 -*-

import selenium
from selenium import webdriver
import time
driver = webdriver.Firefox()

# https://demo-login.dukascopy.com/binary/
# $$(".bp-call-btn") $$(".bp-put-btn")
# yes #button-1006-btnInnerEl
# no #button-1007-btnInnerEl
# Login	    Seamans143
# Password	4dd9b2d4
driver.get("https://demo-login.dukascopy.com/binary/") # http://google.ru

def is_displayed(locator = 'button-1006-btnInnerEl'):
    """Воозвращает True, если элемент отображается для пользователя"""

    time_end = time.time() + 5  # self.config.WAIT_ELEMENT_LOAD
    print(time.time())
    result = None
    while True:
        try:
            elm = driver.find_element_by_id(locator)
            result = elm.is_displayed()
            if result:
                print(time.time())
                elm.click()
                return result
            break
        except Exception as error:
            result = error
        if time.time() > time_end:
            break

    return result
def call():
    call_btn = driver.find_element_by_class_name('bp-call-btn')
    call_btn.click()
    res = is_displayed()
    #if res:
    #    driver.find_element_by_id('button-1006-btnInnerEl').click()

# Login	    Seamans143
# Password	4dd9b2d4
call()
print()