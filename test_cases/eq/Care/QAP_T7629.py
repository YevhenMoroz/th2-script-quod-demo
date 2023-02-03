import logging
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType, CSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.cs_message.CDOrdAckBatchRequest import CDOrdAckBatchRequest
from test_framework.java_api_wrappers.java_api_constants import (
    OrderReplyConst,
    JavaApiFields,
)
from test_framework.java_api_wrappers.oms.ors_messges.FixNewOrderSingleOMS import FixNewOrderSingleOMS
from test_framework.java_api_wrappers.ors_messages.HeldOrderAckRequest import HeldOrderAckRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


def print_message(message, responses):
    logger.info(message)
    for i in responses:
        logger.info(i)
        logger.info(i.get_parameters())


class QAP_T7629(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.qty = "100"
        self.price = "20"
        self.dummy_account = self.data_set.get_client_by_name("client_dummy")
        self.client = self.data_set.get_client("client_pt_1")  # MOClient
        self.security_account = self.data_set.get_account_by_name("client_pt_1_acc_1")  # MOClient_SA1
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.accept_request = CDOrdAckBatchRequest()
        self.nos = FixNewOrderSingleOMS(self.data_set)
        self.group_modify = HeldOrderAckRequest()
        self.note = "test note"
        self.route_id = self.data_set.get_route_id_by_name("route_1")
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1,2 - Create CO order
        self.nos.set_default_care_limit()
        self.nos.update_fields_in_component("NewOrderSingleBlock", {"ClientAccountGroupID": self.dummy_account})
        responses = self.java_api_manager.send_message_and_receive_response(self.nos)
        print_message("Create CO", responses)
        order_notif_message = self.java_api_manager.get_last_message(
            ORSMessageType.OrdNotification.value
        ).get_parameters()[JavaApiFields.OrderNotificationBlock.value]
        ord_id = order_notif_message["OrdID"]
        cl_ord_id = order_notif_message["ClOrdID"]
        desk_id = order_notif_message["RecipientDeskID"]
        self.java_api_manager.compare_values(
            {
                JavaApiFields.OrdStatus.value: OrderReplyConst.OrdStatus_HLD.value,
                JavaApiFields.AccountGroupID.value: self.dummy_account,
            },
            order_notif_message,
            "Step 1,2 - Comparing Status of Care order",
        )
        # endregion

        # region Step 3 - Group Modify Care order
        self.group_modify.set_default(ord_id, self.client)
        self.group_modify.update_fields_in_component(
            "HeldOrderAckBlock",
            {
                "PreTradeAllocationBlock": {
                    "PreTradeAllocationList": {
                        "PreTradeAllocAccountBlock": [{"AllocAccountID": self.security_account, "AllocQty": self.qty}]
                    }
                },
                "RouteID": self.route_id,
                "CDOrdFreeNotes": self.note,
            },
        )
        responses = self.java_api_manager.send_message_and_receive_response(self.group_modify)
        print_message("Group Modify", responses)
        cd_order_notif_message = self.java_api_manager.get_last_message(
            CSMessageType.CDOrdNotif.value
        ).get_parameters()["CDOrdNotifBlock"]
        cd_order_notif_id = cd_order_notif_message["CDOrdNotifID"]
        self.java_api_manager.compare_values(
            {
                JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_SEN.value,
            },
            cd_order_notif_message["OrdNotificationBlock"],
            "Comparing Status of Care order after Group Modify",
        )
        # endregion

        # Step 4 - region Accept CO order in Client Inbox
        self.accept_request.set_default(ord_id, cd_order_notif_id, desk_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.accept_request)
        print_message("Accept order", responses)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        self.java_api_manager.compare_values(
            {
                JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value,
                JavaApiFields.AccountGroupID.value: self.client,
                JavaApiFields.RouteID.value: str(self.route_id),
                JavaApiFields.SingleAllocAccountID.value: self.security_account,
                JavaApiFields.CDOrdFreeNotes.value: self.note,
            },
            order_reply,
            "Step 4 - Comparing Values of Care order after Group Modify",
        )
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
