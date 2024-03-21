import postgresql
from data import Data
from methods_for_api_tests_atf_client.functions import *
import time
from methods_for_api_tests_atf_client.functions_vi import perform_action_stage, prepare_action, get_attacment_object, \
    xxx_write_doc, stage_docflow
import zipfile
from methods_for_api_tests_atf_client.inngenerator import new_inn
from xml.etree import ElementTree
from methods_for_api_tests_atf_client.functions_edo import get_attachment_from_list, get_read_doc, \
    create_signature, wait_stage, generate_stage, create_signature_for_base_64, create_signature
from add_invitation_to_base_roaming_edo import AddInvitationRoamingEDO
from create_container import GenerateContainer, create_temp_dir , create_zip
from request_db import *
from methods_for_api_tests_atf_client.functions_vi import prepare_and_perform_action as prepare_and_perform_action_vi
from copy import deepcopy
import requests

def send_doc(client, our_org: dict, contractor: dict, comment: str, *data_file, obj_cert: list=None,
             num_doc: int=None, error=False, type_doc: str="ДокОтгрИсх", **attachments_info: dict):
    """"
    Функция для отправки документ из личного кабинета
    :param client: Клиент онлайна
    :param our_org: Наша организация
    :param contractor: Контрагент
    :param comment: Комментарий
    :param data_file: Кортеж, содержащий пути к файлам
    :param obj_cert: список или кортеж из двух элементов. Первый - имя контейнера, второй - объект сертификата
    :param num_doc: номер документа
    :param attachments_info: Словарь, содержащий данные вложений вида {"имя вложения": "путь к файлу"}
    :return:
    """
    log("Создаем список вложений")
    attachments = []
    result_dict = {}
    if data_file:
        name_file = "test" + generate_guid()+".xml"
        for path_to_file in data_file:
            Data._ID_ATT = generate_guid()  # Идентификатор вложения
            data_base_64 = read_file(path_to_file, encoding="cp1251", get_base_64=True)
            attachments.append(get_attacment_object(name_file, Data._ID_ATT, data_base_64))
            #Обращаться буду по имени файла в каталоге
            result_dict[path_to_file.split("\\")[-1]] = data_base_64
    elif attachments_info:
        for name_file, path_to_file in attachments_info.items():
            Data._ID_ATT = generate_guid()  # Идентификатор вложения
            data_base_64 = read_file(path_to_file, encoding="cp1251", get_base_64=True)
            attachments.append(get_attacment_object(name_file, Data._ID_ATT, data_base_64))
            result_dict[name_file] = data_base_64
    else:
        raise Exception("Необходимо передать data_file или attachments_info")

    log("Записываем документ в кабинет как черновик")
    id_vi = generate_guid()
    result_dict["ИдентификаторВИ"] = id_vi
    temp_dict = {"attacments": attachments, "data_doc": Data._TODAY, "id_doc": id_vi,
                 "contractor": contractor, "our_org": our_org, "note": comment, "type_doc": type_doc}
    if num_doc:
        temp_dict["params_doc"] = {"Номер": num_doc}
    res = xxx_write_doc(client, **temp_dict)

    log("Отправляем документ")
    if isinstance(obj_cert, list) or isinstance(obj_cert, tuple):
        if len(obj_cert) == 2:
            #локальное подписание
            action = stage_docflow("Отправка", "Отправить", cert=obj_cert[1])
            if error:
                res = prepare_and_perform_action_vi(client, id_vi, action, cont_name=obj_cert[0], error=True)
                return res
            else:
                res = prepare_and_perform_action_vi(client, id_vi, action, cont_name=obj_cert[0])

        else:
            raise Exception("Для подписания локальным сертом необходимо передать obj_cert(list или tuple).\n"
                            " Данный объект должен состоять из 2 элементов, первый - имя контейнера,"
                            " второй(словарь) - описывающий сетрификат ")
    else:
        action = stage_docflow("Отправка", "Отправить")
        if error:
            res = prepare_and_perform_action_vi(client, id_vi, action, error=True)
            return res
        else:
            res = prepare_and_perform_action_vi(client, id_vi, action)

    return result_dict


def find_doc_list_inbound(client, mask, wait=120, sleep=10):
    """Находим документ в кабинете"""
    start = time.time()
    params = {"Фильтр": {"s": [{"n": "usePages", "t": "Строка"}, {"n": "ФильтрИзСписка", "t": "Строка"},
                               {"n": "ФильтрПоМаске", "t": "Строка"}],
                         "d": ["full", "Нет", mask], "_type": "record"},
              "Сортировка": None,
              "Навигация": {"s": [{"n": "ЕстьЕще", "t": "Логическое"}, {"n": "РазмерСтраницы", "t": "Число целое"},
                            {"n": "Страница", "t": "Число целое"}],	"d": [True, 25, 0],	"_type": "record"},
              "ДопПоля": []}
    while True:
        res = client.call_rrecordset("РеестрВходящих.СписокСобытий", **params).result
        if len(res) >= 1:
            return res
        elif time.time() < start + wait:
            time.sleep(sleep)
        else:
            msg = "Ожидали, что в ответе метода РеестрВходящих.СписокСобытий количество записей >= 1"
            raise Exception(msg)


def wait_incoming_doc(client, mask, wait=120, sleep=10, ans=False):
    """

    :param client: Клмент онлайна
    :param mask: Маска - Комментарий или номер документа
    :param wait: Время ожидания
    :param sleep: Время перерыва между запросами
    :param ans: Ответ
    :return: id_vi
    """
    # TODO перевести все модули на использование этой функции вместо find_doc_list_inbound
    """Находим документ в кабинете"""
    start = time.time()
    params = {"Фильтр": {"s": [{"n": "usePages", "t": "Строка"}, {"n": "ФильтрИзСписка", "t": "Строка"},
                               {"n": "ФильтрПоМаске", "t": "Строка"}],
                         "d": ["full", "Нет", mask], "_type": "record"},
              "Сортировка": None,
              "Навигация": {"s": [{"n": "ЕстьЕще", "t": "Логическое"}, {"n": "РазмерСтраницы", "t": "Число целое"},
                            {"n": "Страница", "t": "Число целое"}],	"d": [True, 25, 0],	"_type": "record"},
              "ДопПоля": []}
    while True:
        res = client.call_rrecordset("РеестрВходящих.СписокСобытий", **params).result
        if len(res) >= 1:
            break
        elif time.time() < start + wait:
            time.sleep(sleep)
        else:
            msg = "Ожидали, что в ответе метода РеестрВходящих.СписокСобытий количество записей >= 1"
            raise Exception(msg)
    ido = res[0]["@Документ"]
    params = {"ИдО": ido, "ИмяМетода": "ДокОтгрИсх.Список"}
    res2 = client.call_rrecord("ДокОтгрИсх.Прочитать", **params).result
    id_vi = res2["ДокументРасширение.ИдентификаторВИ"]
    if ans:
        return {"id_vi": id_vi, "Res": res2, "@Документ": ido}
    else:
        return id_vi


