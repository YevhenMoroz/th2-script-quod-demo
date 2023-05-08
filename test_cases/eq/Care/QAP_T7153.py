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

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


def print_message(message, responses):
    logger.info(message)
    for i in responses:
        logger.info(i)
        logger.info(i.get_parameters())


class QAP_T7153(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.qty = "100"
        self.qty_care = "200"
        self.price = "20"
        self.client = self.data_set.get_client("client_1")  # CLIENT1
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.order_submit = OrderSubmitOMS(data_set)
        self.execution_report = ExecutionReportOMS(self.data_set)
        self.trade_request = TradeEntryOMS(self.data_set)
        self.match_request = ManualMatchExecToParentOrdersRequest()
        self.recipient = self.environment.get_list_fe_environment()[0].user_1
        self.desk = self.environment.get_list_fe_environment()[0].desk_ids[0]
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition - Create DMA order
        self.order_submit.set_default_dma_limit()
        responses = self.java_api_manager.send_message_and_receive_response(self.order_submit)
        print_message("Create DMA order", responses)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        ord_id_dma = order_reply["OrdID"]
        # endregion

        # region Precondition - Execute DMA order and checking status
        self.execution_report.set_default_trade(ord_id_dma)
        responses = self.java_api_manager.send_message_and_receive_response(
            self.execution_report, {ord_id_dma: ord_id_dma}
        )
        print_message("Execute DMA order", responses)
        execution_report_message = self.java_api_manager.get_last_message(
            ORSMessageType.ExecutionReport.value, filter_value=ExecutionReportConst.ExecType_TRD.value
        ).get_parameters()[JavaApiFields.ExecutionReportBlock.value]
        self.java_api_manager.compare_values(
            {
                JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value,
            },
            execution_report_message,
            "Precondition - Checking status of DMA order after execution",
        )
        exec_id_dma = execution_report_message["ExecID"]  # get ExecID (EX)
        # endregion

        # region Precondition - Create Care order
        self.order_submit.set_default_care_limit(
            recipient=self.recipient,
            desk=self.desk,
            role=SubmitRequestConst.USER_ROLE_1.value,
        )
        self.order_submit.update_fields_in_component(
            "NewOrderSingleBlock", {"ClOrdID": basic_custom_actions.client_orderid(9), "OrdQty": self.qty_care}
        )
        responses = self.java_api_manager.send_message_and_receive_response(self.order_submit)
        print_message("CREATE CO", responses)

        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        ord_id_care = order_reply["OrdID"]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
            order_reply,
            "Precondition - Checking Status of Care order",
        )
        # endregion

        # region Precondition - Child Care
        self.order_submit.set_default_child_care(recipient=self.recipient, desk=self.desk, parent_id=ord_id_care)
        self.order_submit.update_fields_in_component("NewOrderSingleBlock", {"OrdQty": self.qty_care})
        responses = self.java_api_manager.send_message_and_receive_response(self.order_submit)
        print_message("Create Child CO", responses)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        ord_id_child_care = order_reply["OrdID"]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
            order_reply,
            "Precondition - Checking Status of Child Care order",
        )
        # endregion

        # region Step 1-3 - Match 1 execution to N orders
        qty_to_match = str(int(self.qty_care) / 2)
        self.match_request.set_default(ord_id_child_care, qty_to_match, exec_id_dma)
        responses = self.java_api_manager.send_message_and_receive_response(self.match_request)
        print_message("Match action", responses)
        # endregion

        # region Checking values
        exec_report = self.java_api_manager.get_last_message(
            ORSMessageType.ExecutionReport.value, ord_id_child_care
        ).get_parameter(JavaApiFields.ExecutionReportBlock.value)
        self.java_api_manager.compare_values(
            {
                JavaApiFields.ExecType.value: ExecutionReportConst.ExecType_TRD.value,
                JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_PFL.value,
            },
            exec_report,
            "Step 3 - Checking that the Child care order is Partially Filled after Match action",
        )
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
