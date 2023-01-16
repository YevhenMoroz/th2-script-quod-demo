import logging
import os
import time
from pathlib import Path
import xml.etree.ElementTree as ET

from pkg_resources import resource_filename

from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.HeldOrderAckRequest import HeldOrderAckRequest
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7412(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.dummy_account = self.data_set.get_client_by_name('client_dummy')
        self.client = self.data_set.get_client_by_name('client_pt_1')
        self.sec_acc = self.data_set.get_account_by_name('client_pt_1_acc_1')
        self.route_id = self.data_set.get_route_id_by_name('route_1')
        self.group_modify = HeldOrderAckRequest()
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.local_path = resource_filename("test_resources.be_configs.oms_be_configs", "client_ors.xml")
        self.remote_path = f"/home/{self.ssh_client_env.su_user}/quod/cfg/client_ors.xml"
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.text = '123text123'

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region set up configuration on BackEnd(precondition)
        tree = ET.parse(self.local_path)
        quod = tree.getroot()
        quod.find("ors/FrontToBack/acceptUnknownAccountGroup/DMA").text = "true"
        tree.write("temp.xml")
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        self.ssh_client.send_command("qrestart ORS")
        time.sleep(90)
        # endregion
        # region create Held order
        self.order_submit.set_default_dma_limit()
        self.order_submit.update_fields_in_component('NewOrderSingleBlock', {
            'AccountGroupID': self.dummy_account})
        responses = self.java_api_manager.send_message_and_receive_response(self.order_submit)
        self.__return_result(responses, ORSMessageType.OrdNotification.value)
        order_notify_block = self.result.get_parameter('OrdNotificationBlock')
        self.java_api_manager.compare_values({JavaApiFields.AccountGroupID.value: self.dummy_account,
                                              JavaApiFields.OrdStatus.value: OrderReplyConst.OrdStatus_HLD.value},
                                             order_notify_block, 'Check Held order')
        order_id = order_notify_block['OrdID']
        # endregion

        # region group modify
        self.group_modify.set_default(order_id, self.client)
        self.group_modify.update_fields_in_component('HeldOrderAckBlock',
                                                     {'PreTradeAllocationBlock': {'PreTradeAllocationList': {
                                                         "PreTradeAllocAccountBlock": [
                                                             {'AllocAccountID': self.sec_acc, 'AllocQty': '100'}]}},
                                                         'RouteID': self.route_id, 'CDOrdFreeNotes': self.text})
        responses = self.java_api_manager.send_message_and_receive_response(self.group_modify)
        self.__return_result(responses, ORSMessageType.OrderReply.value)
        order_reply_block = self.result.get_parameter('OrdReplyBlock')
        self.java_api_manager.compare_values({JavaApiFields.AccountGroupID.value: self.client,
                                              JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_SEN.value,
                                              JavaApiFields.RouteID.value: str(self.route_id),
                                              JavaApiFields.SingleAllocAccountID.value: self.sec_acc,
                                              JavaApiFields.CDOrdFreeNotes.value: self.text},
                                             order_reply_block, 'Check order after group modifying')
        # endregion

    def __return_result(self, responses, message_type):
        for response in responses:
            if response.get_message_type() == message_type:
                self.result = response

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.ssh_client.put_file(self.remote_path, self.local_path)
        self.ssh_client.send_command("qrestart ORS")
        os.remove("temp.xml")
