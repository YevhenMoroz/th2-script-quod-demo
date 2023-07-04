import time

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.markets.venues.venues_values_sub_wizard import \
    VenuesValuesSubWizard
from test_framework.web_admin_core.pages.markets.venues.venues_page import VenuesPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3793(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.short_name = "aaaaaaaaaaaaaaaaa"
        self.very_short_name = "aaaaaaaaaaaaaaaaa"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_venues_page()
        time.sleep(2)
        page = VenuesPage(self.web_driver_container)
        page.click_on_new()
        time.sleep(1)
        values_sub_wizard = VenuesValuesSubWizard(self.web_driver_container)
        values_sub_wizard.set_short_name(self.short_name)
        time.sleep(3)

    def test_context(self):
        self.precondition()
        values_sub_wizard = VenuesValuesSubWizard(self.web_driver_container)
        self.verify("Is short Name contains only 10 characters", "aaaaaaaaaa", values_sub_wizard.get_short_name())
        time.sleep(2)
        values_sub_wizard.set_very_short_name(self.very_short_name)
        time.sleep(2)
        self.verify("Is very short name contains only 4 characters", "aaaa",
                    values_sub_wizard.get_very_short_name())
