import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase
from test_framework.web_admin_core.pages.market_making.client_tier.client_tiers_page import ClientTiersPage
from test_framework.web_admin_core.pages.general.common.common_page import CommonPage


class QAP_T9113(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.white_theme = 'rgba(34, 43, 69, 1)'
        self.dark_theme = 'rgba(255, 255, 255, 1)'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_client_tier_page()

    def test_context(self):
        try:
            self.precondition()

            main_page = ClientTiersPage(self.web_driver_container)
            expected_result = [True, True]
            actual_result = [self.white_theme == main_page.get_executable_text_color(),
                             self.white_theme == main_page.get_pricing_text_color()]
            self.verify("Text color for white theme is OK", expected_result, actual_result)

            common_act = CommonPage(self.web_driver_container)
            common_act.click_on_user_icon()
            common_act.click_on_dark_theme()
            time.sleep(1)
            expected_result = [True, True]
            actual_result = [self.dark_theme == main_page.get_executable_text_color(),
                             self.dark_theme == main_page.get_pricing_text_color()]
            self.verify("Text color for dark theme is OK", expected_result, actual_result)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
