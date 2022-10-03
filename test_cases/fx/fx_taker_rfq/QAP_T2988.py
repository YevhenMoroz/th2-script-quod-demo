from pathlib import Path
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import ndf_spo_front_end, ndf_m1_front_end, ndf_m2_front_end, \
    fixing_ndf_m1_front_end, fixing_ndf_m2_front_end
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.win_gui_wrappers.forex.rfq_tile import RFQTile


class QAP_T2988(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.rfq_tile = RFQTile(self.test_id, self.session_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        usd_currency = self.data_set.get_currency_by_name('currency_usd')
        php_currency = self.data_set.get_currency_by_name('currency_php')
        tenor_spot = self.data_set.get_tenor_by_name('tenor_spot')
        tenor_1m = self.data_set.get_tenor_by_name('tenor_1m')
        tenor_2m = self.data_set.get_tenor_by_name('tenor_2m')

        # region Step 1
        self.rfq_tile.crete_tile().modify_rfq_tile(from_cur=usd_currency, to_cur=php_currency, near_tenor=tenor_spot)
        self.rfq_tile.check_date(near_date=ndf_spo_front_end())
        # endregion
        # region Step 2
        self.rfq_tile.modify_rfq_tile(near_tenor=tenor_1m)
        self.rfq_tile.check_date(near_date=ndf_m1_front_end())
        # endregion
        # region Step 3
        self.rfq_tile.check_maturity_date(near_date=fixing_ndf_m1_front_end())
        # endregion
        # region Step 4
        self.rfq_tile.modify_rfq_tile(near_tenor=tenor_2m)
        self.rfq_tile.check_date(near_date=ndf_m2_front_end())
        # endregion
        # region Step 5
        self.rfq_tile.check_maturity_date(near_date=fixing_ndf_m2_front_end())
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rfq_tile.close_tile()
