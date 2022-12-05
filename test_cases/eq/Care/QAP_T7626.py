import logging
import time
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
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


class QAP_T7626(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.qty = "100"
        self.price = "20"
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.client = self.data_set.get_client("client_1")  # CLIENT1
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.cd_ord_ack_batch_request = CDOrdAckBatchRequest()
        self.venue_client_names = self.data_set.get_venue_client_names_by_name("client_1_venue_1")  # XPAR_CLIENT1
        self.exec_destination = self.data_set.get_mic_by_name("mic_1")  # XPAR
        self.fix_env = self.environment.get_list_fix_environment()[0]
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        class_name = QAP_T7626
        # region Create CO order
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
        class_name.print_message("CREATE", responses)
        cd_order_notif_message = self.java_api_manager.get_last_message(CSMessageType.CDOrdNotif.value)
        cd_order_notif_id = cd_order_notif_message.get_parameter("CDOrdNotifBlock")["CDOrdNotifID"]
        order_notif_message = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value)
        ord_id = order_notif_message.get_parameter("OrdNotificationBlock")["OrdID"]
        cl_ord_id = order_notif_message.get_parameter("OrdNotificationBlock")["ClOrdID"]
        status = order_notif_message.get_parameter("OrdNotificationBlock")["TransStatus"]
        desk_id = order_notif_message.get_parameter("OrdNotificationBlock")["RecipientDeskID"]
        self.java_api_manager.compare_values(
            {OrderBookColumns.sts.value: OrderReplyConst.TransStatus_SEN.value},
            {OrderBookColumns.sts.value: status},
            "Comparing Status of Care order in Order_CDOrdNotif",
        )
        # endregion

        # region Accept CO order in Client Inbox
        self.cd_ord_ack_batch_request.set_default(ord_id, cd_order_notif_id, desk_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.cd_ord_ack_batch_request)
        class_name.print_message("ACK ORDER", responses)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value)
        status = order_reply.get_parameter("OrdReplyBlock")["TransStatus"]
        self.java_api_manager.compare_values(
            {OrderBookColumns.sts.value: OrderReplyConst.TransStatus_OPN.value},
            {OrderBookColumns.sts.value: status},
            "Comparing Status of Care order after Accept in Order_OrdReply",
        )
        # endregion

        # region Direct CO order
        self.order_submit.set_default_child_dma(ord_id)
        self.order_submit.update_fields_in_component(
            "NewOrderSingleBlock", {"ExecutionPolicy": "DMA", "OrdQty": self.qty}
        )
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side, self.venue_client_names, self.exec_destination, float(self.price)
            )
            responses = self.java_api_manager.send_message_and_receive_response(self.order_submit)
            class_name.print_message("DIRECT ORDER", responses)
        except Exception as e:
            logger.info(f"Your Exception is {e}")
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(nos_rule)
        # endregion

        # region Comparing Status of Child DMA after Direct in Order_OrdUpdate
        order_update_message = self.java_api_manager.get_last_message(ORSMessageType.OrdUpdate.value).get_parameters()[
            "OrdUpdateBlock"
        ]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
            order_update_message,
            "Comparing Status of Child DMA after Direct in Order_OrdUpdate",
        )
        # endregion

        # Comparing values of Child DMA after Direct in Order_OrdReply
        order_reply_message = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            "OrdReplyBlock"
        ]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value, "OrdQty": str(float(self.qty))},
            order_reply_message,
            "Comparing values of Child DMA after Direct in Order_OrdReply",
        )
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")

    @staticmethod
    def print_message(message, responses):
        logger.info(message)
        for i in responses:
            logger.info(i)
            logger.info(i.get_parameters())
