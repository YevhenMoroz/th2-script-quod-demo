import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_cases.web_admin.web_admin_core.pages.login.login_page import LoginPage
from test_cases.web_admin.web_admin_core.pages.middle_office.commissions.commissions_dimensions_sub_wizard import \
    CommissionsDimensionsSubWizard
from test_cases.web_admin.web_admin_core.pages.middle_office.commissions.commissions_page import CommissionsPage
from test_cases.web_admin.web_admin_core.pages.middle_office.commissions.commissions_values_sub_wizard import \
    CommissionsValuesSubWizard
from test_cases.web_admin.web_admin_core.pages.middle_office.commissions.commissions_wizard import CommissionsWizard
from test_cases.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_5665(CommonTestCase):

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
        self.client = 'CLIENT1'
        self.commission_amount_type = 'Broker'
        self.commission_profile = 'UK Levy'
        self.client_list = "test"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_commissions_page()
        main_page = CommissionsPage(self.web_driver_container)
        dimensions_tab = CommissionsDimensionsSubWizard(self.web_driver_container)
        values_tab = CommissionsValuesSubWizard(self.web_driver_container)
        main_page.click_on_new()
        time.sleep(1)
        dimensions_tab.set_instr_type(self.instr_type)
        dimensions_tab.set_venue(self.venue)
        dimensions_tab.set_side(self.side)
        dimensions_tab.set_execution_policy(self.execution_policy)
        dimensions_tab.set_client(self.client)
        dimensions_tab.set_commission_amount_type(self.commission_amount_type)
        dimensions_tab.set_commission_profile(self.commission_profile)
        dimensions_tab.set_client_list(self.client_list)
        values_tab.set_name(self.name)
        values_tab.set_description(self.description)
        wizard = CommissionsWizard(self.web_driver_container)
        time.sleep(2)
        wizard.click_on_save_changes()
        time.sleep(2)

    def test_context(self):

        try:
            self.precondition()
            dimensions_tab = CommissionsDimensionsSubWizard(self.web_driver_container)
            wizard = CommissionsWizard(self.web_driver_container)
            main_page = CommissionsPage(self.web_driver_container)
            main_page.set_name(self.name)
            time.sleep(2)
            main_page.click_on_more_actions()
            time.sleep(2)
            main_page.click_on_edit()
            time.sleep(2)
            dimensions_tab.clear_client_list_field()
            time.sleep(2)
            wizard.click_on_save_changes()
            time.sleep(2)
            main_page.set_name(self.name)
            time.sleep(2)
            main_page.click_on_more_actions()
            time.sleep(2)
            main_page.click_on_edit()
            time.sleep(4)
            self.verify("Is client list remove", True, dimensions_tab.is_client_list_contains_text())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
