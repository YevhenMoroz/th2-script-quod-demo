import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.general.common.common_page import CommonPage
from test_framework.web_admin_core.pages.middle_office.fees.fees_page import FeesPage
from test_framework.web_admin_core.pages.middle_office.fees.fees_values_sub_wizard import FeesValuesSubWizard
from test_framework.web_admin_core.pages.middle_office.fees.fees_exec_fee_profile_sub_wizard \
    import FeesExecFeeProfileSubWizard
from test_framework.web_admin_core.pages.middle_office.fees.fees_commission_profile_points_sub_wizard \
    import FeesCommissionProfilePointsSubWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T8848(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

        self.wrong_comm_type = ['AbsoluteAmount', 'BasisPoints', 'Percentage']
        self.comm_type = 'PerUnit'
        self.commission_profile_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.comm_xunit = 'Quantity'
        self.comm_algorithm = 'Flat'
        self.base_values = '1 '

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_fees_page()
        fees_page = FeesPage(self.web_driver_container)
        fees_page.click_on_new()
        values_tab = FeesValuesSubWizard(self.web_driver_container)
        values_tab.click_on_manage_exec_fee_profile()

    def test_context(self):
        common_act = CommonPage(self.web_driver_container)

        try:
            self.precondition()

            exec_fee_profile = FeesExecFeeProfileSubWizard(self.web_driver_container)
            exec_fee_profile.click_on_plus()
            exec_fee_profile.set_commission_profile_name(self.commission_profile_name)
            exec_fee_profile.set_comm_xunit(self.comm_xunit)
            comm_type = random.choice(self.wrong_comm_type)
            exec_fee_profile.set_comm_type(comm_type)
            exec_fee_profile.set_comm_algorithm(self.comm_algorithm)
            commission_profile_points = FeesCommissionProfilePointsSubWizard(self.web_driver_container)
            commission_profile_points.click_on_plus()
            commission_profile_points.set_base_value(self.base_values)
            commission_profile_points.click_on_checkmark()
            exec_fee_profile.click_on_checkmark()

            self.verify(f"Commission Profiles not save with Comm Type = {comm_type}", True,
                        common_act.is_error_message_displayed())

            exec_fee_profile.set_comm_type(self.comm_type)
            time.sleep(0.5)

            self.verify("Comm XUnit become disabled", False, exec_fee_profile.is_comm_xunit_enabled())
            exec_fee_profile.click_on_checkmark()
            exec_fee_profile.set_commission_profile_name_filter(self.commission_profile_name)
            time.sleep(1)
            self.verify("Commission Profile save", True,
                        exec_fee_profile.is_searched_commission_profile_found(self.commission_profile_name))

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
