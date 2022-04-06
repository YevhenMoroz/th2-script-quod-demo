import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.market_making.client_tier.client_tier_instrument_external_clients_sub_wizard import \
    ClientTiersInstrumentExternalClientsSubWizard
from test_framework.web_admin_core.pages.market_making.client_tier.client_tier_instruments_page import \
    ClientTierInstrumentsPage
from test_framework.web_admin_core.pages.market_making.client_tier.client_tiers_wizard import ClientTiersWizard
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


# TODO: issue causes filters (we can't search any entity for edit/delete)
class QAP_1692(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.symbol = self.data_set.get_symbol_by_name("symbol_1")
        self.client = self.data_set.get_client("client_2")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_client_tier_page()
        client_tier_instrument_main_page = ClientTierInstrumentsPage(self.web_driver_container)
        time.sleep(2)
        client_tier_instrument_main_page.click_on_more_actions()
        time.sleep(2)
        client_tier_instrument_main_page.click_on_edit()
        time.sleep(2)
        client_tier_external_clients_sub_wizard = ClientTiersInstrumentExternalClientsSubWizard(
            self.web_driver_container)
        client_tier_external_clients_sub_wizard.click_on_plus()
        time.sleep(2)
        client_tier_external_clients_sub_wizard.set_client(self.client)
        time.sleep(1)
        client_tier_external_clients_sub_wizard.click_on_checkmark()
        time.sleep(2)
        client_tiers_wizard = ClientTiersWizard(self.web_driver_container)
        client_tiers_wizard.click_on_save_changes()
        time.sleep(2)
        client_tier_instrument_main_page.click_on_more_actions()
        time.sleep(2)
        client_tier_instrument_main_page.click_on_edit()
        time.sleep(2)
        # client_tier_external_clients_sub_wizard.set_client_filter(self.client)
        # time.sleep(2)
        client_tier_external_clients_sub_wizard.click_on_edit()
        time.sleep(2)

    def test_context(self):
        try:
            self.precondition()
            client_tier_external_clients_sub_wizard = ClientTiersInstrumentExternalClientsSubWizard(
                self.web_driver_container)
            self.verify("Client created correctly", self.client, client_tier_external_clients_sub_wizard.get_client())
            client_tiers_wizard = ClientTiersWizard(self.web_driver_container)
            time.sleep(2)
            client_tiers_wizard.click_on_save_changes()
            time.sleep(2)
            client_tier_instrument_main_page = ClientTierInstrumentsPage(self.web_driver_container)
            client_tier_instrument_main_page.click_on_more_actions()
            time.sleep(2)
            client_tier_instrument_main_page.click_on_edit()
            time.sleep(2)
            client_tier_external_clients_sub_wizard = ClientTiersInstrumentExternalClientsSubWizard(
                self.web_driver_container)
            # client_tier_external_clients_sub_wizard.set_client_filter(self.client)
            # time.sleep(2)
            client_tier_external_clients_sub_wizard.click_on_delete()
            time.sleep(2)
            client_tiers_wizard.click_on_save_changes()

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
