import logging
import os
from pathlib import Path

from custom import basic_custom_actions as bca, basic_custom_actions
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, BasketMessagesConst
from test_framework.java_api_wrappers.oms.ors_messges.NewOrderListOMS import NewOrderListOMS
from test_framework.java_api_wrappers.ors_messages.AddOrdersToOrderListRequest import AddOrdersToOrderListRequest


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7378(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.list_creation_request = NewOrderListOMS(self.data_set)
        self.add_orders_to_orderlist_request = AddOrdersToOrderListRequest()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create first basket
        self.list_creation_request.set_default_order_list()
        self.java_api_manager.send_message_and_receive_response(self.list_creation_request)
        order_list_notification = \
            self.java_api_manager.get_last_message(ORSMessageType.OrdListNotification.value).get_parameters()[
                JavaApiFields.OrdListNotificationBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.ListOrderStatus.value: BasketMessagesConst.ListOrderStatus_EXE.value},
            order_list_notification,
            'Check created first basket')
        list_id_1 = order_list_notification['OrderListID']
        ord_id_from_first_basket = order_list_notification['OrdNotificationElements']['OrdNotificationBlock'][0]['OrdID']
        # endregion

        # region create second basket
        self.list_creation_request.set_default_order_list()
        self.list_creation_request.update_fields_in_component('NewOrderListBlock',
                                                              {'OrderListName': basic_custom_actions.client_orderid(9)})
        self.java_api_manager.send_message_and_receive_response(self.list_creation_request)
        order_list_notification = \
            self.java_api_manager.get_last_message(ORSMessageType.OrdListNotification.value).get_parameters()[
                JavaApiFields.OrdListNotificationBlock.value]
        list_id_2 = order_list_notification['OrderListID']
        self.java_api_manager.compare_values(
            {JavaApiFields.ListOrderStatus.value: BasketMessagesConst.ListOrderStatus_EXE.value},
            order_list_notification,
            'Check created second basket')
        # endregion

        # region add order from first basket to second basket
        self.add_orders_to_orderlist_request.set_default(ord_id_from_first_basket, list_id_2)
        self.java_api_manager.send_message_and_receive_response(self.add_orders_to_orderlist_request)
        add_orders_to_list_reply = \
            self.java_api_manager.get_last_message(ORSMessageType.AddOrdersToOrderListReply.value).get_parameters()[
                JavaApiFields.AddOrdersToOrderListReplyBlock.value]
        self.java_api_manager.compare_values(
            {'FreeNotes': f'Runtime error (order {ord_id_from_first_basket} belongs to list {list_id_1})'},
            add_orders_to_list_reply,
            'Check order from first basket was not add to the second basket')
