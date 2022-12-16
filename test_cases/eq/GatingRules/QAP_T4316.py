import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.OrderModificationRequest import OrderModificationRequest
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.oms.RestApiDisableGatingRuleMessage import RestApiDisableGatingRuleMessage
from test_framework.rest_api_wrappers.oms.RestApiModifyGatingRuleMessage import RestApiModifyGatingRuleMessage

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T4316(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.rest_api_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_api_manager = RestApiManager(session_alias=self.rest_api_connectivity, case_id=self.test_id)
        self.ja_manager = JavaApiManager(environment.get_list_java_api_environment()[0].java_api_conn, self.test_id)
        self.order_submit = OrderSubmitOMS(data_set).set_default_dma_limit()
        self.disable_rule_message = RestApiDisableGatingRuleMessage(self.data_set).set_default_param()
        self.modify_request = OrderModificationRequest()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        modify_rule_message = RestApiModifyGatingRuleMessage(self.data_set)
        modify_rule_message.set_default_param()
        param = modify_rule_message.get_parameter("gatingRuleCondition")
        set_value_params: dict = {"alive": 'true',
                                  "gatingRuleResultIndice": 1,
                                  "splitRatio": 0,
                                  "holdOrder": 'true',
                                  "gatingRuleResultProperty": "APP",
                                  "gatingRuleResultAction": "VAL",
                                  "gatingRuleResultRejectType": "HRD"}
        param[0]["gatingRuleResult"].insert(0, set_value_params)  # Set Action=SetValue above
        param[0]["gatingRuleResult"][1]["gatingRuleResultIndice"] = 2
        modify_rule_message.update_parameters({"gatingRuleCondition": param})
        self.rest_api_manager.send_post_request(modify_rule_message)
        self.ja_manager.send_message_and_receive_response(self.order_submit)
        act_res = self.ja_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameters()[
            "OrdNotificationBlock"]
        self.ja_manager.compare_values({"GatingRuleCondName": "Cond1", "OrdStatus": "HLD"}, act_res,
                                       "check GatingRuleCondName")
        param[0]["gatingRuleResult"][1]["gatingRuleResultIndice"] = 1
        del param[0]["gatingRuleResult"][0]  # Delete set_value_params
        print(param[0]["gatingRuleResult"])
        modify_rule_message.update_parameters({"gatingRuleCondition": param})
        self.modify_request.set_default(self.data_set, act_res["OrdID"])
        self.rest_api_manager.send_post_request(modify_rule_message)
        self.ja_manager.send_message_and_receive_response(self.modify_request)
        act_res = self.ja_manager.get_last_message(ORSMessageType.OrderModificationReply.value).get_parameters()[
            "OrderModificationReplyBlock"]
        print(act_res)
        self.ja_manager.compare_values({"OrdStatus": "HLD"}, act_res["OrdModify"],
                                       "check OrdStatus")

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_api_manager.send_post_request(self.disable_rule_message)
