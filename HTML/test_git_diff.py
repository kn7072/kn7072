# coding="utf-8"
import xxx.mod
import git, sys
a, *b = "span"
[a, b, c] = (1, 2, 3)
path_repo = r"d:\VIRTUAL_PY\test_8\Lib\site-packages\atf"
#repo = git.Repo(path_repo)
#path_to_a_file = "logfactory.py"
#commits_touching_path = list(repo.iter_commits(paths=path_to_a_file))
# https://stackoverflow.com/questions/20061898/gitpython-and-git-diff
#x = repo.git.diff(commits_touching_path[0], commits_touching_path[1], path_to_a_file)
command = 'git diff --no-index 1.txt 2.txt'  # TEST_DIR\1.txt  TEST_DIR\2.txt
git_inst = git.Git()
#git_inst.environment()
z = git_inst.execute(command, with_exceptions=False, stdout_as_string=False)
diff_str = z.decode("cp1251")
print(diff_str) # environment
print("##############################################################################################################")
# def getHtml(diffData):
#     """ This method convertes git diff data to html color code
#     """
#     openTag = "<span style='font-size: .80em; color: "
#     openTagEnd = ";font-family: courier, arial, helvetica, sans-serif;'>"
#     nbsp = '&nbsp;'#'&nbsp;&nbsp;&nbsp;&nbsp;'
#     """
#     &nbsp; неразрывный пробел
#     &thinsp; узкий пробел (применяют в двойных словах)
#     &ensp; средний, разрывной пробел
#     &emsp; длинный разрывной пробел (примеяют в конце предложений)
#     """
#     # https://stackoverflow.com/questions/13648813/what-is-the-pythonic-way-to-count-the-leading-spaces-in-a-string
#     return ''.join([("%s%s%s%s%s</span><br>" % (openTag,
#                                                 '#ff0000' if line.startswith('-') else ('#007900' if line.startswith('+') else '#000000'),
#                                                 openTagEnd,
#                                                 nbsp*(len(line) - len(line.lstrip())),# nbsp*line.count('') \t (len(line) - len(line.lstrip()))
#                                                 line)
#                      ) for line in diffData]
#
#             )
list_all_html = []
def getHtml(diff_text):
    """ This method convertes git diff data to html color code
    """
    openTag = "<span style=' color: "
    openTagEnd = ";font-family: courier, arial, helvetica, sans-serif;'>"
    nbsp = '&nbsp;'#'&nbsp;&nbsp;&nbsp;&nbsp;'
    """
    &nbsp; неразрывный пробел
    &thinsp; узкий пробел (применяют в двойных словах)
    &ensp; средний, разрывной пробел
    &emsp; длинный разрывной пробел (примеяют в конце предложений)
    """
    # https://stackoverflow.com/questions/13648813/what-is-the-pythonic-way-to-count-the-leading-spaces-in-a-string
    # - эталон
    # + сравниваемое значение
    # font-family: courier, arial, helvetica, sans-serif; font-size: .80em;
    temp = """<span style='color: #d14; background-color:{color}; '>
                {content}
              </span><br>
    """
    temp_content = """
            <span style='color: #d14; background-color:{color};'>
                        {content}
            </span>
    """
    temp_simple = """<span style='color: #333; '>
                {content}
              </span><br>
    """
    colors = {"green" : "#ecfdf0",
              "dark_green": "#c7f0d2",
              "red": "#fbe9eb",
              "dard_red": "#fac5cd"}
    list_str = diff_text.split("\n")
    #list_all_html = []
    for i, line_i in enumerate(list_str):
        if line_i.startswith('-'):
            try:
                line_i_ = line_i[1:]  # # убираем символ -
                count_ = nbsp * (len(line_i_) - len(line_i_.lstrip()))  # считаем количество пробелов в начале строки
                line_next = list_str[i+1]
                if line_next.startswith('?'):
                    # убираем символ ?
                    line_next_ = line_next[1:]
                    indexs_1 = [ind for ind, simb in enumerate(line_next_) if simb == "_"]
                    indexs_2 = [ind for ind, simb in enumerate(line_next_) if simb == "^"]
                    # создаем верстку
                    html_list = [i for i in line_i_]  # посимвольный список
                    for i, line_i in enumerate(html_list):
                        if i in indexs_2 or i in indexs_1:
                            html_list[i] = temp_content.format(color=colors["dark_green"], content=line_i)
                        else:
                            html_list[i] = temp_content.format(color=colors["green"], content=line_i)
                    # считаем количество пробелов в начале строки
                    all_srr = "&#8211;" + count_ + "".join(html_list)
                    all_str_html = temp.format(color=colors["green"], content=all_srr).replace("\n", "").replace("\'", "\"")
                    list_all_html.append(all_str_html)
                    print("-?")
                else:
                    all_srr = "&#8211;" + count_ + line_i_
                    all_str_html = temp.format(color=colors["green"], content=all_srr).replace("\n", "").replace("\'", "\"")
                    list_all_html.append(all_str_html)
            except IndexError:
                pass
        elif line_i.startswith('+'):
            try:
                line_next = list_str[i+1]
                line_i_ = line_i[1:]  # # убираем символ -
                count_ = nbsp * (len(line_i_) - len(line_i_.lstrip()))  # считаем количество пробелов в начале строки
                if line_next.startswith('?'):
                    # убираем символ ?
                    line_next_ = line_next[1:]
                    # todo возможно стоит объединить списки
                    indexs_1 = [ind for ind, simb in enumerate(line_next_) if simb == "+"]
                    indexs_2 = [ind for ind, simb in enumerate(line_next_) if simb == "^"]
                    # создаем верстку
                    html_list = [i for i in line_i_]  # посимвольный список
                    for i, line_i in enumerate(html_list):
                        if i in indexs_2 or i in indexs_1:
                            html_list[i] = temp_content.format(color=colors["dard_red"], content=line_i)
                        else:
                            html_list[i] = temp_content.format(color=colors["red"], content=line_i)

                    all_srr = "+" + count_ + "".join(html_list)
                    all_str_html = temp.format(color=colors["red"], content=all_srr).replace("\n", "").replace("\'", "\"")
                    list_all_html.append(all_str_html)
                    #print("-?")
                else:
                    all_srr = "&#8211;" + count_ + line_i_
                    all_str_html = temp.format(color=colors["red"], content=all_srr).replace("\n", "").replace("\'", "\"")
                    list_all_html.append(all_str_html)
                    #print("+?")
            except IndexError:
                pass
        elif line_i.startswith('?'):
            print("?")
            continue
        else:
            count_ = nbsp * (len(line_i) - len(line_i.lstrip()))
            all_srr = count_ + line_i
            all_str_html = temp_simple.format(content=all_srr).replace("\n",
                                                                       "").replace("\'",
                                                                                   "\"")
            list_all_html.append(all_str_html)
            print("simple_line")

    # return ''.join([("%s%s%s%s</span><br>" % (openTag,
    #                                             '#ff0000' if line.startswith('-') else ('#007900' if line.startswith('+') else '#000000'),
    #                                             openTagEnd,
    #                                             nbsp*(len(line) - len(line.lstrip())) + line # nbsp*line.count('') \t (len(line) - len(line.lstrip()))
    #                                             )
    #                  ) for line in diffData]
    #                )

