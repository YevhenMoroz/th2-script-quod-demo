import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage

from test_framework.web_admin_core.pages.middle_office.fees.fees_order_fee_profile_sub_wizard import \
    FeesOrderFeeProfileSubWizard
from test_framework.web_admin_core.pages.middle_office.fees.fees_page import FeesPage
from test_framework.web_admin_core.pages.middle_office.fees.fees_values_sub_wizard import FeesValuesSubWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T7225(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

        self.rounding_direction = ['RoundDown', 'RoundToNearest', 'RoundUp']
        self.rounding_precision = ['asd', '11']

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_fees_page()

    def test_context(self):
        fees_page = FeesPage(self.web_driver_container)
        fees_values_sub_wizard = FeesValuesSubWizard(self.web_driver_container)
        commission_profile = FeesOrderFeeProfileSubWizard(self.web_driver_container)

        try:
            self.precondition()

            fees_page.click_on_new()
            fees_values_sub_wizard.click_on_manage_order_fee_profile()
            commission_profile.click_on_plus()
            displayed_rounding_direction = commission_profile.get_all_rounding_direction_from_drop_menu()
            self.verify(f"Rounding Direction contains all {self.rounding_direction}",
                        sorted(self.rounding_direction), sorted(displayed_rounding_direction))

            commission_profile.set_rounding_precision(self.rounding_precision[0])
            time.sleep(1)
            self.verify("Rounding Precision not contains letters", False,
                        True if self.rounding_precision[0] in commission_profile.get_rounding_precision() else False)
            commission_profile.set_rounding_precision(self.rounding_precision[1])
            time.sleep(1)
            self.verify("Rounding Precision contains digits", True,
                        True if self.rounding_precision[1] in commission_profile.get_rounding_precision() else False)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
