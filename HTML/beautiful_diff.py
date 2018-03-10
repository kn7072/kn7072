# coding="utf-8"
import json
path_test_json = r"response.json"
with open(path_test_json, encoding="cp1251") as f:
    body_json = f.read()
json_obj = json.loads(body_json)

# xx = json.dumps(json_obj)

object_element = """
<span>
    <span class="object" style="display: none;">
        <a class="disclosure" href="#">[+]</a>
        <span class="object syntax">{</span>
        <a href="#">...</a>
        <span class="object syntax">}</span>
    </span>
    <span class="object" style="display: inline;">
        <a class="disclosure" href="#">[-]</a>
        <span class="object syntax">{</span>
            {CONTENT_OBJECT}
        <span class="object syntax">}</span>
    </span>
</span>
"""
# dict_elements = {"object": {"start": """
#                                         <span>
#                                             <span class="object" style="display: none;">
#                                                 <a class="disclosure" href="#">[+]</a>
#                                                 <span class="object syntax">{</span>
#                                                 <a href="#">...</a>
#                                                 <span class="object syntax">}</span>
#                                             </span>
#                                             <span class="object" style="display: inline;">
#                                                 <a class="disclosure" href="#">[-]</a>
#                                                 <span class="object syntax">{</span>
#                                      """,
#                             "finish": """
#                                         <span class="object syntax">}</span>
#                                     </span>
#                                 </span>
#                             """},
#                 "object_open": {"start": """
#                                         <span>
#                                             <span class="object" style="display: inline;">
#                                                 <a class="disclosure" href="#">[+]</a>
#                                                 <span class="object syntax">{</span>
#                                                 <a href="#">...</a>
#                                                 <span class="object syntax">}</span>
#                                             </span>
#                                             <span class="object" style="display: none;">
#                                                 <a class="disclosure" href="#">[-]</a>
#                                                 <span class="object syntax">{</span>
#                                      """,
#                             "finish": """
#                                         <span class="object syntax">}</span>
#                                     </span>
#                                 </span>
#                             """},
#                  "array": {"start": """
#                                         <span>
#                                             <span class="object" style="display: none;">
#                                                 <a class="disclosure" href="#">[+]</a>
#                                                 <span class="array syntax">[</span>
#                                                 <a href="#">...</a>
#                                                 <span class="object syntax">]</span>
#                                             </span>
#                                             <span class="object" style="display: inline;">
#                                                 <a class="disclosure" href="#">[-]</a>
#                                                 <span class="array syntax">[</span>
#                                      """,
#                             "finish": """
#                                         <span class="array syntax">]</span>
#                                     </span>
#                                 </span>
#                             """},
#                  "key_object_simple": """
#                                     <span> </span>
#                                     <span class="key">"{name_key}"</span>
#                                     <span class="object syntax">: </span>
#                                     <span></span>
#                                     <span class="string">"{value_key}"</span>
#                  """,
#                 "object_key": {"start": """
#                                             <span> </span>
#                                             <span class="key">"{name_key}"</span>
#                                             <span class="object syntax">: </span>
#                                             <span></span>
#                                             <span>
#                                                 <span class="object" style="display: none;">
#                                                     <a class="disclosure" href="#">[+]</a>
#                                                     <span class="object syntax">{</span>
#                                                     <a href="#">...</a>
#                                                     <span class="object syntax">}</span>
#                                                 </span>
#                                                 <span class="object" style="display: inline;">
#                                                     <a class="disclosure" href="#">[-]</a>
#                                                     <span class="object syntax">{</span>
#                                          """,
#                                         "finish": """
#                                                     <span class="object syntax">}</span>
#                                                 </span>
#                                             </span>
#                  """},
#                  "element_array": """
#                                  <span> </span>
#                                  <span class="string">"{array_value}"</span>
#                  """,
#                  ",": """<span class="syntax">,</span>"""}
dict_elements = {"object": {"start": """
                                        <div class="object">
                                            <a class="disclosure" href="#">[+]</a>
                                            <div class="object syntax">{</div>
                                            <a href="#">...</a>
                                            <div class="object syntax">}</div>
                                        </div>
                                        <div class="object" style="display: none;">
                                            <a class="disclosure" href="#">[-]</a>
                                            <div class="object syntax">{</div>
                                     """,
                            "finish": """
                                        <div class="object syntax">}</div>
                                    </div>
                            """},
                "object_open": {"start": """
                                            <div class="object">
                                                <a class="disclosure" href="#">[+]</a>
                                                <div class="object syntax">{</div>
                                                <a href="#">...</a>
                                                <div class="object syntax">}</div>
                                            </div>
                                            <div class="object" style="display: none;">
                                                <a class="disclosure" href="#">[-]</a>
                                                <div class="object syntax">{</div>
                                     """,
                            "finish": """
                                        <div class="object syntax">}</div>
                                    </div>
                            """},
                 "array": {"start": """
                                        <div class="object" style="display: none;">
                                            <a class="disclosure" href="#">[+]</a>
                                            <div class="array syntax">[</div>
                                            <a href="#">...</a>
                                            <div class="object syntax">]</div>
                                        </div>
                                        <div class="object">
                                            <a class="disclosure" href="#">[-]</a>
                                            <div class="array syntax">[</div>
                                     """,
                            "finish": """
                                        <div class="array syntax">]</div>
                                    </div>
                            """},
                "array_key": {"start": """
                                        <div class="key vertical_aligan">"%(name_key)s"</div>
                                        <div class="object syntax vertical_aligan">: </div>
                                        <div class="object">
                                            <a class="disclosure" href="#">[+]</a>
                                            <div class="array syntax">[</div>
                                            <a href="#">...</a>
                                            <div class="object syntax">]</div>
                                        </div>
                                        <div class="object" style="display: none;">
                                            <a class="disclosure" href="#">[-]</a>
                                            <div class="array syntax">[</div>
                                     """,
                            "finish": """
                                        <div class="array syntax">]</div>
                                    </div>
                            """},
                 "key_object_simple": """
                                            <div class="key vertical_aligan">"{name_key}"</div>
                                            <div class="object syntax vertical_aligan">: </div>
                                            <div class="string">"{value_key}"</div>
                 """,
                "object_key": {"start": """
                                                <div class="key vertical_aligan">"%(name_key)s"</div>
                                                <div class="object syntax vertical_aligan">: </div>
                                                <div class="object">
                                                    <a class="disclosure" href="#">[+]</a>
                                                    <div class="object syntax">{</div>
                                                    <a href="#">...</a>
                                                    <div class="object syntax">}</div>
                                                </div>
                                                <div class="object" style="display: none;">
                                                    <a class="disclosure" href="#">[-]</a>
                                                    <div class="object syntax">{</div>
                                         """,
                                    "finish": """
                                                <div class="object syntax">}</div>
                                            </div>
                 """},
                 "element_array": """
                                 <div class="string">"{array_value}"</div>
                 """,
                 ",": """<div class="syntax">,</div>""",
                 "div": {"start": "<div>", "finish": "</div><br>"}}
