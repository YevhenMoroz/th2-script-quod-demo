import time
import traceback

from custom import basic_custom_actions
from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.reference_data.venues.venues_market_data_sub_wizard import \
    VenuesMarketDataSubWizard
from quod_qa.web_admin.web_admin_core.pages.reference_data.venues.venues_page import VenuesPage
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_2904(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.console_error_lvl_id = second_lvl_id
        self.login = "adm02"
        self.password = "adm02"
        self.feed_source = ["ActivFinancial", "FeedOS", "InteraciveData", "MarketPrizm", "Native Market",
                            "Quod simulator", "RMDS"]

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_venues_page()
        time.sleep(2)
        page = VenuesPage(self.web_driver_container)
        page.click_on_new()
        time.sleep(2)

    def test_context(self):

        try:
            self.precondition()
            market_data_sub_wizard = VenuesMarketDataSubWizard(self.web_driver_container)

            try:
                for i in range(len(self.feed_source)):
                    market_data_sub_wizard.set_feed_source(self.feed_source[i])
                self.verify("Is feed source contains all valid values", True, True)
            except Exception as e:
                self.verify("Is feed source contains all valid values", True, e.__class__.__name__)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.console_error_lvl_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
