# -*- coding: utf-8 -*-
"""
Модуль для работы с ассертами
"""
import time
# from .elements import Element, Table, TextField, Text
# from .logfactory import log
# from .config import Config
import json
import difflib
from copy import deepcopy
import hashlib
from collections import OrderedDict


class BaseMatcher:

    max_length = 70

    def _matches(self, item):
        raise NotImplementedError('_matches')

    def matches(self, item):
        match_result = self._matches(item)
        return match_result

    def cut(self, value):
        """Урезаем вывод строки"""

        value = str(value)
        if len(value) > self.max_length:
            value = value[:self.max_length] + '...'
        return value

    @staticmethod
    def calc(value):
        """Вычисление значения"""

        if callable(value):
            value = value()
        return value


class IsEmpty(BaseMatcher):

    def _matches(self, item):
        if isinstance(item, Table):
            description = '\nПроверка отсутствия в таблице строк.'
            rows_number = item.rows_number
            result = rows_number == 0
            description += '\nНайдено строк в таблице: %s' % rows_number
        elif isinstance(item, (TextField, Text)):
            description = '\nПроверка отсутствия текста в поле'
            result = item.text == ''
        else:
            description = '\nМатчер предназначен проверки Table, TextField или Text! ' \
                          'Передан ' + item.__class__.__name__
            result = False
        return [result, description]


class IsNotEmpty(BaseMatcher):

    def _matches(self, item):
        result = False
        if isinstance(item, Table):
            description = '\nПроверка наличия строк в таблице (отображения)'
            result = item.is_displayed
            if result:
                rows_number = item.rows_number
                result = item.rows_number != 0
                description += '\nНайдено строк в таблице: %s' % rows_number
        elif isinstance(item, (TextField, Text)):
            description = '\nПроверка наличия текста в поле'
            result = item.text != ''
        else:
            description = '\nМатчер предназначен проверки таблиц! Передан ' + item.__class__.__name__
        return [result, description]


class EqualTo(BaseMatcher):

    def __init__(self, item2):
        self.item2 = item2

    def _matches(self, item1):
        item2 = self.calc(self.item2)
        result = item1 == item2
        type1 = item1.__class__.__name__
        type2 = item2.__class__.__name__
        arg1 = self.cut('arg1 (%s) = %s' % (type1, item1))
        arg2 = self.cut('arg2 (%s) = %s' % (type2, item2))
        description = '\nСравнивались на равенство: \n%s\n%s' % (arg1, arg2)
        return [result, description]


class MoreThan(BaseMatcher):

    def __init__(self, item2):
        self.item2 = item2
        self.result = False
        self.description = ''

    def _matches(self, item1):
        item2 = self.calc(self.item2)
        type1 = item1.__class__.__name__
        type2 = item2.__class__.__name__
        arg1 = self.cut('arg1 (%s) = %s' % (type1, item1))
        arg2 = self.cut('arg2 (%s) = %s' % (type2, item2))
        if isinstance(item1, str) and isinstance(item2, str):
            self.result = len(item1) > len(item2)
            self.description = '\nСравнивались на равенство длины строк: \n%s\n%s' % (arg1, arg2)
        elif isinstance(item1, int) and isinstance(item2, int):
            self.result = item1 > item2
            self.description = '\nСравнивались на равенство: \n%s\n%s' % (arg1, arg2)
        elif isinstance(item1, list) and isinstance(item2, list):
            self.result = len(item1) > len(item2)
            self.description = '\nСравнивались на равенство длины списков: \n%s\n%s' % (arg1, arg2)
        elif isinstance(item1, dict) and isinstance(item2, dict):
            self.result = len(item1) > len(item2)
            self.description = '\nСравнивались на равенство длины словарей: \n%s\n%s' % (arg1, arg2)
        else:
            self.description = '\nСравниваемые значения должны быть одного типа'
        return [self.result, self.description]