str_diff = '{\n     "id": 0, \n     "jsonrpc": "2.0", \n     "result": {\n        "Вложение": [\n           {\n              "ВерсияФормата": "", \n              "Дата": "", \n              "Зашифрован": "Нет", \n              "Идентификатор": "d29086f7-0d82-11e8-9959-94de802a7b19", \n              "Название": "TXT_FILE_7655432117111101001_7654321069760401001_20150925_f6116e0e-3ed9-4fef-a778-b37af4d4af3f.txt", \n-             "Направление": "XXXXXXX", \n?                             ^^^^^^^\n+             "Направление": "Исходящий", \n?                             ^^^^^^^^^\n              "Номер": "", \n              "ПодверсияФормата": "", \n              "Подтип": "", \n              "Редакция": {\n                 "Номер": "1"\n              }, \n              "Служебный": "Нет", \n              "СсылкаНаHTML": "", \n              "Сумма": "", \n              "Тип": "", \n              "Удален": "Нет", \n-             "УдаленКонтрагентом": "XXXXXXX", \n?                                    ^^^^^^^\n+             "УдаленКонтрагентом": "Нет", \n?                                    ^^^\n              "Файл": {\n                 "Имя": "TXT_FILE_7655432117111101001_7654321069760401001_20150925_f6116e0e-3ed9-4fef-a778-b37af4d4af3f.txt"\n              }\n           }, \n           {\n              "ВерсияФормата": "5.01", \n              "Дата": "22.06.2012", \n              "Зашифрован": "Нет", \n              "Идентификатор": "d29086f6-0d82-11e8-bcd3-94de802a7b19", \n              "Название": "Акт № 10 от 22.06.12 на сумму 113 120 р. в т.ч. НДС 17 255.59 р.", \n              "Направление": "Исходящий", \n              "Номер": "10", \n              "ПодверсияФормата": "", \n              "Подтип": "1175012", \n              "Редакция": {\n                 "Номер": "1"\n              }, \n              "Служебный": "Нет", \n              "Сумма": "113120.00", \n              "Тип": "АктВР", \n              "ТипШифрования": "Отсутствует", \n              "Удален": "Нет", \n              "УдаленКонтрагентом": "Нет", \n              "Файл": {\n                 "Имя": "DP_REZRUISP_2BEcde7e56c60cd4c28b8a0129fb4d92b89_2BE5284e2bfe63b4549926e2c12391dbf4c_20160715_615d4da7-6f90-8c35-3cf0-5afb03dcdba8.xml"\n              }\n           }, \n           {\n              "ВерсияФормата": "5.01", \n              "Дата": "04.06.2015", \n              "Зашифрован": "Нет", \n              "Идентификатор": "d29086f8-0d82-11e8-9b07-94de802a7b19", \n              "Название": "Накладная № 32 от 04.06.15 на сумму 10 960.70 р. в т.ч. НДС 1 308.84 р.", \n              "Направление": "Исходящий", \n              "Номер": "32", \n              "ПодверсияФормата": "", \n              "Подтип": "1175010", \n              "Редакция": {\n                 "Номер": "1"\n              }, \n              "Служебный": "Нет", \n              "Сумма": "10960.70", \n              "Тип": "ЭДОНакл", \n              "ТипШифрования": "Отсутствует", \n              "Удален": "Нет", \n              "УдаленКонтрагентом": "Нет", \n              "Файл": {\n                 "Имя": "DP_TOVTORGPR_2BEcde7e56c60cd4c28b8a0129fb4d92b89_2BE5284e2bfe63b4549926e2c12391dbf4c_20160715_615d4da7-6f90-8c35-3cf0-5afb03dcdba8.xml"\n              }\n           }\n        ], \n        "Идентификатор": "d29086fd-0d82-11e8-be0f-94de802a7b19", \n        "Контрагент": {\n           "СвЮЛ": {\n              "ИНН": "7655432117", \n              "КПП": "760401001"\n           }\n        }, \n-       "Направление": "XXXXXXX", \n?                       ^^^^^^^\n+       "Направление": "Исходящий", \n?                       ^^^^^^^^^\n        "НашаОрганизация": {\n           "СвЮЛ": {\n              "ИНН": "7654321069", \n              "КПП": "760401001", \n              "Название": "ЮЛ1"\n           }\n        }, \n-       "Примечание": "АвтотеEEEEEEстирование TestVi2WriteXXXXXXXAndSendDocs - Отправка комплd d29086fd-0d82-11e8-be0f-94de802a7b19", \n?                            ------                       -------                            ^\n+       "Примечание": "Автотестирование TestVi2WriteAndSendDocs - Отправка комплекта фактуры d29086fd-0d82-11e8-be0f-94de802a7b19", \n?                                                                               ^^^^^^^^^^^^\n        "Регламент": {\n           "Название": "Реализация"\n        }, \n        "Редакция": [\n           {\n              "Актуален": "Да", \n-             "ПримечаниеИС": "XXXXXXX"\n?                              ^^^^^^^\n+             "ПримечаниеИС": "ignore"\n?                              ^^^^^^\n           }\n        ], \n        "Состояние": {\n           "Код": "0", \n           "Название": "Документ редактируется", \n           "Описание": "Ожидается отправка", \n           "Примечание": ""\n        }, \n        "Тип": "ДокОтгрИсх", \n        "Удален": "Нет"\n     }\n  }'
diff_error = 'Traceback (most recent call last):\n                          File "D:\\VIRTUAL_PY\\test_8\\lib\\site-packages\\atf\\core\\case.py", line 276, in _execute_test_part\n                            function()\n                          File "D:\\API_TESTS\\3.17.350\\test-vi\\vi_1_debug\\test_trivial.py", line 205, in test_02\n                            assert_that(tmp_response, is_in_json(response), msg)\n                          File "D:\\VIRTUAL_PY\\test_8\\lib\\site-packages\\atf\\assert_that.py", line 669, in assert_that\n                            raise error\n                          File "D:\\VIRTUAL_PY\\test_8\\lib\\site-packages\\atf\\assert_that.py", line 665, in assert_that\n                            _assert_match(actual=item, matcher=arg2, reason=desc)\n                          File "D:\\VIRTUAL_PY\\test_8\\lib\\site-packages\\atf\\assert_that.py", line 712, in _assert_match\n                            raise AssertionError("\\n" + msg)\n                        AssertionError: \n                        ВИ.ПолучитьСостояниеВнешнегоИнтерфейса\n                        \n                        json1 не входит в json2: \n                          {\n                             "id": 0, \n                             "jsonrpc": "2.0", \n                             "result": {\n                                "d": {\n                        -          "ВерсияИнтерфейса": "11111111", \n                        ?                                 ^^^^^^\n                        +          "ВерсияИнтерфейса": "1.16.7", \n                        ?                                + ^^^\n                        -          "ДатаВремяЗапроса": "000000", \n                        ?                                   ^^\n                        +          "ДатаВремяЗапроса": "13-02-2018 14:40:05", \n                        ?                               +++ +++ +++++++ + ^\n                        -          "СостояниеИнтерфейса": "333333"\n                        ?                                  ^^^^^^\n                        +          "СостояниеИнтерфейса": "Готов"\n                        ?                                  ^^^^^\n                                }, \n                                "s": {\n                                   "ВерсияИнтерфейса": "Строка", \n                                   "ДатаВремяЗапроса": "Строка", \n                                   "СостояниеИнтерфейса": "Строка"\n                                }\n                             }\n                          }\n                        '
str_diff = '\njson1 не входит в json2: \n  {\n     "id": 0, \n     "jsonrpc": "2.0", \n     "result": {\n        "Идентификатор": "86c939b8-10da-11e8-9dd0-94de802a7b19", \n        "Контрагент": {\n           "Email": "", \n           "ИдентификаторИС": "", \n           "СвЮЛ": {\n              "ИНН": "", \n              "КПП": ""\n           }, \n           "Телефон": ""\n        }, \n        "Направление": "Исходящий", \n        "НашаОрганизация": {\n           "ИдентификаторИС": "", \n           "СвЮЛ": {\n              "ИНН": "1708003233", \n              "КПП": "170801001"\n           }\n        }, \n        "Ответственный": {\n           "Идентификатор": "", \n           "Имя": "Нина", \n           "Отчество": "Даадыровна", \n           "Фамилия": "Монгуш"\n        }, \n        "Редакция": [\n           {\n              "Актуален": "Нет"\n           }\n        ], \n        "Событие": [\n           {\n              "Группа": {\n                 "ДатаВремя": "", \n                 "Код": "0", \n                 "Название": "Отправка", \n                 "Описание": "Отправлено", \n                 "Приоритет": "0"\n              }, \n              "ДатаВремяДокумента": "", \n              "Комментарий": "", \n              "Название": "Подготовка"\n           }, \n           {\n-             "Вложение": [\n-                {\n-                   "ВерсияФормата": "07.00", \n-                   "Дата": "", \n-                   "Зашифрован": "Нет", \n-                   "Идентификатор": "86c9aee8-10da-11e8-a531-94de802a7b19", \n-                   "Модифицирован": "Нет", \n-                   "Название": "PFR-700-Y-2014-ORG-091-032-421462-DCK-00722-DPT-000000-DCK-00000.XML", \n-                   "Направление": "Исходящий", \n-                   "Номер": "", \n-                   "ПодверсияФормата": "2014", \n-                   "Подпись": [\n-                      {\n-                         "Сертификат": {\n-                            "ИНН": "1708003233", \n-                            "Квалифицированный": "Да", \n-                            "Отпечаток": "CC92BD0D5C9005184B455C7B165C3D8F98F3FEF6", \n-                            "СерийныйНомер": "2D6FB7565000ECB0E711624B244D8DE3", \n-                            "ФИО": "Монгуш Нина Даадыровна"\n-                         }, \n-                         "Тип": "Отсоединенная", \n-                         "Файл": {\n-                            "Имя": "PFR-700-Y-2014-ORG-091-032-421462-DCK-00722-DPT-000000-DCK-00000.XML.sgn", \n-                            "Ссылка": "ignore"\n-                         }\n-                      }\n-                   ], \n-                   "Подтип": "РСВ-1", \n-                   "Редакция": "ignore", \n-                   "Служебный": "Нет", \n-                   "СсылкаНаPDF": "ignore", \n-                   "Сумма": "", \n-                   "Тип": "ОтчетПФР", \n-                   "Удален": "Нет", \n-                   "УдаленКонтрагентом": "Нет", \n-                   "Файл": {\n-                      "Имя": "PFR-700-Y-2014-ORG-091-032-421462-DCK-00722-DPT-000000-DCK-00000.XML", \n-                      "Ссылка": "ignore"\n-                   }\n-                }, \n-                {\n-                   "ВерсияФормата": "", \n-                   "Дата": "", \n-                   "Зашифрован": "Нет", \n-                   "Идентификатор": "86c987db-10da-11e8-bbb2-94de802a7b19", \n-                   "Модифицирован": "Нет", \n-                   "Название": "instrukcija dlia proektirovanija i stroitelstva velox_rus.pdf", \n-                   "Направление": "Исходящий", \n-                   "Номер": "", \n-                   "ПодверсияФормата": "", \n-                   "Подпись": [\n-                      {\n-                         "Сертификат": {\n-                            "ИНН": "1708003233", \n-                            "Квалифицированный": "Да", \n-                            "Отпечаток": "CC92BD0D5C9005184B455C7B165C3D8F98F3FEF6", \n-                            "СерийныйНомер": "2D6FB7565000ECB0E711624B244D8DE3", \n-                            "ФИО": "Монгуш Нина Даадыровна"\n-                         }, \n-                         "Тип": "Отсоединенная", \n-                         "Файл": {\n-                            "Имя": "instrukcija dlia proektirovanija i stroitelstva velox_rus.pdf.sgn", \n-                            "Ссылка": "ignore"\n-                         }\n-                      }\n-                   ], \n-                   "Подтип": "ПриложениеЭО", \n-                   "Редакция": "ignore", \n-                   "Служебный": "Нет", \n-                   "СсылкаНаPDF": "ignore", \n-                   "Сумма": "", \n-                   "Тип": "СлужебныеЭО", \n-                   "Удален": "Нет", \n-                   "УдаленКонтрагентом": "Нет", \n-                   "Файл": {\n-                      "Имя": "instrukcija dlia proektirovanija i stroitelstva velox_rus.pdf", \n-                      "Ссылка": "ignore"\n-                   }\n-                }, \n-                {\n-                   "ВерсияФормата": "1", \n-                   "Дата": "", \n-                   "Зашифрован": "Нет", \n-                   "Идентификатор": "1b69dfd6-8985-4466-bc28-c9ba2f072bae", \n-                   "Модифицирован": "Нет", \n-                   "Название": "Описание письма", \n-                   "Направление": "Исходящий", \n-                   "Номер": "", \n-                   "ПодверсияФормата": "", \n-                   "Подпись": [\n-                      {\n-                         "Сертификат": {\n-                            "ИНН": "1708003233", \n-                            "Квалифицированный": "Да", \n-                            "Отпечаток": "CC92BD0D5C9005184B455C7B165C3D8F98F3FEF6", \n-                            "СерийныйНомер": "2D6FB7565000ECB0E711624B244D8DE3", \n-                            "ФИО": "Монгуш Нина Даадыровна"\n-                         }, \n-                         "Тип": "Отсоединенная", \n-                         "Файл": {\n-                            "Имя": "описаниеПисьма.sgn", \n-                            "Ссылка": "ignore"\n-                         }\n-                      }\n-                   ], \n-                   "Подтип": "описаниеПисьма", \n-                   "Редакция": "ignore", \n-                   "Служебный": "Да", \n-                   "СсылкаНаPDF": "ignore", \n-                   "Сумма": "", \n-                   "Тип": "СлужебПФР", \n-                   "Удален": "Нет", \n-                   "УдаленКонтрагентом": "Нет", \n-                   "Файл": {\n-                      "Имя": "описаниеПисьма", \n-                      "Ссылка": "ignore"\n-                   }\n-                }, \n-                {\n-                   "ВерсияФормата": "", \n-                   "Дата": "", \n-                   "Зашифрован": "Нет", \n-                   "Идентификатор": "86c987da-10da-11e8-9e88-94de802a7b19", \n-                   "Модифицирован": "Нет", \n-                   "Название": "Оформление письма в пенсионный фонд", \n-                   "Направление": "Исходящий", \n-                   "Номер": "", \n-                   "ПодверсияФормата": "", \n-                   "Подпись": [\n-                      {\n-                         "Сертификат": {\n-                            "ИНН": "1708003233", \n-                            "Квалифицированный": "Да", \n-                            "Отпечаток": "CC92BD0D5C9005184B455C7B165C3D8F98F3FEF6", \n-                            "СерийныйНомер": "2D6FB7565000ECB0E711624B244D8DE3", \n-                            "ФИО": "Монгуш Нина Даадыровна"\n-                         }, \n-                         "Тип": "Отсоединенная", \n-                         "Файл": {\n-                            "Имя": "tekst pisma.txt.sgn", \n-                            "Ссылка": "ignore"\n-                         }\n-                      }\n-                   ], \n-                   "Подтип": "Письмо в ПФР", \n-                   "Редакция": "ignore", \n-                   "Служебный": "Нет", \n-                   "СсылкаНаPDF": "ignore", \n-                   "Сумма": "", \n-                   "Тип": "ПисьмоПФР", \n-                   "Удален": "Нет", \n-                   "УдаленКонтрагентом": "Нет", \n-                   "Файл": {\n-                      "Имя": "tekst pisma.txt", \n-                      "Ссылка": "ignore"\n-                   }\n-                }, \n-                {\n-                   "ВерсияФормата": "1", \n-                   "Дата": "", \n-                   "Зашифрован": "Нет", \n-                   "Идентификатор": "ce3183a2-f6a7-40d0-83f0-aeecbad4edeb", \n-                   "Модифицирован": "Нет", \n-                   "Название": "Транспортная информация", \n-                   "Направление": "Исходящий", \n-                   "Номер": "", \n-                   "ПодверсияФормата": "", \n-                   "Подпись": [\n-                      {\n-                         "Сертификат": {\n-                            "ИНН": "1708003233", \n-                            "Квалифицированный": "Да", \n-                            "Отпечаток": "CC92BD0D5C9005184B455C7B165C3D8F98F3FEF6", \n-                            "СерийныйНомер": "2D6FB7565000ECB0E711624B244D8DE3", \n-                            "ФИО": "Монгуш Нина Даадыровна"\n-                         }, \n-                         "Тип": "Отсоединенная", \n-                         "Файл": {\n-                            "Имя": "транспортнаяИнформация.sgn", \n-                            "Ссылка": "ignore"\n-                         }\n-                      }\n-                   ], \n-                   "Подтип": "транспортнаяИнформация", \n-                   "Редакция": "ignore", \n-                   "Служебный": "Да", \n-                   "СсылкаНаPDF": "ignore", \n-                   "Сумма": "", \n-                   "Тип": "СлужебПФР", \n-                   "Удален": "Нет", \n-                   "УдаленКонтрагентом": "Нет", \n-                   "Файл": {\n-                      "Имя": "транспортнаяИнформация", \n-                      "Ссылка": "ignore"\n-                   }\n-                }\n-             ], \n              "Группа": {\n-                "Код": "0", \n?                        ^\n+                "Код": "4", \n?                        ^\n-                "Название": "Отправка", \n?                             ^ ^^^^^^\n+                "Название": "Игнорировать", \n?                             ^^^^^^^^^^ ^\n-                "Описание": "Отправлено", \n?                             ----------\n+                "Описание": "", \n                 "Приоритет": "0"\n              }, \n              "Исполнитель": {\n                 "Идентификатор": "", \n                 "Имя": "Нина", \n                 "Отчество": "Даадыровна", \n                 "Фамилия": "Монгуш"\n              }, \n              "Комментарий": "", \n-             "Название": "письмо", \n?                             ^^^\n+             "Название": "отложенное подписание", \n?                          ++++++++++++++   ^^^^\n              "Подразделение": {}\n           }\n        ], \n        "Состояние": {\n           "Код": "3", \n           "Название": "Письмо отправлено", \n           "Описание": [\n              {\n                 "Код": "1", \n                 "Название": "Ожидается доставка"\n              }\n           ], \n           "Примечание": ""\n        }, \n        "СсылкаДляКонтрагент": ""\n     }\n  }'
list_str = str_diff.split("\n")