def wait_doc_in_cabinet(client, mask, wait=120, sleep=10):
    # TODO мало где используется, избавиться от функции
    """Находим документ в кабинете"""
    start = time.time()
    params = {"Фильтр": {"s": [{"n": "usePages", "t": "Строка"},
                               {"n": "ФильтрИзСписка", "t": "Строка"},
                               {"n": "ФильтрОтветыКонтрагентов", "t": "Логическое"},
                               {"n": "ФильтрПоМаске", "t": "Строка"}],
                         "d": ["full", "Нет", False, mask], "_type": "record"},
              "Сортировка": None,
              "Навигация": {"s": [{"n": "HaveMore", "t": "Логическое"},
                                  {"n": "Limit", "t": "Число целое"},
                                  {"n": "Order", "t": "Строка"},
                                  {"n": "Position", "t": "Запись"}],
                            "d": [True, 21, "after", {"d": [""],"s": [{"n": "StartPosition","t": "Строка"}], "_type": "record"}]},
              "ДопПоля": []}
    while True:
        res = client.call_rrecordset("РеестрИсходящих.СписокСобытий", **params).result
        if len(res) >= 1:
            return res
        elif time.time() < start + wait:
            time.sleep(sleep)
        else:
            msg = "Ожидали, что в ответе метода РеестрИсходящих.СписокСобытий количество записей >= 1"
            raise Exception(msg)


def wait_doc_in_cabinet_real(client, mask, type_doc="ДокОтгрИсх", wait=120, sleep=10):
    #TODO попробовать избавиться от функции
    """Находим документ в кабинете - ДокОтгрИсх.СписокХраним"""
    start = time.time()
    params = {"Фильтр": {"d": [True, "full", type_doc, "Нет", mask],
                         "s": [{"n": "rp_doc", "t": "Логическое"}, {"n": "usePages", "t": "Строка"},
                               {"n": "НазваниеТипаДокумента", "t": "Строка"},
                               {"n": "ФильтрПоЛицуИзСписка", "t": "Строка"}, {"n": "ФильтрПоМаске", "t": "Строка"}],
                         "_type": "record"},
              "Сортировка": None,
              "Навигация": {"d": [True, 25, 0],
                            "s": [{"n": "ЕстьЕще", "t": "Логическое"}, {"n": "РазмерСтраницы", "t": "Число целое"},
                                  {"n": "Страница", "t": "Число целое"}], "_type": "record" },
              "ДопПоля": []}
    while True:
        res = client.call_rrecordset("ДокОтгрИсх.СписокХраним", protocol=4, **params).result
        if len(res) >= 1:
            return res
        elif time.time() < start + wait:
            time.sleep(sleep)
        else:
            msg = "Ожидали, что в ответе метода ДокОтгрИсх.СписокХраним количество записей >= 1"
            raise Exception(msg)

def contractor_connection_roaming(client, params):
    """Контрагент.ПодключитьРоумингФилиалу"""
    return client.call_rvalue("Контрагент.ПодключитьРоумингФилиалу", protocol=4, **params).result

def contractor_change_state(client, params):
    """Контрагент.ИзменитьСостояниеТранспорта"""
    return client.call_rvalue("Контрагент.ИзменитьСостояниеТранспорта", protocol=4, **params).result

def contractor_change_roaming_edo(client, params, code=200, error=False):
    """Контрагент.ИзменитьРоумингЭДО"""

    if error:
        res = client.call_rerror("Контрагент.ИзменитьРоумингЭДО", status_code=code, **params).result
    else:
        res = client.call_rvalue("Контрагент.ИзменитьРоумингЭДО", status_code=code, **params).result
    return res

def contractor_off_connection_roaming(client, params):
    """Контрагент.ОтключитьРоумингФилиалу"""
    return client.call_rvalue("Контрагент.ОтключитьРоумингФилиалу", protocol=4, **params).result

def Message_GetInfo(client, id, method=""):
    """Message.GetInfo"""
    params = {"ИдО": id, "ИмяМетода": method}
    return client.call_rrecord("Message.GetInfo", path="/roaming_admin/", protocol=5, **params).result

def document_delete(client, ido, code=200, error=False):
    """Документ.НаУдалить"""
    params = {"ИдО": ido}
    if error:
        res = client.call_rerror("Документ.НаУдалить", status_code=code, **params).result
    else:
        res = client.call_rvalue("Документ.НаУдалить", status_code=code, **params).result
    return res

def perform_action(client, id_doc, stage, code=200, error=False):
    """СБИС.ВыполнитьДействие"""
    params = {
            "Документ": {
                "Идентификатор": id_doc,
                "Этап": stage
            }
        }
    if error:
        res = client.call_rerror("СБИС.ВыполнитьДействие", status_code=code, **params).result
    else:
        res = client.call_rvalue("СБИС.ВыполнитьДействие", status_code=code, **params).result
    return res

def request_db(table, where, list_keys, base, schema=None, get_list_dict=False):
    list_keys_ = ', '.join('"%s"' % key for key in list_keys)
    query_1 = '''SET search_path = public;'''
    if schema:
        query_1 = '''SET search_path = %s, public;''' % schema
    query_2 = '''SELECT {list_keys} FROM "{table}" WHERE {where};'''
    con = postgresql.open(base)
    query = query_2.format(table=table, where=where, list_keys=list_keys_)
    try:
        con.prepare(query_1)()
        log("Запрос\n%s" % query)
        res = con.prepare(query)()
        log("Ответ\n%s" % res)
    finally:
        con.close()
    if get_list_dict:
        res = [dict(zip(list_keys, x)) for x in res]
    return res

