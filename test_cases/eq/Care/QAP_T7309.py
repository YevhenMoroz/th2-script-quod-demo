import logging
from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, ExecutionReportConst
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7309(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.trade_entry_request = TradeEntryOMS(self.data_set)
        self.price = self.fix_message.get_parameter('Price')

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create CO order
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = response[0].get_parameter("OrderID")
        # endregion

        # region manual execute
        self.trade_entry_request.set_default_trade(order_id, self.price)
        self.java_api_manager.send_message_and_receive_response(self.trade_entry_request)
        # endregion

        # region check execution
        exec_report_block = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value}, exec_report_block,
            'Check execution of order')
        exec_id = exec_report_block['ExecID']
        # endregion

        # region trade cancel
        self.trade_entry_request.set_default_cancel_execution(order_id, exec_id)
        self.java_api_manager.send_message_and_receive_response(self.trade_entry_request)
        # endregion

        # region check cancelled exec
        exec_report_block = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.ExecType.value: ExecutionReportConst.ExecType_CAN.value,
             JavaApiFields.PostTradeExecStatus.value: ExecutionReportConst.PostTradeExecStatus_NAL.value},
            exec_report_block,
            'Check execution of order after trade cancellation')
        # endregion
