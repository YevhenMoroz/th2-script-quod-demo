import logging
import os
from pathlib import Path

from custom import basic_custom_actions as bca
from stubs import Stubs
from test_framework.core.test_case import TestCase
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from test_framework.win_gui_wrappers.base_window import try_except
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, ExecSts
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket
from win_gui_modules.utils import set_session_id

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7687(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, dataset):
        super().__init__(report_id, session_id, dataset)
        self.case_id = bca.create_event(os.path.basename(__file__), self.report_id)
        self.order_book = OMSOrderBook(self.case_id, self.session_id)
        self.order_ticket = OMSOrderTicket(self.case_id, self.session_id)
        self.base_window = BaseMainWindow(self.case_id, self.session_id)
        self.client = self.data_set.get_client_by_name('client_pt_1')
        self.price = '100'
        self.qty = '50'
        self.work_dir = Stubs.custom_config['qf_trading_fe_folder']
        self.user = Stubs.custom_config['qf_trading_fe_user']
        self.session_id2 = set_session_id()
        self.base_window2 = BaseMainWindow(case_id=self.case_id, session_id=self.session_id2)
        self.order_id_first = self.order_book.extract_field(OrderBookColumns.order_id.value)
        self.order_inbox = OMSClientInbox(self.case_id, self.session_id2)
        self.order_book_2 = OMSOrderBook(self.case_id, session_id=self.session_id2)
        self.status = self.order_book_2.extract_field(OrderBookColumns.sts.value)
        self.order_id = self.order_book_2.extract_field(OrderBookColumns.order_id.value)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create CO order
        self.order_ticket.set_order_details(client=self.client, limit=self.price, qty=self.qty, tif='Day', recipient=self.user,
                                       partial_desk=True)
        self.order_ticket.create_order(self.data_set.get_lookup_by_name('lookup_1'))
        # endregion
        # region switch user
        self.base_window2.open_fe(self.report_id, folder=self.work_dir, user='ishevchenko', password='ishevchenko', is_open=False)
        self.base_window2.switch_user()
        # endregion
        # region accept CO order
        self.order_inbox.accept_order(self.data_set.get_lookup_by_name('lookup_1'), self.qty, self.price)
        # endregion
        # region verify values
        self.base_window2.compare_values({OrderBookColumns.sts.value: ExecSts.open.value, OrderBookColumns.order_id.value: self.order_id_first}, {OrderBookColumns.sts.value: self.status,
                                                                                  OrderBookColumns.order_id.value: self.order_id},
                                    "Event_Name")
        # endregion


