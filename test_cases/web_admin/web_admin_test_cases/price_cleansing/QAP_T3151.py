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


class QAP_T3151(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.reference_venue = ''
        self.price_deviation = random.randint(1, 100)
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

    def test_context(self):

        try:
            self.precondition()

            main_page = MainPage(self.web_driver_container)
            main_page.click_on_new()
            values_tab = ValuesTab(self.web_driver_container)
            values_tab.set_name(self.name)
            values_tab.set_price_deviation_format(self.price_deviation_format)
            values_tab.set_reference_price(self.reference_price)

            dimensions_tab = DimensionsTab(self.web_driver_container)
            dimensions_tab.set_venue(self.venue)
            dimensions_tab.set_listing(self.listing)
            dimensions_tab.set_instr_type(self.instr_type)
            dimensions_tab.set_symbol(self.symbol)

            wizard = MainWizard(self.web_driver_container)
            wizard.click_on_save_changes()
            time.sleep(0.5)
            self.verify("Reference Venues field must be filled", True,
                        wizard.is_incorrect_or_missing_value_message_displayed())

            values_tab.set_reference_venues(random.choice(values_tab.get_all_reference_venues_from_drop_menu()))
            wizard.click_on_save_changes()
            time.sleep(0.5)
            self.verify("Reference Venues field must be filled", True,
                        wizard.is_incorrect_or_missing_value_message_displayed())

            values_tab.set_price_deviation(self.price_deviation)

            wizard.click_on_save_changes()
            main_page.set_name_filter(self.name)
            time.sleep(1)

            self.verify(f"Entity {self.name} has been create", True,
                        main_page.is_searched_entity_found_by_name(self.name))

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
