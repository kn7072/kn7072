# -*- coding: utf-8 -*-
"""
Тестируем базовый функционал в реестре документы: создание документа и загрузка соответствующего форматного вложения
 во всех подразделах, прохождение по аккордеону со всеми вкладками, создание, редактирование и удаление документа,
 функция выгрузки в архив для только что сохраненного документа.
ссылка на ТП - "http://inside.xxx.ru/doc/_layouts/DocIdRedir.aspx?ID=xxx-10-1137"
"""
from contextlib import contextmanager
from guppy import hpy
from memory_profiler import profile
fp = open('memory_profiler.log', 'w+')
fp_info = open("mem_info.log", mode='w')
fp_info_type = open("mem_info_type.log", mode="w")

heap = hpy()

# @contextmanager
# def memory_point(msg):
#     print(f"ANALYSIS_MEMORY {msg}")
#     # h_start = hpy()
#     print(h.heap())
#     yield
#     # h_finish = hpy()
#     print(h.heap())
#     print("END_ANALYSIS_MEMORY")

@contextmanager
def memory_point(msg):
    fp.write("#" * 50 + "\n")
    fp.write(f"ANALYSIS_MEMORY {msg}\n")
    h_start = heap.heap()
    fp.write(str(h_start))
    yield
    h_finish = heap.heap()
    fp.write(str(h_finish))

    fp.write(f"DIFF {str(h_finish.diff(h_start))}\n")
    fp.write("END_ANALYSIS_MEMORY\n")
    fp.flush()

@contextmanager
def memory_point_unreachable(msg):
    fp.write("#" * 50 + "\n")
    fp.write(f"ANALYSIS_MEMORY UNREACHABLE {msg}\n")
    h_start = heap.heapu(stat=0)
    fp.write(str(h_start))
    yield
    h_finish = heap.heapu(stat=0)
    fp.write(str(h_finish))

    fp.write(f"DIFF {str(h_finish.diff(h_start))}\n")
    fp.write("END_ANALYSIS_MEMORY UNREACHABLE\n")
    fp.flush()

with memory_point("BEFORE_IMPORT"):
    pass


def print_str(count_str=100):
    type_info = heap.heap()[0]
    # for i in range(count_str):
    #     print()
    fp_info_type.write("heap()[0].referrers.byvia\n")
    fp_info_type.write(str(type_info.referrers.byvia) + "\n")

    fp_info_type.write("RP\n")
    fp_info_type.write(str(type_info.rp)+"\n")


    fp_info_type.write("SP\n")
    fp_info_type.write(str(type_info.sp)+"\n")

    fp_info_type.flush()

def info_memory():
    heap_info = heap.heap()
    fp_info.write("BYTYPE\n")
    fp_info.write(str(heap_info.bytype)+"\n")

    fp_info.write("BYRCS\n")
    fp_info.write(str(heap_info.byrcs) + "\n")

    fp_info.write("BYMODULE\n")
    fp_info.write(str(heap_info.bymodule) + "\n")

    fp_info.write("BYSIZE\n")
    fp_info.write(str(heap_info.bysize) + "\n")

    fp_info.write("BYVIA\n")
    fp_info.write(str(heap_info.byvia) + "\n")

    fp_info.flush()

# @profile(stream=fp)
# def my_func():
#     a = [1] * (10 ** 6)
#     b = [2] * (2 * 10 ** 7)
#     del b
#     return a

# my_func()

import os
import zipfile
import pytest

from atf import *
from atf.ui import *
from atf.api import JsonRpcClient
from pages_inside import login
from pages_inside.documents.methods import post_delete_docs_by_comment, post_delete_docs_by_id, \
    get_doc_id_by_comment_and_type, wait_document_status_by_comment, delete_docs_by_mask_and_type
