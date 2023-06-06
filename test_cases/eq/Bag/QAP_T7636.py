import logging
import os
import random
import string
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import Simulators, RuleManager
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import BagChildCreationPolicy, JavaApiFields, OrderBagConst, \
    OrdTypes, OrderReplyConst
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.OrderBagCreationRequest import OrderBagCreationRequest
from test_framework.java_api_wrappers.ors_messages.OrderBagWaveModificationRequest import \
    OrderBagWaveModificationRequest
from test_framework.java_api_wrappers.ors_messages.OrderBagWaveRequest import OrderBagWaveRequest
from test_framework.java_api_wrappers.ors_messages.OrderModificationRequest import OrderModificationRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7636(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.order_submit2 = OrderSubmitOMS(self.data_set)
        self.rule_manager = RuleManager(Simulators.equity)
        self.bs_connectivity = self.fix_env.buy_side
        self.venue_client_name = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        self.mic = self.data_set.get_mic_by_name('mic_1')
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)
        self.bag_creation_request = OrderBagCreationRequest()
        self.bag_wave_request = OrderBagWaveRequest()
        self.username = self.data_set.get_recipient_by_name("recipient_user_1")
        self.complete_request = DFDManagementBatchOMS(self.data_set)
        self.modification_request = OrderModificationRequest()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition
        # subregion Precondition: Create 1st Care Order
        self.order_submit.set_default_care_limit(self.username, "1")
        self.order_submit.update_fields_in_component("NewOrderSingleBlock", {'OrdType': 'Market'})
        self.order_submit.remove_fields_from_component("NewOrderSingleBlock",['Price'])
        self.qty = self.order_submit.get_parameter("NewOrderSingleBlock")["OrdQty"]
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        ord_notif = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
            order_reply,
            "Precondition: Checking Status of 1st Care order",
        )
        ord_id = ord_notif.get_parameter("OrdNotificationBlock")["OrdID"]

        # subregion Precondition: Create 2nd Care Order
        self.order_submit2.set_default_care_limit(self.username, "1")
        self.order_submit2.update_fields_in_component("NewOrderSingleBlock", {'OrdType': 'Market'})
        self.order_submit2.remove_fields_from_component("NewOrderSingleBlock", ['Price'])
        self.java_api_manager.send_message_and_receive_response(self.order_submit2)
        ord_notif = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
            order_reply,
            "Precondition: Checking Status of 1st Care order",
        )
        ord_id2 = ord_notif.get_parameter("OrdNotificationBlock")["OrdID"]
        orders_id = [ord_id, ord_id2]

        # subregion Precondition: Create Bag
        bag_name = 'QAP_T7636'
        self.bag_creation_request.set_default(BagChildCreationPolicy.Split.value, bag_name, orders_id)
        self.java_api_manager.send_message_and_receive_response(self.bag_creation_request)
        order_bag_notification = \
            self.java_api_manager.get_last_message(ORSMessageType.OrderBagNotification.value).get_parameters()[
                JavaApiFields.OrderBagNotificationBlock.value]
        expected_result = {JavaApiFields.OrderBagStatus.value: OrderBagConst.OrderBagStatus_NEW.value}
        self.java_api_manager.compare_values(expected_result, order_bag_notification,
                                             "Precondition: Check created Bag")

        # subregion Precondition: Mass Modify Orders to include Display Qty
        display_qty = str(int(int(self.qty) // 2))
        self.__send_modification_request(ord_id, "first", display_qty)
        self.__send_modification_request(ord_id2, "second", display_qty)
        # endregion

        # region Step 1-3
        bag_order_id = order_bag_notification[JavaApiFields.OrderBagID.value]
        qty_of_bag = str(int(int(self.qty) * 2))
        price = '20'
        self.bag_wave_request.set_default(bag_order_id, qty_of_bag, OrdTypes.Limit.value)
        self.bag_wave_request.update_fields_in_component('OrderBagWaveRequestBlock', {"Price": price,
                                                                                      "AlgoParametersBlock": {
                                                                                          "AlgoType": "SyntheticIceberg",
                                                                                          "ScenarioID": "26",
                                                                                          "AlgoPolicyID": "1000056"},
                                                                                      "DisplayInstructionBlock": {
                                                                                          "DisplayQty": str(self.qty),
                                                                                          "DisplayMethod": "Initial"
                                                                                      }})
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.bs_connectivity,
                                                                                                  self.venue_client_name,
                                                                                                  self.mic,
                                                                                                  int(price))
            self.java_api_manager.send_message_and_receive_response(self.bag_wave_request)

        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            self.rule_manager.remove_rule(nos_rule)
        wave_notify = self.java_api_manager.get_last_message(ORSMessageType.OrderBagWaveNotification.value) \
            .get_parameters()[JavaApiFields.OrderBagWaveNotificationBlock.value]
        expected_result = {JavaApiFields.OrderWaveStatus.value: OrderBagConst.OrderBagStatus_NEW.value,
                           JavaApiFields.QtyToRelease.value: str(int(self.qty) * 2)+'.0',
                           JavaApiFields.AlgoParametersBlock.value: {"AlgoType": "ICE",
                                                                      "ScenarioID": "26",
                                                                      "AlgoPolicyID": "1000056"}}
        self.java_api_manager.compare_values(expected_result, wave_notify, "Step 1-3: Check wave")
        # endregion

    def __send_modification_request(self, ord_id: str, number_of_order: str, display_qty: str):
        self.modification_request.set_default(self.data_set, ord_id)
        self.modification_request.update_fields_in_component(
            "OrderModificationRequestBlock", {'OrdType': OrdTypes.Market.value, "DisplayInstructionBlock": {"DisplayQty": display_qty, "DisplayMethod": "Initial"}}
        )
        self.modification_request.remove_fields_from_component("OrderModificationRequestBlock", ['Price'])
        responses = self.java_api_manager.send_message_and_receive_response(self.modification_request)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        self.java_api_manager.compare_values(
            {"DisplayInstructionBlock": {"DisplayQty": display_qty+'.0', "DisplayMethod": "INI"}},
            order_reply,
            f"Precondition: Comparing DisplayInstructionBlock {number_of_order} order after Mass Modify",
        )
        # endregion