import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import SubmitRequestConst, OrderReplyConst
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
seconds, nanos = timestamps()


class QAP_T7622(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.ord_sub_message = OrderSubmitOMS(self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create order
        self.ord_sub_message.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                    desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                    role=SubmitRequestConst.USER_ROLE_1.value)
        self.ord_sub_message.update_fields_in_component('NewOrderSingleBlock', {"DiscloseExec": "R"})
        response = self.java_api_manager.send_message_and_receive_response(self.ord_sub_message)
        self.return_result(response, ORSMessageType.OrdNotification.value)
        disclose_exec = self.result.get_parameter('OrdNotificationBlock')['DiscloseExec']
        self.java_api_manager.compare_values(
            {OrderBookColumns.disclose_exec.value: OrderReplyConst.DiscloseExec_R.value},
            {OrderBookColumns.disclose_exec.value: disclose_exec},
            f'Check Order Disclose Execution')

    def return_result(self, responses, message_type):
        for response in responses:
            if response.get_message_type() == message_type:
                self.result = response

