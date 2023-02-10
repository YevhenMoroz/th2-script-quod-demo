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


class QAP_T10363(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.qty = "100"
        self.price = "20"
        self.client = self.data_set.get_client("client_1")  # CLIENT1
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.submit_request = OrderSubmitOMS(self.data_set)
        self.submit_request_2 = OrderSubmitOMS(self.data_set)
        self.washbook_carewb = self.data_set.get_washbook_account_by_name("washbook_account_2")
        self.modification_request = OrderModificationRequest()
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1 - Create first Care order
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
                "WashBookAccountID": self.washbook_carewb,
            },
        )
        responses = self.java_api_manager.send_message_and_receive_response(self.submit_request)
        print_message("CREATE CO", responses)

        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        ord_id_first = order_reply["OrdID"]
        self.java_api_manager.compare_values(
            {
                JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value,
                JavaApiFields.WashBookAccountID.value: self.washbook_carewb,
            },
            order_reply,
            "Step 1 - Comparing Status of first Care order",
        )
        # endregion

        # region Step 1 - Create second Care order
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
                "WashBookAccountID": self.washbook_carewb,
            },
        )
        responses = self.java_api_manager.send_message_and_receive_response(self.submit_request_2)
        print_message("CREATE CO", responses)

        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        ord_id_second = order_reply["OrdID"]
        self.java_api_manager.compare_values(
            {
                JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value,
                JavaApiFields.WashBookAccountID.value: self.washbook_carewb,
            },
            order_reply,
            "Step 1 - Comparing Status of second Care order",
        )
        # endregion

        # region Step 2,3 - Mass Modify orders and filling Misc fields
        self.__send_modif_requst(ord_id_first, "first")
        self.__send_modif_requst(ord_id_second, "second")
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")

    def __send_modif_requst(self, ord_id: str, number_of_order: str):
        self.modification_request.set_default(self.data_set, ord_id)
        misc_block: dict = {
            "OrdrMisc0": "1",
            "OrdrMisc1": "2",
            "OrdrMisc2": "3",
            "OrdrMisc3": "4",
            "OrdrMisc4": "5",
            "OrdrMisc5": "6",
            "OrdrMisc6": "7",
            "OrdrMisc7": "8",
            "OrdrMisc8": "9",
            "OrdrMisc9": "10",
        }
        self.modification_request.update_fields_in_component(
            "OrderModificationRequestBlock", {"WashBookAccountID": self.washbook_carewb, "OrdrMiscBlock": misc_block}
        )
        responses = self.java_api_manager.send_message_and_receive_response(self.modification_request)
        print_message(f"Modify {number_of_order} order", responses)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        self.java_api_manager.compare_values(
            {"WashBookAccountID": self.washbook_carewb},
            order_reply,
            f"Step 3 - Comparing WashBook of {number_of_order} order after Mass Modify",
        )
        self.java_api_manager.compare_values(
            misc_block,
            order_reply["OrdrMiscBlock"],
            f"Step 3 - Comparing Misc fields of {number_of_order} order after Mass Modify",
        )
        # endregion
