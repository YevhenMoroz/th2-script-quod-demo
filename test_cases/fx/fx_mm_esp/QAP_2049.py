from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.win_gui_wrappers.fe_trading_constant import RatesColumnNames
from test_framework.win_gui_wrappers.forex.client_rates_tile import ClientRatesTile


class QAP_2049(TestCase):
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)

        self.ask_base = RatesColumnNames.ask_base
        self.bid_base = RatesColumnNames.bid_base

        self.ask_effective = RatesColumnNames.ask_effective
        self.bid_effective = RatesColumnNames.bid_effective

        self.rates_tile = ClientRatesTile(self.test_id, self.session_id)

        self.palladium1 = self.data_set.get_client_tier_by_name("client_tier_4")
        self.usd_jpy = self.data_set.get_symbol_by_name("symbol_5")
        self.usd_jpy_spot = self.usd_jpy + "-Spot"
        self.base_event = "base value validation"
        self.effective_event = "effective value validation"

        self.expected_bid_base = "0"
        self.expected_ask_base = "0"
        self.expected_bid_effective = "0"
        self.expected_ask_effective = "0"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1
        self.rates_tile.crete_tile()
        self.rates_tile.modify_client_tile(instrument=self.usd_jpy_spot, client_tier=self.palladium1)
        # endregion

        # region step 3-4
        row_values = self.rates_tile.extract_values_from_rates(self.bid_base, self.ask_base, self.bid_effective,
                                                               self.ask_effective)
        bid_base = row_values[str(self.bid_base)]
        ask_base = row_values[str(self.ask_base)]
        bid_effective = row_values[str(self.bid_effective)]
        ask_effective = row_values[str(self.ask_effective)]

        self.rates_tile.compare_values(self.expected_bid_base, bid_base,
                                       event_name=self.base_event)
        self.rates_tile.compare_values(self.expected_ask_base, ask_base,
                                       event_name=self.base_event)
        self.rates_tile.compare_values(self.expected_bid_effective, bid_effective,
                                       event_name=self.effective_event)
        self.rates_tile.compare_values(self.expected_ask_effective, ask_effective,
                                       event_name=self.effective_event)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rates_tile.close_tile()
