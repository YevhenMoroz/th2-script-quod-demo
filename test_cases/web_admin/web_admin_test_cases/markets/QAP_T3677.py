import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.markets.routes.main_page import RoutesPage
from test_framework.web_admin_core.pages.markets.routes.wizard import RoutesWizard
from test_framework.web_admin_core.pages.markets.routes.venues_subwizard import RoutesVenuesSubWizard
from test_framework.web_admin_core.pages.markets.routes.strategy_type_subwizard import RoutesStrategyTypeSubWizard
from test_framework.web_admin_core.pages.markets.routes.instrument_symbols_subwizard import RoutesInstrumentSymbolsSubWizard
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3677(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.client_id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.es_instance = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.description = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.counterpart = "TC Counterpart"
        self.venue = self.data_set.get_venue_by_name("venue_10")
        self.instr_symbol = "AUD/DKK"
        self.price_multiplier = str(random.randint(1, 10))
        self.strategy_type = "Dark SOR"
        self.default_scenario = "Quod Financial Dark SOR"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_routes_page()
        time.sleep(2)
        main_page = RoutesPage(self.web_driver_container)
        main_page.click_on_new_button()
        time.sleep(2)
        wizard = RoutesWizard(self.web_driver_container)
        wizard.set_name_at_values_tab(self.name)
        wizard.set_client_id_at_values_tab(self.client_id)
        wizard.set_es_instance_at_values_tab(self.es_instance)
        wizard.set_description_at_values_tab(self.description)
        wizard.set_counterpart_at_values_tab(self.counterpart)
        venue_tab = RoutesVenuesSubWizard(self.web_driver_container)
        venue_tab.click_on_plus_at_venues_tab()
        venue_tab.set_venue_at_venues_tab(self.venue)
        venue_tab.click_on_check_mark_at_venues_tab()
        insrt_symbols_tab = RoutesInstrumentSymbolsSubWizard(self.web_driver_container)
        insrt_symbols_tab.click_on_plus_button_at_instr_symbols_tab()
        insrt_symbols_tab.set_instr_symbol_at_instr_symbols_tab(self.instr_symbol)
        insrt_symbols_tab.set_price_multiplier_at_instr_symbols_tab(self.price_multiplier)
        insrt_symbols_tab.click_on_checkmark_button_at_instr_symbols_tab()
        strategy_type = RoutesStrategyTypeSubWizard(self.web_driver_container)
        strategy_type.set_strategy_type_at_strategy_type_tab(self.strategy_type)
        strategy_type.set_default_scenario_at_strategy_type_tab(self.default_scenario)

    def test_context(self):
        try:
            self.precondition()

            wizard = RoutesWizard(self.web_driver_container)
            actual_result = [self.name, self.client_id, self.es_instance, self.description, self.counterpart,
                             self.venue, self.instr_symbol, self.price_multiplier, self.strategy_type[0],
                             self.default_scenario]
            self.verify("PDF contains all tested data", True,
                        wizard.click_download_pdf_entity_button_and_check_pdf(actual_result))
            wizard.click_on_save_changes()
            time.sleep(2)

            main_page = RoutesPage(self.web_driver_container)
            main_page.set_name_at_filter(self.name)
            time.sleep(2)
            self.verify("New Route is saved", True, main_page.is_searched_route_found(self.name))

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
