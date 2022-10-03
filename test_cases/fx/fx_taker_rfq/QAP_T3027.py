from pathlib import Path
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import spo_front_end, wk1_front_end, wk2_front_end
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.win_gui_wrappers.forex.rfq_tile import RFQTile


class QAP_T3027(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.rfq_tile = RFQTile(self.test_id, self.session_id)
        self.qty1k = '1k'
        self.qty1m = '1m'
        self.qty1 = '1000'
        self.qty2 = '1000000'

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        eur_currency = self.data_set.get_currency_by_name('currency_eur')
        usd_currency = self.data_set.get_currency_by_name('currency_usd')
        eur_usd_symbol = self.data_set.get_symbol_by_name('symbol_1')
        tenor_spot = self.data_set.get_tenor_by_name('tenor_spot')
        tenor_1w = self.data_set.get_tenor_by_name('tenor_1w')
        tenor_2w = self.data_set.get_tenor_by_name('tenor_2w')

        # region Step 1-2
        self.rfq_tile.crete_tile().modify_rfq_tile(from_cur=eur_currency, to_cur=usd_currency,
                                                   near_tenor=tenor_spot)
        self.rfq_tile.check_currency_pair(currency_pair=eur_usd_symbol)
        # endregion
        # region Step 3
        self.rfq_tile.check_date(near_date=spo_front_end())
        # endregion
        # region Step 4
        self.rfq_tile.modify_rfq_tile(near_tenor=tenor_1w)
        self.rfq_tile.check_date(near_date=wk1_front_end())
        # endregion
        # region Step 5
        self.rfq_tile.modify_rfq_tile(near_tenor=tenor_2w)
        self.rfq_tile.check_date(near_date=wk2_front_end())
        # endregion
        # region Step 6
        self.rfq_tile.modify_rfq_tile(change_currency=True)
        self.rfq_tile.check_currency(currency=usd_currency)
        # endregion
        # region Step 7
        self.rfq_tile.modify_rfq_tile(near_qty=self.qty1k)
        self.rfq_tile.check_qty(near_qty=self.qty1)
        # endregion
        # region Step 8
        self.rfq_tile.modify_rfq_tile(near_qty=self.qty1m)
        self.rfq_tile.check_qty(near_qty=self.qty2)
        # endregion
        # region Step 9
        self.rfq_tile.modify_rfq_tile(near_tenor=tenor_spot)
        self.rfq_tile.check_date(near_date=spo_front_end())
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rfq_tile.close_tile()
