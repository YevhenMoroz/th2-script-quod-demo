import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.middle_office.commissions.commissions_commision_profiles_sub_wizard import \
    CommissionsCommissionProfilesSubWizard
from test_framework.web_admin_core.pages.middle_office.commissions.commissions_commission_profile_points_sub_wizard import \
    CommissionsCommissionProfilePointsSubWizard
from test_framework.web_admin_core.pages.middle_office.commissions.commissions_page import CommissionsPage
from test_framework.web_admin_core.pages.middle_office.commissions.commissions_values_sub_wizard import \
    CommissionsValuesSubWizard
from test_framework.web_admin_core.pages.middle_office.commissions.commissions_wizard import CommissionsWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3826(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.commission_amount_type = self.data_set.get_commission_amount_type("commission_amount_type_1")
        self.commission_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.commission_profile_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.comm_xunit = "Amount"
        self.comm_type = self.data_set.get_comm_type("comm_type_1")
        self.comm_algorithm = self.data_set.get_comm_algorithm("comm_algorithm_1")
        self.base_value = "144"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_commissions_page()
        main_page = CommissionsPage(self.web_driver_container)
        main_page.click_on_new()
        values_tab = CommissionsValuesSubWizard(self.web_driver_container)
        values_tab.set_commission_amount_type(self.commission_amount_type)
        values_tab.set_name(self.commission_name)
        values_tab.click_on_manage_commission_profile()
        commissions_profiles = CommissionsCommissionProfilesSubWizard(self.web_driver_container)
        commissions_profiles.click_on_edit()
        commissions_profiles.set_commission_profile_name(self.commission_profile_name)
        commissions_profiles.set_comm_type(self.comm_type)
        commissions_profiles.set_comm_xunit(self.comm_xunit)
        commissions_profiles.set_comm_algorithm(self.comm_algorithm)
        commission_profile_points = CommissionsCommissionProfilePointsSubWizard(self.web_driver_container)
        commission_profile_points.click_on_plus()
        commission_profile_points.set_base_value(self.base_value)
        commission_profile_points.click_on_checkmark()
        time.sleep(1)
        commissions_profiles.click_on_checkmark()
        time.sleep(1)
        wizard = CommissionsWizard(self.web_driver_container)
        wizard.click_on_go_back()
        values_tab.set_commission_profile(self.commission_profile_name)

    def test_context(self):

        try:
            self.precondition()
            wizard = CommissionsWizard(self.web_driver_container)
            self.verify("Is PDF contains valid data", True,
                        wizard.click_download_pdf_entity_button_and_check_pdf(self.commission_profile_name))
            wizard.click_on_save_changes()
            main_page = CommissionsPage(self.web_driver_container)
            main_page.set_name(self.commission_name)
            time.sleep(1)
            main_page.click_on_more_actions()
            main_page.click_on_edit()
            values_tab = CommissionsValuesSubWizard(self.web_driver_container)
            self.verify("Is commission profile edited correctly", self.commission_profile_name,
                        values_tab.get_commission_profile())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
