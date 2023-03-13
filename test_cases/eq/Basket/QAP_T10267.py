import logging
import os
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType, CSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.cs_message.CDOrdAckBatchRequest import CDOrdAckBatchRequest
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrdListNotificationConst, \
    OrderReplyConst, BagMessagesConst
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.AddOrdersToOrderListRequest import AddOrdersToOrderListRequest
from test_framework.java_api_wrappers.ors_messages.NewOrderListFromExistingOrders import NewOrderListFromExistingOrders
from test_framework.java_api_wrappers.ors_messages.OrderBagCreationRequest import OrderBagCreationRequest
from test_framework.java_api_wrappers.ors_messages.OrderListWaveCancelRequest import OrderListWaveCancelRequest
from test_framework.java_api_wrappers.ors_messages.OrderListWaveCreationRequest import OrderListWaveCreationRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T10267(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_connectivity2 = self.environment.get_list_java_api_environment()[0].java_api_conn_user2
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.java_api_manager2 = JavaApiManager(self.java_api_connectivity2, self.test_id)
        self.qty = '100'
        self.client = self.data_set.get_client_by_name('client_2')
        self.create_list = NewOrderListFromExistingOrders()
        self.basket_name = 'Basket_QAP_T10267'
        self.bag_name = 'Bag_QAP_T10267'
        self.add_orders_to_basket_request = AddOrdersToOrderListRequest()
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.accept_request = CDOrdAckBatchRequest()
        self.wave_creation_request = OrderListWaveCreationRequest()
        self.bag_request = OrderBagCreationRequest()
        self.rule_manager = RuleManager(Simulators.equity)
        self.venue_client_name = self.data_set.get_venue_client_names_by_name('client_2_venue_1')
        self.mic = self.data_set.get_mic_by_name('mic_1')
        self.price = '20'
        self.cancel_wave = OrderListWaveCancelRequest()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        #  Accept CO orders
        order_id1_user1 = self.__create_order_and_accept_by_user1()
        order_id2_user1 = self.__create_order_and_accept_by_user1()
        order_id1_user2 = self.__create_order_and_accept_by_user2()
        order_id2_user2 = self.__create_order_and_accept_by_user2()
        # endregion

        # Create Basket with orders
        list_of_orders = [order_id1_user1, order_id2_user1, order_id1_user2]
        self.create_list.set_default(list_of_orders, self.basket_name)
        self.java_api_manager.send_message_and_receive_response(self.create_list)
        # endregion

        # region check values of basket
        list_notify_block = \
            self.java_api_manager.get_last_message(ORSMessageType.OrdListNotification.value).get_parameter(
                JavaApiFields.OrdListNotificationBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.ListOrderStatus.value: OrdListNotificationConst.ListOrderStatus_EXE.value},
            list_notify_block, 'Check List status')
        i = 0
        for order in list_of_orders:
            self.java_api_manager.compare_values(
                {JavaApiFields.OrdID.value: order},
                list_notify_block['OrdIDList']['OrdIDBlock'][i], f'Check order {order} is in the list')
            i = i + 1
        list_id = list_notify_block['OrderListID']
        # endregion

        # Create add order to basket
        self.add_orders_to_basket_request.set_default(order_id2_user2, list_id)
        self.java_api_manager.send_message_and_receive_response(self.add_orders_to_basket_request)
        # endregion

        # region check values of basket
        list_notify_block = \
            self.java_api_manager.get_last_message(ORSMessageType.OrdListNotification.value).get_parameter(
                JavaApiFields.OrdListNotificationBlock.value)
        list_of_orders.append(order_id2_user2)
        i = 0
        for order in list_of_orders:
            self.java_api_manager.compare_values(
                {JavaApiFields.OrdID.value: order},
                list_notify_block['OrdIDList']['OrdIDBlock'][i], f'Check order {order} is in the list after adding order')
            i = i + 1
        # endregion

        # region Wave
        new_order_single_rule = None
        list_wave_notify_block = None
        ord_list_wave_id = None
        try:
            new_order_single_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side, self.venue_client_name, self.mic, float(self.price))
            self.wave_creation_request.set_default(list_id, list_of_orders)
            self.java_api_manager.send_message_and_receive_response(self.wave_creation_request)
            list_wave_notify_block = self.java_api_manager.get_last_message(
                ORSMessageType.OrderListWaveNotification.value).get_parameter(
                JavaApiFields.OrderListWaveNotificationBlock.value)
            ord_list_wave_id = list_wave_notify_block[JavaApiFields.OrderListWaveID.value]
        except Exception as ex:
            logger.exception(f'{ex} - your exception')
        finally:
            self.rule_manager.remove_rule(new_order_single_rule)
        # endregion

        # region Verify child orders
        for i in range(4):
            ord_notify_element = list_wave_notify_block['OrdNotificationElements']['OrdNotificationBlock']
            self.java_api_manager.compare_values(
                {JavaApiFields.OrdQty.value: '100.0'},
                ord_notify_element[i],
                f'Check {i} Child Order after waving')
        # endregion

        # region cancel wave
        order_cancel_rule = None
        try:
            order_cancel_rule = self.rule_manager.add_OrderCancelRequest_FIXStandard(
                self.fix_env.buy_side, self.venue_client_name, self.mic, True)
            self.cancel_wave.set_default(ord_list_wave_id)
            self.java_api_manager.send_message_and_receive_response(self.cancel_wave)
            list_wave_notify_block = self.java_api_manager.get_last_message(
                ORSMessageType.OrderListWaveNotification.value).get_parameter(
                JavaApiFields.OrderListWaveNotificationBlock.value)
            self.java_api_manager.compare_values(
                {JavaApiFields.OrderListWaveStatus.value: OrdListNotificationConst.OrderListWaveStatus_CXL.value},
                list_wave_notify_block,
                f'Check wave status')
        except Exception as ex:
            logger.exception(f'{ex} - your exception')
        finally:
            self.rule_manager.remove_rule(order_cancel_rule)
        # endregion

        # region Bag Basket
        self.bag_request.set_default('GroupAtAvgPrice', self.bag_name, list_of_orders)
        self.bag_request.update_fields_in_component('OrderBagCreationRequestBlock', {'OrderListID': list_id})
        self.java_api_manager.send_message_and_receive_response(self.bag_request)
        # endregion

        # region Verify child orders
        ord_bag_notify_block = \
            self.java_api_manager.get_last_message(ORSMessageType.OrderBagNotification.value).get_parameter(
                JavaApiFields.OrderBagNotificationBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.OrderBagStatus.value: BagMessagesConst.OrderBagStatus_NEW.value},
            ord_bag_notify_block,
            'Check bag is created')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def __create_order_and_accept_by_user1(self):
        self.order_submit.set_default_care_limit(
            desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
        )
        self.order_submit.update_fields_in_component(
            "NewOrderSingleBlock",
            {"AccountGroupID": self.client, "ClOrdID": bca.client_orderid(9)},
        )
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        cd_order_notif_message = self.java_api_manager.get_last_message(CSMessageType.CDOrdNotif.value)
        cd_order_notif_id = cd_order_notif_message.get_parameter("CDOrdNotifBlock")["CDOrdNotifID"]
        order_notif_message = self.java_api_manager.get_last_message(
            ORSMessageType.OrdNotification.value
        ).get_parameters()[JavaApiFields.OrderNotificationBlock.value]
        ord_id = order_notif_message["OrdID"]
        desk_id = order_notif_message["RecipientDeskID"]
        self.java_api_manager.compare_values(
            {
                JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_SEN.value,
            },
            order_notif_message,
            "Check Status of Care order",
        )
        # endregion

        #  Accept CO order in Client Inbox by User2
        self.accept_request.set_default(ord_id, cd_order_notif_id, desk_id)
        self.java_api_manager.send_message_and_receive_response(self.accept_request)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        self.java_api_manager.compare_values(
            {
                JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value,
                "UserID": "JavaApiUser",
                "RecipientUserID": "JavaApiUser",
            },
            order_reply,
            "Check Status of Care order",
        )
        return ord_id

    @try_except(test_id=Path(__file__).name[:-3])
    def __create_order_and_accept_by_user2(self):
        self.order_submit.set_default_care_limit(
            desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
        )
        self.order_submit.update_fields_in_component(
            "NewOrderSingleBlock",
            {"AccountGroupID": self.client, "ClOrdID": bca.client_orderid(9)},
        )
        self.java_api_manager2.send_message_and_receive_response(self.order_submit)
        cd_order_notif_message = self.java_api_manager2.get_last_message(CSMessageType.CDOrdNotif.value)
        cd_order_notif_id = cd_order_notif_message.get_parameter("CDOrdNotifBlock")["CDOrdNotifID"]
        order_notif_message = self.java_api_manager2.get_last_message(
            ORSMessageType.OrdNotification.value
        ).get_parameters()[JavaApiFields.OrderNotificationBlock.value]
        ord_id = order_notif_message["OrdID"]
        desk_id = order_notif_message["RecipientDeskID"]
        self.java_api_manager2.compare_values(
            {
                JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_SEN.value,
            },
            order_notif_message,
            "Check Status of Care order",
        )
        # endregion

        #  Accept CO order in Client Inbox by User2
        self.accept_request.set_default(ord_id, cd_order_notif_id, desk_id)
        self.java_api_manager2.send_message_and_receive_response(self.accept_request)
        order_reply = self.java_api_manager2.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        self.java_api_manager2.compare_values(
            {
                JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value,
                "UserID": "JavaApiUser2",
                "RecipientUserID": "JavaApiUser2",
            },
            order_reply,
            "Check Status of Care order after Accept by User2",
        )
        return ord_id