#  none inline
# dict_elements = {"object": {"start": """<span><span class="object" style="display: none;"><a class="disclosure" href="#">[+]</a><span class="object syntax">{</span><a href="#">...</a><span class="object syntax">}</span></span><span class="object" style="display: inline;"><a class="disclosure" href="#">[-]</a><span class="object syntax">{</span>""",
#                             "finish": """<span class="object syntax">}</span></span></span>"""},
#                  "object_open": {"start": """<span><span class="object" style="display: inline;"><a class="disclosure" href="#">[+]</a><span class="object syntax">{</span><a href="#">...</a><span class="object syntax">}</span></span><span class="object" style="display: none;"><a class="disclosure" href="#">[-]</a><span class="object syntax">{</span>""",
#                                  "finish": """<span class="object syntax">}</span></span></span>"""},
#                  "array": {"start": """<span><span class="object" style="display: none;"><a class="disclosure" href="#">[+]</a><span class="array syntax">[</span><a href="#">...</a><span class="object syntax">]</span></span><span class="object" style="display: inline;"><a class="disclosure" href="#">[-]</a><span class="array syntax">[</span>""",
#                            "finish": """<span class="array syntax">]</span></span></span>"""},
#                  "key_object": """<span> </span><span class="key">"{name_key}"</span><span class="object syntax">: </span><span></span><span class="string">"{value_key}"</span>""",
#                  "element_array": """<span> </span><span class="string">"{array_value}"</span>""",
#                  ",": """<span class="syntax">,</span>"""}

