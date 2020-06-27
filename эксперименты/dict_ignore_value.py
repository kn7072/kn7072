# coding=utf-8

x = {"z":None,
     "e":{"b":None}}

def replace_none(obj):
    for key, value in obj.items():
        if value == None:
            obj[key] = "ignore"
        if type(value) == dict:
            replace_none(value)

replace_none(x)
print(x)