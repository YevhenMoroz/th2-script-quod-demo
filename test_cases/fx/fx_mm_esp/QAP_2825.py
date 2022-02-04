from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.win_gui_wrappers.fe_trading_constant import ClientPrisingTileAction, PriceNaming, RatesColumnNames
from test_framework.win_gui_wrappers.forex.client_rates_tile import ClientRatesTile


class QAP_2825(TestCase):
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None):
        super().__init__(report_id, session_id, data_set)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.rates_tile = ClientRatesTile(self.test_id, self.session_id)
        self.client = self.data_set.get_client_tier_by_name("client_tier_1")
        symbol = self.data_set.get_symbol_by_name("symbol_1")
        self.instrument = symbol + "-Spot"
        self.px_event = "Px validation"
        self.pips_2 = "2"


        self.ask_px = RatesColumnNames.ask_px
        self.bid_px = RatesColumnNames.bid_px

        self.ask_pips = PriceNaming.ask_pips
        self.bid_pips = PriceNaming.bid_pips

        self.spread = PriceNaming.spread
        self.widen_spread = ClientPrisingTileAction.widen_spread
        self.narrow_spread = ClientPrisingTileAction.narrow_spread
        self.decrease_ask = ClientPrisingTileAction.decrease_ask
        self.decrease_bid = ClientPrisingTileAction.decrease_bid
        self.skew_towards_bid = ClientPrisingTileAction.skew_towards_bid
        self.skew_towards_ask = ClientPrisingTileAction.skew_towards_ask

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1
        self.rates_tile.crete_tile()
        self.rates_tile.modify_client_tile(instrument=self.instrument, client_tier=self.client)
        self.rates_tile.press_use_default()
        # endregion

        # region step 2-3
        row_values = self.rates_tile.extract_values_from_rates(self.ask_px, self.bid_px)
        ask_px_before = row_values[str(self.ask_px)]
        expected_ask_px = str(int(ask_px_before) + 20)
        self.rates_tile.select_rows([1])
        self.rates_tile.modify_client_tile(pips=self.pips_2)
        self.rates_tile.modify_spread(self.decrease_ask)
        row_values = self.rates_tile.extract_values_from_rates(self.ask_px, self.bid_px)
        actual_ask_px = str(int(row_values[str(self.ask_px)]))

        self.rates_tile.compare_values(expected_ask_px, actual_ask_px,
                                       event_name=self.px_event)

        # endregion



    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rates_tile.press_use_default()
        self.rates_tile.close_tile()
