import logging
from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, ExecutionReportConst, OrderReplyConst
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.java_api_wrappers.ors_messages.OrderModificationRequest import OrderModificationRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7670(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.qty = self.fix_message.get_parameter('OrderQtyData')['OrderQty']
        self.price = self.fix_message.get_parameter('Price')
        self.qty2 = str(int(self.qty) + 100)
        self.qty3 = str(int(self.qty2) + 50)
        self.trade_request = TradeEntryOMS(self.data_set)
        self.modify_request = OrderModificationRequest()
        self.dfd_batch = DFDManagementBatchOMS(self.data_set)
        self.washbook = self.data_set.get_washbook_account_by_name('washbook_account_2')

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # endregion
        # region create CO order
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = response[0].get_parameters()['OrderID']
        # endregion

        # region manual execution
        self.trade_request.set_default_trade(order_id, self.price)
        self.java_api_manager.send_message_and_receive_response(self.trade_request)
        # endregion

        # region check exec status
        exec_report_block = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value}, exec_report_block,
            'Check Execution of Order')
        # endregion

        # region amend order
        self.modify_request.set_default(self.data_set, order_id)
        self.modify_request.update_fields_in_component('OrderModificationRequestBlock',
                                                       {'OrdQty': self.qty2, 'WashBookAccountID': self.washbook,
                                                        'PosValidity': 'Delivery'})
        self.java_api_manager.send_message_and_receive_response(self.modify_request)
        # endregion

        # region check qty2
        ord_reply_block = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameter(
            JavaApiFields.OrdReplyBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.OrdQty.value: self.qty2 + '.0',
             JavaApiFields.LeavesQty.value: str(int(self.qty2) - 100) + '.0',
             JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_PFL.value},
            ord_reply_block,
            'Check order after amending')
        # endregion

        # region  second manual execution
        self.trade_request.set_default_trade(order_id, self.price)
        self.java_api_manager.send_message_and_receive_response(self.trade_request)
        # endregion

        # region check 2nd exec
        exec_report_block = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value,
             JavaApiFields.LeavesQty.value: '0.0'}, exec_report_block,
            'Check the second Execution of Order')
        # region

        # region complete order
        self.dfd_batch.set_default_complete(order_id)
        self.java_api_manager.send_message_and_receive_response(self.dfd_batch)
        # endregion

        # region check exec status
        exec_report_block = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.DoneForDay.value: OrderReplyConst.DoneForDay_YES.value,
             JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_RDY.value}, exec_report_block,
            'Check Order after completing')
        # endregion

        # region amend order

        self.modify_request.set_default(self.data_set, order_id)
        self.modify_request.update_fields_in_component('OrderModificationRequestBlock',
                                                       {'OrdQty': self.qty3, 'WashBookAccountID': self.washbook,
                                                        'PosValidity': 'Delivery'})
        self.java_api_manager.send_message_and_receive_response(self.modify_request)
        # endregion

        # region check qty3
        ord_reply_block = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameter(
            JavaApiFields.OrdReplyBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.OrdQty.value: self.qty3 + '.0',
             JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_PFL.value},
            ord_reply_block,
            'Check order after second amending')
        # endregion