class MoreThanStrict(BaseMatcher):

    def __init__(self, item2):
        self.item2 = item2
        self.result = False
        self.description = ''

    def _matches(self, item1):
        item2 = self.calc(self.item2)
        type1 = item1.__class__.__name__
        type2 = item2.__class__.__name__
        arg1 = self.cut('arg1 (%s) = %s' % (type1, item1))
        arg2 = self.cut('arg2 (%s) = %s' % (type2, item2))
        if isinstance(item1, str) and isinstance(item2, str):
            self.result = len(item1) >= len(item2)
            self.description = '\nСравнивались на равенство длины строк: \n%s\n%s' % (arg1, arg2)
        elif isinstance(item1, int) and isinstance(item2, int):
            self.result = item1 >= item2
            self.description = '\nСравнивались на равенство: \n%s\n%s' % (arg1, arg2)
        elif isinstance(item1, list) and isinstance(item2, list):
            self.result = len(item1) >= len(item2)
            self.description = '\nСравнивались на равенство длины списков: \n%s\n%s' % (arg1, arg2)
        elif isinstance(item1, dict) and isinstance(item2, dict):
            self.result = len(item1) >= len(item2)
            self.description = '\nСравнивались на равенство длины словарей: \n%s\n%s' % (arg1, arg2)
        else:
            self.result = False
            self.description = '\nСравниваемые значения должны быть одного типа'
        return [self.result, self.description]


class LessThan(BaseMatcher):

    def __init__(self, item2):
        self.item2 = item2
        self.result = False
        self.description = ''

    def _matches(self, item1):
        item2 = self.calc(self.item2)
        type1 = item1.__class__.__name__
        type2 = item2.__class__.__name__
        arg1 = self.cut('arg1 (%s) = %s' % (type1, item1))
        arg2 = self.cut('arg2 (%s) = %s' % (type2, item2))
        if isinstance(item1, str) and isinstance(item2, str):
            self.result = len(item1) < len(item2)
            self.description = '\nСравнивались на равенство длины строк: \n%s\n%s' % (arg1, arg2)
        elif isinstance(item1, int) and isinstance(item2, int):
            self.result = item1 < item2
            self.description = '\nСравнивались на равенство: \n%s\n%s' % (arg1, arg2)
        elif isinstance(item1, list) and isinstance(item2, list):
            self.result = len(item1) < len(item2)
            self.description = '\nСравнивались на равенство длины списков: \n%s\n%s' % (arg1, arg2)
        elif isinstance(item1, dict) and isinstance(item2, dict):
            self.result = len(item1) < len(item2)
            self.description = '\nСравнивались на равенство длины словарей: \n%s\n%s' % (arg1, arg2)
        else:
            self.result = False
            self.description = '\nСравниваемые значения должны быть одного типа'
        return [self.result, self.description]


class LessThanStrict(BaseMatcher):

    def __init__(self, item2):
        self.item2 = item2
        self.result = False
        self.description = ''

    def _matches(self, item1):
        item2 = self.calc(self.item2)
        type1 = item1.__class__.__name__
        type2 = item2.__class__.__name__
        arg1 = self.cut('arg1 (%s) = %s' % (type1, item1))
        arg2 = self.cut('arg2 (%s) = %s' % (type2, item2))
        if isinstance(item1, str) and isinstance(item2, str):
            self.result = len(item1) <= len(item2)
            self.description = '\nСравнивались на равенство длины строк: \n%s\n%s' % (arg1, arg2)
        elif isinstance(item1, int) and isinstance(item2, int):
            self.result = item1 <= item2
            self.description = '\nСравнивались на равенство: \n%s\n%s' % (arg1, arg2)
        elif isinstance(item1, list) and isinstance(item2, list):
            self.result = len(item1) <= len(item2)
            self.description = '\nСравнивались на равенство длины списков: \n%s\n%s' % (arg1, arg2)
        elif isinstance(item1, dict) and isinstance(item2, dict):
            self.result = len(item1) <= len(item2)
            self.description = '\nСравнивались на равенство длины словарей: \n%s\n%s' % (arg1, arg2)
        else:
            self.result = False
            self.description = '\nСравниваемые значения должны быть одного типа'
        return [self.result, self.description]


class EqualToIgnoringCase(BaseMatcher):

    def __init__(self, item2):
        self.item2 = item2

    def _matches(self, item1):
        item2 = self.calc(self.item2)
        if not type(item1) == type(item2) == str:
            raise TypeError('Матчер equal_to_ignoring_case предназначен для строк')
        result = item1.lower() == item2.lower()
        type1 = item1.__class__.__name__
        type2 = item2.__class__.__name__
        arg1 = self.cut('arg1 (%s) = %s' % (type1, item1))
        arg2 = self.cut('arg2 (%s) = %s' % (type2, item2))
        description = '\nСравнивались на равенство БЕЗ учета регистра: ' \
                      '\n%s\n%s' % (arg1, arg2)
        return [result, description]