def request_db_universal(base, query, schema=None):
    """Выполняет запрос к базе данных
    :param base: адрес базы с логиным/паролем
    :param query: запрос
    :param schema: схема(по умолчанию public)
    """
    query_1 = '''SET search_path = public;'''
    if schema:
        query_1 = '''SET search_path = %s, public;''' % schema
    con = postgresql.open(base)
    try:
        con.prepare(query_1)()
        log("Запрос\n%s" % query)
        res = con.prepare(query)()
        log("Ответ\n{res}".format(res=res))
    finally:
        con.close()

def real_out_record(client, id_doc, face, name, inn, return_record=True):
    params = {"Запись": {"s": [{"n": "@Документ", "t": "Число целое"},
                               {"n": "Лицо1", "t": "Связь"},
                               {"n": "Лицо1.Название", "t": "Строка"},
                               {"n": "Контрагент.ИНН", "t": "Строка"}],
                         "d": [id_doc, face, name, inn],
                         "_type": "record"}}
    return client.call_rvalue("РеалИсх.Записать", protocol=4, **params).result

def client_xxx_read_card(client, ido, return_record=True):
    """КлиентСБИС.ReadCard"""
    params = {"ИдО": ido, "ИмяМетода": None}
    return client.call_rrecord("КлиентСБИС.ReadCard", protocol=4, **params).result


def zipdir(path, ziph_name, list_name_files, path_create_zip="TEMP_ZIP_FILES", del_file=True):
    """
    Создаем архив для отправки - эмулящии 1С
    :param path: путь к каталогу для архивирования(содержимое каталога будет архивироваться)
    :param list_name_files: список файлов в которые необходимо подставить значения
    :param ziph_name: имя файла (архива)
    :param path_create_zip: каталог в корне для создаваемых архивов
    :param del_file: удаляем файл после создания и чтения

    возращает данные архива(бинарные) или путь к созданному архиву
    """
    path_create_zip = os.path.realpath(path_create_zip)
    if not os.path.isdir(path_create_zip):
        os.mkdir(path_create_zip)
    path_create_zip = os.path.join(path_create_zip, ziph_name)
    zipf = zipfile.ZipFile(path_create_zip, 'w', zipfile.ZIP_DEFLATED)
    try:
        for file_name in os.listdir(path):
            path_to_files = os.path.join(path, file_name)
            if file_name in list_name_files:
                data = read_file(os.path.join(path_to_files), encoding="cp1251")
                zipf.writestr(file_name, data.encode("cp1251"))
            else:
                zipf.write(path_to_files, file_name)
    finally:
        zipf.close()

    with open(path_create_zip, "rb") as f:
        data = f.read()
    if del_file:
        os.remove(path_create_zip)
    else:
        # возращаем путь до файла
        return path_create_zip
    return data


def create_temp_dir(name_dir=None):
    """создает отдельный каталог под тест - в этот каталог пападают файлы извлеченные из архивов"""
    path_to_dir = os.path.realpath('TEMP_ZIP')
    if not name_dir:
        name_dir = generate_guid()

    if not os.path.isdir(path_to_dir):
        os.mkdir(path_to_dir)
        folder_files = os.path.join(path_to_dir, name_dir)
        if not os.path.isdir(folder_files):
            os.mkdir(folder_files)
            path_to_dir = folder_files
    else:
        folder_files = os.path.join(path_to_dir, name_dir)
        if not os.path.isdir(folder_files):
            os.makedirs(folder_files)
            path_to_dir = folder_files
        else:
            path_to_dir = folder_files
    return path_to_dir

def get_att_zip(data_zip, ziph_name=None, path_dir_zip="TEMP_ZIP_FILES", encoding="utf-8", extract=False,
                del_file=True, dict_encoding=None, ignore_files=None):
    """Создает архив, возвращает содержимое архива
    :param data_zip: двоичные данные ахрива(полученные из базы)
    :param ziph_name: имя архива
    :param path_dir_zip: каталог, в котормом будет создан ахрив
    :param encoding: кодировка файлов находящихся в архиве
    :param extract: если True, извлекаем содержимое архива, для удобного анализа
    :param del_file: если True, удалем созданный архив
    :return - возвращает словарь, ключ - имя файла, значение - содержание файла
    """
    if not os.path.isdir(path_dir_zip):
        os.mkdir(path_dir_zip)
    if not ziph_name:
        ziph_name = generate_guid()
    path_create_zip = os.path.join(path_dir_zip, ziph_name + ".zip")
    # создали архив
    with open(path_create_zip, 'wb') as f:
        f.write(data_zip)
    with zipfile.ZipFile(path_create_zip, 'r') as myzip:
        if extract:
            # если нужно извлечь - для анализа(отладки)
            path_extract = os.path.join(path_dir_zip, ziph_name)
            myzip.extractall(path_extract)
        dict_att_zip = {}

        for name_file in myzip.namelist():
            with myzip.open(name_file) as myfile:
                data_doc = myfile.read()
                if isinstance(ignore_files, (list, tuple)) and name_file in ignore_files:
                    continue
                elif isinstance(dict_encoding, dict) and name_file in dict_encoding:
                    dict_att_zip[name_file] = data_doc.decode(dict_encoding[name_file])
                else:
                    dict_att_zip[name_file] = data_doc.decode(encoding)

    if del_file:
        os.remove(path_create_zip)
    return dict_att_zip


def get_tag_xml(data_xml, tag_or_xpath, encoding="utf-8"):
    """Возвращаем данные по тегу(xpath)
    :param data_xml: xml ввиде сроки
    :param tag_or_xpath: имя тега или xpath
    :param encoding: кодировка xml файла
    возвращает список - если найдено несколько тегов
    """
    parser = ElementTree.XMLParser(encoding=encoding)
    root = ElementTree.fromstring(data_xml, parser=parser)
    for el in root.iter():
        if '}' in el.tag:
            el.tag = el.tag.split('}', 1)[1]  # strip all namespaces

    info_tag = []
    find_tags = root.findall(tag_or_xpath)

    for info_i in find_tags:
        temp_dict_info = dict(info_i.items())
        text_tag = info_i.text
        if text_tag:
            temp_dict_info["text"] = text_tag
        info_tag.append(temp_dict_info)
    return info_tag


