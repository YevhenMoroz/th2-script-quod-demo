import logging
import os
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrdListNotificationConst
from test_framework.java_api_wrappers.ors_messages.NewOrderListFromExistingOrders import NewOrderListFromExistingOrders
from test_framework.java_api_wrappers.ors_messages.OrderBagCreationRequest import OrderBagCreationRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T9185(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.new_order_single1 = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.new_order_single2 = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit('instrument_3')
        self.bag_request = OrderBagCreationRequest()
        self.list_creation_request = NewOrderListFromExistingOrders()
        self.bag_name = 'BAG_QAP_T9185'
        self.basket_name = 'Basket_QAP_T9185'

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create orders
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.new_order_single1)
        order_id1 = response[0].get_parameter("OrderID")
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.new_order_single2)
        order_id2 = response[0].get_parameter("OrderID")
        # endregion

        # region create basket
        self.list_creation_request.set_default([order_id1, order_id2], self.basket_name)
        self.java_api_manager.send_message_and_receive_response(self.list_creation_request)
        list_notify_block = \
            self.java_api_manager.get_last_message(ORSMessageType.NewOrderListReply.value).get_parameters()[
                'NewOrderListReplyBlock']
        self.java_api_manager.compare_values(
            {JavaApiFields.ListOrderStatus.value: OrdListNotificationConst.ListOrderStatus_EXE.value},
            list_notify_block, 'Check List status')
        list_id = list_notify_block['OrderListID']
        # endregion

        # region verifying of created bag
        self.bag_request.set_default('GroupAtAvgPrice', self.bag_name, [order_id1, order_id2])
        self.bag_request.update_fields_in_component('OrderBagCreationRequestBlock', {'OrderListID': list_id})
        self.java_api_manager.send_message_and_receive_response(self.bag_request)
        bag_notify_block = \
            self.java_api_manager.get_last_message(ORSMessageType.OrderBagCreationReply.value).get_parameters()[
                'OrderBagCreationReplyBlock']
        self.java_api_manager.compare_values(
            {'FreeNotes': 'Cannot create bag with orders on different instruments'}, bag_notify_block,
            'Check bag is not created')
        # endregion
