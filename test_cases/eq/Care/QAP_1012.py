import logging
import os
from pathlib import Path
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except

from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, ExecSts, TimeInForce
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

class QAP_1012(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, dataset):
        super().__init__(report_id, session_id, dataset)
        self.case_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.price = '100'
        self.qty = '100'
        self.user = Stubs.custom_config['qf_trading_fe_user']
        self.order_ticket = OMSOrderTicket(self.case_id, self.session_id)
        self.order_book = OMSOrderBook(self.case_id, self.session_id)
        self.client = self.data_set.get_client_by_name('client_pt_1')
        self.lookup = self.data_set.get_lookup_by_name('lookup_1')
        self.order_id = self.order_book.extract_field(OrderBookColumns.order_id.value)
        self.sts = self.order_book.extract_field(OrderBookColumns.sts.value)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region create CO order
        self.order_ticket.set_order_details(client=self.client, limit=self.price, qty=self.qty, tif=TimeInForce.DAY.value, recipient=self.user,
                                       partial_desk=True
                                       )
        self.order_ticket.create_order(self.lookup)
        self.order_book.scroll_order_book(1)
        # endregion
        # region accept CO order
        order_inbox = OMSClientInbox(self.case_id, self.session_id)
        order_inbox.accept_order(self.lookup, self.qty, self.price)
        # endregion
        # region verify Sts of order
        self.order_book.set_filter([OrderBookColumns.order_id.value, self.order_id])
        self.order_book.compare_values({OrderBookColumns.sts.value: ExecSts.open.value}, {OrderBookColumns.sts.value: self.sts},
                                  'Verifier data')
        # endregion

