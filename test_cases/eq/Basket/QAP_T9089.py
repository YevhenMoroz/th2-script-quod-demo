import logging
import os
from pathlib import Path

from custom import basic_custom_actions as bca, basic_custom_actions
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrdListNotificationConst, OrderBagConst
from test_framework.java_api_wrappers.ors_messages.NewOrderListFromExistingOrders import NewOrderListFromExistingOrders
from test_framework.java_api_wrappers.ors_messages.OrderBagCreationRequest import OrderBagCreationRequest
from test_framework.java_api_wrappers.ors_messages.OrderListWaveCreationRequest import OrderListWaveCreationRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T9089(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.new_order_single = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.wave_creation_request = OrderListWaveCreationRequest()
        self.bag_request = OrderBagCreationRequest()
        self.list_creation_request = NewOrderListFromExistingOrders()
        self.bag_name = 'BAG_QAP_T9089'
        self.basket_name = 'Basket_QAP_T9089'

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region create orders
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.new_order_single)
        order_id1 = response[0].get_parameter("OrderID")
        self.new_order_single.change_parameters({'ClOrdID': basic_custom_actions.client_orderid(9)})
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.new_order_single)
        order_id2 = response[0].get_parameter("OrderID")
        self.new_order_single.change_parameters({'ClOrdID': basic_custom_actions.client_orderid(9), 'Side': '2'})
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.new_order_single)
        order_id3 = response[0].get_parameter("OrderID")
        # endregion

        # step 1
        # region create basket
        self.list_creation_request.set_default([order_id1, order_id2, order_id3], self.basket_name)
        self.java_api_manager.send_message_and_receive_response(self.list_creation_request)
        list_notify_block = \
            self.java_api_manager.get_last_message(ORSMessageType.NewOrderListReply.value).get_parameters()[
                'NewOrderListReplyBlock']
        self.java_api_manager.compare_values(
            {JavaApiFields.ListOrderStatus.value: OrdListNotificationConst.ListOrderStatus_EXE.value},
            list_notify_block, 'Check List status')
        list_id = list_notify_block['OrderListID']
        # endregion

        # step 2
        # region verifying of created bag
        self.bag_request.set_default('GroupAtAvgPrice', self.bag_name, [order_id1, order_id2])
        self.bag_request.update_fields_in_component('OrderBagCreationRequestBlock', {'OrderListID': list_id})
        self.java_api_manager.send_message_and_receive_response(self.bag_request)
        bag_notify_block = \
            self.java_api_manager.get_last_message(ORSMessageType.OrderBagCreationReply.value).get_parameter(
                'OrderBagCreationReplyBlock')
        self.java_api_manager.compare_values(
            {JavaApiFields.OrderBagStatus.value: OrderBagConst.OrderBagStatus_NEW.value}, bag_notify_block,
            'Check bag is created')
        order_bag_order = bag_notify_block['OrderBagOrderList']['OrderBagOrderBlock']
        self.java_api_manager.compare_values({JavaApiFields.OrdID.value: order_id1}, order_bag_order[0],
                                             'Check first order in the bag')
        self.java_api_manager.compare_values({JavaApiFields.OrdID.value: order_id2}, order_bag_order[1],
                                             'Check second order in the bag')
        bag_id = bag_notify_block[JavaApiFields.OrderBagID.value]
        # endregion

        # step 3
        # region Wave
        self.wave_creation_request.set_list_wave_with_bag(list_id, bag_id)
        self.java_api_manager.send_message_and_receive_response(self.wave_creation_request)
        list_wave_notify_block = self.java_api_manager.get_last_message(
            ORSMessageType.OrderListWaveNotification.value).get_parameter(
            JavaApiFields.OrderListWaveNotificationBlock.value)
        # endregion

        # region Verify wave
        self.java_api_manager.compare_values(
            {JavaApiFields.OrderListWaveStatus.value: OrderBagConst.OrderWaveStatus_NEW.value},
            list_wave_notify_block,
            'Check created wave from Bag')
        # endregion

        # region check child order qty
        self.java_api_manager.compare_values(
            {JavaApiFields.OrdQty.value: '200.0'},
            list_wave_notify_block['OrdNotificationElements']['OrdNotificationBlock'][0],
            'Check qty of child order from Bag')
        # endregion

        # region Wave
        self.wave_creation_request.set_default(list_id, [order_id3])
        self.java_api_manager.send_message_and_receive_response(self.wave_creation_request)
        list_wave_notify_block = self.java_api_manager.get_last_message(
            ORSMessageType.OrderListWaveNotification.value).get_parameter(
            JavaApiFields.OrderListWaveNotificationBlock.value)
        # endregion

        # region Verify wave
        self.java_api_manager.compare_values(
            {JavaApiFields.OrderListWaveStatus.value: OrderBagConst.OrderWaveStatus_NEW.value},
            list_wave_notify_block,
            'Check created wave from single order')
        # endregion

        # region check child order qty
        self.java_api_manager.compare_values(
            {JavaApiFields.OrdQty.value: '100.0'},
            list_wave_notify_block['OrdNotificationElements']['OrdNotificationBlock'][0],
            'Check qty of child order from single order')
        # endregion
