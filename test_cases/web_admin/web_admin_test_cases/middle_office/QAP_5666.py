import random
import string
import time
import traceback

from custom import basic_custom_actions
from test_cases.web_admin.web_admin_core.pages.login.login_page import LoginPage
from test_cases.web_admin.web_admin_core.pages.middle_office.commissions.commissions_page import CommissionsPage
from test_cases.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_5666(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm03"
        self.password = "adm03"
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.description = "description"
        self.instr_type = 'Bond'
        self.venue = 'EURONEXT AMSTERDAM'
        self.side = 'Buy'
        self.execution_policy = 'Care'
        self.virtual_account = "test"
        self.client = 'CLIENT1'
        self.client_group = "test"
        self.commission_amount_type = 'Broker'
        self.commission_profile = '1bps'
        self.client_list = "test"
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
            try:
                main_page.set_name(self.name)
                main_page.set_description(self.description)
                time.sleep(1)
                main_page.set_instr_type(self.instr_type)
                time.sleep(1)
                main_page.set_venue(self.venue)
                time.sleep(1)
                main_page.set_side(self.side)
                time.sleep(1)
                main_page.set_execution_policy(self.execution_policy)
                time.sleep(1)
                main_page.set_virtual_account(self.virtual_account)
                time.sleep(1)
                main_page.set_client(self.client)
                time.sleep(1)
                main_page.offset_horizontal_slide()
                time.sleep(1)
                main_page.offset_horizontal_slide()
                time.sleep(1)
                main_page.offset_horizontal_slide()
                time.sleep(1)
                main_page.set_client_group(self.client_group)
                time.sleep(1)
                main_page.set_client_list(self.client_list)
                time.sleep(2)
                main_page.set_commission_amount_type(self.commission_amount_type)
                time.sleep(1)
                main_page.set_commission_profile(self.commission_profile)
                time.sleep(1)
                main_page.click_on_re_calculate_for_allocations()
                self.verify("All columns preloaded", True, True)
            except Exception as e:
                self.verify("Some headers in main page work incorrectly", True, e.__class__.__name__)
        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
