import logging
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import (
    OrderReplyConst,
    JavaApiFields,
    SubmitRequestConst,
    ExecutionReportConst,
)
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
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


class QAP_T7523(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.qty = "100"
        self.price = "20"
        self.client = self.data_set.get_client("client_pt_1")  # MOClient
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.submit_request = OrderSubmitOMS(self.data_set)
        self.trade_request = TradeEntryOMS(self.data_set)
        self.complete_order = DFDManagementBatchOMS(self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1-7 - Create Care order
        self.submit_request.set_default_care_limit(
            recipient=self.environment.get_list_fe_environment()[0].user_1,
            desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
            role=SubmitRequestConst.USER_ROLE_1.value,
        )
        self.submit_request.update_fields_in_component(
            "NewOrderSingleBlock",
            {
                "OrdQty": self.qty,
                "AccountGroupID": self.client,
                "Price": self.price,
            },
        )
        responses = self.java_api_manager.send_message_and_receive_response(self.submit_request)
        print_message("CREATE CO", responses)

        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        ord_id = order_reply["OrdID"]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
            order_reply,
            "Step 7 - Comparing Status of Care order",
        )
        # endregion

        # region Step 8 - Execute Care order
        self.trade_request.set_default_trade(ord_id, self.price, self.qty)
        responses = self.java_api_manager.send_message_and_receive_response(self.trade_request)
        print_message("TRADE", responses)
        exec_report = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value
        ]
        exec_id: str = exec_report["ExecID"]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value},
            exec_report,
            "Step 8 - Comparing Execution status (TransExecStatus)",
        )
        # endregion

        # region Step 9 - Complete CO
        self.complete_order.set_default_complete(ord_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.complete_order)
        print_message("COMPLETE", responses)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        self.java_api_manager.compare_values(
            {
                JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_RDY.value,
                JavaApiFields.DoneForDay.value: OrderReplyConst.DoneForDay_YES.value,
            },
            order_reply,
            "Step 9 - Comparing PostTradeStatus after Complete",
        )
        # endregion

        # region Step 10 - Uncomplete Care order
        self.complete_order.set_default_uncomplete(ord_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.complete_order)
        print_message("UNCOMPLETE", responses)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        post_trade_status_is_empty = not JavaApiFields.PostTradeStatus.value in order_reply
        self.java_api_manager.compare_values(
            {"PostTradeStatusIsEmpty": True},
            {"PostTradeStatusIsEmpty": post_trade_status_is_empty},
            "Step 10 - Comparing that PostTradeStatus=empty after Uncomplete",
        )
        done_for_day_is_empty = not JavaApiFields.DoneForDay.value in order_reply
        self.java_api_manager.compare_values(
            {"DoneForDayIsEmpty": True},
            {"DoneForDayIsEmpty": done_for_day_is_empty},"Step 10 - Comparing that DoneForDay=empty after Uncomplete"
        )
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
