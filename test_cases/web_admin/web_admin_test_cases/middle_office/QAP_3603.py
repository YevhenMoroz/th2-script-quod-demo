import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_cases.web_admin.web_admin_core.pages.login.login_page import LoginPage
from test_cases.web_admin.web_admin_core.pages.middle_office.fix_matching_profile.fix_matching_profile_page import \
    FixMatchingProfilePage
from test_cases.web_admin.web_admin_core.pages.middle_office.fix_matching_profile.fix_matching_profile_wizard import \
    FixMatchingProfileWizard
from test_cases.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_3603(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm03"
        self.password = "adm03"
        self.fix_matching_profile_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.avg_price_precision = "4"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_fix_matching_profile_page()
        time.sleep(1)
        page = FixMatchingProfilePage(self.web_driver_container)
        page.click_on_new()
        time.sleep(2)
        wizard = FixMatchingProfileWizard(self.web_driver_container)
        wizard.set_fix_matching_profile_name(self.fix_matching_profile_name)
        time.sleep(2)
        wizard.set_avg_price_precision(self.avg_price_precision)
        wizard.click_on_save_changes()
        time.sleep(2)

    def test_context(self):

        try:
            self.precondition()
            page = FixMatchingProfilePage(self.web_driver_container)
            wizard = FixMatchingProfileWizard(self.web_driver_container)
            page.set_fix_matching_profile_name(self.fix_matching_profile_name)
            time.sleep(2)
            page.click_on_more_actions()
            time.sleep(2)
            page.click_on_edit()
            expected_data = [self.fix_matching_profile_name,
                             self.avg_price_precision]
            actual_data = [wizard.get_fix_matching_profile_name(),
                           wizard.get_avg_price_precision()]
            self.verify("Is new fix matching profile contains valid values", expected_data, actual_data)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
