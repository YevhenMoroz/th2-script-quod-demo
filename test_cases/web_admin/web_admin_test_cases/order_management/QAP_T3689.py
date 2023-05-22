import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.order_management.order_management_rules.main_page import MainPage
from test_framework.web_admin_core.pages.order_management.order_management_rules.wizard import *
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3689(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.action = 'Reject'
        self.split = '110'
        self.error_message = 'Total percentage is greater than 100'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.click_on_order_management_rules_tab()

    def test_context(self):
        wizard = MainWizard(self.web_driver_container)
        main_page = MainPage(self.web_driver_container)
        condition_tab = ConditionsTab(self.web_driver_container)

        try:
            self.precondition()

            main_page.click_on_new_button()
            condition_tab.click_on_plus_button()
            condition_tab.click_on_plus_button_at_result()
            condition_tab.set_action(self.action)
            condition_tab.set_split(self.split)
            condition_tab.click_on_save_checkmark_at_result()
            time.sleep(1)
            self.verify("Error message displayed", self.error_message, wizard.get_footer_error_text())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
