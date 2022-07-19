from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.win_gui_wrappers.fe_trading_constant import ClientPrisingTileAction, RatesColumnNames
from test_framework.win_gui_wrappers.forex.client_rates_tile import ClientRatesTile


class QAP_1589(TestCase):
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)

        self.pips_1 = "1"

        self.ask_base = RatesColumnNames.ask_base
        self.bid_base = RatesColumnNames.bid_base
        self.widen_spread = ClientPrisingTileAction.widen_spread

        self.rates_tile = ClientRatesTile(self.test_id, self.session_id)

        self.client = self.data_set.get_client_tier_by_name("client_tier_1")
        self.symbol = self.data_set.get_symbol_by_name("symbol_1")
        self.instrument = self.symbol + "-Spot"
        self.base_event = "base value validation"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.rates_tile.crete_tile()
        self.rates_tile.modify_client_tile(instrument=self.instrument, client_tier=self.client)
        self.rates_tile.press_use_default()
        # endregion

        # region Step 2
        row_values = self.rates_tile.extract_values_from_rates(self.bid_base, self.ask_base)
        bid_base_before = row_values[str(self.bid_base)]
        ask_base_before = row_values[str(self.ask_base)]
        expected_bid_base = str(round(int(bid_base_before) + 1, 1))
        expected_ask_base = str(round(int(ask_base_before) + 1, 1))
        self.rates_tile.modify_client_tile(pips=self.pips_1)
        self.rates_tile.deselect_rows()
        self.rates_tile.modify_spread(self.widen_spread)
        row_values = self.rates_tile.extract_values_from_rates(self.bid_base, self.ask_base)
        bid_base_after = row_values[str(self.bid_base)]
        ask_base_after = row_values[str(self.ask_base)]
        self.rates_tile.compare_values(expected_bid_base, bid_base_after,
                                       event_name=self.base_event)
        self.rates_tile.compare_values(expected_ask_base, ask_base_after,
                                       event_name=self.base_event)
        # endregion

        # region Step 3
        self.rates_tile.press_live()
        row_values = self.rates_tile.extract_values_from_rates(self.bid_base, self.ask_base)
        bid_base_after = row_values[str(self.bid_base)]
        ask_base_after = row_values[str(self.ask_base)]
        self.rates_tile.compare_values(bid_base_before, bid_base_after,
                                       event_name=self.base_event)
        self.rates_tile.compare_values(ask_base_before, ask_base_after,
                                       event_name=self.base_event)
        # endregion

        # region Step 4
        self.rates_tile.press_live()
        row_values = self.rates_tile.extract_values_from_rates(self.bid_base, self.ask_base)
        bid_base_after = row_values[str(self.bid_base)]
        ask_base_after = row_values[str(self.ask_base)]
        self.rates_tile.compare_values(expected_bid_base, bid_base_after,
                                       event_name=self.base_event)
        self.rates_tile.compare_values(expected_ask_base, ask_base_after,
                                       event_name=self.base_event)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rates_tile.press_use_default()
        self.rates_tile.close_tile()
