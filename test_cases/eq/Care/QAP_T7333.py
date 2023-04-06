import logging
import os
import time
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

from pkg_resources import resource_filename

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType, CSMessageType
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.cs_message.CDOrdAckBatchRequest import CDOrdAckBatchRequest
from test_framework.java_api_wrappers.java_api_constants import OrderReplyConst, JavaApiFields
from test_framework.java_api_wrappers.oms.ors_messges.FixNewOrderSingleOMS import FixNewOrderSingleOMS
from test_framework.java_api_wrappers.oms.ors_messges.FixOrderModificationRequestOMS import (
    FixOrderModificationRequestOMS,
)
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


def print_message(message, responses):
    logger.info(message)
    for i in responses:
        logger.info(i)
        logger.info(i.get_parameters())


class QAP_T7333(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.qty = "100"
        self.qty_amend = "80"
        self.price = "20"
        self.client = self.data_set.get_client("client_2")  # CLIENT2
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.accept_request = CDOrdAckBatchRequest()
        self.nos = FixNewOrderSingleOMS(self.data_set)
        self.java_api_connectivity2 = self.environment.get_list_java_api_environment()[0].java_api_conn_user2
        self.java_api_manager2 = JavaApiManager(self.java_api_connectivity2, self.test_id)
        self.submit_request = OrderSubmitOMS(self.data_set)
        self.order_modification_request = FixOrderModificationRequestOMS(self.data_set)

        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_verifier = FixVerifier(self.fix_env.buy_side, self.test_id)
        self.rule_manager = RuleManager(Simulators.equity)
        self.venue = self.data_set.get_mic_by_name("mic_1")
        self.venue_client_names = self.data_set.get_venue_client_names_by_name("client_2_venue_1")

        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(
            self.ssh_client_env.host,
            self.ssh_client_env.port,
            self.ssh_client_env.user,
            self.ssh_client_env.password,
            self.ssh_client_env.su_user,
            self.ssh_client_env.su_password,
        )
        self.local_path = resource_filename("test_resources.be_configs.oms_be_configs", "client_cs.xml")
        self.remote_path = f"/home/{self.ssh_client_env.su_user}/quod/cfg/client_cs.xml"
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region prepare pre-precondition:
        tree = ET.parse(self.local_path)
        cs = tree.getroot().find("cs/fixAutoAcknowledge")
        cs.text = "false"
        tree.write("temp.xml")
        self.ssh_client.send_command("~/quod/script/site_scripts/change_permission_script")
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        self.ssh_client.send_command("qrestart CS")
        time.sleep(60)
        # endregion

        # region Precondition - Create CO order
        self.nos.set_default_care_limit()
        self.nos.update_fields_in_component("NewOrderSingleBlock", {"ClientAccountGroupID": self.client})
        responses = self.java_api_manager.send_message_and_receive_response(self.nos)
        print_message("Create CO", responses)
        cd_order_notif_message = self.java_api_manager.get_last_message(
            CSMessageType.CDOrdNotif.value
        ).get_parameters()[JavaApiFields.CDOrdNotifBlock.value]
        cd_order_notif_id = cd_order_notif_message["CDOrdNotifID"]

        order_notif_message = self.java_api_manager.get_last_message(
            ORSMessageType.OrdNotification.value
        ).get_parameters()[JavaApiFields.OrderNotificationBlock.value]
        ord_id = order_notif_message["OrdID"]
        cl_ord_id = order_notif_message["ClOrdID"]
        desk_id = order_notif_message["RecipientDeskID"]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_SEN.value},
            order_notif_message,
            "Precondition - Comparing Status of Care order",
        )
        # endregion

        # region Accept CO order in Client Inbox
        self.accept_request.set_default(ord_id, cd_order_notif_id, desk_id)
        responses = self.java_api_manager2.send_message_and_receive_response(self.accept_request)
        print_message("Accept order", responses)
        order_reply = self.java_api_manager2.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        self.java_api_manager2.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
            order_reply,
            "Comparing Status of Care order after Accept",
        )
        # endregion

        # region Step 1  - Split CO for two child DMA orders
        self.__split_care_order_to_dma(ord_id, "1st")
        self.__split_care_order_to_dma(ord_id, "2nd")
        # region

        # region Step 2 - Sent Fix modification request
        self.order_modification_request.set_modify_order_limit(cl_ord_id, self.qty_amend, self.price)
        self.order_modification_request.update_fields_in_component(
            "OrderModificationRequestBlock", {"ClientAccountGroupID": self.client}
        )
        responses = self.java_api_manager.send_message_and_receive_response(self.order_modification_request)
        print_message("Sent Fix modification request", responses)

        cd_ord_notif_message = self.java_api_manager.get_last_message(CSMessageType.CDOrdNotif.value).get_parameters()[
            JavaApiFields.CDOrdNotifBlock.value
        ]
        cd_order_notif_id = cd_ord_notif_message[JavaApiFields.CDOrdNotifID.value]
        # endregion

        # region Step 3 - Accept modification request, Modify + Child
        try:
            modification_rule = self.rule_manager.add_OrderCancelReplaceRequest_FIXStandard(
                self.fix_env.buy_side, self.venue_client_names, self.venue, True
            )
            self.accept_request.get_parameters().clear()
            self.accept_request.set_default(ord_id, cd_order_notif_id, desk_id, "M")
            self.accept_request.update_fields_in_component("CDOrdAckBatchRequestBlock", {"ModifyChildren": "Y"})
            responses = self.java_api_manager2.send_message_and_receive_response(self.accept_request, {ord_id: ord_id})
            print_message("Accept Modify + Child", responses)
        except Exception as e:
            logger.info(f"Your Exception is {e}")
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(modification_rule)

        cd_ord_ack_batch_reply = self.java_api_manager2.get_last_message(
            CSMessageType.CDOrdAckBatchReply.value
        ).get_parameters()["CDOrdAckBatchReplyBlock"]
        message_reply_block = cd_ord_ack_batch_reply["CDOrdAckReplyList"]["CDOrdAckReplyBlock"][0]["MessageReplyBlock"]
        self.java_api_manager2.compare_values(
            {"ErrorMsg": "Invalid quantity :  The parent order has many children alive orders."},
            message_reply_block,
            "Step 3 - Check ErrorMsg",
        )
        # endregion

    def __split_care_order_to_dma(self, ord_id: str, number_of_order: str):
        self.submit_request.set_default_child_dma(ord_id)
        self.submit_request.update_fields_in_component(
            "NewOrderSingleBlock",
            {
                "AccountGroupID": self.client,
                "ListingList": {"ListingBlock": [{"ListingID": self.data_set.get_listing_id_by_name("listing_3")}]},
                "InstrID": self.data_set.get_instrument_id_by_name("instrument_2"),
                "OrdQty": str(float(self.qty) / 2),
            },
        )
        responses = self.java_api_manager2.send_message_and_receive_response(self.submit_request)
        print_message(f"Split CO on {number_of_order} Child DMA", responses)
        order_reply = self.java_api_manager2.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            "OrdReplyBlock"
        ]
        self.java_api_manager2.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_SEN.value},
            order_reply,
            f"Step 2 - Comparing Status of {number_of_order} Child DMA after Split",
        )

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.ssh_client.put_file(self.remote_path, self.local_path)
        self.ssh_client.send_command("qrestart CS")
        os.remove("temp.xml")
        time.sleep(60)
        self.ssh_client.close()

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
