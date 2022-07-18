from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.win_gui_wrappers.fe_trading_constant import ClientPrisingTileAction, RatesColumnNames
from test_framework.win_gui_wrappers.forex.client_rates_tile import ClientRatesTile


class QAP_1644(TestCase):
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)

        self.pips_1 = "1"
        self.pips_2 = "2"
        self.pips_3 = "3"

        self.ask_base = RatesColumnNames.ask_base
        self.bid_base = RatesColumnNames.bid_base
        self.ask_px = RatesColumnNames.ask_px
        self.bid_px = RatesColumnNames.bid_px

        self.increase_ask = ClientPrisingTileAction.increase_ask
        self.decrease_ask = ClientPrisingTileAction.decrease_ask
        self.decrease_bid = ClientPrisingTileAction.decrease_bid

        self.rates_tile = ClientRatesTile(self.test_id, self.session_id)

        self.silver = self.data_set.get_client_tier_by_name("client_tier_1")
        self.eur_usd = self.data_set.get_symbol_by_name("symbol_1")
        self.eur_usd_spot = self.eur_usd + "-Spot"
        self.base_event = "Base validation"
        self.px_event = "Px validation"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1-2
        self.rates_tile.crete_tile()
        self.rates_tile.modify_client_tile(instrument=self.eur_usd_spot, client_tier=self.silver)
        self.rates_tile.press_use_default()
        # endregion

        # region step 3
        row_values = self.rates_tile.extract_values_from_rates(self.bid_base, self.bid_px, row_number=3)
        bid_base_before = row_values[str(self.bid_base)]
        bid_px_before = row_values[str(self.bid_px)]
        expected_bid_base = str(int(bid_base_before) + 2)
        expected_bid_px = str(int(bid_px_before) - 20)
        self.rates_tile.modify_client_tile(pips=self.pips_2)
        self.rates_tile.select_rows([3])
        self.rates_tile.modify_spread(self.decrease_bid)
        row_values = self.rates_tile.extract_values_from_rates(self.bid_base, self.bid_px, row_number=3)
        actual_bid_base = str(int(row_values[str(self.bid_base)]))
        actual_bid_px = str(int(row_values[str(self.bid_px)]))
        self.rates_tile.compare_values(expected_bid_base, actual_bid_base,
                                       event_name=self.base_event)
        self.rates_tile.compare_values(expected_bid_px, actual_bid_px,
                                       event_name=self.px_event)
        # endregion

        # region step 4
        row_values = self.rates_tile.extract_values_from_rates(self.bid_base, self.bid_px)
        bid_base_before = row_values[str(self.bid_base)]
        bid_px_before = row_values[str(self.bid_px)]
        expected_bid_base = str(int(bid_base_before) + 1)
        expected_bid_px = str(int(bid_px_before) - 10)
        self.rates_tile.deselect_rows()
        self.rates_tile.modify_client_tile(pips=self.pips_1)
        self.rates_tile.modify_spread(self.decrease_bid)
        row_values = self.rates_tile.extract_values_from_rates(self.bid_base, self.bid_px)
        actual_bid_base = str(int(row_values[str(self.bid_base)]))
        actual_bid_px = str(int(row_values[str(self.bid_px)]))
        self.rates_tile.compare_values(expected_bid_base, actual_bid_base,
                                       event_name=self.base_event)
        self.rates_tile.compare_values(expected_bid_px, actual_bid_px,
                                       event_name=self.px_event)
        # endregion

        # region step 5
        row_values = self.rates_tile.extract_values_from_rates(self.ask_base, self.ask_px, row_number=3)
        ask_base_before = row_values[str(self.ask_base)]
        ask_px_before = row_values[str(self.ask_px)]
        expected_ask_base = str(int(ask_base_before) - 3)
        expected_ask_px = str(int(ask_px_before) - 30)
        self.rates_tile.select_rows([3])
        self.rates_tile.modify_client_tile(pips=self.pips_3)
        self.rates_tile.modify_spread(self.increase_ask)
        row_values = self.rates_tile.extract_values_from_rates(self.ask_base, self.ask_px, row_number=3)
        actual_ask_base = str(int(row_values[str(self.ask_base)]))
        actual_ask_px = str(int(row_values[str(self.ask_px)]))
        self.rates_tile.compare_values(expected_ask_base, actual_ask_base,
                                       event_name=self.base_event)
        self.rates_tile.compare_values(expected_ask_px, actual_ask_px,
                                       event_name=self.px_event)
        # endregion

        # region step 6
        row_values = self.rates_tile.extract_values_from_rates(self.ask_base, self.ask_px)
        ask_base_before = row_values[str(self.ask_base)]
        ask_px_before = row_values[str(self.ask_px)]
        expected_ask_base = str(int(ask_base_before) + 2)
        expected_ask_px = str(int(ask_px_before) + 20)
        self.rates_tile.deselect_rows()
        self.rates_tile.modify_client_tile(pips=self.pips_2)
        self.rates_tile.modify_spread(self.decrease_ask)
        row_values = self.rates_tile.extract_values_from_rates(self.ask_base, self.ask_px)
        actual_ask_base = str(int(row_values[str(self.ask_base)]))
        actual_ask_px = str(int(row_values[str(self.ask_px)]))
        self.rates_tile.compare_values(expected_ask_base, actual_ask_base,
                                       event_name=self.base_event)
        self.rates_tile.compare_values(expected_ask_px, actual_ask_px,
                                       event_name=self.px_event)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rates_tile.press_use_default()
        self.rates_tile.close_tile()
