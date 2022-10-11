import sys
import time
import traceback
import random
import string

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.price_cleansing.crossed_venue_rates.crossed_venue_rates_page \
    import CrossedVenueRatesPage
from test_framework.web_admin_core.pages.price_cleansing.crossed_venue_rates.crossed_venue_rates_wizard \
    import CrossedVenueRatesWizard
from test_framework.web_admin_core.pages.price_cleansing.crossed_venue_rates.crossed_venue_rates_values_sub_wizard \
    import CrossedVenueRatesValuesSubWizard
from test_framework.web_admin_core.pages.price_cleansing.crossed_venue_rates.crossed_venue_rates_dimensions_sub_wizard \
    import CrossedVenueRatesDimensionsSubWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3265(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.venue = 'ASE'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_crossed_venue_rates_page()

    def test_context(self):

        try:
            self.precondition()

            main_page = CrossedVenueRatesPage(self.web_driver_container)
            main_page.click_on_new()
            values_tab = CrossedVenueRatesValuesSubWizard(self.web_driver_container)
            values_tab.set_name(self.name)
            dimensions_tab = CrossedVenueRatesDimensionsSubWizard(self.web_driver_container)
            dimensions_tab.set_venue(self.venue)
            wizard = CrossedVenueRatesWizard(self.web_driver_container)
            wizard.click_on_save_changes()
            main_page = CrossedVenueRatesPage(self.web_driver_container)
            main_page.set_name(self.name)
            time.sleep(1)

            self.verify(f"Entity {self.name} has been create", True,
                        main_page.is_searched_entity_found_by_name(self.name))

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