list_elements_tree = []
def json_tree(obj, level):
    """
    :param obj:
    :param level:
    :return:
    """
    if isinstance(obj, dict):
        for key, val in obj.items():
            if isinstance(val, dict):
                list_elements_tree.append(["start", key, "object", level])
                json_tree(val, level+1)
                list_elements_tree.append(["end", key, "object", level])
            elif isinstance(val, tuple) or isinstance(val, list):
                list_elements_tree.append(["start", key, "array", level])
                json_tree(val, level + 1)
                list_elements_tree.append(["end", key, "array", level])
            else:
                list_elements_tree.append(["-", key, "simple", level, val])
    elif isinstance(obj, tuple) or isinstance(obj, list):
        for i, elm_i in enumerate(obj):
            if isinstance(elm_i, dict):
                list_elements_tree.append(["start", "element_array_%s" % i, "object", level, None])
                json_tree(elm_i, level + 1)
                list_elements_tree.append(["end", "element_array_%s" % i, "object", level, None])
            elif isinstance(elm_i, tuple) or isinstance(elm_i, list):
                list_elements_tree.append(["start", "element_array_%s" % i, "array", level, None])
                json_tree(elm_i, level + 1)
                list_elements_tree.append(["end", "element_array_%s" % i, "array", level, None])
            else:
                list_elements_tree.append(["-", "element_array_%s" % i, "simple", level, elm_i])
    else:
        list_elements_tree.append(["-", "element_object", "simple", level, obj])

#json_tree(json_obj, level=0)
# for i in list_elements_tree:
#     print(i)
# print()
# dict_elements = {"object": {"start": """
#                                         <details>
#                                            <summary>
#                                               <span class="spoiler-hidden">{...}</span>
#                                            </summary>
#                                         <span>
#
#                                      """,
#                             "finish": """
#                                         </span></details>
#                             """},
#                  "object_open": {"start": """
#                                         <details>
#                                            <summary>
#                                               <span class="spoiler-hidden">{...}</span>
#                                            </summary>
#                                         <span>
#
#                                      """,
#                                  "finish": """
#                                         </span></details>
#                             """},
#                  "array": {"start": """
#                                         <details>
#                                            <summary>
#                                               <span class="spoiler-hidden">[...]</span>
#                                            </summary>
#                                         <span>
#
#                                      """,
#                            "finish": """
#                                         </span></details>
#                             """},
#                  "key_object": """
#                                     <span> </span>
#                                     <span class="key">"{name_key}"</span>
#                                     <span class="object syntax">: </span>
#                                     <span></span>
#                                     <span class="string">"{value_key}"</span>
#                  """,
#                  "element_array": """
#                                  <span> </span>
#                                  <span class="string">"{array_value}"</span>
#                  """,
#                  ",": """<span class="syntax">,</span>"""}
###########################################################################################################
def print_tree(list_):
    for i in list_:
        print(i)

