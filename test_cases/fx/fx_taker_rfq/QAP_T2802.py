from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.win_gui_wrappers.forex.rfq_tile import RFQTile


class QAP_T2802(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.rfq_tile = RFQTile(self.test_id, self.session_id)
        self.qty = '10000000'
        self.qty1 = '1000000'
        self.qty2 = '2000000'
        self.qty3 = '3000000'
        self.qty4 = '4000000'

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        eur_currency = self.data_set.get_currency_by_name('currency_eur')
        usd_currency = self.data_set.get_currency_by_name('currency_usd')
        near_tenor = self.data_set.get_tenor_by_name('tenor_spot')
        far_tenor = self.data_set.get_tenor_by_name('tenor_1w')
        client = self.data_set.get_client_by_name("client_1")

        # region Step 1
        self.rfq_tile.crete_tile().modify_rfq_tile(from_cur=eur_currency, to_cur=usd_currency, near_tenor=near_tenor,
                                                   far_tenor=far_tenor, client=client)
        self.rfq_tile.check_qty(near_qty=self.qty, far_qty=self.qty)
        # endregion
        # region Step 2
        self.rfq_tile.modify_rfq_tile(near_qty=self.qty2)
        self.rfq_tile.check_qty(near_qty=self.qty2, far_qty=self.qty2)
        # endregion
        # region Step 3
        self.rfq_tile.modify_rfq_tile(far_qty=self.qty3)
        self.rfq_tile.check_qty(near_qty=self.qty2, far_qty=self.qty3)
        # endregion
        # region Step 4
        self.rfq_tile.modify_rfq_tile(near_qty=self.qty4)
        self.rfq_tile.check_qty(near_qty=self.qty4, far_qty=self.qty3)
        # endregion
        # region Step 5
        self.rfq_tile.send_rfq()
        self.rfq_tile.cancel_rfq()
        self.rfq_tile.modify_rfq_tile(near_qty=self.qty1)
        self.rfq_tile.check_qty(near_qty=self.qty1, far_qty=self.qty1)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rfq_tile.close_tile()

