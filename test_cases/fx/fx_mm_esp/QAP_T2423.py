from pathlib import Path
from custom import basic_custom_actions as bca
from custom.verifier import VerificationMethod
from test_cases.fx.fx_wrapper.common_tools import stop_fxfh, start_fxfh
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.win_gui_wrappers.fe_trading_constant import PriceNaming
from test_framework.win_gui_wrappers.forex.client_rates_tile import ClientRatesTile


class QAP_T2423(TestCase):
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ask_pips = PriceNaming.ask_pips
        self.bid_pips = PriceNaming.bid_pips
        self.rates_tile = ClientRatesTile(self.test_id, self.session_id)
        self.client = self.data_set.get_client_tier_by_name("client_tier_1")
        self.symbol = self.data_set.get_symbol_by_name("symbol_1")
        self.dif_symbol = self.data_set.get_symbol_by_name("symbol_2")
        self.instrument = self.symbol + "-Spot"
        self.dif_instrument = self.dif_symbol + "-Spot"
        self.empty_pips_event = "Empty pips validation"
        self.pips_event = "Present pips validation"
        self.empty_pips = ""
        self.not_equal = VerificationMethod.NOT_EQUALS

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1
        self.rates_tile.crete_tile()
        self.rates_tile.modify_client_tile(instrument=self.instrument, client_tier=self.client)

        bid_n_ask_values = self.rates_tile.extract_prices_from_tile(self.bid_pips, self.ask_pips)
        actual_bid_pips = bid_n_ask_values[self.bid_pips.value]
        actual_ask_pips = bid_n_ask_values[self.ask_pips.value]
        self.rates_tile.compare_values(self.empty_pips, actual_bid_pips,
                                       event_name=self.pips_event, ver_method=self.not_equal)
        self.rates_tile.compare_values(self.empty_pips, actual_ask_pips,
                                       event_name=self.pips_event, ver_method=self.not_equal)
        # endregion

        # region step 2
        stop_fxfh()
        self.rates_tile.modify_client_tile(instrument=self.dif_instrument)
        self.rates_tile.modify_client_tile(instrument=self.instrument)
        bid_n_ask_values = self.rates_tile.extract_prices_from_tile(self.bid_pips, self.ask_pips)
        actual_bid_pips = bid_n_ask_values[self.bid_pips.value]
        actual_ask_pips = bid_n_ask_values[self.ask_pips.value]
        self.rates_tile.compare_values(self.empty_pips, actual_bid_pips,
                                       event_name=self.empty_pips_event)
        self.rates_tile.compare_values(self.empty_pips, actual_ask_pips,
                                       event_name=self.empty_pips_event)
        # endregion

        # region step 3
        start_fxfh()
        bid_n_ask_values = self.rates_tile.extract_prices_from_tile(self.bid_pips, self.ask_pips)
        actual_bid_pips = bid_n_ask_values[self.bid_pips.value]
        actual_ask_pips = bid_n_ask_values[self.ask_pips.value]
        self.rates_tile.compare_values(self.empty_pips, actual_bid_pips,
                                       event_name=self.pips_event, ver_method=self.not_equal)
        self.rates_tile.compare_values(self.empty_pips, actual_ask_pips,
                                       event_name=self.pips_event, ver_method=self.not_equal)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rates_tile.close_tile()
