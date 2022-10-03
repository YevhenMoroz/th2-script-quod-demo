import logging
from pathlib import Path

from custom import basic_custom_actions as bca, basic_custom_actions
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.ManualOrderCrossRequest import ManualOrderCrossRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class QAP_T6890(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.submit_request = OrderSubmitOMS(self.data_set)
        self.manual_cross = ManualOrderCrossRequest()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        order_submit = self.submit_request.set_default_care_limit(
            self.data_set.get_recipient_by_name("recipient_user_1"), "1")
        order_submit.update_fields_in_component("NewOrderSingleBlock", {'AccountGroupID':
            self.data_set.get_client_by_name(
                "client_pos_1")})
        response = self.java_api_manager.send_message_and_receive_response(order_submit)
        for res in response:
            if res.get_message_type() == ORSMessageType.OrdReply.value:
                self.java_api_manager.compare_values({"WashBookAccountID":
                                                          self.data_set.get_washbook_account_by_name(
                                                              "washbook_account_2")},
                                                     res.get_parameter("OrdReplyBlock"),
                                                     "compare WashBookAccountID in the OrdReply")
                break
