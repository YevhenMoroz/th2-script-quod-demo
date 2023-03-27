import sys
import time
import traceback
import random
import string
from custom import basic_custom_actions
from stubs import ROOT_DIR
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase
from test_framework.web_trading.web_trading_core.pages.login_and_logout.login_and_logout_page import LoginPage
from test_framework.web_trading.web_trading_core.pages.main_page.main_page import MainPage
from test_framework.web_trading.web_trading_core.pages.main_page.menu.menu_page import MenuPage
from test_framework.web_trading.web_trading_core.pages.main_page.menu.profile.profile_page import ProfilePage
from test_framework.web_trading.web_trading_core.pages.main_page.menu.profile.profile_security_sub_wizard import \
    ProfileSecuritySubWizard


class QAP_T3487(CommonTestCase):
    PATH_TO_TEMPORARY_PASSWORD_RESET_FILE = f'{ROOT_DIR}\\test_cases\\web_trading\\resources\\temporary_password_reset_QAP_6296.txt'

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_12")
        self.password = self.data_set.get_password("password_5")
        self.password_for_reset = str
        self.new_password = '!new1234' + ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.set_login(self.login)
        # this give us ability to enter first time with right password
        try:
            login_page.set_password(self.password)
        except Exception:
            login_page.set_password(login_page.get_password_from_file(self.PATH_TO_TEMPORARY_PASSWORD_RESET_FILE))
        login_page.click_login_button()
        main_page = MainPage(self.web_driver_container)
        main_page.click_on_menu_button()
        menu_page = MenuPage(self.web_driver_container)
        menu_page.click_on_profile_button()
        time.sleep(1)
        profile_page = ProfilePage(self.web_driver_container)
        profile_page.click_on_security_button()
        time.sleep(2)
        security_sub_wizard = ProfileSecuritySubWizard(self.web_driver_container)
        # get actual password from file
        self.password_for_reset = login_page.get_password_from_file(self.PATH_TO_TEMPORARY_PASSWORD_RESET_FILE)
        security_sub_wizard.set_old_password(self.password_for_reset)
        time.sleep(2)
        security_sub_wizard.set_new_password(self.new_password)
        # write new generated password in file for future use
        login_page.write_new_password_if_file(self.PATH_TO_TEMPORARY_PASSWORD_RESET_FILE, self.new_password)
        security_sub_wizard.set_confirm_password(self.new_password)
        time.sleep(4)
        profile_page.click_on_save_button()
        time.sleep(2)
        profile_page.click_on_close_button()
        main_page.click_on_menu_button()
        time.sleep(2)
        menu_page.click_on_logout_button()
        time.sleep(2)
        menu_page.click_on_yes_button()
        time.sleep(2)
        login_page.set_login(self.login)
        login_page.set_password(self.new_password)
        login_page.click_login_button()
        time.sleep(2)

    def test_context(self):
        try:
            self.precondition()
            main_page = MainPage(self.web_driver_container)
            user_name = main_page.get_username()
            self.verify("Is login_and_logout successful? ", self.login.upper(), user_name.upper())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