def _sorting(json):
    """Сортирует json

    :param json - json, который нужно отсортировать
    """

    def sort_elements_in_list(unsorted_list):
        for index, elm in enumerate(unsorted_list):
            if len(tuple(filter(lambda x: not isinstance(x, (str, float, int)), unsorted_list))) == 0:
                sorted_list = unsorted_list.sort()
                break
            else:
                unsorted_list[index] = find_list(elm)
                hash_dict = {hashlib.md5(str(item).encode()).hexdigest(): item for item in unsorted_list}
                order_dict = OrderedDict(sorted(hash_dict.items()))
                sorted_list = list(order_dict.values())
        return sorted_list

    def find_list(dictionary):
        for key, value in dictionary.items():
            if type(value) in (list, dict):
                dictionary[key] = _sorting(value)
        return dictionary

    if type(json) == list:
        json = sort_elements_in_list(json)
    if type(json) == dict:
        json = find_list(json)

    return json

def _delete_tags(json1, json2, ignore_only=False):
    """Удаляет ключи и значения из словарей

    :param json1: эталонный словарь
    :param json2: сравниваемый словарь
    :param ignore_only: удалить только игнорируемые теги
    """

    ignore_values = ('ignore',)  # значения в json которые игнорируются при сравнении
    ignore_tags = ('protocol', 'ignore')  # тэги в json которые игнорируются при сравнении

    def delete_ignore_elm_in_dict(dict1, dict2):
        tmp_dict = deepcopy(dict1)
        for key, value in tmp_dict.items():
            if type(value) not in (dict, list) and key in dict1 and key in dict2:
                if key in ignore_tags or value in ignore_values:
                    dict1.pop(key, None)
                    dict2.pop(key, None)
            elif key in dict1 and key in dict2:
                dict1[key], dict2[key] = _delete_tags(dict1[key], dict2[key], ignore_only)
        return dict1, dict2

    def delete_ignore_elm_in_list(list1, list2):
        
        for index, value in enumerate(list1):
            if type(value) not in (dict, list) and value in ignore_values:
                list2[index] = 'ignore'
            else:
                try:
                    list1[index], list2[index] = _delete_tags(list1[index], list2[index], ignore_only)
                except IndexError:
                    pass
        return list1, list2

    def delete_value_in_list(list1, list2):
        for index, value in enumerate(list1):
            if type(value) in (dict, list):
                try:
                    list1[index], list2[index] = _delete_tags(list1[index], list2[index], ignore_only)
                except IndexError:
                    pass
        return list1, list2

    def delete_value_in_dict(dict1, dict2):
        tmp_dict = deepcopy(dict2)
        for key, value in tmp_dict.items():
            if key not in dict1:
                dict2.pop(key)
            elif type(value) in (dict, list) and key in dict1 and key in dict2:
                dict1[key], dict2[key] = _delete_tags(dict1[key], dict2[key], ignore_only)
        return dict1, dict2

    if type(json1) == list:
        json1, json2 = delete_ignore_elm_in_list(json1, json2)
        if not ignore_only:
            json1, json2 = delete_value_in_list(json1, json2)
    elif type(json1) == dict:
        json1, json2 = delete_ignore_elm_in_dict(json1, json2)
        if not ignore_only:
            json1, json2 = delete_value_in_dict(json1, json2)
    return json1, json2


class EqualToJson(BaseMatcher):

    def __init__(self, item2):
        self.item2 = item2

    def _matches(self, item1):
        item1_copy = deepcopy(item1)
        item2_copy = deepcopy(self.item2)
        item1_copy, item2_copy = _delete_tags(item1_copy, item2_copy, True)
        result = item1_copy == item2_copy
        if not result:
            item1_copy = json.dumps(item1_copy, indent=3, sort_keys=True, ensure_ascii=False)
            item2_copy = json.dumps(item2_copy, indent=3, sort_keys=True, ensure_ascii=False)
            diff = difflib.ndiff(item1_copy.splitlines(1), item2_copy.splitlines(1))
            diff_str = ''.join(diff)
        else:
            diff_str = ''
        description = '\njson не равны: \n%s' % diff_str
        return [result, description]


