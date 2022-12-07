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


class QAP_T3794(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

        self.commission_profile_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.comm_type = 'AbsoluteAmount'
        self.comm_algorithm = 'SlidingScale'
        self.comm_xunit = 'Amount'
        self.base_value = ['1', '10']
        self.min_commission = '35'
        self.upper_limit = '50'
        self.slope = '7'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_fees_page()
        fees_page = FeesPage(self.web_driver_container)
        fees_page.click_on_new()
        fees_values_sub_wizard = FeesValuesSubWizard(self.web_driver_container)
        fees_values_sub_wizard.click_on_manage_order_fee_profile()

        commission_profile = FeesOrderFeeProfileSubWizard(self.web_driver_container)
        commission_profile.click_on_plus()
        commission_profile.set_commission_profile_name(self.commission_profile_name)
        commission_profile.set_comm_xunit(self.comm_xunit)
        commission_profile.set_comm_type(self.comm_type)
        commission_profile.set_comm_algorithm(self.comm_algorithm)
        commission_profile_points = FeesCommissionProfilePointsSubWizard(self.web_driver_container)
        commission_profile_points.click_on_plus()
        commission_profile_points.set_base_value(self.base_value[0])
        commission_profile_points.click_on_checkmark()
        commission_profile.click_on_checkmark()
        wizard = FeesWizard(self.web_driver_container)
        wizard.click_on_go_back()

    def test_context(self):
        fees_values_sub_wizard = FeesValuesSubWizard(self.web_driver_container)
        commission_profile = FeesOrderFeeProfileSubWizard(self.web_driver_container)
        commission_profile_points = FeesCommissionProfilePointsSubWizard(self.web_driver_container)

        try:
            self.precondition()

            fees_values_sub_wizard.click_on_manage_order_fee_profile()
            commission_profile.set_commission_profile_name_filter(self.commission_profile_name)
            time.sleep(1)
            commission_profile.click_on_edit()
            commission_profile_points.click_on_edit()
            commission_profile_points.set_base_value(self.base_value[1])
            commission_profile_points.set_min_commission(self.min_commission)
            commission_profile_points.set_upper_limit(self.upper_limit)
            commission_profile_points.set_slope(self.slope)
            commission_profile_points.click_on_checkmark()
            commission_profile.click_on_checkmark()

            commission_profile.set_commission_profile_name_filter(self.commission_profile_name)
            time.sleep(1)
            commission_profile.click_on_edit()
            commission_profile_points.click_on_edit()

            expected_result = [self.base_value[1], self.min_commission, self.upper_limit, self.slope]
            actual_result = [commission_profile_points.get_base_value(), commission_profile_points.get_min_commission(),
                             commission_profile_points.get_upper_limit(), commission_profile_points.get_slope()]

            self.verify("Commission Profile shows all the existing values/options in the Amend window",
                        expected_result, actual_result)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
