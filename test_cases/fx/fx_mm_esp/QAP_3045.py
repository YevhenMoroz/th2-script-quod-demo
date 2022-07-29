from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.win_gui_wrappers.fe_trading_constant import RatesColumnNames
from test_framework.win_gui_wrappers.forex.client_rates_tile import ClientRatesTile


class QAP_3045(TestCase):
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)

        self.expected_base_1m = "0.1"
        self.expected_base_3m = "0"

        self.ask_base = RatesColumnNames.ask_base
        self.bid_base = RatesColumnNames.bid_base

        self.rates_tile = ClientRatesTile(self.test_id, self.session_id)

        self.silver = self.data_set.get_client_tier_by_name("client_tier_1")
        self.eur_gbp = self.data_set.get_symbol_by_name("symbol_3")
        self.eur_gbp_spot = self.eur_gbp + "-Spot"
        self.base_event = "base value validation"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 5
        self.rates_tile.crete_tile()
        self.rates_tile.modify_client_tile(instrument=self.eur_gbp_spot, client_tier=self.silver)

        row_values = self.rates_tile.extract_values_from_rates(self.bid_base, self.ask_base, row_number=1)
        actual_base_1m = row_values[str(self.ask_base)]
        row_values = self.rates_tile.extract_values_from_rates(self.bid_base, self.ask_base, row_number=2)
        actual_base_3m = row_values[str(self.ask_base)]
        self.rates_tile.compare_values(self.expected_base_1m, actual_base_1m,
                                       event_name=self.base_event)
        self.rates_tile.compare_values(self.expected_base_3m, actual_base_3m,
                                       event_name=self.base_event)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rates_tile.close_tile()
