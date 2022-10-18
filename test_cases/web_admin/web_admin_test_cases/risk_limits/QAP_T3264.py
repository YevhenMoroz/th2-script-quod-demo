import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.general.common.common_page import CommonPage
from test_framework.web_admin_core.pages.risk_limits.risk_limit_dimensions.main_page import MainPage
from test_framework.web_admin_core.pages.risk_limits.risk_limit_dimensions.wizards import DimensionsTab
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3264(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.users_dimensions = ["Users", "Desks"]
        self.actions = ["Select All", "De-Select All"]

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)

    def test_context(self):
        try:
            self.precondition()

            side_menu = SideMenu(self.web_driver_container)
            side_menu.open_risk_limit_dimension_page()
            time.sleep(2)
            main_page = MainPage(self.web_driver_container)
            main_page.click_on_new_button()
            time.sleep(2)
            dimensions_tab = DimensionsTab(self.web_driver_container)
            dimensions_tab.set_users_dimension(self.users_dimensions[0])
            dimensions_tab.set_user([self.actions[0]])
            time.sleep(2)
            selected_accounts = dimensions_tab.get_user().split(",")
            time.sleep(2)
            excepted_result = dimensions_tab.get_all_user_from_drop_menu()

            self.verify("All Users has been selected", len(excepted_result) - 2, len(selected_accounts))

            dimensions_tab.set_user([self.actions[1]])
            time.sleep(2)
            selected_accounts = dimensions_tab.get_user().split(",")
            time.sleep(2)

            self.verify("All Users has been deselected", True, 1 == len(selected_accounts))

            dimensions_tab.set_users_dimension(self.users_dimensions[1])
            dimensions_tab.set_desks([self.actions[0]])
            time.sleep(2)
            selected_accounts = dimensions_tab.get_desks().split(",")
            time.sleep(2)
            excepted_result = dimensions_tab.get_all_desks_from_drop_menu()

            self.verify("All Desks has been selected", len(excepted_result) - 2, len(selected_accounts))

            dimensions_tab.set_desks([self.actions[1]])
            time.sleep(2)
            selected_accounts = dimensions_tab.get_desks().split(",")
            time.sleep(2)

            self.verify("All Desks has been deselected", True, 1 == len(selected_accounts))

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
