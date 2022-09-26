import logging
import os
from custom import basic_custom_actions as bca
from test_framework.fix_wrappers.FixManager import FixManager
from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import  OrderBookColumns, ExecSts
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7403(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.qty = '800'
        self.price = '40'
        self.last_mkt = "XASE"
        self.fix_message1 = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.fix_message1.change_parameters({'OrderQtyData': {'OrderQty': self.qty}, 'Price': self.price})
        self.cl_id1 = self.fix_message1.get_parameter('ClOrdID')
        self.fix_message2 = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.fix_message2.change_parameters({'OrderQtyData': {'OrderQty': self.qty}, 'Price': self.price, "Side": "2"})
        self.cl_id2 = self.fix_message1.get_parameter('ClOrdID')
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)



    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declarations
        # region create first CO
        response1 = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message1)
        self.client_inbox.accept_order()
        order_id1 = response1[0].get_parameter("OrderID")
        # endregion
        # region create second CO
        response2 = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message2)
        self.client_inbox.accept_order()
        order_id2 = response2[0].get_parameter("OrderID")
        # endregion
        # region manual cross
        self.order_book.manual_cross_orders([2,1], "10000", "100", self.last_mkt)
        # endregion
        # region check fields
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id1]).check_order_fields_list(
            {OrderBookColumns.exec_sts.value: ExecSts.filled.value, OrderBookColumns.qty.value: self.qty})
        # endregion
        # region check fields
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id2]).check_order_fields_list(
            {OrderBookColumns.exec_sts.value: ExecSts.filled.value, OrderBookColumns.qty.value: self.qty})
        # endregion
        # region Check ExecutionReports
        exec_report = FixMessageExecutionReportOMS(self.data_set).set_default_filled(self.fix_message1)
        # exec_report.change_parameters({'ClOrdID':self.cl_id1})
        self.fix_verifier.check_fix_message(exec_report, ['ClOrdID', self.cl_id1, "OrdStatus","2"])
        # endregion
        # region Check ExecutionReports
        exec_report = FixMessageExecutionReportOMS(self.data_set).set_default_filled(self.fix_message2)
        # exec_report.change_parameters({'ClOrdID': self.cl_id2})
        self.fix_verifier.check_fix_message(exec_report, ['ClOrdID', self.cl_id2, "OrdStatus","2"])
        # endregion

