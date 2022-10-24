import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import OrderReplyConst, SubmitRequestConst
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
seconds, nanos = timestamps()


class QAP_T7685(TestCase):
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
        response = self.java_api_manager.send_message_and_receive_response(self.ord_sub_message)
        self.return_result(response, ORSMessageType.OrdReply.value)
        order_id = self.result.get_parameter('OrdReplyBlock')['OrdID']
        status = self.result.get_parameter('OrdReplyBlock')['TransStatus']
        self.java_api_manager.compare_values(
            {OrderBookColumns.sts.value: OrderReplyConst.TransStatus_OPN.value},
            {OrderBookColumns.sts.value: status},
            f'Comparing {OrderBookColumns.sts.value}')

    def return_result(self, responses, message_type):
        for response in responses:
            if response.get_message_type() == message_type:
                self.result = response

