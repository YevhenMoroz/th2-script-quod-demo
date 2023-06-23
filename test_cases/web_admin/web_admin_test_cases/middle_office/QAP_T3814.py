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


class QAP_T3814(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.fix_matching_profile_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_allocation_matching_profiles_page()
        page = MainPage(self.web_driver_container)
        page.click_on_new()
        wizard = AllocationMatchingProfilesWizard(self.web_driver_container)
        wizard.set_name(self.fix_matching_profile_name)
        wizard.click_on_save_changes()

    def test_context(self):

        self.precondition()
        page = MainPage(self.web_driver_container)
        page.set_name(self.fix_matching_profile_name)
        time.sleep(1)
        page.click_on_more_actions()
        page.click_on_delete(True)

        page.set_name(self.fix_matching_profile_name)
        time.sleep(1)
        self.verify("Allocation Matching Profile deleted", False,
                    page.is_searched_entity_found_by_name(self.fix_matching_profile_name))