def delete_org(client, info_org):
    """Удаление аккаунта в биллинге
    :param client: экземпляр rtl клинта авторизованног в биллинге(так как вызываются методы биллинга)
    :param info_org: данные организации
    """
    params_1 = {
        'ИНН': info_org["inn"],
        'КПП': info_org.get("kpp", "")

    }

    res = client.call('Контрагент.НайтиПоИННиКПП', return_record=True, protocol=5, **params_1).record
    id_client = res["Идентификатор"]

    params = {
        "ДопПоля": [],
        "Навигация": None,
        "Сортировка": None,
        "Фильтр": {
            "d": [
                id_client
            ],
            "s": [{
                "n": "Идентификатор",
                "t": "Строка"
            }]
        }
    }
    res = client.call('Контрагент.СписокАккаунтовДляУц', return_record=True, protocol=5, **params).record[0]
    id_account = res["@Клиент"]

    res = client.call("КлиентСБИС.Удалить", ИдО=id_account)
    assert_that(res, equal_to(True), "Организация %s не удалилась" % params_1)

def create_data_for_zip(path_to_dir_analysis, dir_for_finish, cont_sing=None, regenerate_id=True):
    """Подготавливаем данные для архива, анализируем имена файлов, генерируем имена и дабавляем эти имана в Data
     так как они испоьзуются в файле description.xml
     :param path_to_dir_analysis: путь до каталога где находятся файлы для создания контейнера
     :param dir_for_finish: путь до каталога где будут находится подготовленные файлы для создания контейнера
     :param cont_sing: имя контейнера(в контейнере находится подпись). Параментр необходим если необходимо создать подписи
     """
    # в каталоге должен находиться файл instruction.json
    path_file_instr = os.path.join(path_to_dir_analysis, "instruction.json")
    if not os.path.isfile(path_file_instr):
        raise Exception("Не обнаружен файл %s" % path_file_instr)
    with open(path_file_instr) as f:
        data_inst_str = f.read()
    data_instr = json.loads(data_inst_str)

    def assert_files(path_dir, data_insrt):
        """Проверет все ли файлы из data_insrt находятся в каталоге path_dir(кроме файла instruction.json
         - это служебный файл)"""
        list_dir = os.listdir(path_dir)
        err_list = []
        for file_i in list_dir:
            if file_i == "instruction.json":
                continue
            if not data_insrt.get(file_i, False):
                msg = "\nВ каталоге {name_dir} обнаружен файл {name_file}, данный файл отсутствует " \
                      "в instruction.json.\n" \
                      "Зарегистрируйте его в файле instruction.json или удалите из каталога \n"
                err_list.append(msg.format(name_dir=path_dir, name_file=file_i))
        for file_i in data_insrt.keys():
            if file_i not in list_dir:
                msg = "\nФайл {name_file} из файла instruction.json не обнаружен в каталоге {path_dir}"
                err_list.append(msg.format(name_file=file_i, path_dir=path_dir))
        if err_list:
            all_msg = "".join(err_list)
            raise Exception(all_msg)

    # проверим, что с содержание каталога(path_to_dir_analysis) и файла instruction.json - ok
    assert_files(path_to_dir_analysis, data_instr)

    # анализируем содержание data_instr - генерируем новые имена файлов и патчим при необходимости
    for name_file_i in data_instr.keys():
        if name_file_i.startswith("$_"):
            name_file, extension_file = name_file_i.split(".")
            name_var_data = name_file.split("$")[1]
            if regenerate_id:
                val_i = generate_guid().replace("-", "")
            else:
                val_i = getattr(Data, name_var_data, generate_guid().replace("-", ""))
            setattr(Data, name_var_data, val_i)
            data_instr[name_file_i]["new_name_file"] = Data.__dict__[name_var_data] + "." + extension_file
        else:
            data_instr[name_file_i]["new_name_file"] = name_file_i

    # Начинем патчить документы(на данном этапе все необходимые)
    def patching_files(path_to_dir_analysis, instr, dir_for_finish, cont_sing):
        """"""

        # Разделяем файлы на те, которые являются подписями и все остальные
        def _diff_file_sign(instr, path_to_dir_analysis):
            """Разделяет файлы на подписи и все остальные"""
            dict_files = {}
            dict_files_sign = {}
            all_list_files = instr.keys()
            for file_name, info_file in instr.items():
                # если ключ is_sign присутствует, то его значение ДОЛЖНО быть название файла,
                # подписью которого он является
                is_sign_val = info_file.get("is_sign", None)
                if is_sign_val:
                    # если is_sign заполнено чем-то
                    if is_sign_val in all_list_files:
                        # файл указанный в is_sign присутствует в каталоге
                        dict_files_sign[file_name] = info_file
                    else:
                        msg = "\nДля файла {name_file_sign} значение ключа is_sign должно соответствовать " \
                              "имени файла, подписью которого он является," \
                              "(Следует обратить внимане не содержание файла instruction.json и " \
                              "содержимое каталога{dir_analysis})".format(name_file_sign=file_name,
                                                                          dir_analysis=path_to_dir_analysis)
                        raise Exception(msg)
                else:
                    dict_files[file_name] = info_file
            return dict_files, dict_files_sign

        def _patching_file(path_to_dir_analysis, dir_for_finish, dict_files):
            """"""
            for name_file_i, info_file in dict_files.items():
                path_to_file_fin = os.path.join(dir_for_finish, info_file["new_name_file"])
                path_temp_file = os.path.join(path_to_dir_analysis, name_file_i)
                if info_file["patching"] == "true":
                    encoding_file = info_file.get("encoding", None)
                    # read_file - патчит файл - возвращает подготовленные данные
                    data_file = read_file(path_temp_file, encoding=encoding_file)
                    with open(path_to_file_fin, "w", encoding=encoding_file) as f:
                        f.write(data_file)
                else:
                    # не патчим - просто копируем содержание, создаем нужный файл с неизменным содержанием
                    with open(path_temp_file, "rb") as f1:
                        data_tmp = f1.read()
                        with open(path_to_file_fin, "bw") as f2:
                            f2.write(data_tmp)

        def _generate_sign(path_to_dir_analysis, dir_for_finish, dict_files_sign, dict_files, cont_sing):
            """"""
            for name_file_i, info_file in dict_files_sign.items():
                name_file_for_sign = info_file["is_sign"]
                # path_fie_for_sign - по этому пути находится файл для которого будет создана подпись
                path_fie_for_sign = os.path.join(dir_for_finish, dict_files[name_file_for_sign]["new_name_file"])
                data_sign = create_signature(path_fie_for_sign, cont_name=cont_sing, is_file=True)
                bin_sign = data_sign.encode()
                # создаем подись
                path_to_sign = os.path.join(dir_for_finish, info_file["new_name_file"])
                # todo тут могут быть проблемы
                with open(path_to_sign, mode="bw") as f:
                    f.write(bin_sign)

        dict_files, dict_files_sign = _diff_file_sign(instr, path_to_dir_analysis)

        _patching_file(path_to_dir_analysis, dir_for_finish, dict_files)
        if dict_files_sign:
            # если подписи в каталоге присутствуют(те, которые должны быть перегенерированы)
            if cont_sing:
                # тогда необходим контейнер с подписью для перегенерации
                _generate_sign(path_to_dir_analysis, dir_for_finish, dict_files_sign, dict_files, cont_sing=cont_sing)
            else:
                msg = "\nВ файле instruction.json обнаружены файлы с инстукциями {dict_inst}, а конейнер для " \
                      "перегенерации не перадан(переменная cont_sing) в функцию create_data_for_zip"
                raise Exception(msg.format(dict_inst=dict_files_sign))

    patching_files(path_to_dir_analysis, data_instr, dir_for_finish, cont_sing=cont_sing)


