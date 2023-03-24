import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.middle_office.fees.fees_wizard import FeesWizard
from test_framework.web_admin_core.pages.middle_office.fees.fees_commission_profile_points_sub_wizard import \
    FeesCommissionProfilePointsSubWizard
from test_framework.web_admin_core.pages.middle_office.fees.fees_order_fee_profile_sub_wizard import \
    FeesOrderFeeProfileSubWizard
from test_framework.web_admin_core.pages.middle_office.fees.fees_page import FeesPage
from test_framework.web_admin_core.pages.middle_office.fees.fees_values_sub_wizard import FeesValuesSubWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T10639(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

        self.profile_name = [''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6)) for _ in range(2)]
        self.comm_algorithm = 'SlidingScale'
        self.comm_xunit = 'Amount'
        self.new_comm_xunit = 'Quantity'
        self.base_value = '1'

    def create_commission_profile(self, profile_name, comm_xunit, comm_algorithm, base_value):
        commission_profile = FeesOrderFeeProfileSubWizard(self.web_driver_container)
        commission_profile.click_on_plus()
        commission_profile.set_commission_profile_name(profile_name)
        commission_profile.set_comm_xunit(comm_xunit)
        commission_profile.set_comm_algorithm(comm_algorithm)
        commission_profile_points = FeesCommissionProfilePointsSubWizard(self.web_driver_container)
        commission_profile_points.click_on_plus()
        commission_profile_points.set_base_value(base_value)
        commission_profile_points.click_on_checkmark()
        time.sleep(0.5)
        commission_profile.click_on_checkmark()
        time.sleep(1)

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_fees_page()

        fees_page = FeesPage(self.web_driver_container)
        fees_page.click_on_new()
        fees_values_sub_wizard = FeesValuesSubWizard(self.web_driver_container)
        fees_values_sub_wizard.click_on_manage_order_fee_profile()

        self.create_commission_profile(self.profile_name[0], self.comm_xunit, self.comm_algorithm, self.base_value)
        self.create_commission_profile(self.profile_name[1], self.comm_xunit, self.comm_algorithm, self.base_value)

        wizard = FeesWizard(self.web_driver_container)
        wizard.click_on_go_back()

    def test_context(self):
        fees_values_sub_wizard = FeesValuesSubWizard(self.web_driver_container)
        commission_profile = FeesOrderFeeProfileSubWizard(self.web_driver_container)

        try:
            self.precondition()

            fees_values_sub_wizard.click_on_manage_order_fee_profile()
            commission_profile.set_commission_profile_name_filter(self.profile_name[0])
            time.sleep(0.5)
            commission_profile.select_commission_profile(self.profile_name[0])
            time.sleep(0.5)
            self.verify("Profile preview appears", True, commission_profile.is_commission_profile_preview_displayed())

            commission_profile.set_commission_profile_name_filter(self.profile_name[1])
            time.sleep(0.5)
            commission_profile.select_commission_profile(self.profile_name[1])
            time.sleep(0.5)
            commission_profile.set_commission_profile_name_filter(self.profile_name[0])
            time.sleep(0.5)
            commission_profile.click_on_delete(True)
            commission_profile.set_commission_profile_name_filter(self.profile_name[1])
            time.sleep(0.5)
            commission_profile.select_commission_profile(self.profile_name[1])
            time.sleep(0.5)
            self.verify("Profile preview appears", True, commission_profile.is_commission_profile_preview_displayed())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
