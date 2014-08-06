from selenium import webdriver
from time import sleep
from subprocess import Popen, PIPE, call
import re
from datetime import datetime
import unittest
import time

def save_report_coverage(driver):
	"""выполняет скрип для сохранения промежуточных изменений о покрытии в отчет"""
	return
	with open('store.js', encoding='utf-8', mode='r') as f:
	            code_script = f.read()
	            driver.execute_script(code_script)
	sleep(2)

def kill_browser(fun):
    def wrapper(*args):
        pid_kill_browser = str(args[0].driver.binary.process.pid)
        fun(*args)
        proc = Popen(['wmic', 'process', 'get', 'ProcessId'], stdout=PIPE)
        out = proc.stdout.read().decode(encoding='utf-8')
        reg = re.compile('.(?:\\r\\r\\n)(?P<pid>[\d]{1,4})')
        list_pid = reg.findall(out)
        if pid_kill_browser in list_pid:
                call(['taskkill', '/PID', str(pid_kill_browser), '/F'])
    return wrapper

def pid_logger(fun):
    def wrapper(*args):
        fun(*args)
        pid_browser = str(args[0].driver.binary.process.pid)
        dt = datetime.strftime(datetime.now(), '%y/%m/%d %H:%M:%S')
        with open("pid_logger.csv", 'a', encoding='utf-8') as f:
            f.write('\n{0};{1};{2}'.format(dt, args[0].__module__, pid_browser))
    return wrapper

class Perfomans(unittest.TestCase):

    def setUp(self):
        print("setUp")
    def tearDown(self):
        #graf()
        print("tearDown")
        # IF EXIST node.pid (for /F %%i in (node.pid) do taskkill /F /T /PID %%i)


    @classmethod
    @kill_browser
    def tearDownClass(cls):
        print("sdfsdfsdfsdfdsf")
        cls.driver.quit()

    @classmethod
    def setUpClass(cls):
        print("sdfsdfsdfsdfdsf")
        driver = webdriver.Firefox()
        driver.get("http://www.google.ru")
        cls.driver = driver

    def test_online_main_page(self):
            """Тест на время открытия разводящей страницы"""

            # driver = webdriver.Firefox()
            # driver.get("http://www.google.ru")
            time.sleep(1)
            print(time.time())
            # print(driver.binary.process.pid)
            #
            # pid_kill_brouser = str(driver.binary.process.pid)
            # proc = Popen(['wmic', 'process', 'get', 'ProcessId'], stdout=PIPE)
            # out = proc.stdout.read().decode(encoding='utf-8')
            # reg = re.compile('.(?:\\r\\r\\n)(?P<pid>[\d]{1,4})')
            # list_pid = reg.findall(out)
            # #driver.quit()
            # if pid_kill_brouser in list_pid:
            #     call(['taskkill', '/PID', str(pid_kill_brouser), '/F'])

if __name__ == '__main__':
    unittest.main()