import sys
import time
import traceback
import random
import string

import txt as txt

from custom import basic_custom_actions
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase
from test_framework.web_trading.web_trading_core.pages.login.login_page import LoginPage
from test_framework.web_trading.web_trading_core.pages.main_page.main_page import MainPage
from test_framework.web_trading.web_trading_core.pages.main_page.menu.menu_page import MenuPage
from test_framework.web_trading.web_trading_core.pages.main_page.menu.profile.profile_page import ProfilePage
from test_framework.web_trading.web_trading_core.pages.main_page.menu.profile.profile_security_sub_wizard import ProfileSecuritySubWizard
from test_cases.web_trading.test_cases.pages.login import temporary_password_reset

#TODO: create logic for password reset , add txt file + parse method for that.
#DOUBLE CHECK
class QAP_6296(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm02"
        self.password = self.getPasswordFromFile("temporary_password_reset.txt")

        # self.old_password = 'Qa4%Qa4%'
        # self.new_password = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        # self.confirm_password = self.new_password

        # TODO:
        # 1. password
        # 2. file --> temporary..txt
        # 3. 2 methods --> : 1 ParseFromfile 2WriteInFile
        # 4. Step :
        #     - password = ParseFromFile(temporary..txt) -- считает твой актуальный старый пароль (и он будет циклически перезаписыватся в этот файл при каждом запуске теста)
        #     - set_old_passrowd(password)
        #     - password = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        #     - WriteInFile(temporary..txt,password) , в итоге old pass changed to new password and eventually new password is your actual old password in next start test case
        #

    def getPasswordFromFile(self, file1):
        with open(file1, "r") as file:
            password = file.readline()
            return password

    def setPasswordToFile(self, file1, password):
        with open(file1, "w") as file:
            file.write(password)


    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.set_login(self.login)
        login_page.set_password(self.password)
        login_page.click_login_button()
        main_page = MainPage(self.web_driver_container)
        main_page.click_on_menu_button()
        menu_page = MenuPage(self.web_driver_container)
        menu_page.click_on_profile_button()
        time.sleep(1)
        profile_page = ProfilePage(self.web_driver_container)
        profile_page.click_on_security_button()
        security_sub_wizard = ProfileSecuritySubWizard(self.web_driver_container)
        security_sub_wizard.set_old_password(self.password)

        new_password = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.setPasswordToFile("temporary_password_reset.txt", new_password)

        security_sub_wizard.set_new_password(new_password)
        security_sub_wizard.set_confirm_password(new_password)
        profile_page.click_on_save_button()
        profile_page.click_on_close_button()
        main_page.click_on_menu_button()
        menu_page.click_on_logout_button()
        menu_page.click_on_yes_button()
        login_page.set_login(self.login)
        login_page.set_password(new_password)
        login_page.click_login_button()
        time.sleep(2)

    def test_context(self):
        try:
            self.precondition()
            main_page = MainPage(self.web_driver_container)
            user_name = main_page.get_username()
            self.verify("Is login successful? ", self.login.upper(), user_name.upper())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)