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
from test_framework.db_wrapper.db_manager import DBManager
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import BagChildCreationPolicy, JavaApiFields, OrderBagConst, \
    OrdTypes, OrderReplyConst, BasketMessagesConst
from test_framework.java_api_wrappers.ors_messages.NewOrderListFromExistingOrders import NewOrderListFromExistingOrders
from test_framework.java_api_wrappers.ors_messages.OrderBagCreationRequest import OrderBagCreationRequest
from test_framework.java_api_wrappers.ors_messages.OrderBagDissociateRequest import OrderBagDissociateRequest
from test_framework.java_api_wrappers.ors_messages.OrderBagWaveRequest import OrderBagWaveRequest
from test_framework.java_api_wrappers.ors_messages.OrderModificationRequest import OrderModificationRequest
from test_framework.java_api_wrappers.ors_messages.RemoveOrdersFromOrderListRequest import \
    RemoveOrdersFromOrderListRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T10562(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.nos1 = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.nos2 = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.nos3 = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.nos4 = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit("instrument_2")
        self.nos5 = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit("instrument_2")
        self.client = self.data_set.get_client_by_name("client_1")
        self.client_acc = self.data_set.get_account_by_name('client_1_acc_1')
        # self.price = self.nos.get_parameter("Price")
        self.price = '5'
        self.qty = self.nos1.get_parameter("OrderQtyData")["OrderQty"]
        self.rule_manager = RuleManager(Simulators.equity)
        self.bs_connectivity = self.fix_env.buy_side
        self.venue_client_name = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        self.mic = self.data_set.get_mic_by_name('mic_1')
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)
        self.create_basket = NewOrderListFromExistingOrders()
        self.bag_creation_request = OrderBagCreationRequest()
        self.bag_wave_request = OrderBagWaveRequest()
        self.bag_dissociate_request = OrderBagDissociateRequest()
        self.modification_request = OrderModificationRequest()
        self.remove_order_from_basket_request = RemoveOrdersFromOrderListRequest()
        self.db_manager = DBManager(environment.get_list_data_base_environment()[0])

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition
        resp1 = self.fix_manager.send_message_and_receive_response_fix_standard(self.nos1)
        resp2 = self.fix_manager.send_message_and_receive_response_fix_standard(self.nos2)
        resp3 = self.fix_manager.send_message_and_receive_response_fix_standard(self.nos3)
        resp4 = self.fix_manager.send_message_and_receive_response_fix_standard(self.nos4)
        resp5 = self.fix_manager.send_message_and_receive_response_fix_standard(self.nos5)
        ord_id1 = resp1[0].get_parameter("OrderID")
        ord_id2 = resp2[0].get_parameter("OrderID")
        ord_id3 = resp3[0].get_parameter("OrderID")
        ord_id4 = resp4[0].get_parameter("OrderID")
        ord_id5 = resp5[0].get_parameter("OrderID")
        orders_id = [ord_id1, ord_id2, ord_id3, ord_id4, ord_id5]
        orders_id_bag1 = [ord_id1, ord_id2, ord_id3]
        orders_id_bag2 = [ord_id4, ord_id5]
        # endregion

        # region Step 1-2: MassModify, set AlloAccount and Price
        self.__send_modif_request(ord_id1, "1st")
        self.__send_modif_request(ord_id2, "2nd")
        self.__send_modif_request(ord_id3, "3rd")
        self.__send_modif_request(ord_id4, "4th")
        self.__send_modif_request(ord_id5, "5th")
        # endregion

        # region Step 3 - Create Basket
        basket_name = 'Basket_for_QAP_T10562'
        self.create_basket.set_default(orders_id, basket_name)
        self.java_api_manager.send_message_and_receive_response(self.create_basket)
        list_notification = self.java_api_manager.get_last_message(
            ORSMessageType.OrdListNotification.value).get_parameter(
            JavaApiFields.OrdListNotificationBlock.value)
        self.java_api_manager.compare_values({JavaApiFields.OrderListName.value: basket_name}, list_notification,
                                             'Step 3: Check created basket')
        list_id = list_notification[JavaApiFields.OrderListID.value]
        # endregion

        # region Step 4 - Create Bags
        bag_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))

        self.bag_creation_request.set_default(BagChildCreationPolicy.AVP.value, bag_name, orders_id_bag1)
        self.java_api_manager.send_message_and_receive_response(self.bag_creation_request)
        order_bag_notification = \
            self.java_api_manager.get_last_message(ORSMessageType.OrderBagNotification.value).get_parameters()[
                JavaApiFields.OrderBagNotificationBlock.value]
        bag_order_id1 = order_bag_notification[JavaApiFields.OrderBagID.value]
        expected_result = {JavaApiFields.OrderBagStatus.value: OrderBagConst.OrderBagStatus_NEW.value}
        self.java_api_manager.compare_values(expected_result, order_bag_notification, "Step 4: Check created 1st Bag")
        self._verify_orders(orders_id_bag1, bag_order_id1, list_id, 4)

        bag_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.bag_creation_request.set_default(BagChildCreationPolicy.AVP.value, bag_name, orders_id_bag2)
        self.java_api_manager.send_message_and_receive_response(self.bag_creation_request)
        order_bag_notification = \
            self.java_api_manager.get_last_message(ORSMessageType.OrderBagNotification.value).get_parameters()[
                JavaApiFields.OrderBagNotificationBlock.value]
        bag_order_id2 = order_bag_notification[JavaApiFields.OrderBagID.value]
        self.java_api_manager.compare_values(expected_result, order_bag_notification, "Step 4: Check created 2nd Bag")
        self._verify_orders(orders_id_bag2, bag_order_id2, list_id, 4)
        # endregion

        # region Step 5 - Dissociate Bags
        self.bag_dissociate_request.set_default(bag_order_id1)
        self.java_api_manager.send_message_and_receive_response(self.bag_dissociate_request)
        order_bag_notification = \
            self.java_api_manager.get_last_message(ORSMessageType.OrderBagNotification.value).get_parameters()[
                JavaApiFields.OrderBagNotificationBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.OrderBagStatus.value: OrderBagConst.OrderBagStatus_TER.value},
            order_bag_notification, 'Step 5: Checking OrderBagStatus after dissociate 1st bag')
        self._verify_orders(orders_id_bag1, None, list_id, 5)

        ord_update = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value, ord_id1).get_parameter(
            JavaApiFields.OrderNotificationBlock.value)
        ord_update2 = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value,
                                                             ord_id2).get_parameter(
            JavaApiFields.OrderNotificationBlock.value)
        expected_result = {JavaApiFields.LeavesQty.value: str(float(self.qty)),
                           JavaApiFields.UnmatchedQty.value: str(float(self.qty)),
                           JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value}

        self.bag_dissociate_request.set_default(bag_order_id2)
        self.java_api_manager.send_message_and_receive_response(self.bag_dissociate_request)
        order_bag_notification = \
            self.java_api_manager.get_last_message(ORSMessageType.OrderBagNotification.value).get_parameters()[
                JavaApiFields.OrderBagNotificationBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.OrderBagStatus.value: OrderBagConst.OrderBagStatus_TER.value},
            order_bag_notification, 'Step 5: Checking OrderBagStatus after dissociate 2nd bag')
        self._verify_orders(orders_id_bag2, None, list_id, 5)

        # endregion
        # region Step 6: remove first order from basket
        order_ids_list = []
        for order in orders_id:
            dict = {"OrdID": order}
            order_ids_list.append(dict)
        self.remove_order_from_basket_request.set_default(ord_id1, list_id)
        self.remove_order_from_basket_request.update_fields_in_component('RemoveOrdersFromOrderListRequestBlock',
                                                                         {"OrdIDList": {"OrdIDBlock": order_ids_list}})
        self.java_api_manager.send_message_and_receive_response(self.remove_order_from_basket_request)
        self.java_api_manager.get_last_message(ORSMessageType.OrdListNotification.value)
        list_notify_block = self.java_api_manager.get_last_message(
            ORSMessageType.OrdListNotification.value).get_parameter(
            JavaApiFields.OrdListNotificationBlock.value)
        # endregion

        # region check values
        self.java_api_manager.compare_values(
            {JavaApiFields.ListOrderStatus.value: BasketMessagesConst.ListOrderStatus_DON.value}, list_notify_block,
            'Step 6: Check basket status after orders are removed')

        self._verify_orders(orders_id, None, None, 6)
        # endregion

    def _verify_orders(self, ord_list: list, orderbagid, orderlistid, step: int):
        for order in ord_list:
            response = self._get_orderbag_orderlist_id(order)[0]
            actual_result = {'orderbagid': str(response[0]) if response[0] is not None else None,
                             'orderlistid': str(response[1]) if response[1] is not None else None}
            self.java_api_manager.compare_values({'orderbagid': orderbagid, 'orderlistid': orderlistid}, actual_result,
                                                 f"Step {step}: Verify Bag and Basket belong to the {order} order")

    def _get_orderbag_orderlist_id(self, order_id):
        result = self.db_manager.execute_query(f"SELECT orderbagid, orderlistid from ordr WHERE ordid = '{order_id}'")
        return result

    def __send_modif_request(self, ord_id: str, number_of_order: str):
        pre_trade_allocation_list_dict = {JavaApiFields.PreTradeAllocationList.value: {
            JavaApiFields.PreTradeAllocAccountBlock.value: [
                {JavaApiFields.AllocAccountID.value: self.client_acc,
                 JavaApiFields.AllocQty.value: str(float(self.qty))}]}}
        self.modification_request.set_default(self.data_set, ord_id)
        self.modification_request.update_fields_in_component(
            "OrderModificationRequestBlock", {"Price": self.price, "AccountGroupID": self.client,
                                              JavaApiFields.PreTradeAllocationBlock.value: pre_trade_allocation_list_dict})
        responses = self.java_api_manager.send_message_and_receive_response(self.modification_request)
        order_modif_reply = self.java_api_manager.get_last_message(
            ORSMessageType.OrderModificationReply.value
        ).get_parameters()[JavaApiFields.OrderModificationReplyBlock.value]
        self.java_api_manager.compare_values(
            {"Price": str(float(self.price)),
             JavaApiFields.PreTradeAllocationBlock.value: pre_trade_allocation_list_dict},
            order_modif_reply["OrdModify"],
            f"Step 1-2: Checking Price and AlloAccount after Modification {number_of_order} order",
        )
