import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.middle_office.commissions.commissions_commision_profiles_sub_wizard import \
    CommissionsCommissionProfilesSubWizard
from quod_qa.web_admin.web_admin_core.pages.middle_office.commissions.commissions_commission_profile_points_sub_wizard import \
    CommissionsCommissionProfilePointsSubWizard
from quod_qa.web_admin.web_admin_core.pages.middle_office.commissions.commissions_dimensions_sub_wizard import \
    CommissionsDimensionsSubWizard
from quod_qa.web_admin.web_admin_core.pages.middle_office.commissions.commissions_page import CommissionsPage
from quod_qa.web_admin.web_admin_core.pages.middle_office.commissions.commissions_wizard import CommissionsWizard
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_3240(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm03"
        self.password = "adm03"
        self.commission_profile_name_buffer_to_delete = str
        self.commission_profile_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.comm_xunit = "Amount"
        self.comm_algorithm = "Flat"
        self.base_value = "12"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_commissions_page()
        main_page = CommissionsPage(self.web_driver_container)
        dimensions_tab = CommissionsDimensionsSubWizard(self.web_driver_container)
        main_page.click_on_new()
        time.sleep(1)
        dimensions_tab.click_on_manage_commission_profile()
        time.sleep(1)
        commissions_profiles = CommissionsCommissionProfilesSubWizard(self.web_driver_container)
        ###
        commissions_profiles.click_on_plus()
        time.sleep(2)
        commissions_profiles.set_commission_profile_name(self.commission_profile_name)
        time.sleep(1)
        commissions_profiles.set_comm_xunit(self.comm_xunit)
        time.sleep(1)
        commissions_profiles.set_comm_algorithm(self.comm_algorithm)
        time.sleep(1)
        commission_profile_points = CommissionsCommissionProfilePointsSubWizard(self.web_driver_container)
        commission_profile_points.click_on_plus()
        time.sleep(1)
        commission_profile_points.set_base_value(self.base_value)
        time.sleep(1)
        commission_profile_points.click_on_checkmark()
        time.sleep(1)
        commissions_profiles.click_on_checkmark()
        time.sleep(2)
        commissions_profiles.set_commission_profile_name_filter(self.commission_profile_name)
        time.sleep(2)
        commissions_profiles.click_on_edit()
        self.commission_profile_name_buffer_to_delete = commissions_profiles.get_commission_profile_name()
        time.sleep(2)
        commissions_profiles.click_on_checkmark()
        time.sleep(2)
        commissions_profiles.click_on_delete()
        time.sleep(2)
        wizard = CommissionsWizard(self.web_driver_container)
        wizard.click_on_ok()
        time.sleep(2)

    def test_context(self):

        try:
            self.precondition()
            commissions_profiles = CommissionsCommissionProfilesSubWizard(self.web_driver_container)
            commissions_profiles.set_commission_profile_name_filter(self.commission_profile_name_buffer_to_delete)
            time.sleep(2)
            try:
                commissions_profiles.click_on_edit()
                self.verify("Commission profile name didn't delete", True, False)
            except Exception:
                self.verify("Commission profile name deleted correctly", True, True)
        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
