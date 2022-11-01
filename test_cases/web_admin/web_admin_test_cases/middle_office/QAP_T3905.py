import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.middle_office.commissions.commissions_dimensions_sub_wizard import \
    CommissionsDimensionsSubWizard
from test_framework.web_admin_core.pages.middle_office.commissions.commissions_page import CommissionsPage
from test_framework.web_admin_core.pages.middle_office.commissions.commissions_values_sub_wizard import \
    CommissionsValuesSubWizard
from test_framework.web_admin_core.pages.middle_office.commissions.commissions_wizard import CommissionsWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3905(CommonTestCase):

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
        self.client = self.data_set.get_client("client_1")
        self.commission_amount_type = self.data_set.get_commission_amount_type("commission_amount_type_1")
        self.commission_profile = self.data_set.get_comm_profile_by_name("commission_profile_1")

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
        values_tab.set_commission_amount_type(self.commission_amount_type)
        values_tab.set_commission_profile(self.commission_profile)
        values_tab.set_name(self.name)
        values_tab.set_description(self.description)

    def test_context(self):

        try:
            self.precondition()
            wizard = CommissionsWizard(self.web_driver_container)
            main_page = CommissionsPage(self.web_driver_container)
            expected_pdf_result = [self.name,
                                   self.description,
                                   self.instr_type,
                                   self.venue,
                                   self.side,
                                   self.execution_policy,
                                   self.client,
                                   self.commission_amount_type,
                                   self.commission_profile]
            self.verify("Is pdf contains correctly values", True,
                        wizard.click_download_pdf_entity_button_and_check_pdf(expected_pdf_result))

            wizard.click_on_save_changes()
            time.sleep(2)
            try:
                main_page.set_name(self.name)
                time.sleep(2)
                main_page.click_on_more_actions()
                self.verify("Entity saved correctly", True, True)
            except Exception as e:
                self.verify("Entity did not save !!!Error!!!", True, e.__class__.__name__)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
