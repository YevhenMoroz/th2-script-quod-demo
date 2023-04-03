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
)
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.OrderModificationRequest import OrderModificationRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


def print_message(message, responses):
    logger.info(message)
    for i in responses:
        logger.info(i)
        logger.info(i.get_parameters())


class QAP_T7204(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.qty = "100"
        self.price = "20"
        self.price_zero = "0"
        self.client = self.data_set.get_client("client_1")  # CLIENT1
        self.client2 = self.data_set.get_client("client_2")  # CLIENT2
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.submit_request = OrderSubmitOMS(self.data_set)
        self.submit_request_2 = OrderSubmitOMS(self.data_set)
        self.modification_request = OrderModificationRequest()
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1 - Create 1st Care order
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
        ord_id_first = order_reply["OrdID"]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value, "AccountGroupID": self.client},
            order_reply,
            "Step 1 - Comparing Status of 1st Care order",
        )
        # endregion

        # region Step 1 - Create 2nd Care order
        self.submit_request_2.set_default_care_limit(
            recipient=self.environment.get_list_fe_environment()[0].user_1,
            desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
            role=SubmitRequestConst.USER_ROLE_1.value,
        )
        self.submit_request_2.update_fields_in_component(
            "NewOrderSingleBlock",
            {
                "OrdQty": self.qty,
                "AccountGroupID": self.client,
                "Price": self.price,
            },
        )
        responses = self.java_api_manager.send_message_and_receive_response(self.submit_request_2)
        print_message("CREATE CO", responses)

        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        ord_id_second = order_reply["OrdID"]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value, "AccountGroupID": self.client},
            order_reply,
            "Step 1 - Comparing Status of 2nd Care order",
        )
        # endregion

        # region Step 2-4 - Mass Modify orders with Price=0
        self.__send_modif_request(ord_id_first, "1st")
        self.__send_modif_request(ord_id_second, "2nd")
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")

    def __send_modif_request(self, ord_id: str, number_of_order: str):
        self.modification_request.set_default(self.data_set, ord_id)
        self.modification_request.update_fields_in_component(
            "OrderModificationRequestBlock", {"Price": self.price_zero, "AccountGroupID": self.client2}
        )
        responses = self.java_api_manager.send_message_and_receive_response(self.modification_request)
        print_message(f"Mass Modify {number_of_order} order", responses)
        order_modif_reply = self.java_api_manager.get_last_message(
            ORSMessageType.OrderModificationReply.value
        ).get_parameters()[JavaApiFields.OrderModificationReplyBlock.value]
        self.java_api_manager.compare_values(
            {"ModifyStatus": "REJ", "FreeNotes": "'Price' (0) negative or zero"},
            order_modif_reply["OrdModify"],
            f"Step 4 - Checking that the Mass Modify request of {number_of_order} order is rejected",
        )

        message_reply = self.java_api_manager.get_last_message(
            ORSMessageType.OrderModificationReply.value
        ).get_parameters()["MessageReply"]
        self.java_api_manager.compare_values(
            {"ErrorMsg": "'Price' (0) negative or zero"},
            message_reply["MessageReplyBlock"][0],
            f"Step 4 - Checking ErrorMsg after Mass Modify {number_of_order} order with Price=0",
        )
