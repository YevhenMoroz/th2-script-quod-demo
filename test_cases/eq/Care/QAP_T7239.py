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
from test_framework.java_api_wrappers.oms.ors_messges.FixOrderCancelRequestOMS import FixOrderCancelRequestOMS
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


class QAP_T7239(TestCase):
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
        self.cancel_request = FixOrderCancelRequestOMS(self.data_set)
        self.java_api_connectivity2 = self.environment.get_list_java_api_environment()[0].java_api_conn_user2
        self.java_api_manager2 = JavaApiManager(self.java_api_connectivity2, self.test_id)
        self.submit_request = OrderSubmitOMS(self.data_set)

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
        # region Prepare pre-precondition:
        tree = ET.parse(self.local_path)
        tree.getroot().find("cs/fixAutoAcknowledge").text = "false"

        element = ET.fromstring("<assignFixModifyCancelToDesk>true</assignFixModifyCancelToDesk>")
        tree.getroot().find("cs").append(element)

        tree.write("temp.xml")
        self.ssh_client.send_command("~/quod/script/site_scripts/change_permission_script")
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        self.ssh_client.send_command("qrestart CS")
        time.sleep(40)
        # endregion

        # region Step 1 - Create CO order
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
            "Step 1 - Comparing Status of Care order",
        )
        # endregion

        # region Step 1 - Accept CO in Client Inbox
        self.accept_request.set_default(ord_id, cd_order_notif_id, desk_id)
        responses = self.java_api_manager2.send_message_and_receive_response(self.accept_request)
        print_message("Accept order", responses)
        order_reply = self.java_api_manager2.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        self.java_api_manager2.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
            order_reply,
            "Step 1 - Comparing Status of Care order after Accept",
        )
        # endregion

        # region Step 2 - Split order to Child DMA
        self.submit_request.set_default_child_dma(ord_id)
        self.submit_request.update_fields_in_component(
            "NewOrderSingleBlock",
            {
                "AccountGroupID": self.client,
                "ListingList": {"ListingBlock": [{"ListingID": self.data_set.get_listing_id_by_name("listing_3")}]},
                "InstrID": self.data_set.get_instrument_id_by_name("instrument_2"),
                "OrdQty": self.qty,
            },
        )
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side, self.venue_client_names, self.venue, float(self.price)
            )
            responses = self.java_api_manager2.send_message_and_receive_response(self.submit_request)
            print_message("Split Parent CO on Child DMA", responses)
        except Exception as e:
            logger.info(f"Your Exception is {e}")
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(nos_rule)

        order_reply = self.java_api_manager2.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            "OrdReplyBlock"
        ]
        ord_id_child_dma = order_reply["OrdID"]
        cl_ord_id_child_dma = order_reply["ClOrdID"]
        self.java_api_manager2.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
            order_reply,
            "Step 2 - Comparing Status of Child DMA after Split",
        )
        # endregion

        # region Step 3 - Send cancel request
        try:
            cancel_rule = self.rule_manager.add_OrderCancelRequest_FIXStandard(
                self.fix_env.buy_side, self.venue_client_names, self.venue, True
            )
            self.cancel_request.set_default_cancel(cl_ord_id)
            responses = self.java_api_manager.send_message_and_receive_response(
                self.cancel_request, {cl_ord_id_child_dma: cl_ord_id_child_dma}
            )
            print_message("Send fix cancel request", responses)
        except Exception as e:
            logger.info(f"Your Exception is {e}")
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(cancel_rule)

        order_reply = self.java_api_manager.get_last_message(
            ORSMessageType.OrdReply.value, ord_id_child_dma
        ).get_parameters()[JavaApiFields.OrdReplyBlock.value]
        print(order_reply)
        self.java_api_manager.compare_values(
            {
                JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_CXL.value,
                JavaApiFields.ExecType.value: OrderReplyConst.ExecType_CXL.value,
            },
            order_reply,
            "Step 3 - Checking that the Child DMA is canceled",
        )

        cd_order_notif_message = self.java_api_manager.get_last_message(
            CSMessageType.CDOrdNotif.value, ord_id
        ).get_parameters()[JavaApiFields.CDOrdNotifBlock.value]
        cd_order_notif_id = cd_order_notif_message[JavaApiFields.CDOrdNotifID.value]
        # endregion

        # region Step 4 - Accept cancel request for Parent CO
        self.accept_request.set_default(ord_id, cd_order_notif_id, desk_id, ack_type="C")
        self.accept_request.update_fields_in_component("CDOrdAckBatchRequestBlock", {"CancelChildren": "Y"})
        responses = self.java_api_manager2.send_message_and_receive_response(self.accept_request)
        print_message("Accept cancel request for Parent CO", responses)
        order_reply = self.java_api_manager2.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        self.java_api_manager2.compare_values(
            {
                JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_CXL.value,
                JavaApiFields.ExecType.value: OrderReplyConst.ExecType_CXL.value,
            },
            order_reply,
            "Step 4 - Checking that the Parent CO is canceled",
        )
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.ssh_client.put_file(self.remote_path, self.local_path)
        self.ssh_client.send_command("qrestart CS")
        os.remove("temp.xml")
        time.sleep(40)
        self.ssh_client.close()
