from jsonschema import validate, Draft3Validator, Draft4Validator, exceptions, ErrorTree

schema = {
    "definitions": {
        "Ключ":{
            "type": "object",
            "properties": {
                "Тип": {"type": "string"},
                "Активирован": {"type": "string"},
                "СпособАктивации": {"type": "string"}
                },
            "required": ["Тип", "Активирован", "СпособАктивации"]
        },
        "Сертификат":{
            "type": "object",
            "properties": {
                "ИНН": {"type": "string"},
                "ФИО": {"type": "string"},
                "Должность": {"type": "string"},
                "Название": {"type": "string"},
                "Издатель": {"type": "string"},
                "СерийныйНомер": {"type": "string"},
                "Отпечаток": {"type": "string"},
                "Квалифицированный": {"type": "string"},
                "ДвоичныеДанные": {"type": "string"},
                "ДействителенС": {"type": "string"},
                "ДействителенПо": {"type": "string"},
                "Ключ": {"$ref": "#/definitions/Ключ"}
                },
            "required": ["ИНН", "ФИО", "Должность", "Название", "Издатель",
                         "СерийныйНомер", "Отпечаток", "Квалифицированный",
                         "ДвоичныеДанные", "ДействителенС", "ДействителенПо", "Ключ"]
        },
        "Файл":{
            "type": "object",
            "properties": {
                "Ссылка": {"type": "string"},
                "Имя": {"type": "string"}
            },
        },
        "Редакция":{
            "type": "object",
            "properties": {
                "Номер": {"type": "string"},
                "ДатаВремя": {"type": "string"}
            }
        },
        "Подпись":{
            "type": "array",
                "minItems": 1,
                "items": {
                        "type": "object",
                        "properties": {
                            "Тип":{"type": "string"},
                            "Сертификат":{"$ref": "#/definitions/Сертификат"},
                            "Файл":{"$ref": "#/definitions/Файл"}
                        },
                        "required": ["Тип", "Сертификат"]
                },
                "uniqueItems": True
        },
    },
    ################# НИЖЕ РЕАЛЬНАЯ СХЕМА #################
    "type": "object",
    "properties": {
            "doc": {
                    "$ref": "#/definitions/Подпись"
                },

    }
}
instance = {"doc":[
                    {
                        'Тип': 'Отсоединенная',
                        'Файл': {'Ссылка': 'https://test-oNC00J4iOjExMTI0NDV9&protocol=3&id=0',
                                'Имя': 'DP_IZVPOL_2B5.xml.p7s'
                        },
                        'Сертификат': {'Квалифицированный': 'Да',
                                        'Должность': 'server_key',
                                        'Отпечаток': 'CF87D824D9293771F8FD413223AF2F4ACA9688C6',
                                        'ДействителенПо': '06.03.2018 06.43.51',
                                        'ИНН': '7654321069',
                                        'Издатель': 'ca-simple-test, Удостоверяющий центр, ООО Тест, Ярославль, 76 Ярославская область, RU, test@test.ru, Московский проспект д.12, 7605016030, 1027600787994',
                                        'ДействителенС': '06.03.2015 06.43.51',
                                        'СерийныйНомер': '1068E0B7000000003786',
                                        'ДвоичныеДанные': '',
                                        'ФИО': 'Сервереый Тест Тестировович',
                                        'Ключ': {'Тип': 'Клиентский',
                                                 'СпособАктивации': '',
                                                 'Активирован': 'Нет'
                                        },
                                        'Название': 'ЮЛ1'
                        }
                   }
]}
errors = Draft4Validator(schema).iter_errors(instance)
#tree = ErrorTree(errors)
#qqq = errors.__next__()  .path[-1]
#ee = [e for e in sorted(errors, key=exceptions.relevance)]
#ee = [e.path[-1] for e in sorted(errors, key=exceptions.relevance)]
ee = [e for e in sorted(errors, key=str)]
print(ee) # ee 'absolute_path',
 # 'absolute_schema_path',
 # 'args',
 # 'cause',
 # 'context',
 # 'create_from',
 # 'instance',
 # 'message',
 # 'parent',
 # 'path',
 # 'relative_path',
 # 'relative_schema_path',
 # 'schema',
 # 'schema_path',
 # 'validator',
 # 'validator_value',
 # 'with_traceback'
Draft4Validator(schema).validate(instance)
ee[0].path