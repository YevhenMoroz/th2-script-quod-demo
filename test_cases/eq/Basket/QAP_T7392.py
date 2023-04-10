import logging
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, BasketMessagesConst, OrderReplyConst
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.NewOrderListOMS import NewOrderListOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


def print_message(message, responses):
    logger.info(message)
    for i in responses:
        logger.info(i)
        logger.info(i.get_parameters())


class QAP_T7392(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.list_creation_request = NewOrderListOMS(self.data_set)
        self.complete_order = DFDManagementBatchOMS(self.data_set)

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

        # region Step 2 - Complete 1st Care order from basket
        self.complete_order.set_default_complete(ord_id1)
        responses = self.java_api_manager.send_message_and_receive_response(self.complete_order)
        print_message("COMPLETE 1st CO", responses)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            "OrdReplyBlock"
        ]
        self.java_api_manager.compare_values(
            {
                JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_RDY.value,
                JavaApiFields.DoneForDay.value: OrderReplyConst.DoneForDay_YES.value,
                JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value,
            },
            order_reply,
            "Step 2 - Check DoneForDay for 1st Care order from Basket",
        )
        # endregion

        # region Step 3 - Complete Basket
        self.complete_order.set_default_complete(ord_id2)
        responses = self.java_api_manager.send_message_and_receive_response(self.complete_order)
        print_message("COMPLETE Basket", responses)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            "OrdReplyBlock"
        ]
        self.java_api_manager.compare_values(
            {
                JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_RDY.value,
                JavaApiFields.DoneForDay.value: OrderReplyConst.DoneForDay_YES.value,
                JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value,
            },
            order_reply,
            "Step 3 - Check DoneForDay for 2nd Care order from Basket",
        )
        # endregion

        # region Step 4 - Uncomplete 1st Care order
        self.complete_order.set_default_uncomplete(ord_id1)
        responses = self.java_api_manager.send_message_and_receive_response(self.complete_order)
        print_message("UNCOMPLETE 1st CO", responses)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        post_trade_status_is_empty = JavaApiFields.PostTradeStatus.value not in order_reply
        self.java_api_manager.compare_values(
            {"PostTradeStatusIsEmpty": True},
            {"PostTradeStatusIsEmpty": post_trade_status_is_empty},
            "Step 4 - Checking that PostTradeStatus=empty after Uncomplete for 1st CO",
        )
        done_for_day_is_empty = JavaApiFields.DoneForDay.value not in order_reply
        self.java_api_manager.compare_values(
            {"DoneForDayIsEmpty": True},
            {"DoneForDayIsEmpty": done_for_day_is_empty},
            "Step 4 - Checking that DoneForDay=empty after Uncomplete for 1st CO",
        )
        # endregion

        # region Step 5 - Uncomplete Basket
        self.complete_order.set_default_uncomplete(ord_id2)
        responses = self.java_api_manager.send_message_and_receive_response(self.complete_order)
        print_message("UNCOMPLETE Basket", responses)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        post_trade_status_is_empty = JavaApiFields.PostTradeStatus.value not in order_reply
        self.java_api_manager.compare_values(
            {"PostTradeStatusIsEmpty": True},
            {"PostTradeStatusIsEmpty": post_trade_status_is_empty},
            "Step 5 - Checking that PostTradeStatus=empty after for 2nd CO after Uncomplete Basket",
        )
        done_for_day_is_empty = JavaApiFields.DoneForDay.value not in order_reply
        self.java_api_manager.compare_values(
            {"DoneForDayIsEmpty": True},
            {"DoneForDayIsEmpty": done_for_day_is_empty},
            "Step 5 - Checking that DoneForDay=empty after for 2nd CO after Uncomplete Basket",
        )
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
