import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.middle_office.fees.fees_commission_profile_points_sub_wizard import \
    FeesCommissionProfilePointsSubWizard
from test_framework.web_admin_core.pages.middle_office.fees.fees_order_fee_profile_sub_wizard import \
    FeesOrderFeeProfileSubWizard
from test_framework.web_admin_core.pages.middle_office.fees.fees_page import FeesPage
from test_framework.web_admin_core.pages.middle_office.fees.fees_values_sub_wizard import FeesValuesSubWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_4152(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.comm_type = self.data_set.get_comm_type("comm_type_2")
        self.comm_algorithm = self.data_set.get_comm_algorithm("comm_algorithm_2")
        self.base_value = "10"
        self.min_commission = "35"
        self.upper_limit = "50"
        self.slope = "7"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_fees_page()
        fees_page = FeesPage(self.web_driver_container)
        fees_page.click_on_new()
        time.sleep(2)
        fees_values_sub_wizard = FeesValuesSubWizard(self.web_driver_container)
        fees_values_sub_wizard.click_on_manage_order_fee_profile()
        time.sleep(2)
        order_fee_profile_sub_wizard = FeesOrderFeeProfileSubWizard(self.web_driver_container)
        order_fee_profile_sub_wizard.click_on_edit()
        time.sleep(2)
        order_fee_profile_sub_wizard.set_comm_type(self.comm_type)
        time.sleep(1)
        order_fee_profile_sub_wizard.set_comm_algorithm(self.comm_algorithm)
        time.sleep(1)
        fees_commission_profile_points_sub_wizard = FeesCommissionProfilePointsSubWizard(self.web_driver_container)
        fees_commission_profile_points_sub_wizard.click_on_edit()
        time.sleep(2)
        fees_commission_profile_points_sub_wizard.set_base_value(self.base_value)
        fees_commission_profile_points_sub_wizard.set_min_commission(self.min_commission)
        fees_commission_profile_points_sub_wizard.set_upper_limit(self.upper_limit)
        fees_commission_profile_points_sub_wizard.set_slope(self.slope)
        fees_commission_profile_points_sub_wizard.click_on_checkmark()
        time.sleep(1)
        order_fee_profile_sub_wizard.click_on_checkmark()
        time.sleep(3)
        order_fee_profile_sub_wizard.click_on_edit()
        time.sleep(1)

    def test_context(self):

        try:
            self.precondition()
            order_fee_profile_sub_wizard = FeesOrderFeeProfileSubWizard(self.web_driver_container)
            fees_commission_profile_points_sub_wizard = FeesCommissionProfilePointsSubWizard(self.web_driver_container)
            expected_data = [self.comm_type,
                             self.comm_algorithm,
                             self.base_value,
                             self.min_commission,
                             self.upper_limit,
                             self.slope]
            actual_data = [order_fee_profile_sub_wizard.get_comm_type(),
                           order_fee_profile_sub_wizard.get_comm_algorithm()]
            fees_commission_profile_points_sub_wizard.click_on_edit()
            time.sleep(1)
            try:
                actual_data = actual_data + [fees_commission_profile_points_sub_wizard.get_base_value(),
                                             fees_commission_profile_points_sub_wizard.get_min_commission(),
                                             fees_commission_profile_points_sub_wizard.get_upper_limit(),
                                             fees_commission_profile_points_sub_wizard.get_slope()]
                self.verify("Is commission profile contains valid values after edited", expected_data, actual_data)
            except Exception:
                self.verify("Commission profile contains invalid values after edited", expected_data, actual_data)


        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
