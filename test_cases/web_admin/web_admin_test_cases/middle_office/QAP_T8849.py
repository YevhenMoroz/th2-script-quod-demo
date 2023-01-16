import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.middle_office.fees.fees_page import FeesPage
from test_framework.web_admin_core.pages.middle_office.fees.fees_values_sub_wizard import FeesValuesSubWizard
from test_framework.web_admin_core.pages.middle_office.fees.fees_exec_fee_profile_sub_wizard \
    import FeesExecFeeProfileSubWizard
from test_framework.web_admin_core.pages.middle_office.fees.fees_commission_profile_points_sub_wizard \
    import FeesCommissionProfilePointsSubWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T8849(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

        self.comm_type = 'PerUnit'
        self.commission_profile_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.comm_xunit = 'Quantity'
        self.comm_algorithm = 'Flat'
        self.base_values = '1'
        self.upper_limit = ['3', '', '2']

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_fees_page()
        fees_page = FeesPage(self.web_driver_container)
        fees_page.click_on_new()

    def create_commission_profile_point(self, base_value, upper_limit):
        commission_profile_points = FeesCommissionProfilePointsSubWizard(self.web_driver_container)
        commission_profile_points.click_on_plus()
        commission_profile_points.set_base_value(base_value)
        commission_profile_points.set_upper_limit(upper_limit)
        commission_profile_points.click_on_checkmark()

    def test_context(self):
        values_tab = FeesValuesSubWizard(self.web_driver_container)
        commission_profile_points = FeesCommissionProfilePointsSubWizard(self.web_driver_container)

        try:
            self.precondition()

            values_tab.click_on_manage_exec_fee_profile()
            exec_fee_profile = FeesExecFeeProfileSubWizard(self.web_driver_container)
            exec_fee_profile.click_on_plus()
            exec_fee_profile.set_commission_profile_name(self.commission_profile_name)
            exec_fee_profile.set_comm_xunit(self.comm_xunit)
            exec_fee_profile.set_comm_type(self.comm_type)
            exec_fee_profile.set_comm_algorithm(self.comm_algorithm)

            self.create_commission_profile_point(self.base_values, self.upper_limit[0])
            self.create_commission_profile_point(self.base_values, self.upper_limit[1])
            self.create_commission_profile_point(self.base_values, self.upper_limit[2])
            exec_fee_profile.click_on_checkmark()

            exec_fee_profile.set_commission_profile_name_filter(self.commission_profile_name)
            time.sleep(1)
            exec_fee_profile.click_on_edit()
            actual_result = commission_profile_points.get_all_upper_limit_values_from_table()
            expected_result = [self.upper_limit[-1], self.upper_limit[0], self.upper_limit[1]]

            self.verify("Sort CommissionPointBlocks in ascending UpperLimit and null one is the last one",
                        expected_result, actual_result)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
