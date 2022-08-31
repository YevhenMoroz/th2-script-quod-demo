from pathlib import Path
from custom import basic_custom_actions as bca
from test_cases.fx.fx_wrapper.common_tools import random_qty
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns as obc
from test_framework.win_gui_wrappers.fe_trading_constant import OrderType
from test_framework.win_gui_wrappers.fe_trading_constant import TimeInForce as tif
from test_framework.win_gui_wrappers.fe_trading_constant import ExecSts
from test_framework.win_gui_wrappers.forex.client_rates_tile import ClientRatesTile
from test_framework.win_gui_wrappers.forex.fx_order_book import FXOrderBook


class QAP_T2898(TestCase):
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None):
        super().__init__(report_id, session_id, data_set)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.rates_tile = None

        self.rates_tile = ClientRatesTile(self.test_id, self.session_id)
        self.order_book = FXOrderBook(self.test_id, self.session_id)

        self.client = self.data_set.get_client_tier_by_name("client_tier_1")
        self.client1 = self.data_set.get_client_by_name("client_mm_1")
        self.symbol = self.data_set.get_symbol_by_name("symbol_1")
        self.instr = self.symbol + "-1W"
        self.order_type = OrderType.market
        self.tif = tif.IOC
        self.exec_sts = ExecSts.partially_filled.value
        self.qty = random_qty(1, 2, 9)
        self.status = ExecSts.eliminated.value

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1
        self.rates_tile.crete_tile()
        self.rates_tile.modify_client_tile(instrument=self.instr, client_tier=self.client)
        # endregion

        # region step 2
        self.rates_tile.place_order(client=self.client1, qty=self.qty, tif=self.tif, order_type=self.order_type)
        # endregion

        # region step 3
        self.order_book.set_filter(
            [obc.qty.value, self.qty]).check_order_fields_list(
            {obc.qty.value: self.qty, obc.client_id.value: self.client1,
             obc.sts.value: self.status, obc.exec_sts.value: self.exec_sts})
        # endregion


    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rates_tile.close_tile()
