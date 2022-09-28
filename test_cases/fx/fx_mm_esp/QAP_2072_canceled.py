from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.win_gui_wrappers.fe_trading_constant import ClientPrisingTileAction, RatesColumnNames
from test_framework.win_gui_wrappers.forex.client_rates_tile import ClientRatesTile


class QAP_2072(TestCase):
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.rates_tile = ClientRatesTile(self.test_id, self.session_id)

        self.silver = self.data_set.get_client_tier_by_name("client_tier_1")
        self.eur_usd = self.data_set.get_symbol_by_name("symbol_1")
        self.eur_usd_spot = self.eur_usd + "-Spot"
        self.px_event_1 = "Px validation of the 1st row"
        self.px_event_2 = "Px validation of the 2nd row"
        self.px_event_3 = "Px validation of the 3rd row"
        self.pips_2 = "2"

        self.ask_px = RatesColumnNames.ask_px
        self.bid_px = RatesColumnNames.bid_px
        self.decrease_ask = ClientPrisingTileAction.decrease_ask

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1
        self.rates_tile.crete_tile()
        self.rates_tile.modify_client_tile(instrument=self.eur_usd_spot, client_tier=self.silver)
        self.rates_tile.press_use_default()
        # endregion

        # region step 2-3
        row_values_1 = self.rates_tile.extract_values_from_rates(self.ask_px, self.bid_px, row_number=1)
        ask_px_before_1 = row_values_1[str(self.ask_px)]
        expected_ask_px_1 = str(int(ask_px_before_1) + 20)
        row_values_2 = self.rates_tile.extract_values_from_rates(self.ask_px, self.bid_px, row_number=2)
        ask_px_before_2 = row_values_2[str(self.ask_px)]
        expected_ask_px_2 = str(int(ask_px_before_2) + 20)
        row_values_3 = self.rates_tile.extract_values_from_rates(self.ask_px, self.bid_px, row_number=3)
        expected_ask_px_3 = row_values_3[str(self.ask_px)]
        self.rates_tile.select_rows([1, 2])
        self.rates_tile.modify_client_tile(pips=self.pips_2)
        self.rates_tile.modify_spread(self.decrease_ask)
        row_values_1 = self.rates_tile.extract_values_from_rates(self.ask_px, self.bid_px, row_number=1)
        actual_ask_px_1 = str(int(row_values_1[str(self.ask_px)]))
        row_values_2 = self.rates_tile.extract_values_from_rates(self.ask_px, self.bid_px, row_number=2)
        actual_ask_px_2 = str(int(row_values_2[str(self.ask_px)]))
        row_values_3 = self.rates_tile.extract_values_from_rates(self.ask_px, self.bid_px, row_number=3)
        actual_ask_px_3 = str(int(row_values_3[str(self.ask_px)]))
        self.rates_tile.compare_values(expected_ask_px_1, actual_ask_px_1,
                                       event_name=self.px_event_1)
        self.rates_tile.compare_values(expected_ask_px_2, actual_ask_px_2,
                                       event_name=self.px_event_2)
        self.rates_tile.compare_values(expected_ask_px_3, actual_ask_px_3,
                                       event_name=self.px_event_3)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rates_tile.press_use_default()
        self.rates_tile.close_tile()
