import logging
import os
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, \
    QtyPercentageProfile, SubmitRequestConst, OrdListNotificationConst, OrderBagConst
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.NewOrderListFromExistingOrders import NewOrderListFromExistingOrders
from test_framework.java_api_wrappers.ors_messages.OrderBagCreationRequest import OrderBagCreationRequest
from test_framework.java_api_wrappers.ors_messages.OrderListWaveCreationRequest import OrderListWaveCreationRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T9465(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.wave_creation_request = OrderListWaveCreationRequest()
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.qty = '100'
        self.client = self.data_set.get_client_by_name('client_pt_1')
        self.alloc_account1 = self.data_set.get_account_by_name('client_pt_1_acc_1')
        self.alloc_account2 = self.data_set.get_account_by_name('client_pt_1_acc_2')
        self.alloc_account3 = self.data_set.get_account_by_name('client_pt_1_acc_3')
        self.create_list = NewOrderListFromExistingOrders()
        self.bag_request = OrderBagCreationRequest()
        self.basket_name = 'Basket_QAP_T9465'
        self.bag_name = 'Bag_QAP_T9465'

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create 3 CO orders
        # 1
        self.order_submit.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                 desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                 role=SubmitRequestConst.USER_ROLE_1.value)
        self.order_submit.update_fields_in_component('NewOrderSingleBlock', {"AccountGroupID": self.client,
                                                                             "PreTradeAllocationBlock": {
                                                                                 "PreTradeAllocationList": {
                                                                                     "PreTradeAllocAccountBlock": [
                                                                                         {
                                                                                             'AllocAccountID': self.alloc_account1,
                                                                                             'AllocQty': self.qty}]}}})
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        ord_id1 = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameter(
            JavaApiFields.OrdReplyBlock.value)['OrdID']

        # 2
        self.order_submit.update_fields_in_component('NewOrderSingleBlock', {"ClOrdID": bca.client_orderid(9),
                                                                             "PreTradeAllocationBlock": {
                                                                                 "PreTradeAllocationList": {
                                                                                     "PreTradeAllocAccountBlock": [
                                                                                         {
                                                                                             'AllocAccountID': self.alloc_account2,
                                                                                             'AllocQty': self.qty}]}}})
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        ord_id2 = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameter(
            JavaApiFields.OrdReplyBlock.value)['OrdID']

        # 3
        self.order_submit.update_fields_in_component('NewOrderSingleBlock', {"ClOrdID": bca.client_orderid(9),
                                                                             "PreTradeAllocationBlock": {
                                                                                 "PreTradeAllocationList": {
                                                                                     "PreTradeAllocAccountBlock": [
                                                                                         {
                                                                                             'AllocAccountID': self.alloc_account3,
                                                                                             'AllocQty': self.qty}]}}})
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        ord_id3 = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameter(
            JavaApiFields.OrdReplyBlock.value)['OrdID']
        # endregion

        # region create basket
        list_of_orders = [ord_id1, ord_id2, ord_id3]
        self.create_list.set_default(list_of_orders, self.basket_name)
        self.java_api_manager.send_message_and_receive_response(self.create_list)
        # endregion

        # region check values of basket
        list_notify_block = \
            self.java_api_manager.get_last_message(ORSMessageType.NewOrderListReply.value).get_parameters()[
                'NewOrderListReplyBlock']
        self.java_api_manager.compare_values(
            {JavaApiFields.ListOrderStatus.value: OrdListNotificationConst.ListOrderStatus_EXE.value},
            list_notify_block, 'Check List status')
        list_id = list_notify_block['OrderListID']
        # endregion

        # region create bag from basket
        self.bag_request.set_default('GroupAtAvgPrice', self.bag_name, list_of_orders)
        self.bag_request.update_fields_in_component('OrderBagCreationRequestBlock', {'OrderListID': list_id})
        self.java_api_manager.send_message_and_receive_response(self.bag_request)
        # endregion

        # region check values of bag
        order_bag_notification = \
            self.java_api_manager.get_last_message(ORSMessageType.OrderBagNotification.value).get_parameters()[
                JavaApiFields.OrderBagNotificationBlock.value]
        expected_result = {JavaApiFields.OrderBagName.value: self.bag_name,
                           JavaApiFields.OrderBagStatus.value: OrderBagConst.OrderBagStatus_NEW.value}
        self.java_api_manager.compare_values(expected_result, order_bag_notification,
                                             'Check bag values')
        # endregion

        # region Wave
        self.wave_creation_request.set_default(list_id, list_of_orders)
        self.java_api_manager.send_message_and_receive_response(self.wave_creation_request)
        # endregion

        # region Verify wave
        list_wave_notify_block = self.java_api_manager.get_last_message(
            ORSMessageType.OrderListWaveNotification.value).get_parameter(
            ORSMessageType.OrderListWaveNotificationBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.QtyPercentageProfile.value: QtyPercentageProfile.RemainingQty.value},
            list_wave_notify_block,
            'Check created wave')
        # endregion

        # region Verify child orders
        ord_notify_element = list_wave_notify_block['OrdNotificationElements']['OrdNotificationBlock']
        self.java_api_manager.compare_values(
            {JavaApiFields.OrdQty.value: self.qty+'.0', JavaApiFields.RootParentOrdID.value: ord_id1},
            ord_notify_element[0],
            'Check first Child Order after waving')
        self.java_api_manager.compare_values(
            {JavaApiFields.OrdQty.value: self.qty+'.0', JavaApiFields.RootParentOrdID.value: ord_id2},
            ord_notify_element[1],
            'Check second Child Order after waving')
        self.java_api_manager.compare_values(
            {JavaApiFields.OrdQty.value: self.qty+'.0', JavaApiFields.RootParentOrdID.value: ord_id3},
            ord_notify_element[2],
            'Check third Child Order after waving')
        # endregion
