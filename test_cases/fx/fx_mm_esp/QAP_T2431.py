from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.forex.RestApiClientTierInstrSymbolMessages import \
    RestApiClientTierInstrSymbolMessages
from test_framework.win_gui_wrappers.fe_trading_constant import PriceNaming, RatesColumnNames
from test_framework.win_gui_wrappers.forex.client_rates_tile import ClientRatesTile


class QAP_T2431(TestCase):
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ask_pips = PriceNaming.ask_pips
        self.bid_pips = PriceNaming.bid_pips
        self.ask_band = RatesColumnNames.ask_band
        self.bid_band = RatesColumnNames.bid_band
        self.spread = PriceNaming.spread
        self.rates_tile = ClientRatesTile(self.test_id, self.session_id)
        self.silver = self.data_set.get_client_tier_by_name("client_tier_1")
        self.eur_usd = self.data_set.get_symbol_by_name("symbol_1")
        self.eur_usd_spot = self.eur_usd + "-Spot"
        self.client_tier_silver = self.data_set.get_client_tier_id_by_name("client_tier_id_1")
        self.expected_band = "1M"
        self.spread_event = "Spread validation"

        self.web_adm_env = self.environment.get_list_web_admin_rest_api_environment()[0]
        self.rest_manager = RestApiManager(self.web_adm_env.session_alias_wa, self.test_id)
        self.rest_message = RestApiClientTierInstrSymbolMessages(self.test_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1
        self.rest_message.find_all_client_tier_instrument()
        params_eur_usd = self.rest_manager.send_get_request(self.rest_message)
        params_eur_usd = self.rest_manager. \
            parse_response_details(params_eur_usd,
                                   {'clientTierID': self.client_tier_silver, 'instrSymbol': self.eur_usd})
        self.rest_message.clear_message_params().modify_client_tier_instrument().set_params(
            params_eur_usd).add_sweepable_qty("1000000").add_sweepable_qty("1000000")
    #     self.rates_tile.crete_tile()
    #     self.rates_tile.modify_client_tile(instrument=self.eur_usd_spot, client_tier=self.silver)
    #     row_values = self.rates_tile.extract_values_from_rates(self.bid_band, self.ask_band, row_number=4)
    #     actual_band = row_values[self.bid_band]
    #     self.rates_tile.compare_values(self.expected_band, actual_band,
    #                                    event_name=self.spread_event)
    #     self.rest_message.clear_message_params().modify_client_tier_instrument().set_params(
    #         params_eur_usd).remove_sweepable_qty("1000000").remove_sweepable_qty("1000000")
    #     # endregion
    #
    # @try_except(test_id=Path(__file__).name[:-3])
    # def run_post_conditions(self):
    #     self.rates_tile.close_tile()
