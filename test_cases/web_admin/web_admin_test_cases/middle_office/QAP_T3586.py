import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.middle_office.commissions.commissions_page import CommissionsPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3586(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.description = "description"
        self.instr_type = self.data_set.get_instr_type("instr_type_1")
        self.venue = self.data_set.get_venue_by_name("venue_9")
        self.side = 'Buy'
        self.execution_policy = self.data_set.get_exec_policy("exec_policy_1")
        self.virtual_account = "test"
        self.client = self.data_set.get_client("client_1")
        self.client_group = self.data_set.get_client_group("client_group_3")
        self.commission_amount_type = self.data_set.get_commission_amount_type("commission_amount_type_1")
        self.commission_profile = '1bps'
        self.client_list = self.data_set.get_client_list("client_list_2")
        self.re_calculate_for_allocations = 'true'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_commissions_page()

    def test_context(self):

        try:
            self.precondition()
            main_page = CommissionsPage(self.web_driver_container)
            #try:
            main_page.set_name(self.name)
            main_page.set_description(self.description)
            main_page.set_commission_amount_type(self.commission_amount_type)
            main_page.set_commission_profile(self.commission_profile)
            main_page.set_instr_type(self.instr_type)
            main_page.set_venue(self.venue)
            main_page.set_side(self.side)
            main_page.set_execution_policy(self.execution_policy)
            main_page.set_virtual_account(self.virtual_account)
            main_page.set_client(self.client)
            main_page.set_client_group(self.client_group)
            main_page.set_client_list(self.client_list)
            main_page.click_on_re_calculate_for_allocations()
            self.verify("All columns preloaded", True, True)
            #except Exception as e:
            #    self.verify("Some headers in main page work incorrectly", True, e.__class__.__name__)
        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
