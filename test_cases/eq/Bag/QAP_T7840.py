import logging
import os
import time
import random
import string
from pathlib import Path

from pkg_resources import resource_filename
import xml.etree.ElementTree as ET

from custom import basic_custom_actions as bca
from custom.verifier import VerificationMethod
from rule_management import Simulators, RuleManager
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.cs_message.ManualMatchExecToParentOrdersRequest import \
    ManualMatchExecToParentOrdersRequest
from test_framework.java_api_wrappers.java_api_constants import BagChildCreationPolicy, JavaApiFields, OrderBagConst, \
    SubmitRequestConst, ExecutionReportConst, OrderReplyConst, OrdTypes
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.NewOrderListFromExistingOrders import NewOrderListFromExistingOrders
from test_framework.java_api_wrappers.ors_messages.OrderBagCreationRequest import OrderBagCreationRequest
from test_framework.java_api_wrappers.ors_messages.OrderBagDissociateRequest import OrderBagDissociateRequest
from test_framework.java_api_wrappers.ors_messages.OrderBagWaveModificationRequest import \
    OrderBagWaveModificationRequest
from test_framework.java_api_wrappers.ors_messages.OrderBagWaveRequest import OrderBagWaveRequest
from test_framework.java_api_wrappers.ors_messages.OrderListWaveCreationRequest import OrderListWaveCreationRequest
from test_framework.java_api_wrappers.ors_messages.UnMatchRequest import UnMatchRequest
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7840(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.order_submit2 = OrderSubmitOMS(self.data_set)
        self.rule_manager = RuleManager(Simulators.equity)
        self.desk = self.environment.get_list_fe_environment()[0].desk_ids[0]
        self.bs_connectivity = self.fix_env.buy_side
        self.client = self.data_set.get_client_by_name('client_pt_1')
        self.venue_client_name = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        self.mic = self.data_set.get_mic_by_name('mic_1')
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)
        self.bag_creation_request = OrderBagCreationRequest()
        self.bag_wave_request = OrderBagWaveRequest()
        self.username = self.data_set.get_recipient_by_name("recipient_user_1")
        self.complete_request = DFDManagementBatchOMS(self.data_set)
        self.basket_wave = OrderListWaveCreationRequest()
        self.create_basket = NewOrderListFromExistingOrders()
        self.dissociate_request = OrderBagDissociateRequest()
        self.manual_match_request = ManualMatchExecToParentOrdersRequest()
        self.unmatch_request = UnMatchRequest()
        self.bag_mod_req = OrderBagWaveModificationRequest()

        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.local_path = resource_filename("test_resources.be_configs.oms_be_configs", "client_ors.xml")
        self.remote_path = f"/home/{self.ssh_client_env.su_user}/quod/cfg/client_ors.xml"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition
        # subregion set config
        tree = ET.parse(self.local_path)
        tree.getroot().find("ors/FrontToBack/enforceParentPrice").text = 'true'
        tree.write("temp.xml")
        self.ssh_client.put_file(self.remote_path, "temp.xml")
        self.ssh_client.send_command("qrestart ORS")
        time.sleep(70)

        # subregion Create 1st Care Order
        self.order_submit.set_default_care_limit(self.username, "1")
        self.order_submit.update_fields_in_component(
            "NewOrderSingleBlock",
            {"Price": '2'})
        self.price = self.order_submit.get_parameter("NewOrderSingleBlock")["Price"]
        self.qty = self.order_submit.get_parameter("NewOrderSingleBlock")["OrdQty"]
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        ord_notif = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
            order_reply,
            "Precondition: Checking Status of 1st Care order",
        )
        ord_id = ord_notif.get_parameter("OrdNotificationBlock")["OrdID"]

        # subregion Create 2nd Care Order
        self.order_submit2.set_default_care_limit(self.username, "1")
        self.order_submit2.update_fields_in_component(
            "NewOrderSingleBlock",
            {"Price": '2'})
        self.java_api_manager.send_message_and_receive_response(self.order_submit2)
        ord_notif = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
            order_reply,
            "Precondition: Checking Status of 2nd Care order",
        )
        ord_id2 = ord_notif.get_parameter("OrdNotificationBlock")["OrdID"]
        orders_id = [ord_id, ord_id2]

        # subregion Create Bag
        bag_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.bag_creation_request.set_default(BagChildCreationPolicy.Split.value, bag_name, orders_id)
        self.java_api_manager.send_message_and_receive_response(self.bag_creation_request)
        order_bag_notification = \
            self.java_api_manager.get_last_message(ORSMessageType.OrderBagNotification.value).get_parameters()[
                JavaApiFields.OrderBagNotificationBlock.value]
        expected_result = {JavaApiFields.OrderBagStatus.value: OrderBagConst.OrderBagStatus_NEW.value}
        self.java_api_manager.compare_values(expected_result, order_bag_notification, "Precondition: Check created Bag")

        # subregion Create BagWave
        bag_order_id = order_bag_notification[JavaApiFields.OrderBagID.value]
        qty_of_bag = str(int(int(self.qty) * 2))
        self.bag_wave_request.set_default(bag_order_id, qty_of_bag, OrdTypes.Limit.value)
        self.bag_wave_request.update_fields_in_component('OrderBagWaveRequestBlock', {"Price": self.price})
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.bs_connectivity,
                                                                                                  self.venue_client_name,
                                                                                                  self.mic,
                                                                                                  int(self.price))
            self.java_api_manager.send_message_and_receive_response(self.bag_wave_request)
        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            self.rule_manager.remove_rule(nos_rule)
        wave_notify = self.java_api_manager.get_last_message(ORSMessageType.OrderBagWaveNotification.value) \
            .get_parameters()[JavaApiFields.OrderBagWaveNotificationBlock.value]
        expected_result = {JavaApiFields.OrderWaveStatus.value: OrderBagConst.OrderBagStatus_NEW.value}
        self.java_api_manager.compare_values(expected_result, wave_notify, "Precondition: Check wave bag")
        wave_id = wave_notify["OrderBagWaveID"]
        # endregion

        # region Step 1-2
        new_price = "100.0"
        self.bag_mod_req.set_default(wave_id, "LMT", "DAY")
        self.bag_mod_req.update_fields_in_component("OrderBagWaveModificationRequestBlock", {"Price": new_price})
        try:
            nos_rule = self.rule_manager.add_OrderCancelReplaceRequest_FIXStandard(self.bs_connectivity,
                                                                                   self.venue_client_name,
                                                                                   self.mic, True)
            self.java_api_manager.send_message_and_receive_response(self.bag_mod_req)
        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            self.rule_manager.remove_rule(nos_rule)

        wave_notify = self.java_api_manager.get_last_message(ORSMessageType.OrderBagWaveNotification.value) \
            .get_parameters()[JavaApiFields.OrderBagWaveNotificationBlock.value]
        expected_result = {JavaApiFields.OrderWaveStatus.value: OrderBagConst.OrderBagStatus_NEW.value,
                           "Price": self.price+'.0'}
        self.java_api_manager.compare_values(expected_result, wave_notify, "Step 1-2: Check wave after modification")

        wave_modif_reply = self.java_api_manager.get_last_message(
            ORSMessageType.OrderBagWaveModificationReply.value).get_parameters()["MessageReply"]['MessageReplyBlock'][0]
        self.java_api_manager.compare_values(
            {"ErrorMsg": "Wave's 'Price' (100) greater than Parent's 'Price' (2)"},
            wave_modif_reply,
            f"Step 1-2: Checking that the Bag Wave is rejected because of wave's price is greater then parent's price",
        )
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.ssh_client.put_file(self.remote_path, self.local_path)
        self.ssh_client.send_command("qrestart ORS")
        os.remove("temp.xml")
        self.ssh_client.close()
        time.sleep(70)