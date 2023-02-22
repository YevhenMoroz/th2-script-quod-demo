import logging
import os
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, BasketMessagesConst, OrderBagConst
from test_framework.java_api_wrappers.oms.ors_messges.NewOrderListOMS import NewOrderListOMS
from rule_management import RuleManager, Simulators
from test_framework.java_api_wrappers.ors_messages.OrderListWaveCreationRequest import OrderListWaveCreationRequest
from test_framework.java_api_wrappers.ors_messages.RemoveOrdersFromOrderListRequest import \
    RemoveOrdersFromOrderListRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7404(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.list_creation_request = NewOrderListOMS(self.data_set)
        self.wave_create_request = OrderListWaveCreationRequest()
        self.remove_order_from_list_request = RemoveOrdersFromOrderListRequest()
        self.rule_manager = RuleManager(Simulators.equity)
        self.client_for_rule = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        self.mic = self.data_set.get_mic_by_name('mic_1')
        self.price = '10'
        self.qty = '100'

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Send NewOrderSingle
        self.list_creation_request.set_default_order_list()
        self.java_api_manager.send_message_and_receive_response(self.list_creation_request)
        list_notify_block = self.java_api_manager.get_last_message(
            ORSMessageType.OrdListNotification.value).get_parameter('OrdListNotificationBlock')
        self.java_api_manager.compare_values(
            {JavaApiFields.ListOrderStatus.value: BasketMessagesConst.ListOrderStatus_EXE.value}, list_notify_block,
            'Check created basket')
        list_id = list_notify_block['OrderListID']
        ord_id1 = list_notify_block['OrdNotificationElements']['OrdNotificationBlock'][0]['OrdID']
        ord_id2 = list_notify_block['OrdNotificationElements']['OrdNotificationBlock'][1]['OrdID']
        # endregion

        # region wave basket
        new_order_single_rule = None
        try:
            new_order_single_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side,
                self.client_for_rule, self.mic,
                float(self.price))

            self.wave_create_request.set_default(list_id, [ord_id1, ord_id2])
            self.java_api_manager.send_message_and_receive_response(self.wave_create_request)
        except Exception as e:
            logger.error(f'{e}')
        finally:
            time.sleep(5)
            self.rule_manager.remove_rule(new_order_single_rule)

        ord_list_wave_notif = \
            self.java_api_manager.get_last_message(
                ORSMessageType.OrderListWaveNotification.value).get_parameters()[
                JavaApiFields.OrderListWaveNotificationBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.OrderListWaveStatus.value: OrderBagConst.OrderBagStatus_NEW.value}, ord_list_wave_notif,
            'Check created Wave')
        chid_ord_id = \
        ord_list_wave_notif[JavaApiFields.OrderNotificationElements.value][JavaApiFields.OrdNotificationBlock.value][0][
            JavaApiFields.OrdID.value]
        # endregion

        # region remove order from basket
        self.remove_order_from_list_request.set_default(ord_id1, list_id)
        self.java_api_manager.send_message_and_receive_response(self.remove_order_from_list_request)
        remove_ords_from_list_reply = \
            self.java_api_manager.get_last_message(
                ORSMessageType.RemoveOrdersFromOrderListReply.value).get_parameters()[
                JavaApiFields.RemoveOrdersFromOrderListReplyBlock.value]
        self.java_api_manager.compare_values(
            {
                'FreeNotes': f'Runtime error (parent order {ord_id1} has child {chid_ord_id} in a terminal state)'},
            remove_ords_from_list_reply, 'Check error in RemoveOrdersFromOrderListReply')
        # endregion
