import random
import string
import sys
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.risk_limits.buying_power.main_page import MainPage
from test_framework.web_admin_core.pages.risk_limits.buying_power.wizards import *
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T10583(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.institution = self.data_set.get_institution("institution_1")
        self.expected_error = 'Global Margin should be between 0 and 100'
        self.global_margin = ["-1", "101", "100", "-5", "123", "0", "55"]

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_buying_power_page()

    def post_condition(self):
        main_page = MainPage(self.web_driver_container)
        main_page.set_name_filter(self.name)
        time.sleep(1)
        main_page.click_on_more_actions()
        main_page.click_on_delete(True)

    def test_context(self):
        main_page = MainPage(self.web_driver_container)
        values_tab = ValuesTab(self.web_driver_container)
        wizard = MainWizard(self.web_driver_container)
        assignment_tab = AssignmentsTab(self.web_driver_container)
        security_values_tab = SecurityValuesTab(self.web_driver_container)

        try:
            self.precondition()

            main_page.click_on_new_button()
            values_tab.set_name(self.name)
            assignment_tab.set_institution(self.institution)
            self.verify("Global Margin default value = 0", "0", security_values_tab.get_global_margin())

            security_values_tab.set_global_margin(self.global_margin[0])
            wizard.click_on_save_changes()
            time.sleep(0.5)
            self.verify("Negative value of Global Margin", self.expected_error, wizard.get_footer_error_text())

            security_values_tab.set_global_margin(self.global_margin[1])
            wizard.click_on_save_changes()
            time.sleep(0.5)
            self.verify("Global Margin more than 100", self.expected_error, wizard.get_footer_error_text())

            security_values_tab.set_global_margin(self.global_margin[2])
            wizard.click_on_save_changes()
            main_page.set_name_filter(self.name)
            time.sleep(1)
            main_page.click_on_more_actions()
            main_page.click_on_edit()
            self.verify("Global Margin value displayed correct", self.global_margin[2],
                        security_values_tab.get_global_margin())

            security_values_tab.set_global_margin(self.global_margin[3])
            wizard.click_on_save_changes()
            time.sleep(0.5)
            self.verify("Negative value of Global Margin", self.expected_error, wizard.get_footer_error_text())

            security_values_tab.set_global_margin(self.global_margin[4])
            wizard.click_on_save_changes()
            time.sleep(0.5)
            self.verify("Global Margin more than 100", self.expected_error, wizard.get_footer_error_text())

            security_values_tab.set_global_margin(self.global_margin[5])
            wizard.click_on_save_changes()
            main_page.set_name_filter(self.name)
            time.sleep(1)
            main_page.click_on_more_actions()
            main_page.click_on_edit()
            self.verify("Global Margin value displayed correct", self.global_margin[5],
                        security_values_tab.get_global_margin())

            security_values_tab.set_global_margin(self.global_margin[6])
            wizard.click_on_save_changes()
            main_page.set_name_filter(self.name)
            time.sleep(1)
            main_page.click_on_more_actions()
            main_page.click_on_edit()
            self.verify("Global Margin value displayed correct", self.global_margin[6],
                        security_values_tab.get_global_margin())

            wizard.click_on_save_changes()

            self.post_condition()

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
