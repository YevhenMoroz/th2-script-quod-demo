import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.middle_office.allocation_matching_profiles.main_page \
    import MainPage
from test_framework.web_admin_core.pages.middle_office.allocation_matching_profiles.wizard \
    import AllocationMatchingProfilesWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3114(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.avg_price_precision = '1'
        self.tolerance_currency = 'USD'
        self.net_tolerance_currency = 'EUR'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_allocation_matching_profiles_page()

    def test_context(self):

        try:
            self.precondition()

            page = MainPage(self.web_driver_container)
            page.click_on_new()
            time.sleep(1)
            wizard = AllocationMatchingProfilesWizard(self.web_driver_container)
            wizard.set_name(self.name)
            wizard.set_avg_price_precision(self.avg_price_precision)
            wizard.set_tolerance_currency(self.tolerance_currency)
            wizard.set_net_tolerance_currency(self.net_tolerance_currency)
            wizard.click_on_client_commission_checkbox()
            wizard.click_on_save_changes()

            page.set_name(self.name)
            time.sleep(1)
            page.click_on_more_actions()
            page.click_on_edit()

            expected_data = [self.name, self.avg_price_precision, self.tolerance_currency, self.net_tolerance_currency,
                             "True"]
            actual_data = [wizard.get_name(), wizard.get_avg_price_precision(), wizard.get_tolerance_currency(),
                           wizard.get_net_tolerance_currency(), str(wizard.is_client_commission_checkbox_selected())]

            self.verify("New Allocation matching profile created and contains saved data", expected_data, actual_data)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
