import logging
import os
import time
import xml.etree.ElementTree as ET
from pathlib import Path

from pkg_resources import resource_filename

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType, CSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.cs_message.CDOrdAckBatchRequest import CDOrdAckBatchRequest
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst, TimeInForces, OrdTypes, \
    ExecutionPolicyConst
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7625(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.client = self.data_set.get_client_by_name("client_2")
        self.accept_request = CDOrdAckBatchRequest()
        self.route_id = self.data_set.get_route_id_by_name('route_1')
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.local_path = resource_filename("test_resources.be_configs.oms_be_configs", "client_ors.xml")
        self.remote_path = f"/home/{self.ssh_client_env.su_user}/quod/cfg/client_ors.xml"
        self.qty = '200'

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition
        tree = ET.parse(self.local_path)
        tree.getroot().find("ors/FrontToBack/enforceParentPrice").text = 'false'
        tree.write("temp.xml")
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        self.ssh_client.send_command("qrestart ORS")
        time.sleep(70)
        # endregion
        # region step 1-6: Create CO order
        desk = self.environment.get_list_fe_environment()[0].desk_ids[0]
        self.order_submit.set_default_care_market(desk=desk)
        self.order_submit.update_fields_in_component('NewOrderSingleBlock', {JavaApiFields.OrdQty.value: self.qty})
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        ord_notification_message = \
            self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameters() \
                [JavaApiFields.OrderNotificationBlock.value]
        order_id = ord_notification_message[JavaApiFields.OrdID.value]
        self.java_api_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_SEN.value},
                                             ord_notification_message, 'Verifying that order has Sts = "Sent" (step 7)')
        # endregion

        # region step 7-8: Accept CO order
        cd_ord_notif_message = self.java_api_manager.get_last_message(CSMessageType.CDOrdNotif.value).get_parameters() \
            [JavaApiFields.CDOrdNotifBlock.value]
        cd_ord_notif_id = cd_ord_notif_message[JavaApiFields.CDOrdNotifID.value]
        self.accept_request.set_default(order_id, cd_ord_notif_id, desk)
        self.java_api_manager.send_message_and_receive_response(self.accept_request)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                                             order_reply, 'Verifying that order "Open" (step 9)')
        # endregion

        # region step 9 - 10: Direct_MOC Care order
        self.order_submit.get_parameters().clear()
        self.order_submit.set_default_direct_moc(order_id)
        self.order_submit.update_fields_in_component('NewOrderSingleBlock', {'OrdQty': str(float(self.qty)),
                                                                             'ExecutionPolicy':ExecutionPolicyConst.DMA.value})
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.OrdQty.value: self.qty,
                                              JavaApiFields.TimeInForce.value: TimeInForces.ATC.value,
                                              JavaApiFields.OrdType.value: OrdTypes.Market.value},
                                             order_reply,
                                             'Verifying that child DMA order has properly values (step 10)')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.ssh_client.put_file(self.remote_path, self.local_path)
        self.ssh_client.send_command("qrestart ORS")
        os.remove("temp.xml")
        self.ssh_client.close()
        time.sleep(70)