from pages_inside.common import SelectFilesDialog
from helpers.downloads import Downloads
from pages_inside.libraries.WHD.Docs.Invoice.Out.dialog import Dialog
from pages_inside.tasks.tasks.functions import post_delete_docs_by_id
from pages_inside.libraries.WHD.Docs.Outflow.dialog import Dialog as RealCard
from pages_inside.saby_pages.outinvoices import Outinvoices
from pages_inside.saby_pages.outgoing import Outgoing
from datetime import datetime
import time
import uuid


with memory_point("AFTER_IMPORT"):
    pass


@profile(stream=fp)
def my_func_import():

    import os
    import zipfile
    import pytest

    from atf.api import JsonRpcClient
    from pages_inside import login
    from pages_inside.documents.methods import post_delete_docs_by_comment, post_delete_docs_by_id, \
        get_doc_id_by_comment_and_type, wait_document_status_by_comment, delete_docs_by_mask_and_type
    from pages_inside.common import SelectFilesDialog
    from helpers.downloads import Downloads
    from pages_inside.libraries.WHD.Docs.Invoice.Out.dialog import Dialog
    from pages_inside.tasks.tasks.functions import post_delete_docs_by_id
    from pages_inside.libraries.WHD.Docs.Outflow.dialog import Dialog as RealCard
    from pages_inside.saby_pages.outinvoices import Outinvoices
    from pages_inside.saby_pages.outgoing import Outgoing
    from datetime import datetime

# my_func_import()

