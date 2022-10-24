import random
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.general.common.common_page import CommonPage
from test_framework.web_admin_core.pages.middle_office.commissions.commissions_page import CommissionsPage
from test_framework.web_admin_core.pages.middle_office.commissions.commissions_values_sub_wizard \
    import CommissionsValuesSubWizard
from test_framework.web_admin_core.pages.middle_office.commissions.commissions_commision_profiles_sub_wizard\
    import CommissionsCommissionProfilesSubWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T8321(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

        self.commission_profile = ''
        self.rounding_precision = str(random.randint(10, 100))

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_commissions_page()
        main_page = CommissionsPage(self.web_driver_container)
        main_page.click_on_new()
        values_tab = CommissionsValuesSubWizard(self.web_driver_container)
        values_tab.click_on_manage_commission_profile()

    def test_context(self):

        try:
            self.precondition()

            commission_profile = CommissionsCommissionProfilesSubWizard(self.web_driver_container)
            commission_profile.click_on_edit()
            self.commission_profile = commission_profile.get_commission_profile_name()
            commission_profile.set_rounding_precision(self.rounding_precision)
            commission_profile.click_on_checkmark()

            common_act = CommonPage(self.web_driver_container)
            common_act.refresh_page(True)

            commission_profile.set_commission_profile_name_filter(self.commission_profile)
            time.sleep(1)
            commission_profile.click_on_edit()

            self.verify("Rounding Precision has value", self.rounding_precision, commission_profile.get_rounding_precision())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