list_elements_tree_html = []
def json_tree_html(obj, level):
    """
    :param obj:
    :param level:
    :return:
    """
    # print_tree(list_elements_tree_html)
    if isinstance(obj, dict):
        for key, val in obj.items():
            if isinstance(val, dict):
                list_elements_tree_html.append(dict_elements["div"]["start"])
                list_elements_tree_html.append(dict_elements["object_key"]["start"] % {"name_key": key})  # object
                json_tree_html(val, level+1)
                list_elements_tree_html.append(dict_elements["object_key"]["finish"])  # object
                list_elements_tree_html.append(dict_elements[","])
                list_elements_tree_html.append(dict_elements["div"]["finish"])
            elif isinstance(val, tuple) or isinstance(val, list):
                list_elements_tree_html.append(dict_elements["div"]["start"])
                list_elements_tree_html.append(dict_elements["array_key"]["start"] % {"name_key": key})  # array
                json_tree_html(val, level + 1)
                list_elements_tree_html.append(dict_elements["array_key"]["finish"])
                list_elements_tree_html.append(dict_elements[","])
                list_elements_tree_html.append(dict_elements["div"]["finish"])
            else:
                list_elements_tree_html.append(dict_elements["div"]["start"])
                list_elements_tree_html.append(dict_elements["key_object_simple"].format(name_key=key, value_key=val)) # ["-", key, "simple", level, val]  key_object
                list_elements_tree_html.append(dict_elements[","])
                list_elements_tree_html.append(dict_elements["div"]["finish"])
        # УБИРАЕМ ПОСЛЕДНЮЮ ЗАПЯТУЮ
        last_elem = list_elements_tree_html[-2]
        if last_elem.startswith(dict_elements[","]):
            list_elements_tree_html[-2] = ""

    elif isinstance(obj, tuple) or isinstance(obj, list):
        for i, elm_i in enumerate(obj):
            if isinstance(elm_i, dict):
                list_elements_tree_html.append(dict_elements["div"]["start"])
                list_elements_tree_html.append(dict_elements["object"]["start"])
                json_tree_html(elm_i, level + 1)
                list_elements_tree_html.append(dict_elements["object"]["finish"])
                list_elements_tree_html.append(dict_elements[","])
                list_elements_tree_html.append(dict_elements["div"]["finish"])
            elif isinstance(elm_i, tuple) or isinstance(elm_i, list):
                list_elements_tree_html.append(dict_elements["div"]["start"])
                list_elements_tree_html.append(dict_elements["array"]["start"])
                json_tree_html(elm_i, level + 1)
                list_elements_tree_html.append(dict_elements["array"]["finish"])
                list_elements_tree_html.append(dict_elements[","])
                list_elements_tree_html.append(dict_elements["div"]["finish"])
            else:
                list_elements_tree_html.append(dict_elements["div"]["start"])
                list_elements_tree_html.append(dict_elements["element_array"].format(array_value=elm_i))  # ["-", "element_array_%s" % i, "simple", level, elm_i] element_array
                list_elements_tree_html.append(dict_elements[","])
                list_elements_tree_html.append(dict_elements["div"]["finish"])
        # УБИРАЕМ ПОСЛЕДНЮЮ ЗАПЯТУЮ
        last_elem = list_elements_tree_html[-2]
        if last_elem.startswith(dict_elements[","]):
            list_elements_tree_html[-2] = ""
    else:
        list_elements_tree_html.append(["-", "element_object", "simple", level, obj])

json_tree_html(json_obj, level=0)
list_elements_tree_html[0:0] = [dict_elements["object_open"]["start"]]
list_elements_tree_html.append(dict_elements["object_open"]["finish"])


for i in list_elements_tree_html:
    print(i)
all_html = "".join(list_elements_tree_html)
with open(r"HTML_REPORT\HTML_REPORT\test_temp.html") as f:
    data = f.read().format(contents_tests=all_html)

path_test_ = r"HTML_REPORT\HTML_REPORT\INDEX_1.html"
with open(path_test_, "w", encoding="utf-8") as f:
   f.write(data)
print()
###########################################################################################################




for i in list_elements_tree_html:
    print(i)
all_html = "".join(list_elements_tree_html)
with open(r"HTML_REPORT\HTML_REPORT\NEW\test_temp.html") as f:
    data = f.read().format(contents_tests=all_html)

path_test_ = r"HTML_REPORT\HTML_REPORT\NEW\INDEX_1.html"
with open(path_test_, "w", encoding="utf-8") as f:
    f.write(data)
