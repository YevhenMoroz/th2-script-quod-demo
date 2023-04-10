import logging
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, BasketMessagesConst, OrderReplyConst
from test_framework.java_api_wrappers.oms.ors_messges.NewOrderListOMS import NewOrderListOMS
from test_framework.java_api_wrappers.ors_messages.ListCancelRequest import ListCancelRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


def print_message(message, responses):
    logger.info(message)
    for i in responses:
        logger.info(i)
        logger.info(i.get_parameters())


class QAP_T7429(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)

        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.list_creation_request = NewOrderListOMS(self.data_set)
        self.list_cancel_request = ListCancelRequest()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1 - Create Basket
        self.list_creation_request.set_default_order_list()
        responses = self.java_api_manager.send_message_and_receive_response(self.list_creation_request)
        print_message("Create Basket", responses)
        list_notify_block = self.java_api_manager.get_last_message(
            ORSMessageType.OrdListNotification.value
        ).get_parameter(JavaApiFields.OrdListNotificationBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.ListOrderStatus.value: BasketMessagesConst.ListOrderStatus_EXE.value},
            list_notify_block,
            "Step 1 - Checking Status for created Basket",
        )
        # endregion

        # region Get order_list_id, order_id
        order_list_id = list_notify_block["OrderListID"]
        ord_id1 = list_notify_block["OrdNotificationElements"]["OrdNotificationBlock"][0]["OrdID"]
        ord_id2 = list_notify_block["OrdNotificationElements"]["OrdNotificationBlock"][1]["OrdID"]
        # endregion

        # region Step 2 - Cancel Basket
        self.list_cancel_request.set_default(order_list_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.list_cancel_request)
        print_message("Cancel Basket", responses)
        list_notify_block = self.java_api_manager.get_last_message(
            ORSMessageType.OrdListNotification.value
        ).get_parameter(JavaApiFields.OrdListNotificationBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.ListOrderStatus.value: BasketMessagesConst.ListOrderStatus_CAN.value},
            list_notify_block,
            "Step 2 - Checking Status for canceled Basket",
        )

        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value, ord_id1).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        self.java_api_manager.compare_values(
            {
                JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_CXL.value,
                JavaApiFields.ExecType.value: OrderReplyConst.ExecType_CXL.value,
            },
            order_reply,
            "Step 2 - Checking the Status of the 1st CO",
        )

        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value, ord_id2).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        self.java_api_manager.compare_values(
            {
                JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_CXL.value,
                JavaApiFields.ExecType.value: OrderReplyConst.ExecType_CXL.value,
            },
            order_reply,
            "Step 2 - Checking the Status of the 2nd CO",
        )
        # endregion

        # region Check ExecutionReports
        list_of_ignored_fields: list = ["Account", "ExecID", "GatingRuleCondName", "LastQty", "GatingRuleName",
                                        "TransactTime", "Side", "AvgPx", "Parties", "SettlDate", "Currency",
                                        "TimeInForce", "HandlInst", "CxlQty", "LeavesQty", "CumQty", "LastPx",
                                        "OrdType", "OrderCapacity", "QtyType", "Price", "OrderListName", "Instrument",
                                        "OrderQtyData", "trailer", "header"]
        exec_report1 = FixMessageExecutionReportOMS(self.data_set)
        exec_report1.change_parameters({"OrderID": ord_id1, "ExecType": "4", "OrdStatus": "4", "ClOrdID": ord_id1})

        exec_report2 = FixMessageExecutionReportOMS(self.data_set)
        exec_report2.change_parameters({"OrderID": ord_id2, "ExecType": "4", "OrdStatus": "4", "ClOrdID": ord_id2})

        self.fix_verifier.check_fix_message(
            exec_report1, key_parameters=["OrderID", "OrdStatus", "ExecType"], ignored_fields=list_of_ignored_fields
        )
        self.fix_verifier.check_fix_message(
            exec_report2, key_parameters=["OrderID", "OrdStatus", "ExecType"], ignored_fields=list_of_ignored_fields
        )
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