class EqualToJsonIgnoringIndex(BaseMatcher):

    def __init__(self, item2):
        self.item2 = item2

    def _matches(self, item1):
        item1_copy = deepcopy(item1)
        item2_copy = deepcopy(self.item2)
        item1_copy, item2_copy = _sorting(item1_copy), _sorting(item2_copy)
        item1_copy, item2_copy = _delete_tags(item1_copy, item2_copy, ignore_only=True)
        result = item1_copy == item2_copy
        if not result:
            diff1 = json.dumps(item1_copy, indent=3, sort_keys=True, separators=(',', ': '), ensure_ascii=False)
            diff2 = json.dumps(item2_copy, indent=3, sort_keys=True, separators=(',', ': '), ensure_ascii=False)
            diff = difflib.ndiff(diff1.splitlines(1), diff2.splitlines(1))
            diff_str = ''.join(diff)
        else:
            diff_str = ''
        description = '\njson не равны: \n%s' % diff_str
        return [result, description]


class NotEqual(BaseMatcher):
    def __init__(self, item2):
        self.item2 = item2

    def _matches(self, item1):
        item2 = self.calc(self.item2)
        result = item1 != item2
        type1 = item1.__class__.__name__
        type2 = item2.__class__.__name__
        arg1 = self.cut('arg1 (%s) = %s' % (type1, item1))
        arg2 = self.cut('arg2 (%s) = %s' % (type2, item2))
        description = '\nПроверялось НЕравенство: \n%s\n%s' % (arg1, arg2)
        return [result, description]


class Is(BaseMatcher):

    def __init__(self, item2):
        self.item2 = item2

    def matches(self, item1):
        return self.item2.matches(item1)
       

class IsNot(BaseMatcher):

    def __init__(self, item2):
        self.item2 = item2

    def _matches(self, item1):
        result = self.item2.matches(item1)
        if isinstance(result, list):
            result[0] = not result[0]
            return result
        else:
            return not result
        
        
class IsInstanceOf(BaseMatcher):

    def __init__(self, item2):
        if not is_matchable_type(item2):
            raise TypeError('IsInstanceOf requires type')
        self.item2 = item2

    def _matches(self, item1):
        return isinstance(item1, self.item2)


class IsIn(BaseMatcher):

    def __init__(self, item2):
        self.item2 = item2

    def _matches(self, item):
        item2 = self.calc(self.item2)
        result = item in item2
        type1 = item.__class__.__name__
        type2 = item2.__class__.__name__
        arg1 = self.cut('arg1 (%s) = %s\n' % (type1, item))
        arg2 = self.cut('arg2 (%s) = %s\n' % (type2, item2))
        description = '\nПроверка вхождения arg1 в arg2:\n%s%s' % (arg1, arg2)
        return [result, description]


class IsInJson(BaseMatcher):

    def __init__(self, item2):
        self.item2 = item2

    def _matches(self, item1):
        item1_copy = deepcopy(item1)
        item2_copy = deepcopy(self.item2)
        item1_copy, item2_copy = _delete_tags(item1_copy, item2_copy)
        result = item1_copy == item2_copy
        if not result:
            item1_copy = json.dumps(item1_copy, indent=3, sort_keys=True, ensure_ascii=False)
            item2_copy = json.dumps(item2_copy, indent=3, sort_keys=True, ensure_ascii=False)
            diff = difflib.ndiff(item1_copy.splitlines(1), item2_copy.splitlines(1))
            diff_str = ''.join(diff)
        else:
            diff_str = ''
        description = '\njson1 не входит в json2: \n%s' % diff_str
        return [result, description]


class IsInIgnoringCase(BaseMatcher):

    def __init__(self, item2):
        self.item2 = item2

    def _matches(self, item):
        item2 = self.calc(self.item2)
        if type(item) == type(item2) == str:
            result = item.lower() in item2.lower()
            item = self.cut(item)
            item2 = self.cut(item2)
            description = '\nПроверка вхождения текста БЕЗ учета ' \
                          'регистра arg1:\n%s\nв arg2:\n%s' % (item, item2)
        elif type(item) == str and hasattr(item2, 'contains_text_ignoring_case'):
            result = item2.contains_text_ignoring_case(item)
            description = '\nПроверка вхождения текста в таблицу БЕЗ ' \
                          'учета регистра arg1 в arg2:\n%s%s' % (item, item2)
        else:
            raise TypeError('Матчер is_in_ignoring_case предназначен для строк или Table')
        return [result, description]


