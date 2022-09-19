import sys
import time
import traceback
import string
import random

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


class QAP_T3198(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = 'QAP_T3198'
        self.new_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.venue = ['ASE', 'AMEX']
        self.instr_type = ['Bond', 'Certificate']
        self.listing = ['ALDAR', 'ORAp']
        self.symbol = ['AUD/BRL', 'CNH/JPY']

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_crossed_venue_rates_page()
        main_page = CrossedVenueRatesPage(self.web_driver_container)
        main_page.click_on_new()
        values_tab = CrossedVenueRatesValuesSubWizard(self.web_driver_container)
        values_tab.set_name(self.name)
        dimensions_tab = CrossedVenueRatesDimensionsSubWizard(self.web_driver_container)
        dimensions_tab.set_venue(self.venue[0])
        dimensions_tab.set_listing(self.listing[0])
        dimensions_tab.set_instr_type(self.instr_type[0])
        dimensions_tab.set_symbol(self.symbol[0])
        wizard = CrossedVenueRatesWizard(self.web_driver_container)
        wizard.click_on_save_changes()

    def post_conditions(self):
        main_page = CrossedVenueRatesPage(self.web_driver_container)
        main_page.set_name(self.new_name)
        time.sleep(1)
        main_page.click_on_more_actions()
        main_page.click_on_delete(True)

    def test_context(self):

        try:
            self.precondition()

            main_page = CrossedVenueRatesPage(self.web_driver_container)
            main_page.set_name(self.name)
            time.sleep(1)
            main_page.click_on_more_actions()
            main_page.click_on_edit()
            values_tab = CrossedVenueRatesValuesSubWizard(self.web_driver_container)
            values_tab.set_name(self.new_name)
            dimensions_tab = CrossedVenueRatesDimensionsSubWizard(self.web_driver_container)
            dimensions_tab.set_venue(self.venue[1])
            dimensions_tab.set_listing(self.listing[1])
            dimensions_tab.set_instr_type(self.instr_type[1])
            dimensions_tab.set_symbol(self.symbol[1])
            wizard = CrossedVenueRatesWizard(self.web_driver_container)
            wizard.click_on_save_changes()

            main_page.set_name(self.new_name)
            time.sleep(1)
            main_page.click_on_more_actions()
            main_page.click_on_edit()

            expected_resul = [self.venue[1], self.listing[1], self.instr_type[1], self.symbol[1]]
            actual_result = [dimensions_tab.get_venue(), dimensions_tab.get_listing(), dimensions_tab.get_instr_type(),
                             dimensions_tab.get_symbol()]

            self.verify(f"Entity {self.new_name} has been modify", expected_resul, actual_result)

            wizard.click_on_save_changes()

            self.post_conditions()

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
