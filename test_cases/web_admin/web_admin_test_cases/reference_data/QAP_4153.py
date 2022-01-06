import sys
import time
import traceback

from custom import basic_custom_actions
from test_cases.web_admin.web_admin_core.pages.login.login_page import LoginPage
from test_cases.web_admin.web_admin_core.pages.reference_data.venues.venues_description_sub_wizard import \
    VenuesDescriptionSubWizard
from test_cases.web_admin.web_admin_core.pages.reference_data.venues.venues_market_data_sub_wizard import \
    VenuesMarketDataSubWizard
from test_cases.web_admin.web_admin_core.pages.reference_data.venues.venues_page import VenuesPage
from test_cases.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_4153(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm02"
        self.password = "adm02"
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
        values_sub_wizard = VenuesDescriptionSubWizard(self.web_driver_container)
        values_sub_wizard.set_short_name(self.short_name)
        time.sleep(3)

    def test_context(self):

        try:
            self.precondition()
            values_sub_wizard = VenuesDescriptionSubWizard(self.web_driver_container)
            self.verify("Is short Name contains only 10 characters", "aaaaaaaaaa", values_sub_wizard.get_short_name())
            time.sleep(2)
            values_sub_wizard.set_very_short_name(self.very_short_name)
            time.sleep(2)
            self.verify("Is very short name contains only 4 characters", "aaaa",
                        values_sub_wizard.get_very_short_name())


        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
