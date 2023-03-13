import logging
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca, basic_custom_actions
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.cs_message.ManualMatchExecToParentOrdersRequest import (
    ManualMatchExecToParentOrdersRequest,
)
from test_framework.java_api_wrappers.java_api_constants import (
    ExecutionReportConst,
    JavaApiFields,
    OrderReplyConst,
    SubmitRequestConst,
)
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.java_api_wrappers.ors_messages.UnMatchRequest import UnMatchRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


def print_message(message, responses):
    logger.info(message)
    for i in responses:
        logger.info(i)
        logger.info(i.get_parameters())


class QAP_T9178(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.qty = "100"
        self.price = "20"
        self.client = self.data_set.get_client("client_1")  # CLIENT1
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.order_submit_first = OrderSubmitOMS(data_set)
        self.order_submit_second = OrderSubmitOMS(data_set)
        self.execution_report = ExecutionReportOMS(self.data_set)
        self.trade_request = TradeEntryOMS(self.data_set)
        self.match_request = ManualMatchExecToParentOrdersRequest()
        self.unmatch_request = UnMatchRequest()
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1 - Create 1st DMA order
        self.order_submit_first.set_default_dma_limit()
        responses = self.java_api_manager.send_message_and_receive_response(self.order_submit_first)
        print_message("Create 1'st DMA order", responses)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        ord_id_first_dma = order_reply["OrdID"]
        # endregion

        # region Step 1 - Execute 1st DMA order and checking status
        self.execution_report.set_default_trade(ord_id_first_dma)
        responses = self.java_api_manager.send_message_and_receive_response(self.execution_report)
        print_message("Execute 1st DMA order", responses)
        execution_report_message = self.java_api_manager.get_last_message(
            ORSMessageType.ExecutionReport.value, filter_value=ExecutionReportConst.ExecType_TRD.value
        ).get_parameters()[JavaApiFields.ExecutionReportBlock.value]
        self.java_api_manager.compare_values(
            {
                JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value,
            },
            execution_report_message,
            "Step 1 - Checking the status of the 1st DMA order after execution",
        )
        exec_id_first_dma = execution_report_message["ExecID"]  # get first ExecID (EX)
        # endregion

        # region Step 1 - Create 2nd DMA order
        self.order_submit_second.set_default_dma_limit()
        responses = self.java_api_manager.send_message_and_receive_response(self.order_submit_second)
        print_message("Create 2nd DMA order", responses)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        ord_id_second_dma = order_reply["OrdID"]
        # endregion

        # region Step 1 - Execute 2nd DMA order and checking status
        self.execution_report.set_default_trade(ord_id_second_dma)
        responses = self.java_api_manager.send_message_and_receive_response(self.execution_report)
        print_message("Execute 2nd DMA order", responses)
        execution_report_message = self.java_api_manager.get_last_message(
            ORSMessageType.ExecutionReport.value, filter_value=ExecutionReportConst.ExecType_TRD.value
        ).get_parameters()[JavaApiFields.ExecutionReportBlock.value]
        self.java_api_manager.compare_values(
            {
                JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value,
            },
            execution_report_message,
            "Step 1 - Checking the status of the 2nd DMA order after execution",
        )
        exec_id_second_dma = execution_report_message["ExecID"]  # get second ExecID (EX)
        # endregion

        # region Step 2 - Create 1st Care order
        self.__create_care_order(self.order_submit_first, "1st")

        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        ord_id_first_care = order_reply["OrdID"]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
            order_reply,
            "Step 2 - Checking Status of 1st Care order",
        )
        # endregion

        # region Step 2 - Create 2nd Care order
        self.__create_care_order(self.order_submit_second, "2nd")

        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        ord_id_second_care = order_reply["OrdID"]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
            order_reply,
            "Step 2 - Checking Status of 2nd Care order",
        )
        # endregion

        # region Step 3-5 - Manual Match N to M 1st Care order
        self.match_request.set_default(ord_id_first_care, self.qty, exec_id_first_dma)
        responses = self.java_api_manager.send_message_and_receive_response(self.match_request)
        print_message("Manual Match N to M 1st Care", responses)

        exec_report = self.java_api_manager.get_last_message(
            ORSMessageType.ExecutionReport.value, ord_id_first_care
        ).get_parameter(JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values(
            {
                JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value,
                JavaApiFields.AvgPrice.value: str(float(self.price)),
                JavaApiFields.OrdQty.value: str(float(self.qty)),
                JavaApiFields.LeavesQty.value: "0.0",
            },
            exec_report,
            "Step 5 - Check the values of the 1st Care order after Manual Match",
        )
        exec_id_first_care = exec_report["ExecID"]
        # endregion

        # region Step 3-5 - Manual Match N to M 2nd Care order
        self.match_request.set_default(ord_id_second_care, self.qty, exec_id_second_dma)
        responses = self.java_api_manager.send_message_and_receive_response(self.match_request)
        print_message("Manual Match N to M 2nd Care", responses)

        exec_report = self.java_api_manager.get_last_message(
            ORSMessageType.ExecutionReport.value, ord_id_second_care
        ).get_parameter(JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values(
            {
                JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value,
                JavaApiFields.AvgPrice.value: str(float(self.price)),
                JavaApiFields.OrdQty.value: str(float(self.qty)),
                JavaApiFields.LeavesQty.value: "0.0",
            },
            exec_report,
            "Step 5 - Check the values of the 2nd Care order after Manual Match",
        )
        exec_id_second_care = exec_report["ExecID"]
        # endregion

        # region Step 6 - Mass Unmatch executions of Care order
        self.unmatch_request.set_default(self.data_set, exec_id_first_care, self.qty)
        un_matching_block_2: dict = {
            "VirtualExecID": exec_id_second_care,
            "UnMatchingQty": self.qty,
        }
        self.unmatch_request.get_parameters()["UnMatchRequestBlock"]["UnMatchingList"]["UnMatchingBlock"][0].pop(
            "SourceAccountID"
        )
        self.unmatch_request.get_parameters()["UnMatchRequestBlock"]["UnMatchingList"]["UnMatchingBlock"][0].pop(
            "PositionType"
        )
        self.unmatch_request.get_parameters()["UnMatchRequestBlock"]["UnMatchingList"]["UnMatchingBlock"].append(
            un_matching_block_2
        )
        responses = self.java_api_manager.send_message_and_receive_response(
            self.unmatch_request, {exec_id_first_care: exec_id_first_care, exec_id_second_care: exec_id_second_care}
        )
        print_message("Mass Unmatch executions", responses)

        # Check Execution report of the 1st Care order
        exec_report = self.java_api_manager.get_last_message(
            ORSMessageType.ExecutionReport.value, ord_id_first_care
        ).get_parameter(JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
            exec_report,
            "Step 6 - Checking the status of the 1st Care order after Mass Unmatch executions",
        )

        # Check Execution report of the 2nd Care order
        exec_report2 = self.java_api_manager.get_last_message(
            ORSMessageType.ExecutionReport.value, ord_id_second_care
        ).get_parameter(JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
            exec_report2,
            "Step 6 - Checking the status of the 2nd Care order after Mass Unmatch executions",
        )
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")

    def __create_care_order(self, order_submit, number_of_order: str):
        order_submit.set_default_care_limit(
            recipient=self.environment.get_list_fe_environment()[0].user_1,
            desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
            role=SubmitRequestConst.USER_ROLE_1.value,
        )
        order_submit.update_fields_in_component(
            "NewOrderSingleBlock", {"ClOrdID": basic_custom_actions.client_orderid(9)}
        )
        responses = self.java_api_manager.send_message_and_receive_response(order_submit)
        print_message(f"CREATE {number_of_order} CO", responses)
