import time
from pathlib import Path

from custom import basic_custom_actions as bca
from test_cases.fx.fx_wrapper.common_tools import random_qty
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, Status, Side, QuoteBookColumns, \
    QuoteStatus, QuoteRequestBookColumns, TradeBookColumns
from test_framework.win_gui_wrappers.forex.client_rfq_tile import ClientRFQTile
from test_framework.win_gui_wrappers.forex.fx_dealer_intervention import FXDealerIntervention
from test_framework.win_gui_wrappers.forex.fx_order_book import FXOrderBook
from test_framework.win_gui_wrappers.forex.fx_quote_book import FXQuoteBook
from test_framework.win_gui_wrappers.forex.fx_trade_book import FXTradeBook


class QAP_T2606(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.quote_book = FXQuoteBook(self.test_id, self.session_id)

        self.qty_column = TradeBookColumns.qty.value

        self.client_rfq_tile = ClientRFQTile(self.test_id, self.session_id)
        self.dealer_intervention = FXDealerIntervention(self.test_id, self.session_id)
        self.client = self.data_set.get_client_by_name("client_mm_1")
        self.gbp_cur = self.data_set.get_currency_by_name("currency_gbp")
        self.usd_cur = self.data_set.get_currency_by_name("currency_usd")
        self.spot_tenor = self.data_set.get_tenor_by_name("tenor_spot")
        self.qty_for_di = random_qty(2, 3, 8)
        self.quote_sts_column = QuoteBookColumns.quote_status.value
        self.quote_status_column = QuoteRequestBookColumns.status.value
        self.bid_size_column = QuoteBookColumns.bid_size.value
        self.accepted_sts = QuoteStatus.accepted.value
        self.new_sts = Status.new.value

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        # TODO Need send QuoteRequest through FIX
        self.client_rfq_tile.modify_rfq_tile(from_cur=self.gbp_cur, to_cur=self.usd_cur, client=self.client,
                                             clientTier=self.client, near_qty=self.qty_for_di,
                                             near_tenor=self.spot_tenor)
        self.client_rfq_tile.send_rfq()
        # endregion

        # region Step 2
        self.dealer_intervention.set_list_filter([self.qty_column, self.qty_for_di]).check_unassigned_fields({
            self.quote_status_column: self.new_sts})
        self.dealer_intervention.assign_quote()
        self.dealer_intervention.estimate_quote()
        time.sleep(3)
        self.dealer_intervention.send_quote()
        self.dealer_intervention.close_window()
        # TODO Need check Quote through FIX
        self.quote_book.set_filter([self.bid_size_column, self.qty_for_di]).check_quote_book_fields_list({
            self.quote_sts_column: self.accepted_sts})
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.client_rfq_tile.close_tile()
