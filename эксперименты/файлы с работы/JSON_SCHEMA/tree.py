from jsonschema import validate, Draft3Validator, Draft4Validator, exceptions
schema = {
    "type": "object",
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
                    "enum": ["n", "g", "a", "c"]
                },
                "uniqueItems": True,
                "minItems": 4,
                }
            },
            "required": ["xxx"]
        },

    },
    "required": ["name"]
}
instance_err = {"name": 123, "phones": {"home": [123]}}
instance = {"name": "eeeeee", "phones": {"home": "23456", "xxx": 5555}}
instance_req = {"name": "eeeeee", "phones": {"home": "23456", "xxx": 5555, "yyyy": 5555, "dict_" :['n', 'g', 'a', 'c']}}  #, 'q', 'W' 'n', 'g' , "xxx": 5555
errors = Draft4Validator(schema).iter_errors(instance_req)
#qqq = errors.__next__()
ee = [e.path[-1] for e in sorted(errors, key=exceptions.relevance)]
print(ee)