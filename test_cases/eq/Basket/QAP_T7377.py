import logging
import os
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, BasketMessagesConst, \
    SubmitRequestConst, OrderReplyConst, BagChildCreationPolicy, OrderBagConst
from test_framework.java_api_wrappers.oms.ors_messges.NewOrderListOMS import NewOrderListOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.AddOrdersToOrderListRequest import AddOrdersToOrderListRequest
from test_framework.java_api_wrappers.ors_messages.OrderBagCreationRequest import OrderBagCreationRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7377(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.list_creation_request = NewOrderListOMS(self.data_set)
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.bag_creation_request = OrderBagCreationRequest()
        self.name_of_bag = 'BasketPrecondition'
        self.add_orders_to_orderlist_request = AddOrdersToOrderListRequest()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        self.list_creation_request.set_default_order_list()
        self.java_api_manager.send_message_and_receive_response(self.list_creation_request)
        order_list_notification = \
            self.java_api_manager.get_last_message(ORSMessageType.OrdListNotification.value).get_parameters()[
                JavaApiFields.OrdListNotificationBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.ListOrderStatus.value: BasketMessagesConst.ListOrderStatus_EXE.value},
            order_list_notification,
            'Check created basket')
        list_id = order_list_notification['OrderListID']
        # endregion

        # region create orders
        self.order_submit.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                 desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                 role=SubmitRequestConst.USER_ROLE_1.value)
        orders_id = []
        for counter in range(2):
            self.order_submit.update_fields_in_component('NewOrderSingleBlock',
                                                         {
                                                             "ClOrdID": bca.client_orderid(9)
                                                         })
            self.java_api_manager.send_message_and_receive_response(self.order_submit)
            order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
                JavaApiFields.OrdReplyBlock.value]
            orders_id.append(order_reply[JavaApiFields.OrdID.value])

            self.java_api_manager.compare_values(
                {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                order_reply,
                f'Checking sts of {counter + 1} order')
            # endregion

        # region create bag
        self.bag_creation_request.set_default(BagChildCreationPolicy.Split.value, self.name_of_bag, orders_id)
        self.java_api_manager.send_message_and_receive_response(self.bag_creation_request)

        order_bag_notification = \
                self.java_api_manager.get_last_message(ORSMessageType.OrderBagNotification.value).get_parameters()[
                    JavaApiFields.OrderBagNotificationBlock.value]
        bag_id = order_bag_notification['OrderBagID']
        expected_result = {JavaApiFields.OrderBagName.value: self.name_of_bag,
                               JavaApiFields.OrderBagStatus.value: OrderBagConst.OrderBagStatus_NEW.value}
        self.java_api_manager.compare_values(expected_result, order_bag_notification,
                                                 'Check created bag')
        # endregion

        # region add order from bag to basket
        self.add_orders_to_orderlist_request.set_default(orders_id[0], list_id)
        self.java_api_manager.send_message_and_receive_response(self.add_orders_to_orderlist_request)
        add_orders_to_list_reply = \
        self.java_api_manager.get_last_message(ORSMessageType.AddOrdersToOrderListReply.value).get_parameters()[
                    JavaApiFields.AddOrdersToOrderListReplyBlock.value]
        self.java_api_manager.compare_values(
                {'FreeNotes': f'Runtime error (order {orders_id[0]} belongs to bag {bag_id})'},
                add_orders_to_list_reply,
                'Check order from bag was not add to basket')
