from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.win_gui_wrappers.fe_trading_constant import ClientPrisingTileAction, \
    RatesColumnNames, PricingButtonColor
from test_framework.win_gui_wrappers.forex.client_rates_tile import ClientRatesTile


class QAP_T2948(TestCase):
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)

        self.pips_1 = "1"
        self.pips_1_5 = "1.5"

        self.ask_base = RatesColumnNames.ask_base
        self.bid_base = RatesColumnNames.bid_base

        self.widen_spread = ClientPrisingTileAction.widen_spread
        self.narrow_spread = ClientPrisingTileAction.narrow_spread

        self.rates_tile = ClientRatesTile(self.test_id, self.session_id)

        self.silver = self.data_set.get_client_tier_by_name("client_tier_1")
        self.eur_usd = self.data_set.get_symbol_by_name("symbol_1")
        self.eur_usd_spot = self.eur_usd + "-Spot"
        self.base_event = "base value validation"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1
        self.rates_tile.crete_tile()
        self.rates_tile.modify_client_tile(instrument=self.eur_usd_spot, client_tier=self.silver)
        # endregion

        # region step 2
        self.rates_tile.press_use_default()
        # endregion

        # region step 3-4
        row_values = self.rates_tile.extract_values_from_rates(self.bid_base, self.ask_base, row_number=2)
        bid_base_before = row_values[str(self.bid_base)]
        ask_base_before = row_values[str(self.ask_base)]
        expected_bid_base = str(round(int(bid_base_before) + 1.5, 1))
        expected_ask_base = str(round(int(ask_base_before) + 1.5, 1))
        self.rates_tile.select_rows([2])
        self.rates_tile.modify_client_tile(pips=self.pips_1_5)
        self.rates_tile.modify_spread(self.widen_spread)
        row_values = self.rates_tile.extract_values_from_rates(self.bid_base, self.ask_base, row_number=2)
        bid_base_after = row_values[str(self.bid_base)]
        ask_base_after = row_values[str(self.ask_base)]
        self.rates_tile.compare_values(expected_bid_base, bid_base_after,
                                       event_name=self.base_event)
        self.rates_tile.compare_values(expected_ask_base, ask_base_after,
                                       event_name=self.base_event)
        # endregion

        # region step 5
        self.rates_tile.press_pricing()
        self.rates_tile.check_color_of_pricing_button(expected_color=str(PricingButtonColor.yellow_button.value))
        # endregion

        # region step 6
        self.rates_tile.modify_client_tile(pips=self.pips_1)
        self.rates_tile.modify_spread(self.narrow_spread)
        row_values = self.rates_tile.extract_values_from_rates(self.bid_base, self.ask_base, row_number=2)
        expected_bid_base = str(round(int(bid_base_before) + 0.5, 1))
        expected_ask_base = str(round(int(ask_base_before) + 0.5, 1))
        bid_base_value = row_values[str(self.bid_base)]
        ask_base_value = row_values[str(self.ask_base)]
        self.rates_tile.compare_values(expected_bid_base, bid_base_value,
                                       event_name=self.base_event)
        self.rates_tile.compare_values(expected_ask_base, ask_base_value,
                                       event_name=self.base_event)
        # endregion

        # region step 7
        self.rates_tile.press_pricing()
        self.rates_tile.check_color_of_pricing_button(expected_color=str(PricingButtonColor.green_button.value))
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region step 8
        self.rates_tile.press_use_default()
        # endregion
        self.rates_tile.close_tile()
