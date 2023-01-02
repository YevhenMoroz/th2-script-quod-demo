import logging
import os
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import SubmitRequestConst, JavaApiFields, OrderReplyConst, \
    BagChildCreationPolicy, OrderBagConst
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.java_api_wrappers.ors_messages.ModifyBagOrderRequest import ModifyBagOrderRequest
from test_framework.java_api_wrappers.ors_messages.OrderBagCreationRequest import OrderBagCreationRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7649(TestCase):
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)
        self.order_submit = OrderSubmitOMS(data_set)
        self.bag_creation_request = OrderBagCreationRequest()
        self.trade_entry = TradeEntryOMS(self.data_set)
        self.bag_modification_request = ModifyBagOrderRequest()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        qty = '1000'
        price = '10'
        orders_id = []
        name_of_bag = 'QAP_T7649'
        qty_of_bag = str(float(qty) * 3)
        last_bag_order_qty = str(float(qty) * 4)
        client = self.data_set.get_client_by_name('client_pt_1')
        # endregion

        # region precondition
        self.order_submit.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                 desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                 role=SubmitRequestConst.USER_ROLE_1.value)
        self.order_submit.update_fields_in_component(
            "NewOrderSingleBlock",
            {"OrdQty": qty,
             "AccountGroupID": client,
             "Price": price})
        for counter in range(4):
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
                f'Checking expected and actually results for {orders_id[counter]} (precondition part 1)')
        # endregion

        # region step 1, step 2, step 3 , step 4, step 5 : create bag with 3 first orders
        fourth_order_id = orders_id.pop(3)

        self.bag_creation_request.set_default(BagChildCreationPolicy.Split.value, name_of_bag, orders_id)
        self.java_api_manager.send_message_and_receive_response(self.bag_creation_request)

        order_bag_notification = \
            self.java_api_manager.get_last_message(ORSMessageType.OrderBagNotification.value).get_parameters()[
                JavaApiFields.OrderBagNotificationBlock.value]
        bag_order_id = order_bag_notification[JavaApiFields.OrderBagID.value]
        expected_result = {JavaApiFields.OrderBagName.value: name_of_bag,
                           JavaApiFields.OrderBagStatus.value: OrderBagConst.OrderBagStatus_NEW.value,
                           JavaApiFields.OrderBagQty.value: qty_of_bag}
        self.java_api_manager.compare_values(expected_result, order_bag_notification,
                                             'Checking expected and actually results (step 5)')
        # endregion

        # region step 6 step 7 , step 8 step 9 : Modify Bag
        orders_id.append(fourth_order_id)
        self.bag_modification_request.set_default(bag_order_id, price, name_of_bag)
        self.bag_modification_request.add_components_into_repeating_group('OrderBagOrderList', 'OrderBagOrderBlock',
                                                                          'OrdID',
                                                                          orders_id)

        self.java_api_manager.send_message_and_receive_response(self.bag_modification_request)

        order_bag_notification = self.java_api_manager.get_last_message(ORSMessageType.OrderBagNotification.value). \
            get_parameters()[JavaApiFields.OrderBagNotificationBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.OrderBagQty.value: last_bag_order_qty},
                                             order_bag_notification,
                                             'Checking expected and actually results (step 9)')
        # endregion
