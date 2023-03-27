import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import SubmitRequestConst, JavaApiFields
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.oms.RestApiWashBookRuleMessages import RestApiWashBookRuleMessages

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7419(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ja_manager = JavaApiManager(environment.get_list_java_api_environment()[0].java_api_conn, self.test_id)
        self.client = self.data_set.get_client_by_name("client_pos_1")
        self.washbook_acc = self.data_set.get_washbook_account_by_name('washbook_account_5')
        self.recipient = self.data_set.get_recipient_by_name("recipient_user_1")
        self.order_submit = OrderSubmitOMS(data_set).set_default_care_limit(
            self.environment.get_list_fe_environment()[0].user_1, "1", SubmitRequestConst.USER_ROLE_1.value)
        self.rest_api_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_api_manager = RestApiManager(session_alias=self.rest_api_connectivity, case_id=self.test_id)
        self.mod_washbook = RestApiWashBookRuleMessages(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Precondition
        self.mod_washbook.modify_wash_book_rule(client=self.client, desk="1", exec_policy="C", instr_type="EQU")
        self.rest_api_manager.send_post_request(self.mod_washbook)
        time.sleep(3)
        # endregion
        # region Create CO order
        self.order_submit.update_fields_in_component("NewOrderSingleBlock", {"AccountGroupID": self.client})
        self.ja_manager.send_message_and_receive_response(self.order_submit)
        ord_rep = self.ja_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.ja_manager.compare_values({"WashBookAccountID": self.washbook_acc}, ord_rep, "Check WashBookAccountID")
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.mod_washbook.delete_wash_book_rule()
        self.rest_api_manager.send_post_request(self.mod_washbook)
