import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType, CSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.cs_message.ManualMatchExecsToParentOrderRequest import \
    ManualMatchExecsToParentOrderRequest
from test_framework.java_api_wrappers.java_api_constants import SubmitRequestConst, OrderReplyConst, JavaApiFields
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, ExecSts

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7432(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.client = self.data_set.get_client_by_name("client_1")
        self.mic = self.data_set.get_mic_by_name('mic_1')

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1: create CO orders
        orders_ids = []
        desk_id = self.environment.get_list_fe_environment()[0].desk_ids[0]
        for counter in range(3):
            self.order_submit.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                     desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                     role=SubmitRequestConst.USER_ROLE_1.value)
            self.order_submit.update_fields_in_component('NewOrderSingleBlock', {"ClOrdID": bca.client_orderid(9)})
            self.java_api_manager.send_message_and_receive_response(self.order_submit)
            order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
                JavaApiFields.OrdReplyBlock.value]
            orders_ids.append(order_reply[JavaApiFields.OrdID.value])
            self.java_api_manager.compare_values(
                {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                order_reply, 'Verifying that CO order created (step 1)')

        # endregion

        # region step 2-4: Create Child CO orders via Direct Child Care
        for order_id in orders_ids:
            self.order_submit.set_default_direct_child_care(order_id, desk=desk_id)
            self.java_api_manager.send_message_and_receive_response(self.order_submit)
            ord_update = self.java_api_manager.get_last_message(ORSMessageType.OrdUpdate.value).get_parameters()[
                JavaApiFields.OrdUpdateBlock.value]
            self.java_api_manager.compare_values(
                {JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value}, ord_update,
                f'Check that parent order: {order_id} is open (step 4)')
            cd_ord_notif = self.java_api_manager.get_last_message(CSMessageType.CDOrdNotif.value).get_parameters()[JavaApiFields.CDOrdNotifBlock.value]
            self.java_api_manager.compare_values({JavaApiFields.TransStatus.value:OrderReplyConst.TransStatus_SEN.value}, cd_ord_notif[JavaApiFields.OrdNotificationBlock.value],
                                                 f'Check that child order of {order_id} has Send status (step 4)')

        # endregion
