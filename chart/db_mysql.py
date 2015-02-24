# -*- coding: utf-8 -*-

import MySQLdb

try:
    con = MySQLdb.connect(host="localhost", user="root", passwd="5213", db="test")
    cur = con.cursor()