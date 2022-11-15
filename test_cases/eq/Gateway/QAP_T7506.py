import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.win_gui_wrappers.java_api_constants import SubmitRequestConst

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
seconds, nanos = timestamps()


class QAP_T7506(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.bo_connectivity = self.fix_env.drop_copy
        self.fix_verifier_dc = FixVerifier(self.bo_connectivity, self.test_id)
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.ord_sub_message = OrderSubmitOMS(self.data_set)
        self.trade_entry_message = TradeEntryOMS(self.data_set)
        self.complete_order = DFDManagementBatchOMS(self.data_set)
        self.desk_id = self.environment.get_list_fe_environment()[0].desk_ids[1]
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create order
        responses = self.java_api_manager.send_message_and_receive_response(
            self.ord_sub_message.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                        desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                        role=SubmitRequestConst.USER_ROLE_1.value))
        self.return_result(responses, ORSMessageType.OrdReply.value)
        parent_order_id = self.result.get_parameter('OrdReplyBlock')['OrdID']
        client_order_id = self.result.get_parameter('OrdReplyBlock')['ClOrdID']
        # endregion
        # region create child order
        responses = self.java_api_manager.send_message_and_receive_response(
            self.ord_sub_message.set_default_child_care(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                        desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                        role=SubmitRequestConst.USER_ROLE_1.value,
                                                        parent_id=parent_order_id))
        self.return_result(responses, ORSMessageType.OrdReply.value)
        child_order_id = self.result.get_parameter('OrdReplyBlock')['RequestID']
        qty = self.result.get_parameter('OrdReplyBlock')['OrdQty']
        price = self.result.get_parameter('OrdReplyBlock')['Price']
        # endregion
        # region trade child order
        self.trade_entry_message.set_default_trade(child_order_id, price, qty)
        responses = self.java_api_manager.send_message_and_receive_response(self.trade_entry_message)
        self.return_result(responses, ORSMessageType.ExecutionReport.value)
        exec_id = self.result.get_parameter('ExecutionReportBlock')['ExecID']
        # endregion
        # region check exec report
        list_of_ignore_fields = ['Account', 'ExecID', 'OrderQtyData', 'LastQty', 'TransactTime', 'Side', 'AvgPx',
                                 'QuodTradeQualifier', 'BookID', 'SettlCurrency', "SettlDate", 'Currency',
                                 'TimeInForce', 'PositionEffect', 'TradeDate', 'HandlInst', 'LeavesQty', 'NoParty',
                                 'CumQty', 'LastPx', 'OrdType', 'SecondaryOrderID', 'tag5120', 'LastMkt',
                                 'OrderCapacity', 'QtyType', 'ExecBroker', 'Price', 'VenueType', 'Instrument',
                                 'ExDestination', 'GrossTradeAmt']
        change_parameters = {
            "ExecType": "F", "OrdStatus": "2", "ClOrdID": client_order_id, "OrderID": parent_order_id,
            "SecondaryExecID": exec_id}
        fix_execution_report = FixMessageExecutionReportOMS(self.data_set, change_parameters)
        self.fix_verifier_dc.check_fix_message_fix_standard(fix_execution_report, ignored_fields=list_of_ignore_fields)
        # endregion

    def return_result(self, responses, message_type):
        for response in responses:
            if response.get_message_type() == message_type:
                self.result = response
