from selenium import webdriver
import time
from subprocess import Popen, PIPE, call
import unittest
import re

def kill_brouse(fun):
    def wrapper(*args):
        pid_kill_brouser = str(args[0].driver.binary.process.pid)
        fun(*args)
        proc = Popen(['wmic', 'process', 'get', 'ProcessId'], stdout=PIPE)
        out = proc.stdout.read().decode(encoding='utf-8')
        reg = re.compile('.(?:\\r\\r\\n)(?P<pid>[\d]{1,4})')
        list_pid = reg.findall(out)
        if pid_kill_brouser in list_pid:
                call(['taskkill', '/PID', str(pid_kill_brouser), '/F'])
    return wrapper

class Perfomans(unittest.TestCase):

    def setUp(self):
        print("setUp")
    def tearDown(self):
        #graf()
        print("tearDown")
        # IF EXIST node.pid (for /F %%i in (node.pid) do taskkill /F /T /PID %%i)


    @classmethod
    @kill_brouse
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