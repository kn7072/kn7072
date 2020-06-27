import json


class Message:
    def __init__(self, text, code=None):
        self.text = text
        self.code = code

    def to_json(self):
        return json.dumps({'text': self.text, 'code': self.code})


class MetaMessage(type):

    def __new__(mcs, name, bases, attrs):
        for attr, value in attrs.items():
            # проходим по всем описанным в классе атрибутам с типом Message
            # и заменяем поле code на называние атрибута
            # (если code не задан заранее)
            if isinstance(value, Message) and value.code is None:
                value.code = attr

        return super().__new__(mcs, name, bases, attrs)


class Messages(metaclass=MetaMessage):
    not_found = Message('Resource not found')
    bad_request = Message('Request body is invalid')