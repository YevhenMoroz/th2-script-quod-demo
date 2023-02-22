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
from test_framework.java_api_wrappers.ors_messages.AddOrdersToOrderListRequest import AddOrdersToOrderListRequest
from test_framework.java_api_wrappers.ors_messages.NewOrderListFromExistingOrders import NewOrderListFromExistingOrders
from test_framework.java_api_wrappers.ors_messages.RemoveOrdersFromOrderListRequest import \
    RemoveOrdersFromOrderListRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T9433(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit()
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.qty = '100'
        self.client = self.data_set.get_client_by_name('client_pt_1')
        self.alloc_account1 = self.data_set.get_account_by_name('client_pt_1_acc_1')
        self.alloc_account2 = self.data_set.get_account_by_name('client_pt_1_acc_2')
        self.alloc_account3 = self.data_set.get_account_by_name('client_pt_1_acc_3')
        self.create_list = NewOrderListFromExistingOrders()
        self.basket_name = 'Basket_QAP_T9433'
        self.remove_orders_from_basket_request = RemoveOrdersFromOrderListRequest()
        self.add_orders_to_basket_request = AddOrdersToOrderListRequest()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create 4 CO orders
        # 1
        self.fix_message.set_default_care_limit()
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id1 = response[0].get_parameter("OrderID")
        # 2
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id2 = response[0].get_parameter("OrderID")
        # 3
        self.fix_message.set_default_care_limit('instrument_3')
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id3 = response[0].get_parameter("OrderID")
        # 4
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id4 = response[0].get_parameter("OrderID")
        # endregion

        # region create basket
        list_of_orders = [order_id1, order_id2, order_id3, order_id4]
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

        # region remove orders from basket
        order_list = []
        for order_id in list_of_orders:
            order_id_dict = {"OrdID": order_id}
            order_list.append(order_id_dict)
        self.remove_orders_from_basket_request.set_default(order_id1, list_id)
        self.remove_orders_from_basket_request.update_fields_in_component('RemoveOrdersFromOrderListRequestBlock',
                                                                          {"OrdIDList":
                                                                              {
                                                                                  "OrdIDBlock":
                                                                                      order_list
                                                                              }})
        self.java_api_manager.send_message_and_receive_response(self.remove_orders_from_basket_request)
        # endregion

        # region check basket sts after removing orders
        ord_list_notify = self.java_api_manager.get_last_message(
            ORSMessageType.OrdListNotification.value).get_parameter(
            JavaApiFields.OrdListNotificationBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.ListOrderStatus.value: OrdListNotificationConst.ListOrderStatus_DON.value},
            ord_list_notify, 'Check Basket sts after removing orders')
        # endregion

        # region add orders to list
        self.add_orders_to_basket_request.set_default(order_id1, list_id)
        self.add_orders_to_basket_request.update_fields_in_component('AddOrdersToOrderListRequestBlock', {"OrdIDList":
            {
                "OrdIDBlock":
                    order_list
            }})
        self.java_api_manager.send_message_and_receive_response(self.add_orders_to_basket_request)
        # endregion

        # region Verify wave
        add_orders_to_list_reply = self.java_api_manager.get_last_message(
            ORSMessageType.AddOrdersToOrderListReply.value).get_parameter(
            JavaApiFields.AddOrdersToOrderListReplyBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.FreeNotes.value: f'Runtime error (OrderList {list_id} is in a terminal state)'},
            add_orders_to_list_reply, 'Check error in Add Orders To List action')
        # endregion
