# coding="utf-8"
import git
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

def getHtml(diffData):
    """ This method convertes git diff data to html color code
    """
    openTag = "<span style='font-size: .80em; color: "
    openTagEnd = ";font-family: courier, arial, helvetica, sans-serif;'>"
    nbsp = '&nbsp;&nbsp;&nbsp;&nbsp;'
    return ''.join([("%s%s%s%s%s</span><br>" % (openTag, '#ff0000' if line.startswith('-') else ('#007900' if line.startswith('+') else '#000000'), openTagEnd, nbsp*line.count('\t') ,line)) for line in diffData])

xxxx = '"params":\n    {"ВходныеДанные":\n       {"s":\n-         {"ИдентификаторПакетаДокументов":"Строка",\n+         {"ИдентификаторПакетаДокументов":"cccc",\n           "ОтпечатокСертификата":"Строка",\n           "ТекстУточнения":"Строка"},\n        "d":\n          {"ИдентификаторПакетаДокументов":"$_TEST_3_GUID_DOC",\n           "ОтпечатокСертификата":"$_SERVER_CERT",\n-          "ТекстУточнения":"Тестирование отклонения серверным ключом"}\n+          "ТекстУточнения":"Тестирование отdddddddddия серверным ключом"}\n       }\n    },\n "id":0'
for line in xxxx:
    print(line)
diff_html = getHtml(xxxx.split("\n"))


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

