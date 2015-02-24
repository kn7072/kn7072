# -*- coding: utf-8 -*-
import pymysql
host = '127.0.0.1'  # http://itdell.ru:3306 http://itdell.ru   http://mysql.remtvstudio.myjino.ru
database = 'remtvstudio_test'
user = '045333190_test'  # 045333190_test
password = 'testpassword2015'  # testpassword2015
host_2 = 'http://mysql.remtvstudio.myjino.ru'

ssh_host = 'remtvstudio.myjino.ru'
ssh_login = 'remtvstudio'
ssh_password = 'testpassword2014'

conn = pymysql.connect(host=host, port=3306, user=user, passwd=password, db=database)

cur = conn.cursor()