print()
###########################################################################################################
dict_elements = {"object": {"start": """
                                        <details>
                                           <summary>
                                              <span class="spoiler-hidden">{...}</span>
                                           </summary>
                                        <span>

                                     """,
                            "finish": """
                                        </details></span>
                                    </span>
                                </span>
                            """},
                "object_open": {"start": """
                                        <details>
                                           <summary>
                                              <span class="spoiler-hidden">{...}</span>
                                           </summary>
                                        <span>

                                     """,
                            "finish": """
                                        </details></span>
                                    </span>
                                </span>
                            """},
                 "array": {"start": """
                                        <details>
                                           <summary>
                                              <span class="spoiler-hidden">[...]</span>
                                           </summary>
                                        <span>

                                     """,
                            "finish": """
                                        </details></span>
                                    </span>
                                </span>
                            """},
                 "key_object": """
                                    <span> </span>
                                    <span class="key">"{name_key}"</span>
                                    <span class="object syntax">: </span>
                                    <span></span>
                                    <span class="string">"{value_key}"</span>
                 """,
                 "element_array": """
                                 <span> </span>
                                 <span class="string">"{array_value}"</span>
                 """,
                 ",": """<span class="syntax">,</span>"""}
print()

def getHtml(diffData):
    """ This method convertes git diff data to html color code
    """
    openTag = "<span style='font-size: .80em; color: "
    openTagEnd = ";font-family: courier, arial, helvetica, sans-serif;'>"
    nbsp = '&nbsp;&nbsp;&nbsp;&nbsp;'
    return ''.join([("%s%s%s%s%s</span><br>" % (openTag, '#ff0000' if line.startswith('-') else ('#007900' if line.startswith('+') else '#000000'), openTagEnd, nbsp*line.count('\t') ,line)) for line in diffData])

# xxxx = '"params":\n    {"ВходныеДанные":\n       {"s":\n-         {"ИдентификаторПакетаДокументов":"Строка",\n+         {"ИдентификаторПакетаДокументов":"cccc",\n           "ОтпечатокСертификата":"Строка",\n           "ТекстУточнения":"Строка"},\n        "d":\n          {"ИдентификаторПакетаДокументов":"$_TEST_3_GUID_DOC",\n           "ОтпечатокСертификата":"$_SERVER_CERT",\n-          "ТекстУточнения":"Тестирование отклонения серверным ключом"}\n+          "ТекстУточнения":"Тестирование отdddddddddия серверным ключом"}\n       }\n    },\n "id":0'
# for line in xxxx:
#     print(line)
# diff_html = getHtml(xxxx.split("\n"))


