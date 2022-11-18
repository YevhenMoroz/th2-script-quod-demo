from pathlib import Path
from custom import basic_custom_actions as bca
from test_cases.fx.fx_wrapper.common_tools import random_qty
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.forex.RestApiClientTierInstrSymbolMessages import \
    RestApiClientTierInstrSymbolMessages
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, QuoteRequestBookColumns
from test_framework.win_gui_wrappers.forex.fx_dealer_intervention import FXDealerIntervention


class QAP_T2691(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)

        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side_rfq, self.test_id)

        self.web_adm_env = self.environment.get_list_web_admin_rest_api_environment()[0]
        self.rest_manager = RestApiManager(self.web_adm_env.session_alias_wa, self.test_id)
        self.rest_massage = RestApiClientTierInstrSymbolMessages(self.test_id)

        self.dealer_intervention = FXDealerIntervention(self.test_id, self.session_id)
        self.free_notes_column = OrderBookColumns.free_notes.value
        self.qty_column = OrderBookColumns.qty.value
        self.client_column = QuoteRequestBookColumns.client.value
        self.presence_event = "Order presence check"
        self.expected_qty = ""
        self.expected_free_notes = "WK1 is not being priced or not executable over this client tier"

        self.qty = random_qty(1, 2, 7)
        self.eur_usd = self.data_set.get_symbol_by_name('symbol_1')
        self.client_tier_argentina = self.data_set.get_client_tier_id_by_name("client_tier_id_2")
        self.client_argentina = self.data_set.get_client_by_name("client_mm_2")

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1-2
        self.rest_massage.find_client_tier_instrument(self.client_tier_argentina, self.eur_usd)
        params_eur_usd = self.rest_manager.send_get_request_filtered(self.rest_massage)
        params_eur_usd = self.rest_manager. \
            parse_response_details(params_eur_usd,
                                   {'clientTierID': self.client_tier_argentina, 'instrSymbol': self.eur_usd})
        self.rest_massage.clear_message_params().modify_client_tier_instrument() \
            .set_params(params_eur_usd). \
            update_value_in_component('clientTierInstrSymbolTenor', 'activeQuote', 'false', {'tenor': 'WK1'})
        self.rest_manager.send_post_request(self.rest_massage)
        self.sleep(3)
        # endregion

        # region Step 3
        self.quote_request.set_swap_rfq_params().update_repeating_group_by_index(component="NoRelatedSymbols", index=0,
                                                                                 Account=self.client_argentina)
        self.quote_request.update_near_leg(leg_qty=self.qty)
        self.quote_request.update_far_leg(leg_qty=self.qty)
        self.fix_manager.send_message(self.quote_request)

        self.dealer_intervention.set_list_filter(
            [self.qty_column, self.expected_qty, self.client_column, self.client_argentina])
        actual_free_notes = self.dealer_intervention.extract_field_from_unassigned(self.free_notes_column)
        self.dealer_intervention.compare_values(self.expected_free_notes, actual_free_notes, self.presence_event)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_massage.modify_client_tier_instrument(). \
            update_value_in_component('clientTierInstrSymbolTenor', 'activeQuote', 'true', {'tenor': 'WK1'})
        self.rest_manager.send_post_request(self.rest_massage)