class IsNotIn(BaseMatcher):

    def __init__(self, item2):
        self.item2 = item2

    def _matches(self, item):
        item2 = self.calc(self.item2)
        result = not item in item2
        type1 = item.__class__.__name__
        type2 = item2.__class__.__name__
        arg1 = self.cut('arg1 (%s) = %s\n' % (type1, item))
        arg2 = self.cut('arg2 (%s) = %s\n' % (type2, item2))
        description = '\nПроверка отсутствия вхождения arg1 в arg2:\n%s%s' % (arg1, arg2)
        return [result, description]


class IsPresent(BaseMatcher):

    def _matches(self, item):
        result = False
        description = '\nПроверка наличия ' + item.__class__.__name__
        if issubclass(item.__class__, Element):
            result = item.is_present
            description = '\nПроверка присутсвия на странице элемента:\n ' + item.name_output()
        return [result, description]


class IsNotPresent(BaseMatcher):

    def _matches(self, item):
        result = False
        description = '\nПроверка отсутствия ' + item.__class__.__name__
        if issubclass(item.__class__, Element):
            result = not item.is_present
            description = '\nПроверка отсутствия на странице элемента:\n ' + item.name_output()
        return [result, description]


class IsDisplayed(BaseMatcher):

    def _matches(self, item):
        result = False
        description = '\nПроверка отображения  ' + item.__class__.__name__
        if issubclass(item.__class__, Element):
            description = '\nПроверка отображения на странице элемента:'
            try:
                result = item.is_displayed
            except Exception as e:
                result = False
                description = '{0}\n{1}'.format(description, e)
        return [result, description]


class IsNotDisplayed(BaseMatcher):

    def _matches(self, item):
        result = False
        description = '\nПроверка НЕ отображения  ' + item.__class__.__name__
        if issubclass(item.__class__, Element):
            result = item.is_not_displayed
            description = '\nПроверка НЕ отображения на странице элемента:\n ' + item.name_output()
        return [result, description]


def check_args(arg1, arg2, desc, wait_time):
    """Проверка соответствует ли вызов ассерта всем стандартам"""

    from .controls import ControlTable

    # второй аргумент всегда должен быть матчером
    if not isinstance(arg2, BaseMatcher):
        raise Exception('Не верное использование assert_that! '
                        'Второй агрумент должен быть матчером!')

    if not isinstance(desc, str):
        raise Exception('Не верное описание ошибки. '
                        'Описание должно быть строкой!')

    # проверка, что всегда пишется and_wait() или and_wait(5)
    if wait_time and not isinstance(wait_time, WaitTime):
        raise Exception('Не верное написание ассерта! '
                        'Допутимо указание ожидание только в методе and_wait')
    elif wait_time:
        if not isinstance(arg1, Element) and not callable(arg1):
            if hasattr(arg2, 'item2'):
                if not callable(arg2.item2) and type(arg2.item2) not in (ControlTable, Table):
                    raise Exception('Wait в assert_that не работает! '
                                    'Проверьте правильность написания assert')


def assert_that(arg1, arg2, desc, wait_time=0):
    """Комплексные ассерты
    :param arg1: первый аргумент сравнения (что сравниваем)
    :param arg2: второй аргумент сравнения (с чем сравниваем)
    :param desc: текстовое описание ошибки
    :param wait_time:  разрешено только передавать and_wait()/and_wait(5)

    """
    check_args(arg1, arg2, desc, wait_time)

    if wait_time:
        wait_time = time.time() + wait_time.wait_time

    while True:
        try:
            item = arg1
            if callable(item):
                item = item()

            _assert_match(actual=item, matcher=arg2, reason=desc)
            break
        except (AssertionError, IndexError) as error:
            if time.time() > wait_time:
                raise error
            time.sleep(0.2)
    log('Проверка пройдена: %s' % desc, '[a]')
    

def instance_of(atype):

    return IsInstanceOf(atype)


def wrap_matcher(x):

    if isinstance(x, BaseMatcher):
        return x
    else:
        return equal_to(x)


def is_matchable_type(expected_type):

    if isinstance(expected_type, type):
        return True
    return False


def wrap_value_or_type(x):

    if is_matchable_type(x):
        return instance_of(x)
    else:
        return wrap_matcher(x)

    
