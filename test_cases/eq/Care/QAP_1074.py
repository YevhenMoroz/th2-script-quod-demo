import logging
import os

from custom import basic_custom_actions as bca
from stubs import Stubs
from test_framework.fix_wrappers.DataSet import MessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.SessionAlias import SessionAliasOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.TestCase import TestCase
from test_framework.win_gui_wrappers.base_main_window import BaseMainWindow
from test_framework.win_gui_wrappers.base_window import decorator_try_except
from test_framework.win_gui_wrappers.data_set import OrderBookColumns
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_1074(TestCase):
    def __init__(self, report_id, session_id, file_name):
        super().__init__(report_id, session_id)
        self.case_id = bca.create_event(os.path.basename(__file__), self.test_id)
        self.file_name = file_name
        self.ss_connectivity = SessionAliasOMS().ss_connectivity
        self.bs_connectivity = SessionAliasOMS().bs_connectivity

    def qap_1074(self):
        # region Declaration
        order_book = OMSOrderBook(self.case_id, self.session_id)
        base_window = BaseMainWindow(self.case_id, self.session_id)
        work_dir = Stubs.custom_config['qf_trading_fe_folder']
        username = Stubs.custom_config['qf_trading_fe_user']
        password = Stubs.custom_config['qf_trading_fe_password']
        fix_manager = FixManager(self.ss_connectivity)
        fix_message = FixMessageNewOrderSingleOMS().set_default_care_limit()
        fix_message.change_parameter('OrderQtyData', {'OrderQty': '150'})
        qty = fix_message.get_parameter('OrderQtyData')['OrderQty']
        price = fix_message.get_parameter('Price')
        # endregion

        # region open FE
        base_window.open_fe(self.report_id, work_dir, username, password, True)
        # endregion

        # region create CO order
        fix_manager.send_message_fix_standard(fix_message)
        order_id = order_book.extract_field(OrderBookColumns.order_id.value)
        # endregion

        # region accept CO order
        # order_book.scroll_order_book(1)
        order_inbox = OMSClientInbox(self.case_id, self.session_id)
        order_inbox.accept_order('O', 'M', 'S')
        # endregion

        # region compare values 1
        order_book.set_filter(['Order ID', order_id])
        exec_sts = order_book.extract_field(OrderBookColumns.exec_sts.value)
        order_book.manual_execution(qty=qty, price=price)
        order_book.set_filter(['Order ID', order_id])
        exec_sts = order_book.extract_field(OrderBookColumns.exec_sts.value)
        order_book.compare_values({'ExecSts': 'PartiallyFilled'}, {'Sts': exec_sts}, 'Compare values 1')
        # endregion

        # region amend order via FIX
        order_book.set_filter(['Order ID', order_id])
        fix_message.set_message_type(message_type=MessageType.OrderCancelReplaceRequest.value)
        fix_message.add_tag({'OrigClOrdID': fix_message.get_parameter('ClOrdID')})
        fix_message.change_parameter('OrderQtyData', {'OrderQty': '300'})
        fix_manager.send_message_fix_standard(fix_message)
        order_inbox.accept_modify_plus_child('O', 'M', 'S')
        # endregion

        # region compare values 2
        order_book.set_filter(['Order ID', order_id])
        qty = order_book.extract_field(OrderBookColumns.qty.value)
        order_book.compare_values({'Qty': '300'}, {'Qty': qty}, 'Compare values 2')
        # endregion

    @decorator_try_except(test_id=os.path.basename(__file__))
    def execute(self):
        self.qap_1074()
