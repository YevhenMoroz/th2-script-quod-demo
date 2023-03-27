import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.market_making.client_tier.client_tiers_page import ClientTiersPage
from test_framework.web_admin_core.pages.market_making.client_tier.client_tiers_wizard import ClientTiersWizard
from test_framework.web_admin_core.pages.market_making.client_tier.client_tiers_schedules_sub_wizard import \
    ClientTiersSchedulesSubWizard
from test_framework.web_admin_core.pages.market_making.client_tier.client_tiers_values_sub_wizard import \
    ClientTiersValuesSubWizard
from test_framework.web_admin_core.pages.market_making.client_tier.client_tier_instruments_page \
    import ClientTierInstrumentsPage
from test_framework.web_admin_core.pages.market_making.client_tier.client_tier_instrument_values_sub_wizard \
    import ClientTierInstrumentValuesSubWizard
from test_framework.web_admin_core.pages.market_making.client_tier.client_tier_instrument_wizard \
    import ClientTierInstrumentWizard
from test_framework.web_admin_core.pages.market_making.client_tier.client_tier_instrument_external_clients_sub_wizard \
    import ClientTiersInstrumentExternalClientsSubWizard
from test_framework.web_admin_core.pages.market_making.client_tier.client_tier_instrument_internal_clients_sub_wizard \
    import ClientTiersInstrumentInternalClientsSubWizard

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3879(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

        self.client_tiers = {"entity_1": {"name": ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))},
                             "entity_2": {"name": ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))},
                             "core_spot_price_strategy": "Direct",
                             "instrument": "EUR/USD",
                             "tod_end_time": "01:00:00",
                             "schedule_name_1": ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6)),
                             "schedule_name_2": ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6)),
                             "schedule_day": "Monday",
                             "schedule_from_time_1": "15:00:00",
                             "schedule_from_time_2": "18:00:00",
                             "schedule_to_time_1": "18:00:00",
                             "schedule_to_time_2": "20:00:00"}

        self.client_tiers_instrument = {"symbol": "EUR/USD",
                                        "tod_end_time": "01:00:00",
                                        "external_client": "CLIENT1",
                                        "internal_client": "HouseFill"}

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_client_tier_page()
        client_tiers_page = ClientTiersPage(self.web_driver_container)
        client_tiers_page.click_on_new()
        client_tiers_values_tab = ClientTiersValuesSubWizard(self.web_driver_container)
        client_tiers_values_tab.click_on_manage_button_for_schedules()

        schedules_wizard = ClientTiersSchedulesSubWizard(self.web_driver_container)
        schedules_wizard.click_on_plus_button_at_schedule_name()
        schedules_wizard.set_schedule_name(self.client_tiers["schedule_name_1"])
        schedules_wizard.click_on_plus_button_at_schedules()
        schedules_wizard.set_day(self.client_tiers["schedule_day"])
        schedules_wizard.set_from_time(self.client_tiers["schedule_from_time_1"])
        schedules_wizard.set_to_time(self.client_tiers["schedule_to_time_1"])
        schedules_wizard.click_on_checkmark_button_at_schedules()
        schedules_wizard.click_on_checkmark_button_at_schedule_name()

        schedules_wizard.click_on_plus_button_at_schedule_name()
        schedules_wizard.set_schedule_name(self.client_tiers["schedule_name_2"])
        schedules_wizard.click_on_plus_button_at_schedules()
        schedules_wizard.set_day(self.client_tiers["schedule_day"])
        schedules_wizard.set_from_time(self.client_tiers["schedule_from_time_2"])
        schedules_wizard.set_to_time(self.client_tiers["schedule_to_time_2"])
        schedules_wizard.click_on_checkmark_button_at_schedules()
        schedules_wizard.click_on_checkmark_button_at_schedule_name()

        wizard = ClientTiersWizard(self.web_driver_container)
        wizard.click_on_go_back_button()

        client_tiers_values_tab.set_name(self.client_tiers["entity_1"]["name"])
        client_tiers_values_tab.set_core_spot_price_strategy(self.client_tiers["core_spot_price_strategy"])
        client_tiers_values_tab.set_tod_end_time(self.client_tiers["tod_end_time"])
        client_tiers_values_tab.select_schedule_checkbox()
        client_tiers_values_tab.set_schedule(self.client_tiers["schedule_name_1"])
        wizard.click_on_save_changes()

        client_tiers_page.click_on_new()
        client_tiers_values_tab.set_name(self.client_tiers["entity_2"]["name"])
        client_tiers_values_tab.set_core_spot_price_strategy(self.client_tiers["core_spot_price_strategy"])
        client_tiers_values_tab.set_tod_end_time(self.client_tiers["tod_end_time"])
        wizard.click_on_save_changes()

    def post_conditions(self):
        client_tiers_page = ClientTiersPage(self.web_driver_container)
        client_tiers_page.set_name(self.client_tiers["entity_1"]["name"])
        time.sleep(1)
        client_tiers_page.select_client_tier_by_name(self.client_tiers["entity_1"]["name"])
        client_tiers_page.click_on_more_actions()
        client_tiers_page.click_on_delete_and_confirmation(True)
        time.sleep(1)
        client_tiers_page.set_name(self.client_tiers["entity_2"]["name"])
        time.sleep(1)
        client_tiers_page.select_client_tier_by_name(self.client_tiers["entity_2"]["name"])
        client_tiers_page.click_on_more_actions()
        client_tiers_page.click_on_edit()
        client_tiers_values_tab = ClientTiersValuesSubWizard(self.web_driver_container)
        client_tiers_values_tab.click_on_manage_button_for_schedules()
        schedules_wizard = ClientTiersSchedulesSubWizard(self.web_driver_container)
        schedules_wizard.set_schedule_name_filter(self.client_tiers["schedule_name_1"])
        time.sleep(1)
        schedules_wizard.click_on_delete_button_at_schedule_name()
        schedules_wizard.set_schedule_name_filter(self.client_tiers["schedule_name_2"])
        time.sleep(1)
        schedules_wizard.click_on_delete_button_at_schedule_name()
        wizard = ClientTiersWizard(self.web_driver_container)
        wizard.click_on_go_back_button()
        client_tiers_values_tab.select_schedule_checkbox()
        wizard.click_on_save_changes()

        client_tiers_page.set_name(self.client_tiers["entity_2"]["name"])
        time.sleep(1)
        client_tiers_page.select_client_tier_by_name(self.client_tiers["entity_2"]["name"])
        client_tiers_page.click_on_more_actions()
        client_tiers_page.click_on_delete_and_confirmation(True)

    def test_context(self):
        try:
            self.precondition()

            client_tiers_page = ClientTiersPage(self.web_driver_container)
            client_tiers_page.set_name(self.client_tiers["entity_1"]["name"])
            time.sleep(1)
            client_tiers_page.select_client_tier_by_name(self.client_tiers["entity_1"]["name"])
            instrument_page = ClientTierInstrumentsPage(self.web_driver_container)
            instrument_page.click_on_new()

            instrument_values_tab = ClientTierInstrumentValuesSubWizard(self.web_driver_container)
            instrument_values_tab.set_symbol(self.client_tiers_instrument["symbol"])
            instrument_values_tab.set_tod_end_time(self.client_tiers_instrument["tod_end_time"])
            instrument_external_client = ClientTiersInstrumentExternalClientsSubWizard(self.web_driver_container)
            instrument_external_client.click_on_plus()
            instrument_external_client.set_client(self.client_tiers_instrument["external_client"])
            instrument_external_client.click_on_checkmark()
            instrument_internal_client = ClientTiersInstrumentInternalClientsSubWizard(self.web_driver_container)
            instrument_internal_client.click_on_plus()
            instrument_internal_client.set_client(self.client_tiers_instrument["internal_client"])
            instrument_internal_client.click_on_checkmark()

            instrument_wizard = ClientTierInstrumentWizard(self.web_driver_container)
            instrument_wizard.click_on_save_changes()

            client_tiers_page.set_name(self.client_tiers["entity_2"]["name"])
            time.sleep(1)
            client_tiers_page.select_client_tier_by_name(self.client_tiers["entity_2"]["name"])
            instrument_page.click_on_new()
            instrument_values_tab.set_symbol(self.client_tiers_instrument["symbol"])
            instrument_values_tab.set_tod_end_time(self.client_tiers_instrument["tod_end_time"])
            instrument_external_client.click_on_plus()
            instrument_external_client.set_client(self.client_tiers_instrument["external_client"])
            instrument_external_client.click_on_checkmark()

            self.verify("Warning for external client appears", True,
                        instrument_external_client.is_warning_icon_displayed())

            instrument_internal_client.click_on_plus()
            instrument_internal_client.set_client(self.client_tiers_instrument["internal_client"])
            instrument_internal_client.click_on_checkmark()

            self.verify("Warning for internal client appears", True,
                        instrument_internal_client.is_warning_icon_displayed())
            instrument_wizard.click_on_save_changes()

            client_tiers_page.set_name(self.client_tiers["entity_2"]["name"])
            time.sleep(1)
            client_tiers_page.select_client_tier_by_name(self.client_tiers["entity_2"]["name"])
            client_tiers_page.click_on_more_actions()
            client_tiers_page.click_on_edit()

            client_tiers_values_tab = ClientTiersValuesSubWizard(self.web_driver_container)
            client_tiers_values_tab.select_schedule_checkbox()
            client_tiers_values_tab.set_schedule(self.client_tiers["schedule_name_2"])
            wizard = ClientTiersWizard(self.web_driver_container)
            wizard.click_on_save_changes()

            client_tiers_page.set_name(self.client_tiers["entity_2"]["name"])
            time.sleep(1)
            client_tiers_page.select_client_tier_by_name(self.client_tiers["entity_2"]["name"])
            instrument_page.set_symbol(self.client_tiers_instrument["symbol"])
            time.sleep(1)
            instrument_page.click_on_more_actions()
            instrument_page.click_on_edit()

            self.verify("Warning for external client not appears", False,
                        instrument_external_client.is_warning_icon_displayed())

            self.verify("Warning for internal client not appears", False,
                        instrument_internal_client.is_warning_icon_displayed())
            instrument_wizard.click_on_save_changes()

            self.post_conditions()

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
