# -*- coding: utf-8 -*-
# импортируем pymongo
import pymongo
# подключаемся к другому серверу, на другой порт
conn = pymongo.Connection('localhost', 27017)
# выбираем базу данных # БД можно выбрать и так  db = conn['mydb']
db = conn.har
# выбираем коллекцию документов # альтернативный выбор коллекции документов coll = db['mycoll']
coll = db.json_har
# осуществляем добавление документа в коллекцию,
# который содержит поля name и surname - имя и фамилия
doc = {"name":"Иван", "surname":"Иванов"}
coll.save(doc)