def get_info_contractor(client, info_org):
    """Возвращает сведения о контраненте
    :param client: экземпляр класса авторизованного в кабинете
    :param info_org: словарь с обязательными ключами type, inn и kpp(для случая ul)
    """
    if not info_org.get("type", None):
        raise Exception("В переданном объекте не обнаружен ключ type, "
                        "ключ необходим для определения типа контрагента\nДопустимые значения ul или ip")

    if info_org["type"] == "ul":
        params = {
            "Участник": {
                "СвЮЛ": {
                    "ИНН": info_org["inn"],
                    "КПП": info_org["kpp"]
                }
            }
        }
    elif info_org["type"] == "ip":
        params = {
            "Участник": {
                "СвФЛ": {
                    "ИНН": info_org["inn"]
                }
            }
        }
    else:
        raise Exception("Значение ключа type должно быть ul или ip")
    return client.call_rvalue("СБИС.ИнформацияОКонтрагенте", **params).result


def incoming_processor(client, tesk, site=r"/roaming-edo/"):#asdasd
    params = {"task_pk": tesk}
    headers = deepcopy(client.headers)
    headers.update({"X-Uniq-ID": generate_guid()})
    client.call_rvalue("IncomingProcessor.ParsePackage", path=site, headers=headers, **params)


def get_name_roaming_org(org):
    """

    :param org:
    :return:
    """
    if org["type"] == "ip":
        name_roaming_org = org["lastname"] + " " + org["firstname"] + " " + org["patronymic"] + ", ИП"
    else:
        name_roaming_org =org["name"]
    return name_roaming_org


def search_name(temp_search, dict_for_search):
    """
    ВРЕМЕННЫЙ МЕТОД - ПОКА НЕ ПОПАДЕТСЯ БОЛЕЕ СЛОЖНЫЙ СЛУЧАЙ
    :param temp_search: шаблон поиска
    :param dict_for_search: словарь с ключами для поиска
    :return: список, содержащий содержание файлов чьи имена подошли под шаблон поиска temp_search
    """
    list_serch_files = []
    for name, val in dict_for_search.items():
        if temp_search in name:
            list_serch_files.append(name)
    return list_serch_files

def send_package(client_private, path_to_dir_for_zip, url_service, regenerate = True, operator=6):
    """
   Функция создает архив в рабочей директории и загружает его в БД роуминга
   :param dir: Путь к директории, файлы которой нужно пропатчить и сделать из них архив
   :param package_sender: Отправитель пакета
   :param package_receiver: Получатель пакета
   :return: возвращает идентификатор задачи по загрузке пакета в БД роуминга
    """
    parent_dit = generate_guid(False)
    child_dir = generate_guid(False)
    dir_path_patching_files = create_temp_dir("{guid_1}\{guid_2}".format(guid_1=parent_dit, guid_2=child_dir))
    log("Создали каталог - в нем находятся файлы для дальнейшего архивирования"
        "] и загрузки в базу %s" % dir_path_patching_files)
    path_to_create_zip = dir_path_patching_files.rsplit("\\", 1)[0]
    create_data_for_zip(path_to_dir_for_zip, dir_path_patching_files, regenerate_id=regenerate)
    name_zip = generate_guid(False) + ".zip"
    path_to_zip = create_zip(path_to_create_zip, name_zip, [], path_create_zip="TEMP_ZIP_FILES",del_file=False)
    log("По адресу %s находится архив, загружаемый в базу(в конце теста удаляется)" % path_to_zip)
    inst = AddInvitationRoamingEDO(**Data._DATA_BASE)
    log("Кладем наше приглашение(архив) в базу роуминга ЭДО")
    info_invation = inst.add_invitation(path_to_zip, url=url_service, operator=operator)
    log("IncomingProcessor.ProcessPackage - толкаем на выполнение задачу")
    incoming_processor(client_private, info_invation["task"])
    return info_invation


