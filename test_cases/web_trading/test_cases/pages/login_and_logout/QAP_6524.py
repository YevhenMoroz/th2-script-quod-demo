import sys
import time
import traceback
from custom import basic_custom_actions
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase
from test_framework.web_trading.web_trading_core.pages.login_and_logout.login_and_logout_page import LoginPage
from test_framework.web_trading.web_trading_core.pages.main_page.main_page import MainPage
from test_framework.web_trading.web_trading_core.pages.main_page.menu.menu_page import MenuPage
from test_framework.web_trading.web_trading_core.pages.main_page.menu.profile.profile_page import ProfilePage
from test_framework.web_trading.web_trading_core.pages.main_page.menu.profile.profile_security_sub_wizard import \
    ProfileSecuritySubWizard


class QAP_6524(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.set_login(self.login)
        # this give us ability to enter first time with right password
        login_page.set_password(self.password)
        login_page.click_login_button()
        main_page = MainPage(self.web_driver_container)
        main_page.click_on_menu_button()
        menu_page = MenuPage(self.web_driver_container)
        menu_page.click_on_profile_button()
        time.sleep(1)
        profile_page = ProfilePage(self.web_driver_container)
        profile_page.click_on_security_button()
        time.sleep(2)

    def test_context(self):
        try:
            self.precondition()
            try:
                security_sub_wizard = ProfileSecuritySubWizard(self.web_driver_container)
                # Xpath for these passwords fields set with @type="password", that give us True in search and confirm
                security_sub_wizard.set_old_password(self.password)
                time.sleep(2)
                security_sub_wizard.set_new_password(self.password)
                time.sleep(2)
                security_sub_wizard.set_confirm_password(self.password)
                time.sleep(2)
                self.verify("Is passwords fields hidden", True, True)
            except Exception:
                self.verify("Is passwords fields hidden", True,
                            "Passwords fields not hidden or contain incorrect xPath")

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
