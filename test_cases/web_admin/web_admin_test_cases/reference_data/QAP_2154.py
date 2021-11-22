import time
import traceback

from custom import basic_custom_actions
from test_cases.web_admin.web_admin_core.pages.login.login_page import LoginPage
from test_cases.web_admin.web_admin_core.pages.reference_data.listings.listings_page import ListingsPage
from test_cases.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_2154(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm02"
        self.password = "adm02"
        self.listing = "a"

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
        listing_page.click_on_load()
        time.sleep(2)

    def test_context(self):

        try:
            self.precondition()
            listing_page = ListingsPage(self.web_driver_container)
            try:
                listing_page.click_on_enable_disable_button()
                time.sleep(1)
                listing_page.click_on_enable_disable_button()
                time.sleep(2)
                self.verify("Listing disable/enable correctly", True, True)
            except Exception:
                self.verify("Listing not disable/enable incorrectly", True, False)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
