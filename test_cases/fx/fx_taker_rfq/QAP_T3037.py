import random
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import spo_front_end, wk1_front_end
from custom.verifier import Verifier
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.win_gui_wrappers.forex.rfq_tile import RFQTile


class QAP_T3037(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.rfq_tile = RFQTile(self.test_id, self.session_id)
        self.qty = str(random.randint(1000000, 2000000))
        self.near_date = spo_front_end()
        self.far_date = wk1_front_end()
        self.blank_tenor = "No Far Tenor"
        self.left_eur_label = "Sell EUR Far"
        self.right_eur_label = "Buy EUR Far"
        self.left_usd_label = "Buy USD Far"
        self.right_usd_label = "Sell USD Far"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        eur_currency = self.data_set.get_currency_by_name('currency_eur')
        usd_currency = self.data_set.get_currency_by_name('currency_usd')
        tenor_spot = self.data_set.get_tenor_by_name('tenor_spot')
        tenor_1w = self.data_set.get_tenor_by_name('tenor_1w')
        venue = self.data_set.get_venue_by_name('venue_1')
        client = self.data_set.get_client_by_name("client_1")

        # region Step 1
        self.rfq_tile.crete_tile().modify_rfq_tile(from_cur=eur_currency, to_cur=usd_currency,
                                                   near_tenor=tenor_spot, far_tenor=tenor_1w, near_qty=self.qty,
                                                   client=client, single_venue=venue)
        # endregion
        # region Step 2
        self.rfq_tile.check_diff(near_date=spo_front_end(), far_date=wk1_front_end())
        # endregion
        # region Step 3
        self.rfq_tile.modify_rfq_tile(clear_far_tenor=True)
        self.rfq_tile.check_tenor(near_tenor=tenor_spot, far_tenor=self.blank_tenor)
        # endregion
        # region Step 4
        self.rfq_tile.modify_rfq_tile(from_cur=eur_currency, to_cur=usd_currency, near_tenor=tenor_spot,
                                      far_tenor=tenor_1w, near_qty=self.qty, client=client, single_venue=venue)
        self.rfq_tile.check_labels(left_label=self.left_eur_label, right_label=self.right_eur_label)
        # endregion
        # region Step 5
        self.rfq_tile.modify_rfq_tile(change_currency=True)
        self.rfq_tile.check_labels(left_label=self.left_usd_label, right_label=self.right_usd_label)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rfq_tile.close_tile()
