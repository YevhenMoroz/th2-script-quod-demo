import sys
import time
import traceback
from custom import basic_custom_actions
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase
from test_framework.web_trading.web_trading_core.pages.login.login_page import LoginPage
from test_framework.web_trading.web_trading_core.pages.main_page.main_page import MainPage
from test_framework.web_trading.web_trading_core.pages.main_page.menu.menu_page import MenuPage
from test_framework.web_trading.web_trading_core.pages.main_page.menu.profile.profile_page import ProfilePage
from test_framework.web_trading.web_trading_core.pages.main_page.menu.profile.profile_preference_sub_wizard import \
    ProfilePreferenceSubWizard


class QAP_6287(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "web_trading_test3"
        self.password = "Web3_trading_test"
        self.client = "POOJA"

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

    def test_context(self):
        try:
            self.precondition()
            profile_page = ProfilePage(self.web_driver_container)
            profile_page.click_on_preference_button()
            time.sleep(2)
            profile_preference_sub_wizard = ProfilePreferenceSubWizard(self.web_driver_container)
            try:
                profile_preference_sub_wizard.set_default_client_from_dropdown_list(self.client)
                self.verify("Is default client set correctly from dropdown list", True, True)
            except Exception as e:
                self.verify("Is default client set correctly from dropdown list", True,
                            e.__class__.__name__ + "Check client name or selector in F12")

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
