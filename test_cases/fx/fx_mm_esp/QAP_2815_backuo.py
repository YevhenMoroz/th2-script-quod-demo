from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.win_gui_wrappers.forex.client_rates_tile import ClientRatesTile


class QAP_2815(TestCase):
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.rates_tile = None

        self.rates_tile = ClientRatesTile(self.test_id, self.session_id)

        self.argentum = self.data_set.get_client_tier_by_name("client_tier_7")
        self.swedcust3 = self.data_set.get_client_by_name("client_mm_9")
        self.palladium1 = self.data_set.get_client_by_name("client_mm_4")
        self.eur_usd = self.data_set.get_symbol_by_name("symbol_1")
        self.gbp_usd = self.data_set.get_symbol_by_name("symbol_2")
        self.eur_usd_spot = self.eur_usd + "-Spot"
        self.gbp_usd_spot = self.gbp_usd + "-Spot"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1
        self.rates_tile.crete_tile()
        self.rates_tile.modify_client_tile(instrument=self.gbp_usd_spot, client_tier=self.argentum)
        # endregion

        # region step 2
        self.rates_tile.place_order(client=self.palladium1)
        # endregion

        # region step 3
        self.rates_tile.modify_client_tile(instrument=self.eur_usd_spot)
        # endregion

        # region step 4
        self.rates_tile.place_order(client=self.swedcust3)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rates_tile.close_tile()
