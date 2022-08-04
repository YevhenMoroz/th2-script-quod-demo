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

class QAP_T7688(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.price = '35'
        self.qty = '100'
        self.desk = environment.get_list_fe_environment()[0].desk_2
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.client = self.data_set.get_client_by_name('client_pt_1')
        self.lookup = self.data_set.get_lookup_by_name('lookup_1')

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region create CO order
        self.order_ticket.set_order_details(client=self.client, limit=self.price, qty=self.qty, tif=TimeInForce.DAY.value, recipient=self.desk,
                                       partial_desk=False
                                       )
        self.order_ticket.create_order(self.lookup)
        order_id = self.order_book.extract_field(OrderBookColumns.order_id.value)
        # endregion
        # region accept CO order
        self.client_inbox.reject_order()
        # endregion
        # region verify Sts of order
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).check_order_fields_list(
            {OrderBookColumns.sts.value: ExecSts.rejected.value})
        # endregion