def sign_ssl(path_to_zip, ziping):
    """Генерация подписанного пакета .cms для честной отправки в роуминг через POST-запрос
    path_to_zip - Дерриктория с архивом для подписи
    ziping - Имя подписываемого архива
    """
    name_zip = ziping.split(".")[0]
    name_zip = os.path.join(path_to_zip, ziping.split(".")[0])
    ziping = name_zip + ".zip"
    name_zip = name_zip + ".cms"

    dir_key = os.path.join((path_to_zip.rsplit("\\", 1)[0] + r"\test-files\Sign25"), "2bc_1.key")
    dir_sign = os.path.join((path_to_zip.rsplit("\\", 1)[0] + r"\test-files\Sign25"), "2bc_1.cer")
    # command_list = [r'openssl cms -sign -binary -inkey "{dir_key}" '
    #                 r'-signer "{dir_sign}" -in "{ziping}" -out "{name_zip}" -outform DER -nodetach'
    #                 .format(dir_key=dir_key, dir_sign=dir_sign, ziping=ziping, name_zip=name_zip)]
    command_list = [r'"C:\Program Files\OpenSSL-Win64\bin\openssl.exe"', 'cms', '-sign', '-binary',
                    '-inkey', r'"{dir_key}"'.format(dir_key=dir_key),
                    '-signer', r'"{dir_sign}"'.format(dir_sign=dir_sign),
                    '-in', r'"{ziping}"'.format(ziping=ziping),
                    '-out', r'"{name_zip}"'.format(name_zip=name_zip),
                    '-outform',  'DER', '-nodetach']

    command_list = ['openssl', 'cms', '-sign', '-binary',
                    '-inkey', r"f:\\API_TESTS_GIT\\api_transit\\test_roseu_transport_doc\\test-files\\Sign25\\2bc_1.key",
                    '-signer', r"f:\\API_TESTS_GIT\\api_transit\\test_roseu_transport_doc\\test-files\\Sign25\\2bc_1.cer",
                    '-in', r"f:\\API_TESTS_GIT\\api_transit\\test_roseu_transport_doc\\TEMP_ZIP_FILES\\f261a3ee9a8f11eaa40794de802a7b19.zip" ,
                    '-out', r"f:\\API_TESTS_GIT\\api_transit\\test_roseu_transport_doc\\TEMP_ZIP_FILES\\f261a3ee9a8f11eaa40794de802a7b19.cms",
                    '-outform', 'DER', '-nodetach']

    # r'c:\Program Files\OpenSSL-Win64\bin\openssl.exe',
    my_env = os.environ.copy()
    my_env["PATH"] = my_env["PATH"] + r"C:\Program Files\OpenSSL-Win64\bin;"
    str_commands = " ".join(command_list)
    process = subprocess.Popen(command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,  env=my_env)#,  env=my_env , cwd=path_to_zip
    stdout, stderr = process.communicate(timeout=30)
    exit_code = process.returncode
    # stderr.decode("cp866")

    # os.chdir(path_to_zip)
    dir_key = os.path.join((path_to_zip.rsplit("\\", 1)[0]+r"\test-files\Sign25"), "2bc_1.key")
    dir_sign = os.path.join((path_to_zip.rsplit("\\", 1)[0]+r"\test-files\Sign25"), "2bc_1.cer")
    log("Передаем команду для подписания и создани .cms для openssl")
    commands = [r'openssl cms -sign -binary -inkey "{dir_key}" '
                r'-signer "{dir_sign}" -in {ziping} -out {name_zip}.cms -outform DER -nodetach'
                    .format(dir_key=dir_key, dir_sign=dir_sign, ziping=ziping, name_zip=name_zip)]
    # log("Выполняем")
    # procs = os.system(commands[0])


    log("Указываем деррикторию в которой нужно найти .cms")
    # file_cms = r"D:\Git-test\api\test_roseu_transport_doc\TEMP_ZIP_FILES\{name_zip}".format(name_zip=name_zip)
    file_cms = path_to_zip + r"\{name_zip}".format(name_zip=name_zip)
    if procs == 0:
        log("Генерация пакета .cms прошла успешно, открываем и читаем его")
        with open(file_cms + ".cms", "rb") as f:
            package = f.read()
        log("Указываем заголовки POST-запроса")
        headers = {
            "Content-Disposition": f'filename="{name_zip}.cms"',
            "Send-Receipt-To": "{}".format(config.URL_ROAMING_EDO_SERVICE),
        }
        log("Указываем URLна который шлем")
        # url = "http://test1-api.xxx.ru/roaming-edo-ext/service/"
        res = requests.post(config.TRUE_URL_ROAMING_SERVICE, data=package, headers=headers)
        print(res.status_code)
        print(res.text)
        log("По идентификатору пакета с регистрацией получаем задачу формирования ЛС")
        where = '"Id"=\'{id}\''.format(id=name_zip)
        package = request_db_wait_record("Package", where, ["@Package"])[0]["@Package"]
        where = '"Package"=\'{package}\''.format(package=package)
        task = request_db_wait_record("Message", where, ["Task"])[0]["Task"]
        where2 = '"ОбъектИдентификатор"=\'{task}\''.format(task=task)
        state = request_db_wait_record("Состояние", where2, ["Значение"])[0]["Значение"]
        # where3 = '"Событие"=\'{state}\''.format(state=state)
        # value = request_db_wait_record("ЖурналИзменений", where3, ["Примечание"],
        #                                count_record=1,)[0]["Примечание"]
        os.remove(file_cms + ".cms")
        os.remove(file_cms + ".zip")
        info_invation = {"task": task, "package": name_zip, "condition": state}
        return info_invation
    else:
        log("При генерации подписи возникла ошибка")


def send_secondary_package(client_private, path_to_dir, cont_name=None, url_service=None, operator=6, regenerate=True,
                           ls=True, client_cloud=None):
    # todo - ОПИСАНИЕ ГДЕ ?
    parent_dit = generate_guid(False)
    child_dir = generate_guid(False)
    dir_path_patching_files = create_temp_dir("{guid_1}\{guid_2}".format(guid_1=parent_dit, guid_2=child_dir))

    log("Создали каталог - в нем находятся файлы для дальнейшего архивирования"
        " и загрузки в базу %s" % dir_path_patching_files)
    path_to_create_zip = dir_path_patching_files.rsplit("\\", 1)[0]

    log("Создаем архив c .p7s подписью под вторичным документом")
    GenerateContainer().create_data_for_zip(path_to_dir, dir_path_patching_files, cont_sing=cont_name,
                                            regenerate_id=regenerate)
    name_zip = generate_guid(False) + ".zip"
    path_to_zip = create_zip(path_to_create_zip, name_zip, del_file=False, ls_mode=ls)
    if operator == 25 and url_service == "https://fix1-api.xxx.ru/roaming-edo-ext/service/":
        info_invation = sign_ssl(path_to_zip.rsplit("\\", 1)[0], name_zip)
        # os.remove(path_to_create_zip)
    else:
        log("По адресу %s находится архив, загружаемый в базу(в конце теста удаляется)" % path_to_zip)
        inst = AddInvitationRoamingEDO(**Data._DATA_BASE)
        log("Кладем пакет со служебным документом в базу роуминга ЭДО")
        info_invation = inst.add_invitation(path_to_zip, url=url_service, operator=operator)
        log("IncomingProcessor.ProcessPackage - толкаем на выполнение задачу")
        incoming_processor(client_private, info_invation["task"])
    return info_invation



def wait_doc_by_vi(client, id_vi):
    """
    Функция ожидает документ в кабинете по идентификатору ВИ
    :param client: Клиент онлайна
    :param id_vi: Идентификатор ВИ
    :return:
    """
    start = time.time()
    while True:
        try:
            client.call_rvalue("СБИС.ПрочитатьДокумент", **{"Документ": {"Идентификатор": id_vi}}).result
        except Exception:
            if time.time() < start + 120:
                time.sleep(10)
            else:
                raise Exception("Не дождались документа {id_vi} в кабинете получателя в "
                                "течение 120 секунд".format(id_vi=id_vi))
        else:
            log("Неформализованный документ получен на получателе")
            break

