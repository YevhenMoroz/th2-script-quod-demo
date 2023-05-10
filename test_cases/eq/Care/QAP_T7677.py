import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import Simulators, RuleManager
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import CSMessageType, ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.cs_message.CDOrdAckBatchRequest import CDOrdAckBatchRequest
from test_framework.java_api_wrappers.java_api_constants import SubmitRequestConst, JavaApiFields, OrderReplyConst, \
    ExecutionPolicyConst
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7677(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.qty_to_split = "50"
        self.qty_to_display = "30"
        self.exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.rule_manager = RuleManager(Simulators.equity)
        self.client_for_rule = self.data_set.get_venue_client_names_by_name('client_2_venue_1')
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_connectivity2 = self.environment.get_list_java_api_environment()[0].java_api_conn_user2
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.java_api_manager2 = JavaApiManager(self.java_api_connectivity2, self.test_id)
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.client = self.data_set.get_client_by_name("client_2")
        self.accept_request = CDOrdAckBatchRequest()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1-6: Create CO order
        user_2 = self.environment.get_list_fe_environment()[0].user_1
        role = SubmitRequestConst.USER_ROLE_1.value
        desk = self.environment.get_list_fe_environment()[0].desk_ids[0]
        self.order_submit.set_default_care_limit(recipient=user_2,
                                                 desk=desk,
                                                 role=role)
        price = self.order_submit.get_parameter(JavaApiFields.NewOrderSingleBlock.value)[JavaApiFields.Price.value]
        self.java_api_manager2.send_message_and_receive_response(self.order_submit)
        cd_order_notif_message = self.java_api_manager2.get_last_message(CSMessageType.CDOrdNotif.value)
        order_id = self.java_api_manager2.get_last_message(ORSMessageType.OrdNotification.value).get_parameters()[
            JavaApiFields.OrderNotificationBlock.value][JavaApiFields.OrdID.value]
        cd_order_notif_id = cd_order_notif_message.get_parameter("CDOrdNotifBlock")["CDOrdNotifID"]
        order_notification = \
            self.java_api_manager2.get_last_message(ORSMessageType.OrdNotification.value).get_parameters()[
                JavaApiFields.OrderNotificationBlock.value]
        self.java_api_manager2.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_SEN.value},
                                              order_notification,
                                              'Verifying that CO order has Status = Sent (step 6)')
        # endregion

        # region step 7-9: Accept CO order
        self.accept_request.set_default(order_id, cd_order_notif_id, desk, set_reject=False)
        self.java_api_manager.send_message_and_receive_response(self.accept_request)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                                             order_reply, 'Checking expected and actually result for (step 9)')
        # endregion

        # region step 10-11: Split CO order on half qty (DMA order)
        nos_rule = None
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side,
                self.client_for_rule,
                self.exec_destination,
                float(price))
            self.order_submit.set_default_child_dma(order_id)
            self.order_submit.update_fields_in_component('NewOrderSingleBlock', {'OrdQty': self.qty_to_split,
                                                                                 'ExecutionPolicy': ExecutionPolicyConst.DMA.value,
                                                                                 'AccountGroupID': self.client})
            self.java_api_manager.send_message_and_receive_response(self.order_submit)
            order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
                JavaApiFields.OrdReplyBlock.value]
            self.java_api_manager.compare_values(
                {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value,
                 JavaApiFields.ExecutionPolicy.value: ExecutionPolicyConst.DMA.value}, order_reply,
                'Verifying that Child DMA order created (step 10)')
        finally:
            time.sleep(3)
            self.rule_manager.remove_rule(nos_rule)
        # endregion

        # region step 12-13:Split CO order on half qty (Algo Order)
        self.order_submit.set_default_direct_algo_iceberg(order_id, self.qty_to_display)
        self.order_submit.update_fields_in_component('NewOrderSingleBlock',
                                                     {'OrdQty': self.qty_to_split})
        self.order_submit.remove_parameter('CDOrdAssignInstructionsBlock')
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameters()[
            JavaApiFields.OrderNotificationBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.ExecutionPolicy.value: ExecutionPolicyConst.Synthetic.value},
                                             order_reply, 'Verifying that Child DMA order created (step 12)')
        # endregion
