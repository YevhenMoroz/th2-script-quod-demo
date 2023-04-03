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


class QAP_T10586(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_14")
        self.password = self.data_set.get_password("password_14")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))

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

        try:
            self.precondition()

            main_page.click_on_new_button()
            values_tab.set_name(self.name)
            self.verify("Institution field disabled", False, assignment_tab.is_institution_field_enable())
            wizard.click_on_save_changes()
            main_page.set_name_filter(self.name)
            time.sleep(1)
            main_page.click_on_more_actions()
            main_page.click_on_edit()
            self.verify("Institution field disabled", False, assignment_tab.is_institution_field_enable())
            wizard.click_on_save_changes()

            self.post_condition()

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
