import logging
import os
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import Simulators, RuleManager
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrdListNotificationConst, \
    BasketMessagesConst, OrderReplyConst
from test_framework.java_api_wrappers.oms.ors_messges.NewOrderListOMS import NewOrderListOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.CancelOrderRequest import CancelOrderRequest
from test_framework.java_api_wrappers.ors_messages.NewOrderListFromExistingOrders import NewOrderListFromExistingOrders
from test_framework.java_api_wrappers.ors_messages.RemoveOrdersFromOrderListRequest import \
    RemoveOrdersFromOrderListRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T9184(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.list_creation_request = NewOrderListOMS(self.data_set)
        self.rule_manager = RuleManager(Simulators.equity)
        self.venue_client_name = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        self.mic = self.data_set.get_mic_by_name('mic_1')
        self.price = '10'
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.cancel_request = CancelOrderRequest()
        self.remove_orders_from_basket_request = RemoveOrdersFromOrderListRequest()
        self.create_basket_from_exist_orders = NewOrderListFromExistingOrders()
        self.basket_name = 'QAP_T9184'

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create orders
        self.list_creation_request.set_default_order_list()
        self.java_api_manager.send_message_and_receive_response(self.list_creation_request)
        order_list_notification = \
            self.java_api_manager.get_last_message(ORSMessageType.OrdListNotification.value).get_parameters()[
                JavaApiFields.OrdListNotificationBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.ListOrderStatus.value: BasketMessagesConst.ListOrderStatus_EXE.value},
            order_list_notification,
            'Check created first basket')
        list_id = order_list_notification['OrderListID']
        ord_id1 = order_list_notification['OrdNotificationElements']['OrdNotificationBlock'][0][
            'OrdID']
        ord_id2 = order_list_notification['OrdNotificationElements']['OrdNotificationBlock'][1][
            'OrdID']
        # endregion

        # region split order
        new_order_single_rule = None
        child_ord_id = None
        try:
            new_order_single_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side, self.venue_client_name, self.mic, float(self.price))
            self.order_submit.set_default_child_dma(ord_id1)
            self.order_submit.update_fields_in_component('NewOrderSingleBlock', {"Price": "10"})
            self.java_api_manager.send_message_and_receive_response(self.order_submit)
            child_ord_id = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameter(
                JavaApiFields.OrdNotificationBlock.value)['OrdID']
        except Exception as ex:
            logger.exception(f'{ex} - your exception')
        finally:
            self.rule_manager.remove_rule(new_order_single_rule)
        # endregion

        # region cancel child order
        order_cancel_rule = None
        try:
            order_cancel_rule = self.rule_manager.add_OrderCancelRequest_FIXStandard(
                self.fix_env.buy_side, self.venue_client_name, self.mic, True)
            self.cancel_request.set_default(child_ord_id)
            self.java_api_manager.send_message_and_receive_response(self.cancel_request)
            ord_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value,
                                                               child_ord_id).get_parameter(
                JavaApiFields.OrdReplyBlock.value)
            self.java_api_manager.compare_values({JavaApiFields.ExecType.value: OrderReplyConst.TransStatus_CXL.value},
                                                 ord_reply, 'Check cancelletion of child order')
        except Exception as ex:
            logger.exception(f'{ex} - your exception')
        finally:
            self.rule_manager.remove_rule(order_cancel_rule)
        # endregion

        # region remove orders from basket
        list_of_orders = [ord_id1, ord_id2]
        order_list = []
        for order_id in list_of_orders:
            order_id_dict = {"OrdID": order_id}
            order_list.append(order_id_dict)
        self.remove_orders_from_basket_request.set_default(ord_id1, list_id)
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

        # region create basket
        self.create_basket_from_exist_orders.set_default(list_of_orders, self.basket_name)
        self.java_api_manager.send_message_and_receive_response(self.create_basket_from_exist_orders)
        # endregion

        # region check basket sts after creation
        list_notify_block = \
            self.java_api_manager.get_last_message(ORSMessageType.NewOrderListReply.value).get_parameters()[
                'NewOrderListReplyBlock']
        self.java_api_manager.compare_values(
            {JavaApiFields.ListOrderStatus.value: OrdListNotificationConst.ListOrderStatus_EXE.value},
            list_notify_block, 'Check List status')
        # endregion
