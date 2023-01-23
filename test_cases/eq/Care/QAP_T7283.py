import logging
import os
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import SubmitRequestConst, JavaApiFields, OrderReplyConst
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.SuspendOrderManagementRequest import SuspendOrderManagementRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7283(TestCase):
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.environment.get_list_fix_environment(), self.test_id)
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.mic = self.data_set.get_mic_by_name('mic_1')
        self.qty = '100'
        self.price = '20'
        self.client = self.data_set.get_client_by_name('client_1')
        self.client_for_rule = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        self.rule_manager = RuleManager(Simulators.equity)
        self.suspend_order = SuspendOrderManagementRequest()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region precondition : create CO order
        self.order_submit.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                 desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                 role=SubmitRequestConst.USER_ROLE_1.value)
        self.order_submit.update_fields_in_component('NewOrderSingleBlock', {
            'AccountGroupID': self.client,
            'OrdQty': self.qty,
            'Price': self.price,
        })
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        order_id = order_reply[JavaApiFields.OrdID.value]
        # endregion

        # region step 1: create Child DMA order
        nos_rule = None
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.fix_env.buy_side,
                                                                                                  self.client_for_rule,
                                                                                                  self.mic,
                                                                                                  int(self.price))
            self.order_submit.set_default_child_dma(order_id, order_id)
            self.order_submit.update_fields_in_component('NewOrderSingleBlock', {'AccountGroupID': self.client,
                                                                                 "Price": self.price,
                                                                                 'OrdQty': self.qty,
                                                                                 'ExecutionPolicy': 'DMA'})
            self.java_api_manager.send_message_and_receive_response(self.order_submit)
            order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
                JavaApiFields.OrdReplyBlock.value]
            self.java_api_manager.compare_values(
                {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                order_reply, 'Checking expected and actually result (step 1)')
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(nos_rule)
        # endregion

        # region step 2, step 3: Suspend CO order with Cancel Child
        cancel_rule = None
        try:
            cancel_rule = self.rule_manager.add_OrderCancelRequest_FIXStandard(self.fix_env.buy_side,
                                                                               self.client_for_rule,
                                                                               self.mic,
                                                                               True)
            self.suspend_order.set_default(order_id, 'Y', 'Y')
            self.java_api_manager.send_message_and_receive_response(self.suspend_order)
            child_order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
                JavaApiFields.OrdReplyBlock.value]
            self.java_api_manager.compare_values(
                {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_CXL.value},
                child_order_reply, 'Checking that child order canceled (step 3)')
            suspend_reply = \
            self.java_api_manager.get_last_message(ORSMessageType.SuspendOrderManagementReply.value).get_parameters()[
                JavaApiFields.SuspendOrderManagementReplyBlock.value]
            self.java_api_manager.compare_values({JavaApiFields.SuspendedCare.value: 'Y',
                                                  JavaApiFields.OrdID.value: order_id},
                                                 suspend_reply,
                                                 f'Checking that parent order has {JavaApiFields.SuspendedCare.value} = "Y" (step 3)')
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(cancel_rule)

        # endregion
