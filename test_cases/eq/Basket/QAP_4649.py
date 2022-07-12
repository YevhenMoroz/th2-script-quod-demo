import os
import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.oms.FixMessageOrderCancelRequestOMS import FixMessageOrderCancelRequestOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, ExecSts
from test_framework.win_gui_wrappers.oms.oms_basket_order_book import OMSBasketOrderBook
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderListOMS import FixMessageNewOrderListOMS
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

@try_except(test_id=Path(__file__).name[:-3])
class QAP_4649(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__), self.report_id)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.basket_book = OMSBasketOrderBook(self.test_id, self.session_id)
        self.cl_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.message = FixMessageNewOrderListOMS(self.data_set).set_default_order_list()
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.new_price = "456"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region Send NewOrderList
        self.fix_manager.send_message_fix_standard(self.message)
        order_id1 =self.order_book.extract_field(OrderBookColumns.order_id.value, row_number=1)
        order_id2 = self.order_book.extract_field(OrderBookColumns.order_id.value, row_number=2)
        # endregion
        # region Accept orders
        self.cl_inbox.accept_order()
        self.cl_inbox.accept_order()
        # endregion
        # region check order status
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id1]).check_order_fields_list(
        {OrderBookColumns.sts.value: ExecSts.open.value})
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id2]).check_order_fields_list(
            {OrderBookColumns.sts.value: ExecSts.open.value})
        # endregion
        # region Set-up parameters for ExecutionReports
        exec_report1 = FixMessageExecutionReportOMS(self.data_set).set_default_new_list(self.message)
        exec_report2 = FixMessageExecutionReportOMS(self.data_set).set_default_new_list(self.message, 1)
        # endregion
        # region Check ExecutionReports
        self.fix_verifier.check_fix_message_fix_standard(exec_report1)
        self.fix_verifier.check_fix_message_fix_standard(exec_report2)
        # endregion
        # region Send OrderCancelReplaceRequest
        rep_req = FixMessageOrderCancelRequestOMS().set_default_ord_list(self.message)
        self.fix_manager.send_message_fix_standard(rep_req)
        self.cl_inbox.accept_and_cancel_children()
        # endregion
        # region Set-up parameters for ExecutionReports
        exec_report3 = FixMessageExecutionReportOMS(self.data_set).set_default_canceled_list(self.message)
        exec_report3.change_parameter("ExpireDate", "*")
        exec_report3.change_parameter("SettlDate", "*")
        exec_report3.change_parameter("CxlQty", "*")
        # endregion
        # region Check ExecutionReports
        self.fix_verifier.check_fix_message_fix_standard(exec_report3)
        # endregion

