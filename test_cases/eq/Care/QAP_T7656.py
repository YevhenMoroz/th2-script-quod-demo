import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.fix_wrappers.oms.FixMessageOrderCancelRequestOMS import FixMessageOrderCancelRequestOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.cs_message.CDOrdAckBatchRequest import CDOrdAckBatchRequest
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, ExecutionReportConst
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7656(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.accept_request = CDOrdAckBatchRequest()
        self.ss_connectivity = self.environment.get_list_fix_environment()[0].sell_side
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.nos = FixMessageNewOrderSingleOMS(self.data_set)
        self.cancel_request = FixMessageOrderCancelRequestOMS()

        self.trd_request = TradeEntryOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition
        self.nos.set_default_care_limit()
        self.fix_manager.send_message_and_receive_response_fix_standard(self.nos)
        ord_id = self.fix_manager.get_last_message("ExecutionReport").get_parameter("OrderID")
        self.trd_request.set_default_trade(ord_id, exec_qty="1")
        self.java_api_manager.send_message_and_receive_response(self.trd_request)
        execution_report_co_order = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value). \
            get_parameters()[JavaApiFields.ExecutionReportBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_PFL.value},
            execution_report_co_order, 'Checking execution')
        # endregion
        # region Step 1-3
        self.cancel_request.set_default(self.nos)
        self.fix_manager.send_message_and_receive_response_fix_standard(self.cancel_request)
        exec_rep = self.fix_manager.get_last_message("ExecutionReport").get_parameters()
        self.fix_manager.compare_values({JavaApiFields.ExecType.value: "4"}, exec_rep, "Check cancel")
        # endregion
