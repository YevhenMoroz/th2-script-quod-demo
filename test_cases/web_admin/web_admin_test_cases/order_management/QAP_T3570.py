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


class QAP_T3570(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.action = ['SendDirect', 'SendCare']
        self.split = '10'
        self.venue = ['A2X', 'BINANCE']

    def add_new_result(self, action, split, venue=None):
        default_result_entity = DefaultResultEntity(self.web_driver_container)

        default_result_entity.click_on_plus_button_at_result()
        default_result_entity.set_action(action)
        default_result_entity.set_split(split)
        if venue is None:
            pass
        else:
            default_result_entity.set_venue(venue)
        default_result_entity.click_on_save_checkmark_at_result()

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.click_on_order_management_rules_tab()
        page = MainPage(self.web_driver_container)
        page.click_on_new_button()

    def test_context(self):
        wizard = MainWizard(self.web_driver_container)
        default_result_entity = DefaultResultEntity(self.web_driver_container)

        try:
            self.precondition()

            default_result_entity.click_on_edit_button()
            self.add_new_result(self.action[0], self.split, self.venue[0])
            self.add_new_result(self.action[0], self.split, self.venue[0])
            time.sleep(1)
            expected_result = 'Such a record already exists'
            self.verify(f"{expected_result} - warning appears", expected_result, wizard.get_footer_error_text())

            default_result_entity.set_venue(self.venue[1])
            default_result_entity.click_on_save_checkmark_at_result()

            self.add_new_result(self.action[1], self.split)
            self.add_new_result(self.action[1], self.split)
            time.sleep(1)
            expected_result = 'Use Send Care only one time'
            self.verify(f"{expected_result} - warning appears", expected_result, wizard.get_footer_error_text())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier without name",
                                              self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
