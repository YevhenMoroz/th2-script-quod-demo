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
from test_framework.java_api_wrappers.oms.ors_messges.FixNewOrderSingleOMS import FixNewOrderSingleOMS
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


class QAP_T7687(TestCase):
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
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.accept_request = CDOrdAckBatchRequest()
        self.nos = FixNewOrderSingleOMS(self.data_set)
        self.java_api_connectivity2 = self.environment.get_list_java_api_environment()[0].java_api_conn_user2
        self.java_api_manager2 = JavaApiManager(self.java_api_connectivity2, self.test_id)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1-6 Create CO order
        self.nos.set_default_care_limit()
        self.nos.update_fields_in_component("NewOrderSingleBlock", {"ClientAccountGroupID": self.client})
        responses = self.java_api_manager.send_message_and_receive_response(self.nos)
        print_message("Create CO", responses)
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

        # region Step 10 - Accept Care order by User2
        self.accept_request.set_default(ord_id, cd_order_notif_id, desk_id)
        responses = self.java_api_manager2.send_message_and_receive_response(self.accept_request)
        print_message("Accept order by User2", responses)
        order_reply = self.java_api_manager2.get_last_message(ORSMessageType.OrdReply.value)
        status = order_reply.get_parameter("OrdReplyBlock")["TransStatus"]
        self.java_api_manager2.compare_values(
            {OrderBookColumns.sts.value: OrderReplyConst.TransStatus_OPN.value},
            {OrderBookColumns.sts.value: status},
            "Step 10 - Comparing Status of Care order after Accept by User2",
        )
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
