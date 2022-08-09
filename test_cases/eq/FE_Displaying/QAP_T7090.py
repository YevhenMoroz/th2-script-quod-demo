import logging
from pathlib import Path

from custom.basic_custom_actions import create_event
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class QAP_T7090(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set):
        super().__init__(report_id, session_id, data_set)
        self.qty = "2998"
        self.price = "2998"
        self.client = self.data_set.get_client_by_name("client_pt_1")
        self.account = self.data_set.get_account_by_name("client_pt_1_acc_3")
        self.venue_account = self.data_set.get_venue_client_account("client_pt_1_acc_3_venue_client_account")
        self.case_id = create_event(self.__class__.__name__, self.report_id)
        self.order_ticket = OMSOrderTicket(self.case_id, self.session_id)
        self.order_book = OMSOrderBook(self.case_id, self.session_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        self.order_ticket.set_order_details(client=self.client, limit=self.price, qty=self.qty,
                                            account=self.venue_account)
        self.order_ticket.create_order("VETO")
        actual_account = self.order_book.extract_field(OrderBookColumns.account_id.value)
        self.order_book.compare_values({OrderBookColumns.account_id.value: self.account},
                                       {OrderBookColumns.account_id.value: actual_account},
                                       "Verify Alloc Account")
