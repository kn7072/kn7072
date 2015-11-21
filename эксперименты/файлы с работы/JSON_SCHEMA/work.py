from jsonschema import validate, Draft3Validator, Draft4Validator, exceptions, ErrorTree
# http://habrahabr.ru/post/158927/
# http://spacetelescope.github.io/understanding-json-schema/structuring.html
# http://spacetelescope.github.io/understanding-json-schema/reference/combining.html
schema_ex = {
    "id": "urn:product_name#",
    "type": "string",
    "minLength": 3,
    "maxLength": 5
}
schema = {
    "definitions": {
        "address": {
            "type": "object",
            "properties": {
                "street_address": {"type": "string"},
                "city":           {"type": "string"},
                "state":          {"type": "string"}
                },
            "required": ["street_address", "city", "state"]
        },
        "diskUUID": {
            "type": "string",
            "maxLength": 5
        },
    },


    "type": "object",
    "properties": {
        "Сертификат": {
            "type": "object",
            "properties": {
                "Квалифицированный": {"type": "string"},
                "СерийныйНомер": {"type": "string"},
                "Должность": {"type": "string"},
                "name": {
                    "$ref": "#/definitions/address"
                },
            },
            "required": ["Квалифицированный", "СерийныйНомер", "Должность", "name"]
        },
        "Файл": {
            "type": "object",
            "properties": {
                "Ссылка": {"type": "string"},
                "Имя": {"type": "string"},
                "mause":
                    {"$ref": "#/definitions/diskUUID"}
            },
            "required": ["Ссылка", "Имя", "mause"]
        }
    }
}

instance = {"Сертификат":
                {"Квалифицированный": "eeeeee",
                 "СерийныйНомер": "eeeeee",
                 "Должность": "eeeeee",
                 "name":
                     {"street_address": "e",
                      "city": "q",
                      "state": "ss"
                     }
                },  # , "name":"QQQQQQ"
            "Файл": {"Ссылка": "http", "Имя": "hallo", "xxxxxxxxxxx":10, "mause":"rrrww"}} #

errors = Draft4Validator(schema).iter_errors(instance)
#tree = ErrorTree(errors)
#qqq = errors.__next__()
ee = [e.path[-1] for e in sorted(errors, key=exceptions.relevance)]
print(ee)