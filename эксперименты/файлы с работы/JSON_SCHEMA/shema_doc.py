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
        "DocumentSLEDCTVIE": {"type": "object",
                              "properties": {
                                "key1": {"type": "string"},
                                "key2": {"type": "string"},
                                "key3": {"type": "string"}
                              },
                               "required": ["key1", "key3"]

        }
    },


    "type": "object",
    "properties": {
            "doc": {
                "type": "array",
                "minItems": 1,
                "items": {
                            "$ref": "#/definitions/DocumentSLEDCTVIE"
                },
                "uniqueItems": True
            }
    }
}

instance = {"doc": [
                    {
                        "key1": "1",
                        "key2": "1"
                    },
                    {
                        "key1": "1",
                        "key2": "2"
                    }
]}

errors = Draft4Validator(schema).iter_errors(instance)
tree = ErrorTree(errors)
#qqq = errors.__next__()  .path[-1]
ee = [e for e in sorted(errors, key=exceptions.relevance)]
print(ee)
ee[0].path