# for i, line_i in enumerate(list_str):
#     print(line_i)
#     if line_i.startswith('-'):
#         print()
#     #print(line_i.lstrip())
#     print()
print("##############################################################################################################")
# for line_i in diff_error:
#     if line_i.startswith('-'):
#         print()

diff_html = getHtml(str_diff)  # str_diff.split("\n")
xxx = "".join(list_all_html)
print()

test_str = '{\n     "id": 0, \n     "jsonrpc": "2.0", \n     "result": {\n        "Вложение": [\n           {\n              "ВерсияФормата": "", \n              "Дата": "", \n              "Зашифрован": "Нет", \n              "Идентификатор": "d29086f7-0d82-11e8-9959-94de802a7b19", \n              "Название": "TXT_FILE_7655432117111101001_7654321069760401001_20150925_f6116e0e-3ed9-4fef-a778-b37af4d4af3f.txt", \n-             "Направление": "XXXXXXX", \n?                             ^^^^^^^\n+             "Направление": "Исходящий", \n?                             ^^^^^^^^^\n              "Номер": "", \n              "ПодверсияФормата": "", \n              "Подтип": "", \n              "Редакция": {\n                 "Номер": "1"\n              }, \n              "Служебный": "Нет", \n              "СсылкаНаHTML": "", \n              "Сумма": "", \n              "Тип": "", \n              "Удален": "Нет", \n-             "УдаленКонтрагентом": "XXXXXXX", \n?                                    ^^^^^^^\n+             "УдаленКонтрагентом": "Нет", \n?                                    ^^^\n              "Файл": {\n                 "Имя": "TXT_FILE_7655432117111101001_7654321069760401001_20150925_f6116e0e-3ed9-4fef-a778-b37af4d4af3f.txt"\n              }\n           }, \n           {\n              "ВерсияФормата": "5.01", \n              "Дата": "22.06.2012", \n              "Зашифрован": "Нет", \n              "Идентификатор": "d29086f6-0d82-11e8-bcd3-94de802a7b19", \n              "Название": "Акт № 10 от 22.06.12 на сумму 113 120 р. в т.ч. НДС 17 255.59 р.", \n              "Направление": "Исходящий", \n              "Номер": "10", \n              "ПодверсияФормата": "", \n              "Подтип": "1175012", \n              "Редакция": {\n                 "Номер": "1"\n              }, \n              "Служебный": "Нет", \n              "Сумма": "113120.00", \n              "Тип": "АктВР", \n              "ТипШифрования": "Отсутствует", \n              "Удален": "Нет", \n              "УдаленКонтрагентом": "Нет", \n              "Файл": {\n                 "Имя": "DP_REZRUISP_2BEcde7e56c60cd4c28b8a0129fb4d92b89_2BE5284e2bfe63b4549926e2c12391dbf4c_20160715_615d4da7-6f90-8c35-3cf0-5afb03dcdba8.xml"\n              }\n           }, \n           {\n              "ВерсияФормата": "5.01", \n              "Дата": "04.06.2015", \n              "Зашифрован": "Нет", \n              "Идентификатор": "d29086f8-0d82-11e8-9b07-94de802a7b19", \n              "Название": "Накладная № 32 от 04.06.15 на сумму 10 960.70 р. в т.ч. НДС 1 308.84 р.", \n              "Направление": "Исходящий", \n              "Номер": "32", \n              "ПодверсияФормата": "", \n              "Подтип": "1175010", \n              "Редакция": {\n                 "Номер": "1"\n              }, \n              "Служебный": "Нет", \n              "Сумма": "10960.70", \n              "Тип": "ЭДОНакл", \n              "ТипШифрования": "Отсутствует", \n              "Удален": "Нет", \n              "УдаленКонтрагентом": "Нет", \n              "Файл": {\n                 "Имя": "DP_TOVTORGPR_2BEcde7e56c60cd4c28b8a0129fb4d92b89_2BE5284e2bfe63b4549926e2c12391dbf4c_20160715_615d4da7-6f90-8c35-3cf0-5afb03dcdba8.xml"\n              }\n           }\n        ], \n        "Идентификатор": "d29086fd-0d82-11e8-be0f-94de802a7b19", \n        "Контрагент": {\n           "СвЮЛ": {\n              "ИНН": "7655432117", \n              "КПП": "760401001"\n           }\n        }, \n-       "Направление": "XXXXXXX", \n?                       ^^^^^^^\n+       "Направление": "Исходящий", \n?                       ^^^^^^^^^\n        "НашаОрганизация": {\n           "СвЮЛ": {\n              "ИНН": "7654321069", \n              "КПП": "760401001", \n              "Название": "ЮЛ1"\n           }\n        }, \n-       "Примечание": "АвтотеEEEEEEстирование TestVi2WriteXXXXXXXAndSendDocs - Отправка комплd d29086fd-0d82-11e8-be0f-94de802a7b19", \n?                            ------                       -------                            ^\n+       "Примечание": "Автотестирование TestVi2WriteAndSendDocs - Отправка комплекта фактуры d29086fd-0d82-11e8-be0f-94de802a7b19", \n?                                                                               ^^^^^^^^^^^^\n        "Регламент": {\n           "Название": "Реализация"\n        }, \n        "Редакция": [\n           {\n              "Актуален": "Да", \n-             "ПримечаниеИС": "XXXXXXX"\n?                              ^^^^^^^\n+             "ПримечаниеИС": "ignore"\n?                              ^^^^^^\n           }\n        ], \n        "Состояние": {\n           "Код": "0", \n           "Название": "Документ редактируется", \n           "Описание": "Ожидается отправка", \n           "Примечание": ""\n        }, \n        "Тип": "ДокОтгрИсх", \n        "Удален": "Нет"\n     }\n  }'
diff_html_2 = getHtml(test_str.split("\n")).replace("\'", "\"")

print()
# command_2 = 'git diff --color-words --no-index 1.txt 2.txt > myfile.txt'  # TEST_DIR\1.txt  TEST_DIR\2.txt
# z2 = git_inst.execute(command_2, with_exceptions=False, stdout_as_string=False)
# diff_str = z.decode("cp1251")
# print(diff_str) # environment


a_commit = "ccccc"
b_commit = "bbbbbb"

y = repo.git.diff(a_commit, b_commit)


repo.diff(a_commit, b_commit)