def _assert_match(actual, matcher, reason=None):

    rslt = matcher.matches(actual)

    if isinstance(rslt, bool):    
        if not rslt:
            raise AssertionError(reason + "\n")
    elif not rslt[0]:
        msg = reason + "\n" + rslt[1]
        raise AssertionError("\n" + msg)


def equal_to(obj):
    """Сравнение двух объектов на равенство

    :param obj: объект для сравнения

    Примеры::

        a = 5
        b = 6
        assert_that(a, equal_to(b), 'Текстовое описание ошибки') # упадет
        assert_that(a, equal_to(5), 'Текстовое описание ошибки') # не упадет

        a = {'width':1, 'left':1, 'height':2}
        b = {'width':1, 'height':2, 'left':1}
        assert_that(a, equal_to(b), 'Текстовое описание ошибки') # не упадет
        b = {'width':1, 'height':2, 'left':2}
        assert_that(a, equal_to(b), 'Текстовое описание ошибки') # упадет
    """
    return EqualTo(obj)


def equal_to_ignoring_case(obj):
    """Сравнение двух объектов на равенство

    :param obj: объект для сравнения
    """
    return EqualToIgnoringCase(obj)


def equal_to_json(obj):
    """Сравнение два JSON на равенство

    ** Отличие от equal_to игнорирует ключи protocol и значений ignore

    :param obj: объект для сравнения
    """
    return EqualToJson(obj)


def equal_to_json_ignoring_index(obj):
    """Сравнение двух JSON на равенство, не учитывая порядок ключей в них

    :param obj - объект для сравнения

    """

    return EqualToJsonIgnoringIndex(obj)


def is_in_json(obj):
    """Сравнение два JSON на вхождение эталонного в тестируемый

    ** Отличие от equal_to игнорирует ключи protocol и значений ignore

    :param obj: объект для сравнения
    """
    return IsInJson(obj)


def more_than(obj):
    """Сравнение двух объектов на неравенство

    :param obj: объект для сравнения

    Примеры::

        a = 5
        b = 6
        assert_that(a, more_than(4), 'Текстовое описание ошибки') # не упадет
        assert_that(a, more_than(b), 'Текстовое описание ошибки') # упадет

        a = '55'
        assert_that(a, more_than('b'), 'Текстовое описание ошибки') # не упадет
        assert_that(a, more_than('aaa'), 'Текстовое описание ошибки') # упадет
    """
    return MoreThan(obj)


def more_than_strict(obj):
    """Сравнение двух объектов на неравенство

    :param obj: объект для сравнения

    Примеры::

        a = 5
        b = 6
        assert_that(a, more_than_strict(4), 'Текстовое описание ошибки') # не упадет
        assert_that(a, more_than_strict(b), 'Текстовое описание ошибки') # упадет

        a = '5'
        assert_that(a, more_than_strict('b'), 'Текстовое описание ошибки') # не упадет
        assert_that('55', more_than_strict('a'), 'Текстовое описание ошибки') # упадет
    """
    return MoreThanStrict(obj)


def less_than(obj):
    """Сравнение двух объектов на неравенство

    :param obj: объект для сравнения

    Примеры::

        a = 5
        b = 6
        assert_that(a, less_than(4), 'Текстовое описание ошибки') # упадет
        assert_that(a, less_than(b), 'Текстовое описание ошибки') # не упадет

        a = '55'
        assert_that(a, less_than('b'), 'Текстовое описание ошибки') # упадет
        assert_that(a, less_than('aaa'), 'Текстовое описание ошибки') # не упадет
    """
    return LessThan(obj)


def less_than_strict(obj):
    """Сравнение двух объектов на неравенство

    :param obj: объект для сравнения

    Примеры::

        a = 5
        b = 6
        assert_that(a, less_than_strict(4), 'Текстовое описание ошибки') # упадет
        assert_that(a, less_than_strict(b), 'Текстовое описание ошибки') # не упадет

        a = '5'
        assert_that(a, less_than_strict('b'), 'Текстовое описание ошибки') # упадет
        assert_that('55', less_than_strict('a'), 'Текстовое описание ошибки') # не упадет
    """
    return LessThanStrict(obj)