def get_service_doc_id(client, id_doc, wait_event_list):
    """
    Получаем идентификатор служебного этапа
    :param client: Клиент онлайна
    :param id_doc: Идентификатор ВИ документа
    :param wait_event_list: Список служебок, по которым нужно получить идентификатор
    :return: Идентификаторы указанных служебных этапов по служебкам
    """
    list_id_servise_stage = []
    for i in wait_stage(client, id_doc=id_doc, wait_event_list=wait_event_list):
        service_doc_id = i["Этап"][0]['Идентификатор']
        list_id_servise_stage.append(service_doc_id)
    return list_id_servise_stage


def prepare_and_perform_service_stage(client, id_doc, list_id_service, cont_name=None, cert=None):
    """
    Обрабатываем служебный этап
    :param client: Клиент онлайна
    :param id_doc: Идентификатор ВИ
    :param list_id_service: Список с идентификаторами служебных этапов
    :param cont_name: Имя контейнера
    :param cert: отпечаток серта
    :return:
    """
    for id_service in list_id_service:
        if cert:
            stage_service = {"Действие": [{"Название": "Обработать служебное",
                                           "Сертификат": cert}], "Идентификатор": id_service}
        else:
            stage_service = {"Действие": [{"Название": "Обработать служебное"}], "Идентификатор": id_service}
        prepare_and_perform_action_vi(client, id_doc, stage_service, cont_name=cont_name)


def check_package_send_in_roaming(name):
    """По имени файла получаем состояние обработки ТП с ним"""
    log("Вычисляем состояние обработки пакета с документом. \n"
        "Состояние 0 - пакет успешно отправлен в роуминг, получена положительная тех. квитанция; \n"
        "Состояние 3 - пакет успешно отправлен в роуминг, но получена тех. квитанция с ошибкой. \n"
        "оба состояния означают, что пакет успешно отправлен в роуминг, поэтому проверяем равенство одному из них")
    where = '"Filename"=\'{}\''.format(name)
    message = lambda: len(request_db_wait_record("Document", where, ["Message"]))
    assert_that(message, equal_to(1), "Документ не ушел в роуминг - таблица Document не заполнена", and_wait(180, 10))
    log("По имени документа из таблицы Document получаем идентификатор ЛС")
    message = request_db_wait_record("Document", where, ["Message"])[0]["Message"]
    log("По идентификатору ЛС из таблицы Message получаем Task - номер задачи")
    where = '"@Message"=\'{message}\''.format(message=message)
    task = request_db_wait_record("Message", where, ["Task"])[0]["Task"]
    log("По номеру задачи из таблицы Task получаем состояние ее обработки")
    where = '"@Task"=\'{task}\''.format(task=task)
    state = request_db_wait_record("Task", where, ["State", "Retries"])[0]
    state, retries = state["State"], state["Retries"]
    log("Получаем идентификатор ЛС - нужно для формирования удобного исключения")
    where = '"@Message"=\'{message}\''.format(message=message)
    message_id = request_db_wait_record("Message", where, ["Id"])[0]["Id"]
    statement = state in (0, 3) and retries != 10
    return {"state": statement, "message": message_id, "task": task}

def check_stage_pakage_in_roaming(package):
    '''
    По пакету получаем состояние обработки ТП
    :param package: номер пакета загруженного в базу
    :return:
    '''
    log("По идентификатору ТП из таблицы Message получаем Task - номер задачи")
    where = '"Package"=\'{package}\''.format(package=package)
    task = request_db_wait_record("Message", where, ["Task"])[0]["Task"]
    log("Из таблицы Message плучаем-@Message- номер сообщения")
    message = request_db_wait_record("Message", where, ["@Message"])[0]["@Message"]
    log("По номеру задачи из таблицы Task получаем состояние ее обработки")
    where = '"@Task"=\'{task}\''.format(task=task)
    state = request_db_wait_record("Task", where, ["State", "Retries"])[0]
    state, retries = state["State"], state["Retries"]
    log("Получаем идентификатор ЛС - нужно для формирования удобного исключения")
    where = '"@Message"=\'{message}\''.format(message=message)
    message_id = request_db_wait_record("Message", where, ["Id"])[0]["Id"]
    statement = state in (0, 3) and retries != 10
    return {"state": statement, "message": message_id, "task": task}

def get_attachment_name(client, id_vi, phase, type_doc):
    #TODO подумать о возможности вывода результата в виде {"СЧФДОП": "DP_IZVPOL..", .. и в common}
    """
    Получение имени файла на основании этапа документооборота и типа документа
    :param client: Клиент-отправитель документа
    :param id_vi: Идентификатор ВИ
    :param phase: Название этапа, например, Загрузка
    :param type_doc: Тип отправленного документа, например УпдСчфДоп
    :return:
    """
    wait_event = lambda: len(get_attachment_from_list(get_read_doc(client, id_vi, get_result=False)["Событие"], {"Название": phase})) > 0
    assert_that(wait_event, equal_to(True), "На документе нет этапа " + phase, and_wait(90, 5))
    event_list = get_read_doc(client, id_vi, get_result=False)["Событие"]
    event = get_attachment_from_list(event_list, {"Название": phase})[0]
    if type_doc:
        wait_attachment = lambda: len(get_attachment_from_list(event["Вложение"], {"Тип": type_doc}))
        assert_that(wait_attachment() > 0, equal_to(True), "На этапе нет документа " + type_doc, and_wait(90, 5))
        attachments = get_attachment_from_list(event["Вложение"], {"Тип": type_doc})
    name_files = [attachment_i["Файл"]["Имя"] for attachment_i in attachments]
    if len(name_files) == 1:
        name_files = name_files[0]
    return name_files

def wait_doc_by_name(client, id_vi, name_file, wait=90):
    """
    Дожидаемся в кабинете документ по его имени
    :param client: Клиент онлайна
    :param id_vi: Идентификатор ВИ
    :param name_file: Имя служебного документа
    :param wait: Необязательный параметр времени ожидания
    """
    start = time.time()
    while time.time() < start + wait:
        attachment_list = get_read_doc(client, id_vi)['result']['Вложение']
        for attachment in attachment_list:
            if name_file == attachment["Файл"]["Имя"]:
                log("На документе найдено искомое вложение")
                break
            else:
                continue
        else:
            time.sleep(5)
        break
    else:
        raise AssertionError("Не найдено вложение с именем " + name_file)


