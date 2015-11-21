from jsonschema import validate, Draft3Validator, Draft4Validator

schema = {
    "type": "object",
    "properties": {
    "price": {"type": "number"},
    "name": {"type": "string"},
    },
}

x = validate({"name": "Eggs", "price": 34.99}, schema)
print()
####################
schema = {
    "type": "array",
    "items": {"enum": [1, 2, 3, 5]},
    "maxItems": 2,
}

v = Draft3Validator(schema)
for error in sorted(v.iter_errors([2, 3, 4]), key=str):
    print(error.message)
####################

schema = {
    #"$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "price": {"type": "number"},
    },
    }
v4 = Draft4Validator.check_schema(schema)
test = {"name" : "Eggs", "email" : "ssss"}
validate({"name" : "Eggs", "price" : 34.99}, schema)
v4.validate(test)
#validate({"name" : "Eggs", "price" : 34.99}, schema) дока

