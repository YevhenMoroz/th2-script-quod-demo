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
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderBagConst, ExecutionReportConst, \
    OrderReplyConst, BagChildCreationPolicy, SubmitRequestConst
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.java_api_wrappers.ors_messages.CancelOrderRequest import CancelOrderRequest
from test_framework.java_api_wrappers.ors_messages.OrderBagCreationRequest import OrderBagCreationRequest
from test_framework.java_api_wrappers.ors_messages.OrderBagDissociateRequest import OrderBagDissociateRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7168(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)
        self.order_submit = OrderSubmitOMS(data_set)
        self.order_submit2 = OrderSubmitOMS(self.data_set)
        self.order_submit3 = OrderSubmitOMS(self.data_set)
        self.order_submit4 = OrderSubmitOMS(self.data_set)
        self.bs_connectivity = self.fix_env.buy_side
        self.venue_client_name = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        self.mic = self.data_set.get_mic_by_name('mic_1')
        self.bag_creation_request = OrderBagCreationRequest()
        self.rule_manager = RuleManager(Simulators.equity)
        self.execution_report = ExecutionReportOMS(self.data_set)
        self.bag_dissociate_request = OrderBagDissociateRequest()
        self.trade_entry = TradeEntryOMS(self.data_set)
        self.cancel_order = CancelOrderRequest()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        qty = '150'
        price = '2'
        client = self.data_set.get_client_by_name('client_1')
        orders_id = []
        child_orders_id = []
        name_of_bag = 'QAP_T7168'
        new_order_single_rule = None
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
                f'Checking expected and actually results for {orders_id[counter]} (precondition)')

        # endregion

        # region 1 - Split both CO
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.bs_connectivity,
                                                                                                  self.venue_client_name,
                                                                                                  self.mic,
                                                                                                  int(price))
            self.order_submit2.set_default_child_dma(orders_id[0])
            self.order_submit2.update_fields_in_component(
                "NewOrderSingleBlock", {"OrdQty": "50", "Price": "2"}
            )
            self.order_submit3.set_default_child_dma(orders_id[1])
            self.order_submit3.update_fields_in_component(
                "NewOrderSingleBlock", {"OrdQty": "50", "Price": "2"}
            )
            self.java_api_manager.send_message_and_receive_response(self.order_submit2)
            child_orders_id.append(
                self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
                    JavaApiFields.OrdReplyBlock.value][JavaApiFields.OrdID.value])
            self.java_api_manager.send_message_and_receive_response(self.order_submit3)
            child_orders_id.append(
                self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
                    JavaApiFields.OrdReplyBlock.value][JavaApiFields.OrdID.value])

        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            self.rule_manager.remove_rule(nos_rule)
        # endregion

        # region 2 - Cancel Child Orders
        try:
            cancel_rule = self.rule_manager.add_OrderCancelRequest_FIXStandard(self.bs_connectivity,
                                                                           self.venue_client_name,
                                                                           self.mic, True)

            self.cancel_order.set_default(child_orders_id[0])
            self.java_api_manager.send_message_and_receive_response(self.cancel_order)
            ord_notify = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
                JavaApiFields.OrdReplyBlock.value]
            expected_result = {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_CXL.value}
            self.java_api_manager.compare_values(expected_result, ord_notify, "Check TransStatus")
            self.cancel_order.set_default(child_orders_id[1])
            self.java_api_manager.send_message_and_receive_response(self.cancel_order)
            ord_notify = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
                JavaApiFields.OrdReplyBlock.value]
            self.java_api_manager.compare_values(expected_result, ord_notify, "Check TransStatus 2")
        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            self.rule_manager.remove_rule(cancel_rule)
        # endregion

        # region Step 3 and 4 - Create Bag Order
        self.bag_creation_request.set_default(BagChildCreationPolicy.AVP.value, name_of_bag, orders_id)
        self.java_api_manager.send_message_and_receive_response(self.bag_creation_request)
        order_bag_notification = \
            self.java_api_manager.get_last_message(ORSMessageType.OrderBagNotification.value).get_parameters()[
                JavaApiFields.OrderBagNotificationBlock.value]
        bag_order_id = order_bag_notification[JavaApiFields.OrderBagID.value]
        expected_result = {JavaApiFields.OrderBagName.value: name_of_bag,
                           JavaApiFields.OrderBagStatus.value: OrderBagConst.OrderBagStatus_NEW.value}
        self.java_api_manager.compare_values(expected_result, order_bag_notification,
                                             'Checking expected and actually results (step 4)')

        # endregion