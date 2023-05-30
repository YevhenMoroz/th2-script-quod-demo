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
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import BagChildCreationPolicy, JavaApiFields, OrderBagConst, \
    OrdTypes, ExecutionPolicyConst, OrderReplyConst
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.OrderBagCreationRequest import OrderBagCreationRequest
from test_framework.java_api_wrappers.ors_messages.OrderBagWaveModificationRequest import \
    OrderBagWaveModificationRequest
from test_framework.java_api_wrappers.ors_messages.OrderBagWaveRequest import OrderBagWaveRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T11052(TestCase):
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
        self.bag_mod_req = OrderBagWaveModificationRequest()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition
        # subregion Precondition: Create 1st Care Order
        self.order_submit.set_default_care_limit(self.username, "1")
        self.order_submit.update_fields_in_component("NewOrderSingleBlock", {'OrdType': 'Market'})
        self.order_submit.remove_fields_from_component("NewOrderSingleBlock", ['Price'])
        self.qty = self.order_submit.get_parameter("NewOrderSingleBlock")["OrdQty"]
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        ord_notif = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value)
        ord_id = ord_notif.get_parameter("OrdNotificationBlock")["OrdID"]
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
            order_reply,
            "Step Precondition: Checking Status of created 1st Care order",
        )

        # subregion Precondition: Create 2nd Care Order
        self.order_submit2.set_default_care_limit(self.username, "1")
        self.order_submit2.update_fields_in_component("NewOrderSingleBlock", {'OrdType': 'Market'})
        self.order_submit2.remove_fields_from_component("NewOrderSingleBlock", ['Price'])
        self.java_api_manager.send_message_and_receive_response(self.order_submit2)
        ord_notif = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value)
        ord_id2 = ord_notif.get_parameter("OrdNotificationBlock")["OrdID"]
        orders_id = [ord_id, ord_id2]
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
            order_reply,
            "Step Precondition: Checking Status of created 2nd Care order",
        )

        # subregion Precondition: Create Bag
        bag_name = 'QAP_T11052'
        self.bag_creation_request.set_default(BagChildCreationPolicy.Split.value, bag_name, orders_id)
        self.java_api_manager.send_message_and_receive_response(self.bag_creation_request)
        order_bag_notification = \
            self.java_api_manager.get_last_message(ORSMessageType.OrderBagNotification.value).get_parameters()[
                JavaApiFields.OrderBagNotificationBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.OrderBagStatus.value: OrderBagConst.OrderBagStatus_NEW.value}, order_bag_notification,
            'Precondition: Check Bag Status after Bag creation')
        # endregion

        # region Step 1: Create Wave
        bag_order_id = order_bag_notification[JavaApiFields.OrderBagID.value]
        qty_of_bag = str(int(int(self.qty) * 2))
        price = '20'
        self.bag_wave_request.set_default(bag_order_id, qty_of_bag, OrdTypes.Market.value)
        self.bag_wave_request.update_fields_in_component('OrderBagWaveRequestBlock', {"AlgoParametersBlock": {
                                                                                          "AlgoType": "Participate",
                                                                                          "ScenarioID": "12",
                                                                                          "AlgoPolicyID": "12"}})
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
        order_bag_wave_notification = \
            self.java_api_manager.get_last_message(ORSMessageType.OrderBagWaveNotification.value).get_parameter(
                JavaApiFields.OrderBagWaveNotificationBlock.value)
        expected_result = {JavaApiFields.OrderWaveStatus.value: OrderBagConst.OrderWaveStatus_NEW.value,
                           "AlgoParametersBlock": {
                               "AlgoType": "PCP",
                               "ScenarioID": "12",
                               "AlgoPolicyID": "12"}}
        self.java_api_manager.compare_values(expected_result, order_bag_wave_notification, "Check wave is created")
        wave_id = order_bag_wave_notification["OrderBagWaveID"]
        algo_ord_id = order_bag_wave_notification["OrderBagWaveOrderList"]["OrderBagWaveOrderBlock"][0]["OrdID"]
        algo_ord_id2 = order_bag_wave_notification["OrderBagWaveOrderList"]["OrderBagWaveOrderBlock"][1]["OrdID"]
        ord_update = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value, algo_ord_id) \
            .get_parameters()[JavaApiFields.OrdReplyBlock.value]
        expected_result = {JavaApiFields.OrdType.value: OrdTypes.Market.value,
                           JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value,
                           JavaApiFields.ExecutionPolicy.value: ExecutionPolicyConst.Synthetic.value}
        self.java_api_manager.compare_values(expected_result, ord_update,
                                             f"Step 1: Check fields for {algo_ord_id} after wave creation")


        ord_update2 = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value, algo_ord_id2) \
            .get_parameters()[JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values(expected_result, ord_update2,
                                             f"Step 1: Check fields for {algo_ord_id2} after wave creation")
        # endregion

        # region Step 2: Modify Wave
        new_price = "10.0"
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
        ord_update = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value, algo_ord_id) \
            .get_parameters()[JavaApiFields.OrdReplyBlock.value]
        expected_result = {JavaApiFields.OrdType.value: OrdTypes.Limit.value,
                           JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value,
                           JavaApiFields.Price.value: new_price,
                           JavaApiFields.ExecutionPolicy.value: ExecutionPolicyConst.Synthetic.value}
        self.java_api_manager.compare_values(expected_result, ord_update, f"Step 2: Check fields for {algo_ord_id} after wave modification")
        ord_update2 = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value, algo_ord_id2) \
            .get_parameters()[JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values(expected_result, ord_update2, f"Step 2: Check fields for {algo_ord_id2} after wave modification")
        # endregion