@pytest.mark.ext64
class TestDocumentsExpress(TestCaseUI):
    """Экспресс тестирование документообороста """

    # x = h.heap()
    org2 = Config().get('RECEIVER_NAME')
    org1 = 'Интеграционное Тестирование 1'
    comment = 'DEBUG MEMORY STEPAN '
    client = None
    doc_id = []

    @classmethod
    def setUpClass(cls):
        cls.browser.open(cls.config.get('SITE'))
        cls.browser.maximize_window()
        page = login.LoginPage(cls.driver)
        cls.client = page.login_with_transit(cls.config.get('USER_NAME'), cls.config.get('PASSWORD'),
                                             hide_long_operations=False)
        cls.card = Dialog(cls.driver)
        cls.out_invoices = Outinvoices(cls.driver)

    def setUp(self):
        self.out_invoices.open()

    def tearDown(self):
        self.browser.close_windows_and_alert()
        post_delete_docs_by_id(self.client, [self.doc_id], forever=True)

    @classmethod
    def tearDownClass(cls):
        post_delete_docs_by_comment(cls.comment, client=cls.client)
        client2 = JsonRpcClient(cls.config.get('SITE'))
        client2.auth(cls.config.get('USER_NAME_3'), cls.config.get('PASSWORD_3'))
        post_delete_docs_by_comment(cls.comment, client=client2, out_docs=False)

        # time.sleep(5)
        # with memory_point("tearDownClass"):
        #     a = [i + 500 for i in range(5000)]
        #     b = [str(uuid.uuid4()) for _ in range(1000)]
        #     pass

    # def test_02_save_doc_on_disk(self):
    #     """Тест проверки загрузки сохраненного документа на диск в виде архива """
    #
    #     # x = h.heap()
    #     # log(x.heap())
    #     comment = 'printer_не_удалять!'
    #     ido = get_doc_id_by_comment_and_type(self.client, comment, 'ФактураИсх')
    #     self.out_invoices.open_doc_js(ido)
    #
    #     log('Ищем, открываем документ и выгружаем его в архив')
    #     self.card.check_open()
    #     self.card.attachments.internal_list.check_list_view_file_present("Фактура")
    #     self.card.addressee.addressee_lookup.should_be(Displayed, wait_time=True)
    #     sender = self.card.our_org_lnk.text
    #     receiver = self.card.addressee.get_adresse()
    #     delay(1)
    #     download = Downloads(self.driver)
    #     file_name = download.check_save_files(action=lambda: self.card.service_commands.upload_in_zip(False),
    #                                           wait_time=45)[0]
    #     for texts in ['Фактура', 'printer_не_удалять', '121212', '2012-12-12', '.zip', sender, receiver]:
    #         assert_that(texts, is_in(file_name), f'Неверно сформировано название выгруженного файла - {file_name}')
    #
    #     path_arh = os.path.join(Config().get('DOWNLOAD_DIR'), file_name)
    #     file_list = zipfile.ZipFile(path_arh).namelist()
    #     for doc in ['test1-2.txt', 'test-docx.docx']:  #  'test-docxSGN', 'test1-2SGN'
    #         assert_that(doc, is_in(file_list), "Нет файла %s в скаченном архиве" % doc)
    #     for doc in ['test-docx_SGN_', 'test1-2_SGN_']:
    #         assert_that(any([x for x in file_list if x.startswith(doc)]), is_(True), "Нет файлов подписи в архиве")
    #     assert_that(len(file_list) >= 20, is_(True), "В скаченном архиве должно быть не менее 20 файлов")

    # def test_03_load_documents_ne_format(self):
    #     """Тест загрузки неформатного вложения в документ """
    #
    #     name_file = 'testxps.xps'
    #
    #     log("Создаем фактуру, заполняем поля")
    #     self.out_invoices.create_doc('Фактура')
    #     self.card.check_open()
    #     self.doc_id = self.card.get_doc_id()
    #     log('Грузим неформатное вложение')
    #     # self.card.attachments.add_attachment(self.config.get('FILE_PATH'), name_file)
    #
    #     self.card.attachments.add_attachment(self.config.get('FILE_PATH'), name_file, xxx_plugin=True)


    def test_06_create_realization_from_xml(self):
        """Создание реализации через загрузку форматки в реестре"""

        print("DEBUG")
        log("DEBUG_TEST")

        file_name = 'catren.xml'

        comment = self.comment + datetime.now().strftime('%d%m%y_%H%M%S')
        num = 'ТестикЗагрузкаКатрен'
        delete_docs_by_mask_and_type(self.client, num, 'ДокОтгрИсх', field_name="Номер")

        log('LOG1 Создаем документ из форматного файла')

        with memory_point("Outgoing(self.driver, open=True)"):
            page = Outgoing(self.driver, open=True)

        info_memory()
        print_str()

        # time.sleep(20)
        # page = Outgoing(self.driver, open=True)
        page.add('С компьютера')
        select_file = SelectFilesDialog(self.driver)

        # select_file.load_file_js(self.config.get('FILE_PATH'), file_name)
        select_file.load_file_js_with_plugin(self.config.get('FILE_PATH'), file_name)

        # with memory_point("RealCard(self.driver)"):
        #     card = RealCard(self.driver)
        card = RealCard(self.driver)

        card.check_open()
        self.doc_id = card.get_doc_id()
        card.check_comment('разбор документа')
        card.comment.comment.clear(human=True)
        card.check_our_org(self.config.get('SENDER_NAME'))
        card.check_addressee(self.org2)
        card.check_addressee(self.org2, consignee=True)
        card.check_nom_info("Товар №00618225", {"Кол-во": '5', "Цена": '400.00',
                                                "Сумма": "2 000.00", "ЕдиницыИзмерения": 'шт'})
        card.check_nom_info("Неисключительные права использования",
                            {"Кол-во": '1', "Цена": '430.00', "Сумма": "430.00", "ЕдиницыИзмерения": 'шт'})
        card.set_comment(comment, human=True)

        log('Документ должен уйти спокойно на получателя')
        card.next_phase_click()
        card.skip_error_abt_doc_number()
        card.popup_confirmation.wait_and_close('Продолжить', wait_time=3)
        card.check_close()
        card.tabs.check_error_absence()
        wait_document_status_by_comment(self.client, comment, [3, 4])

        with memory_point("END OF TEST"):
            pass

        with memory_point_unreachable("END OF TEST"):
            pass