import sys
import time
import traceback
import random
import string

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.price_cleansing.rate_deviation.main_page import MainPage
from test_framework.web_admin_core.pages.price_cleansing.rate_deviation.wizards import *
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3150(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = [''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6)) for _ in range(2)]
        self.reference_venue = []
        self.price_deviation = ["1", "11", "-1"]
        self.price_deviation_format = 'ExactPrice'
        self.reference_price = 'BidAndAsk'
        self.venue = 'AMEX'
        self.listing = 'ARMX'
        self.instr_type = 'Equity'
        self.symbol = 'AUD/BRL'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_rate_deviation_page()
        main_page = MainPage(self.web_driver_container)
        main_page.click_on_new()
        values_tab = ValuesTab(self.web_driver_container)
        values_tab.set_name(self.name[0])
        self.reference_venue = random.choices(values_tab.get_all_reference_venues_from_drop_menu(), k=3)
        values_tab.set_reference_venues(self.reference_venue)
        values_tab.set_price_deviation(self.price_deviation[0])
        wizard = MainWizard(self.web_driver_container)
        wizard.click_on_save_changes()

    def test_context(self):

        try:
            self.precondition()

            main_page = MainPage(self.web_driver_container)
            main_page.set_name_filter(self.name[0])
            time.sleep(1)
            main_page.click_on_more_actions()
            main_page.click_on_edit()
            values_tab = ValuesTab(self.web_driver_container)
            values_tab.set_name(self.name[1])
            values_tab.set_reference_venues(self.reference_venue)
            wizard = MainWizard(self.web_driver_container)
            wizard.click_on_save_changes()
            time.sleep(0.5)
            self.verify("Reference Venues field must be filled", True,
                        wizard.is_incorrect_or_missing_value_message_displayed())

            values_tab.set_reference_venues(self.reference_venue)
            values_tab.set_price_deviation(self.price_deviation[-1])

            wizard.click_on_save_changes()
            time.sleep(0.5)
            self.verify("Price Deviation field must be positive", True,
                        wizard.is_incorrect_or_missing_value_message_displayed())

            values_tab.set_price_deviation(self.price_deviation[1])
            dimensions_tab = DimensionsTab(self.web_driver_container)
            dimensions_tab.set_venue(self.venue)
            dimensions_tab.set_listing(self.listing)
            dimensions_tab.set_instr_type(self.instr_type)
            dimensions_tab.set_symbol(self.symbol)
            wizard.click_on_save_changes()

            main_page.set_name_filter(self.name[1])
            time.sleep(1)
            main_page.click_on_more_actions()
            main_page.click_on_edit()

            expected_result = [*[self.name[1], self.price_deviation[1], self.venue, self.listing,
                               self.instr_type, self.symbol], *self.reference_venue]
            actual_result = [*[values_tab.get_name(), values_tab.get_price_deviation(),
                             dimensions_tab.get_venue(), dimensions_tab.get_listing(), dimensions_tab.get_instr_type(),
                             dimensions_tab.get_symbol()],
                             *[_.strip() for _ in values_tab.get_reference_venues().split(',')]]

            self.verify("New data saved", sorted(expected_result), sorted(actual_result))

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