test_str = '{\n     "id": 0, \n     "jsonrpc": "2.0", \n     "result": {\n        "Вложение": [\n           {\n              "ВерсияФормата": "", \n              "Дата": "", \n              "Зашифрован": "Нет", \n              "Идентификатор": "d29086f7-0d82-11e8-9959-94de802a7b19", \n              "Название": "TXT_FILE_7655432117111101001_7654321069760401001_20150925_f6116e0e-3ed9-4fef-a778-b37af4d4af3f.txt", \n-             "Направление": "XXXXXXX", \n?                             ^^^^^^^\n+             "Направление": "Исходящий", \n?                             ^^^^^^^^^\n              "Номер": "", \n              "ПодверсияФормата": "", \n              "Подтип": "", \n              "Редакция": {\n                 "Номер": "1"\n              }, \n              "Служебный": "Нет", \n              "СсылкаНаHTML": "", \n              "Сумма": "", \n              "Тип": "", \n              "Удален": "Нет", \n-             "УдаленКонтрагентом": "XXXXXXX", \n?                                    ^^^^^^^\n+             "УдаленКонтрагентом": "Нет", \n?                                    ^^^\n              "Файл": {\n                 "Имя": "TXT_FILE_7655432117111101001_7654321069760401001_20150925_f6116e0e-3ed9-4fef-a778-b37af4d4af3f.txt"\n              }\n           }, \n           {\n              "ВерсияФормата": "5.01", \n              "Дата": "22.06.2012", \n              "Зашифрован": "Нет", \n              "Идентификатор": "d29086f6-0d82-11e8-bcd3-94de802a7b19", \n              "Название": "Акт № 10 от 22.06.12 на сумму 113 120 р. в т.ч. НДС 17 255.59 р.", \n              "Направление": "Исходящий", \n              "Номер": "10", \n              "ПодверсияФормата": "", \n              "Подтип": "1175012", \n              "Редакция": {\n                 "Номер": "1"\n              }, \n              "Служебный": "Нет", \n              "Сумма": "113120.00", \n              "Тип": "АктВР", \n              "ТипШифрования": "Отсутствует", \n              "Удален": "Нет", \n              "УдаленКонтрагентом": "Нет", \n              "Файл": {\n                 "Имя": "DP_REZRUISP_2BEcde7e56c60cd4c28b8a0129fb4d92b89_2BE5284e2bfe63b4549926e2c12391dbf4c_20160715_615d4da7-6f90-8c35-3cf0-5afb03dcdba8.xml"\n              }\n           }, \n           {\n              "ВерсияФормата": "5.01", \n              "Дата": "04.06.2015", \n              "Зашифрован": "Нет", \n              "Идентификатор": "d29086f8-0d82-11e8-9b07-94de802a7b19", \n              "Название": "Накладная № 32 от 04.06.15 на сумму 10 960.70 р. в т.ч. НДС 1 308.84 р.", \n              "Направление": "Исходящий", \n              "Номер": "32", \n              "ПодверсияФормата": "", \n              "Подтип": "1175010", \n              "Редакция": {\n                 "Номер": "1"\n              }, \n              "Служебный": "Нет", \n              "Сумма": "10960.70", \n              "Тип": "ЭДОНакл", \n              "ТипШифрования": "Отсутствует", \n              "Удален": "Нет", \n              "УдаленКонтрагентом": "Нет", \n              "Файл": {\n                 "Имя": "DP_TOVTORGPR_2BEcde7e56c60cd4c28b8a0129fb4d92b89_2BE5284e2bfe63b4549926e2c12391dbf4c_20160715_615d4da7-6f90-8c35-3cf0-5afb03dcdba8.xml"\n              }\n           }\n        ], \n        "Идентификатор": "d29086fd-0d82-11e8-be0f-94de802a7b19", \n        "Контрагент": {\n           "СвЮЛ": {\n              "ИНН": "7655432117", \n              "КПП": "760401001"\n           }\n        }, \n-       "Направление": "XXXXXXX", \n?                       ^^^^^^^\n+       "Направление": "Исходящий", \n?                       ^^^^^^^^^\n        "НашаОрганизация": {\n           "СвЮЛ": {\n              "ИНН": "7654321069", \n              "КПП": "760401001", \n              "Название": "ЮЛ1"\n           }\n        }, \n-       "Примечание": "АвтотеEEEEEEстирование TestVi2WriteXXXXXXXAndSendDocs - Отправка комплd d29086fd-0d82-11e8-be0f-94de802a7b19", \n?                            ------                       -------                            ^\n+       "Примечание": "Автотестирование TestVi2WriteAndSendDocs - Отправка комплекта фактуры d29086fd-0d82-11e8-be0f-94de802a7b19", \n?                                                                               ^^^^^^^^^^^^\n        "Регламент": {\n           "Название": "Реализация"\n        }, \n        "Редакция": [\n           {\n              "Актуален": "Да", \n-             "ПримечаниеИС": "XXXXXXX"\n?                              ^^^^^^^\n+             "ПримечаниеИС": "ignore"\n?                              ^^^^^^\n           }\n        ], \n        "Состояние": {\n           "Код": "0", \n           "Название": "Документ редактируется", \n           "Описание": "Ожидается отправка", \n           "Примечание": ""\n        }, \n        "Тип": "ДокОтгрИсх", \n        "Удален": "Нет"\n     }\n  }'
list_str = test_str.split("\n")


diff_html_2 = getHtml(test_str.split("\n")).replace("\'", "\"")