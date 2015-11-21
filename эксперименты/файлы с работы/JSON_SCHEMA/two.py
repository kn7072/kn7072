from jsonschema import validate, Draft3Validator, Draft4Validator, exceptions
schema = {
    "items": {
        "anyOf": [
            {"type": "string", "maxLength": 25},
            {"type": "integer", "minimum": 5}
        ]
    }
}
instance = [{"foo"}, 3222222, "foo",  "fooeeeeeeeeeeee"]
v = Draft4Validator(schema)
errors = sorted(v.iter_errors(instance), key=lambda e: e.path)
for error in errors:
    print(error.message)
print()
#########################################
schema = {
    "type" : "array",
    "items" : {"type" : "number", "enum" : [1, 2, 3]},
    "minItems" : 3,
}
instance = ["spam", 2]
v = Draft3Validator(schema)
errors = sorted(v.iter_errors(instance), key=lambda e: e.path)
for error in errors:
    print(error.message)
print("#########################################")
#########################################
schema = {
    "properties": {
    "name": {"type": "string"},
    "phones": {
        "properties": {
            "home": {"type": "string"},
            "xxx": {"type": "number"},
            "dict_": {
                "type": "array",
                "items": {
                    "type": "string",
                    "enum": ["n", "g"]
                },
                "uniqueItems": True
                }
            },
            "required": ["xxx"]
        },

    },
    "required": ["name"]
}
instance_err = {"name": 123, "phones": {"home": [123]}}
instance = {"name": "eeeeee", "phones": {"home": "23456", "xxx": 5555}}
instance_req = {"name": "eeeeee", "phones": {"home": "23456", "xxx": 5555, "yyyy": 5555, "dict_" :['n', 'g', 'W']}}  #'n', 'g' , "xxx": 5555
errors = Draft4Validator(schema).iter_errors(instance_req)
qqq = errors.__next__()
ee = [e.path[-1] for e in sorted(errors, key=exceptions.relevance)]
print(ee)