def not_equal(obj):
    """Сравнение двух объектов на неравенство

    :param obj: объект для сравнения

    Примеры::

        a = 5
        b = 6
        assert_that(a, not_equal(b), 'Текстовое описание ошибки') # не упадет
        assert_that(a, not_equal(5), 'Текстовое описание ошибки') # упадет

        a = {'width':1, 'left':1, 'height':2}
        b = {'width':1, 'height':2, 'left':1}
        assert_that(a, not_equal(b), 'Текстовое описание ошибки') # упадет
        b = {'width':1, 'height':2, 'left':2}
        assert_that(a, not_equal(b), 'Текстовое описание ошибки') # не упадет
    """
    return NotEqual(obj)


def is_not(x):
    """Сравнение объекта и логического отрицания x

    :param x: объект для сравнения (обычно это True или False)

    Примеры::

        a = True
        b = False
        assert_that(a, is_not(b), 'Текстовое описание ошибки') # не упадет
        b = True
        assert_that(a, is_not(b), 'Текстовое описание ошибки') # упадет
    """
    return IsNot(wrap_value_or_type(x))


def is_(x):
    """Сравнение объекта и x

    :param x: объект для сравнения (обычно это True или False)
    """
    return Is(wrap_value_or_type(x))


def is_in(sequence):
    """Проверка вхождения объекта в sequence

    :param sequence: объект для сравнения

    Примеры::

        a = 'очная'
        b = 'проверочная строка'
        assert_that(a, is_in(b), 'Текстовое описание ошибки') # не упадет
        a = 'очная1'
        assert_that(a, is_in(b), 'Текстовое описание ошибки') # упадет
    """
    return IsIn(sequence)


def is_in_ignoring_case(sequence):
    """Проверка вхождения объекта в sequence

    :param sequence: объект для сравнения
    """
    return IsInIgnoringCase(sequence)


def is_not_in(sequence):
    """Проверка отсутствия вхождения объекта в sequence

    :param sequence: объект для сравнения

    Пример::

        a = 'очная'
        b = 'проверочная строка'
        assert_that(a, is_not_in(b), 'Текстовое описание ошибки') # упадет
        a = 'очная1'
        assert_that(a, is_not_in(b), 'Текстовое описание ошибки') # не упадет
    """
    return IsNotIn(sequence)


def is_present():
    """Проверка наличия элемента на странице

    Пример::

        assert_that(page_t.main_fix_1_table, is_present(), 'Здесь текстовое описание ошибки')
    """
    return IsPresent()


def is_not_present():
    """Проверка наличия элемента на странице

    Пример::

        assert_that(page_t.main_fix_1_table, is_not_present(), 'Здесь текстовое описание ошибки')
    """
    return IsNotPresent()


def is_displayed():
    """Проверка отображения элемента на странице

    Пример::
        assert_that(page_t.main_fix_1_table, is_displayed(), 'Здесь текстовое описание ошибки')
    """
    return IsDisplayed()


def is_not_displayed():
    """Проверка отсутствия отображения элемента на странице

    Пример::
        assert_that(page_t.main_fix_1_table, is_not_displayed(), 'Здесь текстовое описание ошибки')
    """
    return IsNotDisplayed()


def is_empty():
    """Проверка очистки таблицы (отсутствия строк в ней)

    Пример::
        assert_that(page_t.main_fix_1_table, is_empty(), 'Ошибка! Таблица не пуста', and_wait())
    """
    return IsEmpty()


def is_not_empty():
    """Проверка, что таблица не пустая

    Пример::
        assert_that(page_t.main_fix_1_table, is_not_empty(), 'Ошибка! Таблица пуста', and_wait())
    """
    return IsNotEmpty()


class WaitTime:
    """Класс создан для проверки написания ассерта

    Чтобы не писали так: assert_that(elm, is_displayed(), "Ошибка", and_wait(5))
    """

    def __init__(self, wait_time):
        if wait_time is True:
            self.wait_time = Config().WAIT_ELEMENT_LOAD
        elif isinstance(wait_time, (int, float)):
            self.wait_time = wait_time
        else:
            self.wait_time = 0


def and_wait(wait_time=True):
    """Использовать ли в AssertThat wait

    :param wait_time:   время в сек. в течении которого присходит сравнение. Если не указано или True, то значение
                        ожидания берется из параметра WAIT_ELEMENT_LOAD файла настроек config.ini
    """
    return WaitTime(wait_time)