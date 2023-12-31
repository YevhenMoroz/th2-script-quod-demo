import random
import string
import time

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.middle_office.allocation_matching_profiles.main_page import \
    MainPage
from test_framework.web_admin_core.pages.middle_office.allocation_matching_profiles.wizard import \
    AllocationMatchingProfilesWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3815(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.fix_matching_profile_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.avg_price_precision = "4"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_allocation_matching_profiles_page()

    def test_context(self):

        self.precondition()
        page = MainPage(self.web_driver_container)
        wizard = AllocationMatchingProfilesWizard(self.web_driver_container)
        page.click_on_more_actions()
        page.click_on_edit()
        wizard.set_name(self.fix_matching_profile_name)
        wizard.set_avg_price_precision(self.avg_price_precision)
        expected_data = [self.fix_matching_profile_name,
                         self.avg_price_precision]
        actual_data = [wizard.get_name(),
                       wizard.get_avg_price_precision()]
        wizard.click_on_save_changes()
        page.set_name(self.fix_matching_profile_name)
        time.sleep(1)
        page.click_on_more_actions()
        page.click_on_edit()
        self.verify("Is new fix matching profile contains valid values", expected_data, actual_data)
