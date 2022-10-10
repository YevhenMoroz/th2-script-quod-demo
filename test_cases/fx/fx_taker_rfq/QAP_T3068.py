from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.win_gui_wrappers.forex.rfq_tile import RFQTile


class QAP_T3068(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.rfq_tile = RFQTile(self.test_id, self.session_id)
        self.qty = '5000000'
        self.qty1 = '1000000'
        self.qty_1m = '1m'
        self.qty2 = '1000'
        self.qty_1k = '1k'

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        eur_currency = self.data_set.get_currency_by_name('currency_eur')
        usd_currency = self.data_set.get_currency_by_name('currency_usd')
        default_currency = self.data_set.get_symbol_by_name('symbol_ndf_3')
        eur_usd_symbol = self.data_set.get_symbol_by_name('symbol_1')

        # region Step 1
        self.rfq_tile.crete_tile()
        self.rfq_tile.check_currency_pair(currency_pair=default_currency)
        # endregion
        # region Step 2
        # TODO Change currency pair from drop down
        # endregion
        # region Step 3
        self.rfq_tile.crete_tile().modify_rfq_tile(from_cur=eur_currency, to_cur=usd_currency)
        self.rfq_tile.check_currency_pair(currency_pair=eur_usd_symbol)
        # endregion
        # region Step 4
        self.rfq_tile.modify_rfq_tile(near_qty=self.qty)
        self.rfq_tile.check_qty(near_qty=self.qty)
        # endregion
        # region Step 5
        self.rfq_tile.modify_rfq_tile(near_qty=self.qty_1m)
        self.rfq_tile.check_qty(near_qty=self.qty1)
        self.rfq_tile.modify_rfq_tile(near_qty=self.qty_1k)
        self.rfq_tile.check_qty(near_qty=self.qty2)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rfq_tile.close_tile()
