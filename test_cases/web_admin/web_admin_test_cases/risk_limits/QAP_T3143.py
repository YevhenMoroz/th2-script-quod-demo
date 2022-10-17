import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.risk_limits.risk_limit_dimensions.main_page import MainPage
from test_framework.web_admin_core.pages.risk_limits.risk_limit_dimensions.wizards import DimensionsTab
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3143(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_risk_limit_dimension_page()
        time.sleep(2)

    def test_context(self):
        try:
            self.precondition()

            main_page = MainPage(self.web_driver_container)
            main_page.click_on_new_button()
            time.sleep(2)
            dimensions_tab = DimensionsTab(self.web_driver_container)

            self.verify(
                "Reference Data Dimensions contains fields: Position Type, Position Validity, Settlement Period",
                [True, True, True],
                [dimensions_tab.is_position_type_field_displayed(),
                 dimensions_tab.is_position_validity_field_displayed(),
                 dimensions_tab.is_settlement_period_field_displayed()])

            actual_result = dimensions_tab.get_all_position_type_from_drop_menu()

            self.verify("Position Type contains the options: Long, Short, Net",
                        sorted(["Long", "Short", "Net"]), sorted(actual_result))

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
