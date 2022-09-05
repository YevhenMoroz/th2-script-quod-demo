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


class QAP_T3408(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.base_value = "0"
        self.limit = "9999"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_fees_page()

    def test_context(self):

        try:
            self.precondition()

            main_page = FeesPage(self.web_driver_container)
            value_tab = FeesValuesSubWizard(self.web_driver_container)
            main_page.click_on_new()
            value_tab.click_on_manage_exec_fee_profile()
            fees_profiles = FeesExecFeeProfileSubWizard(self.web_driver_container)
            fees_profiles.click_on_plus()
            commissions_profiles_points = FeesCommissionProfilePointsSubWizard(self.web_driver_container)
            commissions_profiles_points.click_on_plus()
            commissions_profiles_points.set_base_value(self.base_value)
            commissions_profiles_points.set_upper_limit(self.limit)
            commissions_profiles_points.click_on_checkmark()
            commissions_profiles_points.click_on_edit()

            self.verify("Is base value set as zero", self.base_value, commissions_profiles_points.get_base_value())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
