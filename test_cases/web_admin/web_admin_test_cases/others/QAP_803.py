import random
import string
import time
import traceback

from custom import basic_custom_actions
from test_cases.web_admin.web_admin_core.pages.login.login_page import LoginPage
from test_cases.web_admin.web_admin_core.pages.others.market_data_source.market_data_source_page import \
    MarketDataSourcePage
from test_cases.web_admin.web_admin_core.pages.others.market_data_source.market_data_source_wizard import \
    MarketDataSourceWizard
from test_cases.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_803(CommonTestCase):
    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm02"
        self.password = "adm02"
        self.symbol = "EUR/PHP"
        self.user = "adm02"
        self.venue = "AMEX"
        self.md_source = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_market_data_source_page()
        main_page = MarketDataSourcePage(self.web_driver_container)
        main_page.click_on_new_button()
        time.sleep(2)
        wizard = MarketDataSourceWizard(self.web_driver_container)
        wizard.set_symbol(self.symbol)
        time.sleep(1)
        wizard.set_user(self.user)
        time.sleep(1)
        wizard.set_venue(self.venue)
        time.sleep(1)
        wizard.set_md_source(self.md_source)

    def test_context(self):
        try:
            self.precondition()
            wizard = MarketDataSourceWizard(self.web_driver_container)
            main_page = MarketDataSourcePage(self.web_driver_container)
            expected_pdf = [self.symbol, self.user, self.venue, self.md_source]
            self.verify("Is pdf contains selected value ? ", True,
                        wizard.click_download_pdf_entity_button_and_check_pdf(expected_pdf))
            time.sleep(2)
            wizard.click_on_save_changes()
            time.sleep(2)
            main_page.set_md_source_at_filter(self.md_source)
            time.sleep(2)
            headers = ["Symbol", "User", "Venue", "MDSource"]
            expected_saved_values_at_main_page = [self.symbol, self.user, "AMERICAN STOCK EXCHANGE", self.md_source]
            actual_saved_values_at_main_page = [main_page.get_symbol(),
                                                main_page.get_user(),
                                                main_page.get_venue(),
                                                main_page.get_md_source()]
            self.verify_arrays_of_data_objects("After saved", headers, expected_saved_values_at_main_page,
                                               actual_saved_values_at_main_page)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
