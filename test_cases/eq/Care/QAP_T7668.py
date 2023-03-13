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
from test_framework.java_api_wrappers.java_api_constants import OrderReplyConst, JavaApiFields
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


def print_message(message, responses):
    logger.info(message)
    for i in responses:
        logger.info(i)
        logger.info(i.get_parameters())


class QAP_T7668(TestCase):
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
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.cd_ord_ack_batch_request = CDOrdAckBatchRequest()
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1-6 Create CO order
        self.order_submit.set_default_care_limit(
            desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
        )
        self.order_submit.update_fields_in_component(
            "NewOrderSingleBlock",
            {
                "OrdQty": self.qty,
                "AccountGroupID": self.client,
                "Price": self.price,
            },
        )
        responses = self.java_api_manager.send_message_and_receive_response(self.order_submit)
        print_message("CREATE CO", responses)
        cd_order_notif_message = self.java_api_manager.get_last_message(CSMessageType.CDOrdNotif.value)
        cd_order_notif_id = cd_order_notif_message.get_parameter("CDOrdNotifBlock")["CDOrdNotifID"]
        order_notif_message = self.java_api_manager.get_last_message(
            ORSMessageType.OrdNotification.value
        ).get_parameters()[JavaApiFields.OrderNotificationBlock.value]
        ord_id = order_notif_message["OrdID"]
        cl_ord_id = order_notif_message["ClOrdID"]
        desk_id = order_notif_message["RecipientDeskID"]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_SEN.value},
            order_notif_message,
            "Step 6 - Comparing Status of Care order",
        )
        # endregion

        # region Accept CO order in Client Inbox
        self.cd_ord_ack_batch_request.set_default(ord_id, cd_order_notif_id, desk_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.cd_ord_ack_batch_request)
        print_message("ACK ORDER", responses)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value)
        status = order_reply.get_parameter("OrdReplyBlock")["TransStatus"]
        self.java_api_manager.compare_values(
            {OrderBookColumns.sts.value: OrderReplyConst.TransStatus_OPN.value},
            {OrderBookColumns.sts.value: status},
            "Comparing Status of Care order after Accept",
        )
        # endregion

        # region Step 8 - Direct Care order
        self.order_submit.set_default_child_dma(parent_id=ord_id)
        self.order_submit.update_fields_in_component(
            "NewOrderSingleBlock", {"ExecutionPolicy": "DMA", "OrdQty": self.qty}
        )
        self.order_submit.remove_parameters(["CDOrdAssignInstructionsBlock"])
        self.order_submit.remove_fields_from_component(
            "NewOrderSingleBlock", ["SettlCurrency", "ExecutionOnly", "BookingType", "ClientInstructionsOnly"]
        )
        responses = self.java_api_manager.send_message_and_receive_response(self.order_submit)
        print_message("Direct Care order", responses)
        # endregion

        # region Step 9 - Comparing values of Child DMA after Direct
        order_reply_message = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            "OrdReplyBlock"
        ]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_SEN.value, "OrdQty": str(float(self.qty))},
            order_reply_message,
            "Step 9 - Comparing values of Child DMA after Direct",
        )
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
