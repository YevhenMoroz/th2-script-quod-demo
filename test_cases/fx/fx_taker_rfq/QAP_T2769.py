from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.win_gui_wrappers.forex.rfq_tile import RFQTile


class QAP_T2769(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.rfq_tile = RFQTile(self.test_id, self.session_id)
        self.qty_1m = '1m'
        self.qty1m = '1000000'
        self.qty_1k = '1k'
        self.qty1k = '1000'
        self.qty_1b = '1b'
        self.qty1b = '1000000000'
        self.qty_1kk = '1kk'

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        near_tenor = self.data_set.get_tenor_by_name('tenor_spot')
        far_tenor = self.data_set.get_tenor_by_name('tenor_1w')

        # region Step 1
        self.rfq_tile.crete_tile().modify_rfq_tile(near_tenor=near_tenor, far_tenor=far_tenor, far_qty=self.qty_1m)
        self.rfq_tile.check_qty(far_qty=self.qty1m)
        # endregion
        # region Step 2
        self.rfq_tile.modify_rfq_tile(far_qty=self.qty_1k)
        self.rfq_tile.check_qty(far_qty=self.qty1k)
        # endregion
        # region Step 3
        self.rfq_tile.modify_rfq_tile(far_qty=self.qty_1b)
        self.rfq_tile.check_qty(far_qty=self.qty1b)
        # endregion
        # region Step 4
        self.rfq_tile.modify_rfq_tile(far_qty=self.qty_1kk)
        self.rfq_tile.check_qty(far_qty=self.qty1k)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rfq_tile.close_tile()

