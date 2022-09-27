import sys
import time
import traceback
import random

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.market_making.client_tier.client_tier_instrument_external_clients_sub_wizard \
    import ClientTiersInstrumentExternalClientsSubWizard
from test_framework.web_admin_core.pages.market_making.client_tier.client_tier_instrument_internal_clients_sub_wizard \
    import ClientTiersInstrumentInternalClientsSubWizard
from test_framework.web_admin_core.pages.market_making.client_tier.client_tier_instruments_page \
    import ClientTierInstrumentsPage
from test_framework.web_admin_core.pages.market_making.client_tier.client_tier_instrument_values_sub_wizard \
    import ClientTierInstrumentValuesSubWizard
from test_framework.web_admin_core.pages.market_making.client_tier.client_tier_instrument_wizard \
    import ClientTierInstrumentWizard
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3987(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.symbol = self.data_set.get_symbol_by_name("symbol_1")
        self.external_client = ''
        self.internal_client = ''
        self.tod_end_time = "01:00:00"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_client_tier_page()
        client_tier_instrument_main_page = ClientTierInstrumentsPage(self.web_driver_container)
        client_tier_instrument_main_page.click_on_new()
        client_tier_instrument_values_tab = ClientTierInstrumentValuesSubWizard(self.web_driver_container)
        client_tier_instrument_values_tab.set_symbol(self.symbol)
        client_tier_instrument_values_tab.set_tod_end_time(self.tod_end_time)
        client_tier_external_clients_sub_wizard = ClientTiersInstrumentExternalClientsSubWizard(
            self.web_driver_container)
        client_tier_external_clients_sub_wizard.click_on_plus()
        self.external_client = random.choice(client_tier_external_clients_sub_wizard
                                             .get_all_external_client_from_drop_menu())
        client_tier_external_clients_sub_wizard.set_client(self.external_client)
        client_tier_external_clients_sub_wizard.click_on_checkmark()
        client_tier_internal_client_sub_wizard = ClientTiersInstrumentInternalClientsSubWizard(self.web_driver_container)
        client_tier_internal_client_sub_wizard.click_on_plus()
        self.internal_client = random.choice(client_tier_internal_client_sub_wizard
                                             .get_all_internal_client_from_drop_menu())
        client_tier_internal_client_sub_wizard.set_client(self.internal_client)
        client_tier_internal_client_sub_wizard.click_on_checkmark()
        client_tier_instrument_wizard = ClientTierInstrumentWizard(self.web_driver_container)
        client_tier_instrument_wizard.click_on_save_changes()

    def test_context(self):
        try:
            self.precondition()

            client_tier_instrument_main_page = ClientTierInstrumentsPage(self.web_driver_container)
            client_tier_instrument_main_page.set_symbol(self.symbol)
            time.sleep(1)
            client_tier_instrument_main_page.click_on_more_actions()
            client_tier_instrument_main_page.click_on_edit()
            client_tier_external_clients_sub_wizard = ClientTiersInstrumentExternalClientsSubWizard(
                self.web_driver_container)
            client_tier_external_clients_sub_wizard.set_client_filter(self.external_client)
            time.sleep(1)
            client_tier_external_clients_sub_wizard.click_on_edit()
            self.verify("External client saved", self.external_client,
                        client_tier_external_clients_sub_wizard.get_client())
            client_tier_external_clients_sub_wizard.click_on_checkmark()
            client_tier_external_clients_sub_wizard.click_on_delete()
            time.sleep(1)
            client_tier_internal_client_sub_wizard = ClientTiersInstrumentInternalClientsSubWizard(
                self.web_driver_container)
            client_tier_internal_client_sub_wizard.set_client_filter(self.internal_client)
            time.sleep(1)
            client_tier_internal_client_sub_wizard.click_on_edit()
            self.verify("Internal client saved", self.internal_client,
                        client_tier_internal_client_sub_wizard.get_client())
            client_tier_internal_client_sub_wizard.click_on_checkmark()
            client_tier_internal_client_sub_wizard.click_on_delete()

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
