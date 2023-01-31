import logging
import os
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, BagChildCreationPolicy, OrderBagConst, \
    OrderReplyConst, SubmitRequestConst
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.OrderBagCancelRequest import OrderBagCancelRequest
from test_framework.java_api_wrappers.ors_messages.OrderBagCreationRequest import OrderBagCreationRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7643(TestCase):
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)

        self.order_submit = OrderSubmitOMS(data_set)
        self.bag_creation_request = OrderBagCreationRequest()
        self.bag_cancel_request = OrderBagCancelRequest()
        self.rule_manager = RuleManager(Simulators.equity)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        qty = '1000'
        price = '10'
        orders_id = []
        name_of_bag = 'QAP_T7643'
        qty_of_bag = str(float(qty) * 2)
        client = self.data_set.get_client_by_name('client_pt_1')
        venue_client_account = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        exec_destination = self.data_set.get_mic_by_name('mic_1')
        # endregion

        # region precondition
        # part 1: Create 2 CO orders
        self.order_submit.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                 desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                 role=SubmitRequestConst.USER_ROLE_1.value)
        self.order_submit.update_fields_in_component(
            "NewOrderSingleBlock",
            {"OrdQty": qty,
             "AccountGroupID": client,
             "Price": price})
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
                f'Checking expected and actually results for {orders_id[counter]} (precondition part 1)')
        # end of part

        # part 2 : create bag
        self.bag_creation_request.set_default(BagChildCreationPolicy.Split.value, name_of_bag, orders_id)
        self.java_api_manager.send_message_and_receive_response(self.bag_creation_request)

        order_bag_notification = \
            self.java_api_manager.get_last_message(ORSMessageType.OrderBagNotification.value).get_parameters()[
                JavaApiFields.OrderBagNotificationBlock.value]
        bag_order_id = order_bag_notification[JavaApiFields.OrderBagID.value]
        expected_result = {JavaApiFields.OrderBagName.value: name_of_bag,
                           JavaApiFields.OrderBagStatus.value: OrderBagConst.OrderBagStatus_NEW.value}

        self.java_api_manager.compare_values(expected_result, order_bag_notification,
                                             'Checking expected and actually results (precondition part 2)')
        # end of part

        # endregion

        # region step 2 : cancel bag

        # part 1: send cancel request via JavaApi
        cancel_rule = None
        self.bag_cancel_request.set_default(bag_order_id)
        try:
            cancel_rule = self.rule_manager.add_OrderCancelRequest_FIXStandard(
                self.fix_env.buy_side,
                venue_client_account, exec_destination, True)
            self.java_api_manager.send_message_and_receive_response(self.bag_cancel_request)
        except Exception as e:
            logger.error(f'{e}')
        finally:
            time.sleep(3)
            self.rule_manager.remove_rule(cancel_rule)
        # end of part

        # part 2 :check bag status
        order_bag_notification = \
            self.java_api_manager.get_last_message(ORSMessageType.OrderBagNotification.value).get_parameters()[
                JavaApiFields.OrderBagNotificationBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.OrderBagStatus.value: OrderBagConst.OrderBagStatus_CXL.value,
             JavaApiFields.LeavesQty.value: str(float(0))},
            order_bag_notification, f'Checking {JavaApiFields.OrderBagStatus.value} (step 2)')
        # end of part
        # endregion
