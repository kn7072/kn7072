# -*- coding: utf-8 -*-
import atf
from atf.helper import wait
from atf.helper import performance
import unittest
import time
from pages.test_online.login import LoginPage
from pages.test_online.main import MainPage
import pages.test_online.registrationOnline as RegistrationPage
import pages.test_online.registrationOnline.functions as RegistrationFunctions
import random
from atf.email import EmailIMAP4

class TestPagesPerfomance(atf.ATFSuite):
    """Данный набор тестов предназначен для тестирования времени"""

    def setUp(self):
        atf.ATFSuite.setUp(self)
        self.browser.open(self.config.SITE)

    @performance("CertificateAuthentication", 10)
    def test_certificate_authentication(self):
        """Авторизация по сертификату"""
        self.browser.open(self.config.SITE + '/auth')
        loginOnline = LoginPage(self)
        wait(lambda: loginOnline.login_btn.is_present)
        atf.helper.start(self)
        loginOnline.sert_link.click()
        cert_dialog = RegistrationPage.index.ChoseCertificateDialog(self)
        if wait(lambda: cert_dialog.chose_cert_tbl.is_present):
            cert_dialog.chose_cert_tbl.cell(contains_text = "Зарегистрированный Клиент Клиентович").click()
        mainOnline = MainPage(self)
        self.assertTrue(wait(lambda: mainOnline.org_table.is_present),
                        "---Ошибка! Нет таблицы Нашей организации")
        atf.helper.finish(self)

    @performance("LoginAuthentication", 10)
    def test_login_authentication(self):
        """Авторизация по логину паролю"""
        self.browser.open(self.config.SITE + '/auth')
        loginOnline = LoginPage(self)
        wait(lambda: loginOnline.login_btn.is_present)
        atf.helper.start(self)
        loginOnline.login_as("Зарегистрированный Клиент", "Тест123")
        mainOnline = MainPage(self)
        self.assertTrue(wait(lambda: mainOnline.org_table.is_present),
                        "---Ошибка! Нет таблицы Нашей организации")
        atf.helper.finish(self)

    @performance("RegisterWithoutCertificate", 5)
    def test_register_without_certificate(self):
        """Свободная регистрация без сертификата"""
        inn = atf.datageneration.inngen10(random.randint(1111111111,9999999999))
        inn = str(inn)
        kpp = '999999999'
        name = 'ООО ' + str(inn)
        self.browser.open(self.config.SITE + '/reg/reg.html')
        reg = RegistrationPage.index.ReghtmlPage(self)
        wait(lambda : reg.regTemplate_btn.is_present)
        reg.inn_txt.type_in(inn)
        reg.kpp_txt.type_in(kpp)
        reg.name_txt.type_in(name)
        reg.email_txt.type_in(self.config.EMAIL_USER)
        reg.regTemplate_btn.click()
        sentInvitation = RegistrationPage.index.SentInvitationPage(self)
        wait(lambda: sentInvitation.send_btn.is_present)
        time.sleep(20)
        email = EmailIMAP4()
        data = email.get_data_letter()
        url_post = RegistrationPage.functions.get_link(self, data[4])
        self.browser.open(url_post)
        registration = RegistrationPage.index.RegistrationPage(self)
        self.assertTrue(wait(lambda: registration.add_client_btn.is_present),
                        "---Ошибка! Нет кнопки Зарегистрировать")
        atf.helper.start(self)
        registration = RegistrationPage.index.RegistrationPage(self)
        registration.registration_as(name, 'Тест123', 'Тест123')
        mainOnline = MainPage(self)
        self.assertTrue(wait(lambda: mainOnline.org_table.is_present),
                        "---Ошибка! Нет таблицы Нашей организации")
        atf.helper.finish(self)
        RegistrationFunctions.Clear_DB(self, inn, kpp)

    @performance("RegisterWithCertificate", 5)
    def test_register_with_certificate(self):
        """Свободная регистрация по сертификату"""
        name = 'Тестова Любовь Анатольевна'
        RegistrationFunctions.Clear_DB(self, '661200265924', None, 'F7586CA02C80E68B37A84557EBA92980D8079421')
        time.sleep(120)
        self.browser.open(self.config.SITE + '/reg/Invitation.html?is_free=true')
        searchCertificatePage = RegistrationPage.index.SearchCertificatePage(self)
        atf.helper.start(self)
        cert_dialog = RegistrationPage.index.ChoseCertificateDialog(self)
        self.assertTrue(wait(lambda : cert_dialog.chose_cert_tbl.is_present),
                        "---Ошибка! Нет таблицы Выбора сертификатов")
        cert_dialog.chose_cert_tbl.cell( contains_text = name).click()
        self.assertTrue(wait(lambda: not searchCertificatePage.found_cert_dlg.is_present),
                        "---Ошибка! Электронная подпись уже зарегистрирована в системе. Скорее всего организация уже зарегистрирована. Не удалилась схема")
        registration = RegistrationPage.index.RegistrationPage(self)
        self.assertTrue(wait(lambda: registration.add_client_btn.is_present),
                        "---Ошибка! Нет кнопки Зарегистрироваться")
        txt = atf.datageneration.inngen10(random.randint(11111,99999))
        name_login = name + str(txt)
        registration.registration_as_with_cert(name_login, 'Тест123', 'Тест123')
        mainOnline = MainPage(self)
        self.assertTrue(wait(lambda: mainOnline.org_table.is_present),
                        "---Ошибка! Нет таблицы Нашей организации")
        atf.helper.finish(self)

if __name__ == '__main__':
    unittest.main(testRunner=atf.XMLTestRunner(output='test-reports'))