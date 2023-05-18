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
from test_framework.java_api_wrappers.ors_messages.CancelOrderRequest import CancelOrderRequest
from test_framework.java_api_wrappers.ors_messages.OrderBagCreationRequest import OrderBagCreationRequest
from test_framework.java_api_wrappers.ors_messages.OrderBagDissociateRequest import OrderBagDissociateRequest
from test_framework.java_api_wrappers.ors_messages.OrderBagWaveRequest import OrderBagWaveRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T10910(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
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
        self.cancel_ord = CancelOrderRequest()
        self.bag_dissociate_request = OrderBagDissociateRequest()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.order_submit.set_default_care_limit(self.username, "1")
        self.price = self.order_submit.get_parameter("NewOrderSingleBlock")["Price"]
        self.qty = self.order_submit.get_parameter("NewOrderSingleBlock")["OrdQty"]
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        ord_notif = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value)
        ord_id = ord_notif.get_parameter("OrdNotificationBlock")["OrdID"]

        self.order_submit2.set_default_care_limit(self.username, "1")
        self.java_api_manager.send_message_and_receive_response(self.order_submit2)
        ord_notif = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value)
        ord_id2 = ord_notif.get_parameter("OrdNotificationBlock")["OrdID"]
        orders_id = [ord_id, ord_id2]
        # endregion

        # region Step 2
        bag_name = 'QAP_T10910'

        self.bag_creation_request.set_default(BagChildCreationPolicy.Split.value, bag_name, orders_id)
        self.java_api_manager.send_message_and_receive_response(self.bag_creation_request)
        order_bag_notification = \
            self.java_api_manager.get_last_message(ORSMessageType.OrderBagNotification.value).get_parameters()[
                JavaApiFields.OrderBagNotificationBlock.value]
        # endregion

        # region Step 3 and 4
        bag_order_id = order_bag_notification[JavaApiFields.OrderBagID.value]
        trd_qty = int(self.qty)//2
        self.bag_wave_request.set_default(bag_order_id, int(self.qty), OrdTypes.Limit.value)
        self.bag_wave_request.update_fields_in_component('OrderBagWaveRequestBlock', {"Price": self.price})
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                          self.venue_client_name,
                                                                                          self.mic, int(self.price),
                                                                                          trd_qty, 0)
            self.java_api_manager.send_message_and_receive_response(self.bag_wave_request)
        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            self.rule_manager.remove_rule(nos_rule)
        wave_notify = self.java_api_manager.get_last_message(ORSMessageType.OrderBagWaveNotification.value) \
            .get_parameters()[JavaApiFields.OrderBagWaveNotificationBlock.value]
        expected_result = {JavaApiFields.OrderWaveStatus.value: OrderBagConst.OrderWaveStatus_TER.value}
        self.java_api_manager.compare_values(expected_result, wave_notify, "Check wave")
        child_ord_id = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value, ord_id) \
            .get_parameters()[JavaApiFields.OrderNotificationBlock.value]["OrdID"]
        # endregion

        # region Step 5
        self.bag_dissociate_request.set_default(bag_order_id)
        self.java_api_manager.send_message_and_receive_response(self.bag_dissociate_request)
        order_bag_notification = \
            self.java_api_manager.get_last_message(ORSMessageType.OrderBagNotification.value).get_parameters()[
                JavaApiFields.OrderBagNotificationBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.OrderBagStatus.value: OrderBagConst.OrderBagStatus_TER.value},
            order_bag_notification, 'Checking OrderBagStatus')
        ord_update = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value, ord_id).get_parameter(
            JavaApiFields.OrderNotificationBlock.value)
        ord_update2 = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value,
                                                             ord_id2).get_parameter(
            JavaApiFields.OrderNotificationBlock.value)
        expected_result = {JavaApiFields.LeavesQty.value: str(float(self.qty)//2),
                           JavaApiFields.UnmatchedQty.value: str(float(self.qty)//2),
                           JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value}
        self.java_api_manager.compare_values(expected_result, ord_update, "UnmatchedQty for order 1")
        self.java_api_manager.compare_values(expected_result, ord_update2, "UnmatchedQty for order 2")
        # endregion

        # region Step 6

        self.bag_creation_request.set_default(BagChildCreationPolicy.Split.value, bag_name, orders_id)
        self.java_api_manager.send_message_and_receive_response(self.bag_creation_request)
        order_bag_notification = \
            self.java_api_manager.get_last_message(ORSMessageType.OrderBagNotification.value).get_parameters()[
                JavaApiFields.OrderBagNotificationBlock.value]
        # endregion

        # region Step 7
        new_bag_order_id = order_bag_notification[JavaApiFields.OrderBagID.value]
        trd_qty = int(self.qty) // 2
        self.bag_wave_request.set_default(new_bag_order_id, int(self.qty), OrdTypes.Limit.value)
        self.bag_wave_request.update_fields_in_component('OrderBagWaveRequestBlock', {"Price": self.price})
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                          self.venue_client_name,
                                                                                          self.mic, int(self.price),
                                                                                          trd_qty, 0)
            self.java_api_manager.send_message_and_receive_response(self.bag_wave_request)
        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            self.rule_manager.remove_rule(nos_rule)
        wave_notify = self.java_api_manager.get_last_message(ORSMessageType.OrderBagWaveNotification.value) \
            .get_parameters()[JavaApiFields.OrderBagWaveNotificationBlock.value]
        expected_result = {JavaApiFields.OrderWaveStatus.value: OrderBagConst.OrderWaveStatus_TER.value}
        self.java_api_manager.compare_values(expected_result, wave_notify, "Check wave")
        child_ord_id = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value, ord_id) \
            .get_parameters()[JavaApiFields.OrderNotificationBlock.value]["OrdID"]
        # endregion

        # region Step 7 compare values
        self.java_api_manager.compare_values(
            {JavaApiFields.OrderBagStatus.value: OrderBagConst.OrderBagStatus_NEW.value},
            order_bag_notification, 'Checking OrderBagStatus')
        exec_for_order = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                                ord_id).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)

        exec_for_order2 = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                                ord_id2).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)
        expected_result = {JavaApiFields.LeavesQty.value: '0.0',
                           JavaApiFields.UnmatchedQty.value: '0.0',
                           JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value}
        self.java_api_manager.compare_values(expected_result, exec_for_order, "UnmatchedQty for order 1")
        self.java_api_manager.compare_values(expected_result, exec_for_order2, "UnmatchedQty for order 2")
        # endregion