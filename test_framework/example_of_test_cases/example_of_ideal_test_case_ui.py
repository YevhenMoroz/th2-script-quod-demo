from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.win_gui_wrappers.fe_trading_constant import ExecSts
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns as ob
from test_framework.win_gui_wrappers.fe_trading_constant import RatesColumnNames
from test_framework.win_gui_wrappers.forex.fx_order_book import FXOrderBook
from test_framework.win_gui_wrappers.forex.rfq_tile import RFQTile


class QAP_Example(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.rfq_tile = RFQTile(self.test_id, self.session_id)
        self.order_book = FXOrderBook(self.test_id, self.session_id)
        self.case_from_currency = data_set.get_currency_by_name("currency_eur")
        self.case_to_currency = data_set.get_currency_by_name("currency_usd")
        self.case_qty = "1000000"
        self.case_near_tenor = RatesColumnNames.ask_spot
        self.fix_env = environment.get_list_fix_environment()[0]
        self.sell_side = self.fix_env.sell_side

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Variables
        client = self.data_set.get_client_by_name("client_1")
        venue = self.data_set.get_venue_by_name("venue_1")
        # endregion
        # region Step1
        self.rfq_tile.crete_tile().modify_rfq_tile(from_cur=self.case_from_currency, to_cur=self.case_to_currency,
                                                   near_qty=self.case_qty, near_tenor=self.case_near_tenor,
                                                   client=client, single_venue=venue)
        self.rfq_tile.send_rfq()
        self.rfq_tile.place_order(self.sell_side)
        # endregion
        # region Step2
        self.order_book.check_order_fields_list({ob.sts.value: ExecSts.terminated.value})
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rfq_tile.close_tile()
