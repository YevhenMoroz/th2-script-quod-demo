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
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.cs_message.CDOrdAckBatchRequest import CDOrdAckBatchRequest
from test_framework.java_api_wrappers.java_api_constants import OrderReplyConst, JavaApiFields, SubmitRequestConst
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.CancelOrderRequest import CancelOrderRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


def print_message(message, responses):
    logger.info(message)
    for i in responses:
        logger.info(i)
        logger.info(i.get_parameters())


class QAP_T8696(TestCase):
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
        self.java_api_connectivity2 = self.environment.get_list_java_api_environment()[0].java_api_conn_user2
        self.java_api_manager2 = JavaApiManager(self.java_api_connectivity2, self.test_id)
        self.submit_request = OrderSubmitOMS(self.data_set)
        self.cancel_request = CancelOrderRequest()
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_verifier = FixVerifier(self.fix_env.buy_side, self.test_id)
        self.rule_manager = RuleManager(Simulators.equity)
        self.venue = self.data_set.get_mic_by_name("mic_1")
        self.venue_client_names = self.data_set.get_venue_client_names_by_name("client_2_venue_1")
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1 - Create CO order by User 1
        self.submit_request.set_default_care_limit(
            recipient=self.environment.get_list_fe_environment()[0].user_1,
            desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
            role=SubmitRequestConst.USER_ROLE_1.value,
        )
        self.submit_request.update_fields_in_component(
            "NewOrderSingleBlock",
            {"OrdQty": self.qty, "Price": self.price, "AccountGroupID": self.client},
        )
        responses = self.java_api_manager2.send_message_and_receive_response(self.submit_request)
        print_message("CREATE", responses)
        cd_order_notif_message = self.java_api_manager2.get_last_message(CSMessageType.CDOrdNotif.value)
        cd_order_notif_id = cd_order_notif_message.get_parameter("CDOrdNotifBlock")["CDOrdNotifID"]
        order_notif_message = self.java_api_manager2.get_last_message(
            ORSMessageType.OrdNotification.value
        ).get_parameters()[JavaApiFields.OrderNotificationBlock.value]
        ord_id = order_notif_message["OrdID"]
        cl_ord_id = order_notif_message["ClOrdID"]
        desk_id = order_notif_message["RecipientDeskID"]
        self.java_api_manager2.compare_values(
            {
                JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_SEN.value,
            },
            order_notif_message,
            "Step 1 - Comparing Status of Care order",
        )
        # endregion

        # region Step 1 - Accept CO order in Client Inbox by User2
        self.accept_request.set_default(ord_id, cd_order_notif_id, desk_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.accept_request)
        print_message("Accept order", responses)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        self.java_api_manager.compare_values(
            {
                JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value,
            },
            order_reply,
            "Step 1 - Comparing Status of Care order after Accept by User2",
        )
        # endregion

        # region 2 - Create a Сhild CO by User_1
        self.submit_request.set_default_child_care(desk=desk_id, parent_id=ord_id)
        responses = self.java_api_manager2.send_message_and_receive_response(self.submit_request)
        print_message("Create Child CO", responses)
        cd_ord_notif_message = self.java_api_manager2.get_last_message(CSMessageType.CDOrdNotif.value).get_parameters()[
            JavaApiFields.CDOrdNotifBlock.value
        ]
        ord_id_child_care = cd_ord_notif_message["OrdID"]
        cd_ord_notif_id = cd_ord_notif_message["CDOrdNotifID"]

        order_notif_message = self.java_api_manager2.get_last_message(
            ORSMessageType.OrdNotification.value
        ).get_parameters()[JavaApiFields.OrderNotificationBlock.value]
        self.java_api_manager2.compare_values(
            {
                JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_SEN.value,
            },
            order_notif_message,
            "Step 2 - Comparing Status of Child Care order",
        )
        # endregion

        # region Step 3 - Accept Child CO order in Client Inbox by User2
        self.accept_request.set_default(ord_id_child_care, cd_ord_notif_id, desk_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.accept_request)
        print_message("Accept Child CO", responses)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        self.java_api_manager.compare_values(
            {
                JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value,
            },
            order_reply,
            "Step 3 - Comparing Status of Child CO after Accept by User2",
        )
        # endregion

        # region Step 4 - Create a Сhild MO from Child CO by User_2
        self.submit_request.get_parameters().clear()
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side, self.venue_client_names, self.venue, float(self.price)
            )
            self.submit_request.set_default_child_dma(ord_id_child_care)
            self.submit_request.update_fields_in_component(
                "NewOrderSingleBlock",
                {
                    "OrdQty": self.qty,
                    "Price": self.price,
                    "AccountGroupID": self.client,
                },
            )

            responses = self.java_api_manager.send_message_and_receive_response(self.submit_request)
            print_message("Split Child CO on Child DMA", responses)
        except Exception as e:
            logger.info(f"Your Exception is {e}")
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(nos_rule)

        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            "OrdReplyBlock"
        ]
        ord_id_child_dma = order_reply["OrdID"]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
            order_reply,
            "Step 4 - Comparing Status of Child DMA after Split",
        )
        # endregion

        # region Step 5 - Cancel parent Care order by User 1
        self.cancel_request.set_default(ord_id, cancel_child="Y")
        responses = self.java_api_manager2.send_message_and_receive_response(
            self.cancel_request, {ord_id: ord_id, ord_id_child_care: ord_id_child_care}
        )
        print_message("Cancel Parent CO", responses)

        cd_order_notif_message = self.java_api_manager2.get_last_message(
            CSMessageType.CDOrdNotif.value, ord_id
        ).get_parameters()["CDOrdNotifBlock"]
        cd_order_notif_id_parent = cd_order_notif_message["CDOrdNotifID"]

        cd_order_notif_message = self.java_api_manager2.get_last_message(
            CSMessageType.CDOrdNotif.value, ord_id_child_care
        ).get_parameters()["CDOrdNotifBlock"]
        cd_order_notif_id_child_care = cd_order_notif_message["CDOrdNotifID"]
        # endregion

        # region Step 6 - Accept cancel request for Child CO by User2
        self.accept_request.set_default(ord_id_child_care, cd_order_notif_id_child_care, desk_id, ack_type="C")
        self.accept_request.update_fields_in_component("CDOrdAckBatchRequestBlock", {"CancelChildren": "Y"})
        try:
            cancel_rule = self.rule_manager.add_OrderCancelRequest_FIXStandard(
                self.fix_env.buy_side, self.venue_client_names, self.venue, True
            )
            responses = self.java_api_manager.send_message_and_receive_response(
                self.accept_request, {ord_id_child_care: ord_id_child_care, ord_id_child_dma: ord_id_child_dma}
            )
            print_message("Accept cancel request for Child CO and Child MO", responses)
        except Exception as e:
            logger.info(f"Your Exception is {e}")
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(cancel_rule)

        order_reply = self.java_api_manager.get_last_message(
            ORSMessageType.OrdReply.value, ord_id_child_care
        ).get_parameters()[JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values(
            {
                JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_CXL.value,
                JavaApiFields.ExecType.value: OrderReplyConst.ExecType_CXL.value,
            },
            order_reply,
            "Step 6 - Checking that the Child CO is canceled",
        )

        order_reply = self.java_api_manager.get_last_message(
            ORSMessageType.OrdReply.value, ord_id_child_dma
        ).get_parameters()[JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values(
            {
                JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_CXL.value,
                JavaApiFields.ExecType.value: OrderReplyConst.ExecType_CXL.value,
            },
            order_reply,
            "Step 6 - Checking that the Child DMA is canceled",
        )
        # endregion

        # region Step 7 - Accept cancel request for Parent CO by User2
        self.accept_request.set_default(ord_id, cd_order_notif_id_parent, desk_id, ack_type="C")
        self.accept_request.update_fields_in_component("CDOrdAckBatchRequestBlock", {"CancelChildren": "Y"})
        responses = self.java_api_manager.send_message_and_receive_response(self.accept_request)
        print_message("Accept cancel request for Parent CO", responses)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        self.java_api_manager.compare_values(
            {
                JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_CXL.value,
                JavaApiFields.ExecType.value: OrderReplyConst.ExecType_CXL.value,
            },
            order_reply,
            "Step 7 - Checking that the Parent CO is canceled",
        )
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
