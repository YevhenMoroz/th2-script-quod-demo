import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.middle_office.commissions.commissions_page import CommissionsPage
from test_framework.web_admin_core.pages.middle_office.commissions.commissions_wizard import CommissionsWizard
from test_framework.web_admin_core.pages.middle_office.commissions.commissions_values_sub_wizard \
    import CommissionsValuesSubWizard
from test_framework.web_admin_core.pages.middle_office.commissions.commissions_dimensions_sub_wizard \
    import CommissionsDimensionsSubWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3847(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.new_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.description = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.venue_list = ''
        self.instr_type = ''
        self.venue = ''
        self.side = ''
        self.client = ''
        self.commission_amount_type = ''
        self.commission_profile = ''

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_commissions_page()
        time.sleep(1)
        commission_page = CommissionsPage(self.web_driver_container)
        commission_page.click_on_new()
        time.sleep(3)
        commission_wizard_value_tab = CommissionsValuesSubWizard(self.web_driver_container)
        commission_wizard_value_tab.set_name(self.name)
        commission_wizard_value_tab.set_description(self.description)
        commission_wizard_value_tab.click_on_re_calculate_for_allocations()
        time.sleep(2)
        commission_wizard_dimensions_tab = CommissionsDimensionsSubWizard(self.web_driver_container)
        self.venue_list = random.choice(commission_wizard_dimensions_tab.get_all_venue_list_from_drop_menu())
        commission_wizard_dimensions_tab.set_venue_list(self.venue_list)
        self.instr_type = random.choice(commission_wizard_dimensions_tab.get_all_instr_types_from_drop_menu())
        commission_wizard_dimensions_tab.set_instr_type(self.instr_type)
        self.side = random.choice(commission_wizard_dimensions_tab.get_all_side_from_drop_menu())
        commission_wizard_dimensions_tab.set_side(self.side)
        self.execution_policy = random.choice(commission_wizard_dimensions_tab.get_all_execution_policy_from_drop_menu())
        commission_wizard_dimensions_tab.set_execution_policy(self.execution_policy)
        self.client = random.choice(commission_wizard_dimensions_tab.get_all_client_from_drop_menu())
        commission_wizard_dimensions_tab.set_client(self.client)
        self.commission_amount_type = random.choice(
            commission_wizard_value_tab.get_all_commission_amount_type_from_drop_menu())
        commission_wizard_value_tab.set_commission_amount_type(self.commission_amount_type)
        self.commission_profile = random.choice(
            commission_wizard_value_tab.get_all_commission_profile_from_drop_menu())
        commission_wizard_value_tab.set_commission_profile(self.commission_profile)
        commission_wizard = CommissionsWizard(self.web_driver_container)
        commission_wizard.click_on_save_changes()

    def test_context(self):

        try:
            self.precondition()
            commission_page = CommissionsPage(self.web_driver_container)
            commission_page.set_name(self.name)
            time.sleep(1)
            commission_page.click_on_more_actions()
            time.sleep(1)
            commission_page.click_on_clone()
            time.sleep(2)

            actual_result = [self.name,
                             self.description,
                             True,
                             self.venue_list,
                             self.instr_type,
                             self.side,
                             self.client,
                             self.commission_amount_type,
                             self.commission_profile]

            commission_wizard_value_tab = CommissionsValuesSubWizard(self.web_driver_container)
            commission_wizard_dimensions_tab = CommissionsDimensionsSubWizard(self.web_driver_container)

            excepted_result = [commission_wizard_value_tab.get_name(),
                               commission_wizard_value_tab.get_description(),
                               commission_wizard_value_tab.is_re_calculate_for_allocations_selected(),
                               commission_wizard_dimensions_tab.get_venue_list(),
                               commission_wizard_dimensions_tab.get_instr_type(),
                               commission_wizard_dimensions_tab.get_side(),
                               commission_wizard_dimensions_tab.get_client(),
                               commission_wizard_value_tab.get_commission_amount_type(),
                               commission_wizard_value_tab.get_commission_profile()]

            self.verify("Cloned entity contains all data", actual_result, excepted_result)

            commission_wizard_value_tab.set_name(self.new_name)
            commission_wizard = CommissionsWizard(self.web_driver_container)
            commission_wizard.click_on_save_changes()
            time.sleep(2)
            commission_page.set_name(self.new_name)
            time.sleep(1)
            commission_page.click_on_more_actions()
            time.sleep(1)

            actual_result_after_change_name = [self.new_name,
                                               self.description,
                                               "true",
                                               self.venue_list,
                                               self.instr_type,
                                               self.side,
                                               self.client,
                                               self.commission_amount_type,
                                               self.commission_profile]

            time.sleep(2)
            excepted_result_after_change_name = commission_page.click_download_pdf_entity_button_and_check_pdf(
                actual_result_after_change_name)
            time.sleep(1)
            self.verify("Is PDF contains all data", True, excepted_result_after_change_name)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
