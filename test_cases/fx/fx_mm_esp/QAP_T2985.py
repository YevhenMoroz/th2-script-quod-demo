from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.win_gui_wrappers.fe_trading_constant import RatesColumnNames
from test_framework.win_gui_wrappers.forex.client_rates_tile import ClientRatesTile





class QAP_T2985(TestCase):
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.rates_tile = ClientRatesTile(self.test_id, self.session_id)
        self.client = self.data_set.get_client_tier_by_name("client_tier_1")
        self.symbol1 = self.data_set.get_symbol_by_name("symbol_1")
        self.symbol3 = self.data_set.get_symbol_by_name("symbol_3")
        self.instrument1 = self.symbol1 + "-Spot"
        self.instrument2 = self.symbol3 + "-Spot"

        self.event_name = "qty validation"

        self.expected_qty_1 = "1M"
        self.expected_qty_3 = "3M"
        self.expected_qty_5 = "5M"
        self.expected_qty_10 = "10M"

        self.ask_band = RatesColumnNames.ask_band
        self.bid_band = RatesColumnNames.bid_band

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1
        self.rates_tile.crete_tile()
        self.rates_tile.modify_client_tile(instrument=self.instrument1, client_tier=self.client)
        # endregion

        # region step 2
        actual_qty = self.rates_tile.extract_values_from_rates(self.bid_band, self.ask_band)
        bid_qty = actual_qty[str(self.bid_band)]
        self.rates_tile.compare_values(self.expected_qty_1, bid_qty,
                                       event_name=self.event_name)
        actual_qty = self.rates_tile.extract_values_from_rates(self.bid_band, self.ask_band, row_number=2)
        bid_qty = actual_qty[str(self.bid_band)]
        self.rates_tile.compare_values(self.expected_qty_5, bid_qty,
                                       event_name=self.event_name)
        actual_qty = self.rates_tile.extract_values_from_rates(self.bid_band, self.ask_band, row_number=3)
        bid_qty = actual_qty[str(self.bid_band)]
        self.rates_tile.compare_values(self.expected_qty_10, bid_qty,
                                       event_name=self.event_name)
        # endregion

        # region step 3
        self.rates_tile.modify_client_tile(instrument=self.instrument2)
        # endregion

        # region step 4
        actual_qty = self.rates_tile.extract_values_from_rates(self.bid_band, self.ask_band)
        ask_qty = actual_qty[str(self.ask_band)]
        self.rates_tile.compare_values(self.expected_qty_1, ask_qty,
                                       event_name=self.event_name)
        actual_qty = self.rates_tile.extract_values_from_rates(self.bid_band, self.ask_band, row_number=2)
        ask_qty = actual_qty[str(self.ask_band)]
        self.rates_tile.compare_values(self.expected_qty_3, ask_qty,
                                       event_name=self.event_name)
        # endregion


    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rates_tile.close_tile()