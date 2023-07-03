import time

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.markets.listings.listings_page import ListingsPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3952(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.listing = "test"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_listings_page()
        time.sleep(2)
        listing_page = ListingsPage(self.web_driver_container)
        listing_page.set_listing_in_global_filter(self.listing)
        time.sleep(2)
        listing_page.click_on_load_button()
        time.sleep(2)

    def test_context(self):
        self.precondition()
        listing_page = ListingsPage(self.web_driver_container)
        try:
            listing_page.click_on_enable_disable_button()
            time.sleep(2)
            self.verify("Listing disable correctly", False, listing_page.is_toggle_button_enabled_disabled())
        except Exception as e:
            self.verify("Listing not disable", True, e.__class__.__name__)

        try:
            time.sleep(1)
            listing_page.click_on_enable_disable_button()
            time.sleep(2)
            self.verify("Listing enable correctly", True, listing_page.is_toggle_button_enabled_disabled())
        except Exception:
            self.verify("Listing not enable", True, False)
