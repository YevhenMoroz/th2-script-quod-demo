import logging
from datetime import datetime, timedelta
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType, CSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.cs_message.CDOrdAckBatchRequest import CDOrdAckBatchRequest
from test_framework.java_api_wrappers.java_api_constants import OrderReplyConst, JavaApiFields
from test_framework.java_api_wrappers.oms.ors_messges.FixNewOrderSingleOMS import FixNewOrderSingleOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


def print_message(message, responses):
    logger.info(message)
    for i in responses:
        logger.info(i)
        logger.info(i.get_parameters())


class QAP_T6865(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.qty = "100"
        self.price = "20"
        self.client = self.data_set.get_client("client_2")  # CLIENT2
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.accept_request = CDOrdAckBatchRequest()
        self.nos = FixNewOrderSingleOMS(self.data_set)
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.expire_date = (datetime.now() + timedelta(days=1)).strftime("%Y%m%d")
        self.expire_time = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S")
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 2 - Create CO order
        self.nos.set_default_care_limit()
        self.nos.update_fields_in_component(
            "NewOrderSingleBlock",
            {
                "ClientAccountGroupID": self.client,
                "TimeInForce": "GTD",
                "ExpireDate": self.expire_date,
                "ExpireTime": self.expire_time,
            },
        )
        responses = self.java_api_manager.send_message_and_receive_response(self.nos)
        print_message("Create CO", responses)
        cd_order_notif_message = self.java_api_manager.get_last_message(CSMessageType.CDOrdNotif.value)
        cd_order_notif_id = cd_order_notif_message.get_parameter(JavaApiFields.CDOrdNotifBlock.value)[
            JavaApiFields.CDOrdNotifID.value
        ]
        order_notif_message = self.java_api_manager.get_last_message(
            ORSMessageType.OrdNotification.value
        ).get_parameters()[JavaApiFields.OrderNotificationBlock.value]
        ord_id = order_notif_message["OrdID"]
        cl_ord_id = order_notif_message["ClOrdID"]
        desk_id = order_notif_message["RecipientDeskID"]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_SEN.value},
            order_notif_message,
            "Comparing Status of Care order",
        )
        # endregion

        # region Accept CO order in Client Inbox
        self.accept_request.set_default(ord_id, cd_order_notif_id, desk_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.accept_request)
        print_message("Accept order", responses)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        self.java_api_manager.compare_values(
            {
                JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value,
                "ExpireDate": self.expire_date,
                "ExpireTime": self.expire_time,
            },
            order_reply,
            "Step 2 - Checking Status, ExpireDate and ExpireTime of Care order after Accept",
        )
        expire_date_parent = order_reply["ExpireDate"]
        expire_time_parent = order_reply["ExpireTime"]
        # endregion

        # region Step 3,4 - Direct External Care
        self.order_submit.set_default_child_dma(ord_id)
        self.order_submit.update_fields_in_component(
            "NewOrderSingleBlock",
            {
                "AccountGroupID": self.client,
                "TimeInForce": "GTD",
                "ExpireDate": expire_date_parent,
                "ExpireTime": expire_time_parent,
                "ListingList": {"ListingBlock": [{"ListingID": self.data_set.get_listing_id_by_name("listing_3")}]},
                "InstrID": self.data_set.get_instrument_id_by_name("instrument_2"),
                "RouteList": {"RouteBlock": [{"RouteID": "24"}]},
            },
        )
        responses = self.java_api_manager.send_message_and_receive_response(self.order_submit)
        print_message("Direct External Care", responses)
        # endregion

        # region Comparing values after Direct External Care
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        self.java_api_manager.compare_values(
            {
                JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_SEN.value,
                "ExpireDate": expire_date_parent,
                "ExpireTime": expire_time_parent,
            },
            order_reply,
            "Step 4 - Checking that child's ExpireDate and ExpireTime are the same as the parent's",
        )
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
