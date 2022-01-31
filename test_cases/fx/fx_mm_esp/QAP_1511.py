from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.win_gui_wrappers.fe_trading_constant import RatesColumnNames, ClientPrisingTileAction, PriceNaming
from test_framework.win_gui_wrappers.forex.client_rates_tile import ClientRatesTile


expected_qty_1 = "1M"
expected_qty_3 = "3M"
expected_qty_5 = "5M"
expected_qty_10 = "10M"

ask_band = RatesColumnNames.ask_band
bid_band = RatesColumnNames.bid_band


class QAP_1511(TestCase):
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None):
        super().__init__(report_id, session_id, data_set)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.rates_tile = None

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Initialization
        self.rates_tile = ClientRatesTile(self.test_id, self.session_id)
        # endregion
        # region Variables
        client = self.data_set.get_client_tier_by_name("client_tier_1")
        symbol1 = self.data_set.get_symbol_by_name("symbol_1")
        symbol3 = self.data_set.get_symbol_by_name("symbol_3")
        instrument1 = symbol1 + "-Spot"
        instrument2 = symbol3 + "-Spot"
        event_name = "qty validation"
        # end region

        # region step 1
        self.rates_tile.crete_tile()
        self.rates_tile.modify_client_tile(instrument=instrument1, client_tier=client)
        # endregion

        # region step 2
        actual_qty = self.rates_tile.extract_values_from_rates(bid_band, ask_band)
        bid_qty = actual_qty[str(bid_band)]
        self.rates_tile.compare_values(expected_qty_1, bid_qty,
                                       event_name=event_name)
        # self.rates_tile.select_rows([2])
        actual_qty = self.rates_tile.extract_values_from_rates(bid_band, ask_band, row_number=2)
        bid_qty = actual_qty[str(bid_band)]
        self.rates_tile.compare_values(expected_qty_5, bid_qty,
                                       event_name=event_name)
        # self.rates_tile.select_rows([3])
        actual_qty = self.rates_tile.extract_values_from_rates(bid_band, ask_band, row_number=3)
        bid_qty = actual_qty[str(bid_band)]
        self.rates_tile.compare_values(expected_qty_10, bid_qty,
                                       event_name=event_name)
        # endregion

        # region step 3
        self.rates_tile.modify_client_tile(instrument=instrument2)
        # endregion

        # region step 4
        actual_qty = self.rates_tile.extract_values_from_rates(bid_band, ask_band)
        ask_qty = actual_qty[str(ask_band)]
        self.rates_tile.compare_values(expected_qty_1, ask_qty,
                                       event_name=event_name)
        actual_qty = self.rates_tile.extract_values_from_rates(bid_band, ask_band, row_number=2)
        ask_qty = actual_qty[str(ask_band)]
        self.rates_tile.compare_values(expected_qty_3, ask_qty,
                                       event_name=event_name)
        # endregion


    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rates_tile.close_tile()