def download_doc_by_num(client, id_doc):
    """
    Скачивает документ по номеру пакета
    :param client: Клиент админки
    :param id_doc: Индификатор PK
    :return:
    """
    params = {"PK" : id_doc }
    container_b64data = client.call_rvalue("RoamingDocument.Download", path="/roaming_admin/service/", **params).result["Данные"]
    return container_b64data

def download_package_by_id(client, pack_id):
    """
    Скачивает ТП по ID пакета
    :param client: Клиент админки
    :param pack_id: Индификатор ТП - @Package из таблицы Package
    :return:
    """
    params = {"Id": pack_id}
    container_b64data = client.call_rvalue("Package.Download", path="/roaming_admin/service/", **params).result["Данные"]
    return container_b64data


def check_document_state(client, id_vi, code):# из EDI

    '''
    Функция проверяет состояние документа
    :param client: Клиент онлайна
    :param id_vi: Индификатор ВИ
    :param code: Ожидаемое состояние
    :return:
    '''

    start = time.time()
    while time.time() < start + 120:
        doc_state = get_read_doc(client, id_vi, log_out=False)['result']['Состояние']['Код']
        if doc_state == code:
            get_read_doc(client, id_vi)
            break
        time.sleep(2)
    else:
        get_read_doc(client, id_vi)
        assert False, "Состояник документа отличается от ожидемого"

def rosey_switch(client, id_contactor, id_account, indifier, enabled):
    '''
    Функция отклчает или подключает Роминг
    :param client: Клиент оглайна
    :param id_contactor: @Лицо
    :param id_account: Идентификатор Аккаунта
    :param indifier: ИД Получателя
    :param enabled:  Принимает значения True/False
    :return:
    '''

    params = {"counterpart_pk": id_contactor, "account_pk": id_account, "operator": "2BC",
              "identifier": indifier, "enabled": enabled}
    client.call_rvalue("Контрагент.ИзменитьРоумингЭДО", **params).result


def edo_switch(client, id_contactor, id_account, enabled, state):
    '''
    Функция отключает или подключает ЭДО
    :param client: Клиент биллинга
    :param id_contactor: ИД Контрагента
    :param id_account: Идентификатор Аккаунта
    :param indifier: ИД Получателя
    :param enabled:  Принимает значения True/False
    :param enabled:  Принимает значения 0/1
    :return:
    '''

    params = {"ИдКонтрагента": int(id_contactor), "ИдентификаторАккаунта": int(id_account),
              "ТипТранспорта": 1, "Состояние": state, "Уверен": enabled, "ИмяПользователя": "Трякин С.В."}
    client.call_rvalue("Контрагент.ИзменитьСостояниеТранспорта", **params).result


def add_route(client, id_roseu, id_edo, id_billing_edo):
    """
    Добавляет маршрут по ИД
    :param client: Клиент биллинга
    :param id_roseu: ИД А/Я клиентта которуму подключаем
    :param id_edo: @Лицо , того к кому настраиваем маршрут
    :param id_billing_edo: ИД кабинета в биллинге клиентта которуму подключаем
    :return:
    """
    params = {"clientEdoId": id_roseu, "contractorFaceId": id_edo,
              "faceId": id_billing_edo, "branchCode": None}

    client.call_rvalue("RoamingRoutes.Add", path_without_dll='/roaming_admin/service/', **params).result


def event_list(client, id_doc):
    """

    :param client: Клиент онлайна
    :param id_doc: ИД документа
    :return:
    """
    params = {"Фильтр":{"d":[id_doc], "s": [{"n": "ИдДокумента", "t": "Строка"}], "f": 0, "_type": "record"}}
    res = client.call_rvalue("ЭДО.СписокСобытий", **params).result
    return res


def reprocessing(client, container, id):
    """
    Метод из админки роуминга заставляющий переобрабатывать ТП или ЛС
    :param client: Клиент админки
    :param container: 0-ЛС, 1-ТП
    :param id:
    :return:
    """
    params = {"containerType": container, "containerId": id}
    client.call_rvalue("Roaming.ResendContainer", path_without_dll='/roaming_admin/service/', **params).result


def favorited_language(client, value):
    """
    Метод меняет язык в онлайне(для проверки приглашений на en)
    :param client: Клиент онлайнв
    :param value: значение языка("ru-RU","en-EN")
    :return:
    """
    params = {"Value": value}
    client.call_rvalue("ProfileServicePerson.SetFavoritedLanguage", **params).result

def data_in_package(name_file):
    """
    Получение двоичных данных из пакета по имени документа.
    :param name_file: Имя документа
    :return: message - ид лс, data_package - двоичные данные пакета, doc_id - ид документа в пакете, sign_id - ид подписи в пакете
    """
    log("Получаем данные о description исходящего в роуминг пакета")
    where = '"Filename"=\'{}\''.format(name_file)
    document = request_db_wait_record("Document", where, ["Message", "ToDocument", "ExtId", "@Document"])[0]
    doc_id, doc_in_base = str(document["ExtId"]).replace("-", ""), document["@Document"]
    log("Получаем имя подписи в пакете - нужно для вычитывания архива со связанным документом")
    message = '"Message"=\'{}\''.format(document["Message"])
    sign_id = str(request_db_wait_record("Signature", message, ["Id"])[0]["Id"]).replace("-", "")
    log("Получаем двочные данные пакета ")
    where2 = '"@Message"=\'{}\''.format(document["Message"])
    package_all = request_db_wait_record("Message", where2, ["Package", "Id"])[0]
    package, message_id = package_all["Package"], package_all["Id"]
    where3 = '"@Package"=\'{}\''.format(package)
    data = request_db_wait_record("Package", where3, ["Data"])[0]["Data"]
    return {"message": message_id, "data_package": data, "doc_id": doc_id, "sign_id": sign_id}

def add_notificationtask(id):
    """
    Функция получает на вход ИД тп, а на выхое выдает сообщение для таблицы NotificationTask
    :param id: ИД ТП
    :return:
    """
    where = '"@Package"=\'{}\''.format(id)
    package_id = request_db_wait_record("Package", where, ["Id"])[0]["Id"]
    msg = {"PackageId": package_id, "StateProps": 17}# аналитическое состояние. 17 = входящий транспортный пакет, состояние "на обработке"
    msg = json.dumps(msg)
    return msg