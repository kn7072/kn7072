# -*- coding: utf-8 -*-
from selenium import  webdriver
ff_Profile = r"D:\ff_profile"
ffp = webdriver.FirefoxProfile(ff_Profile)  # Установка профиля мозиллы, где ff_Profile - это путь к каталогу с профилем
driver = webdriver.Firefox(firefox_profile=ffp)

def error_console(f):
    list_error = []
    def fun(self, *args, **kwargs):
        f(self, *args, **kwargs)
        browser_error = driver.get_log('browser')
        error = [er['message'] for er in browser_error if er['level'] == 'SEVERE']
        if len(error) > len(list_error):
            error_massage = list_error[len(error):]
            error_massage = set(error_massage)  # убираем дубли ошибок
            v = '\n'.join(error_massage)
            massage = "во время выполнения теста были обнаружены следующие критические ошибки\n"+v

            #raise
        list_error.append(1)
    return fun

# w = error_console()
# for i in range(3):
#     w()


text_error_1 = """var elm = document.getElementById("gs_ok0");
                  elm.onclick = function(){throw "esssss"}"""

text_error_2 = """var elm = document.getElementById("gs_ok0");
                  elm.onclick=function(){throw "esssss";};
                  elm.addEventListener("click",function(){alert(qqq);},false);
                  elm.addEventListener("click",function(){var a = 1, b = "1"; console.assert(a === b, "A doesn't equal B");},false);
                  elm.addEventListener("click",function(){console.error("Ошибка: %s (%i)", "Сервер не отвечает",500);},false)

                  """

driver.get("http://www.google.ru")

driver.execute_script(text_error_2)
# driver.execute_script("console.clear()")

dr = driver.get_log('driver')
browser_error = driver.get_log('browser')
error = [er['message'] for er in browser_error if er['level'] == 'SEVERE']

error_massage = set(error)  # убираем дубли ошибок
v = ('\n'+" "*15).join(error_massage)
massage = "во время выполнения теста были обнаружены следующие критические ошибки:\n"+" "*15+v
raise Exception(massage)

cl = driver.get_log('client')
sv = driver.get_log('server')

print()
# http://internetka.in.ua/selenium-browser-logs/
# for (LogEntry logEntry : driver.manage().logs().get("browser").getAll()) {
#       System.out.println(logEntry);
# }