import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.oms.RestApiModifyGatingRuleMessage import RestApiModifyGatingRuleMessage

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T4295(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.rest_api_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_api_manager = RestApiManager(session_alias=self.rest_api_connectivity, case_id=self.test_id)
        self.ja_manager = JavaApiManager(environment.get_list_java_api_environment()[0].java_api_conn, self.test_id)
        self.order_submit = OrderSubmitOMS(data_set).set_default_dma_limit()
        self.modify_rule_message = RestApiModifyGatingRuleMessage(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        self.modify_rule_message.set_default_param()
        param = self.modify_rule_message.get_parameter("gatingRuleCondition")
        param[0]["gatingRuleResult"][0]["routeID"] = "1"
        param[0]['gatingRuleCondExp'] = "AND(ExecutionPolicy=DMA,OrdQty<1000)"
        param[0]['gatingRuleResult'][0]['gatingRuleResultAction'] = 'DMA'
        self.modify_rule_message.update_parameters({"gatingRuleCondition": param})
        self.rest_api_manager.send_post_request(self.modify_rule_message)
        self.ja_manager.send_message_and_receive_response(self.order_submit)
        act_res = self.ja_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        act_res_2 = self.ja_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameters()[JavaApiFields.OrderNotificationBlock.value]
        self.ja_manager.compare_values({JavaApiFields.GatingRuleCondName.value: "All Orders", JavaApiFields.RouteID.value: "1",
                                        JavaApiFields.VenueID.value: self.data_set.get_venue_id("paris")}, act_res,
                                       "check GatingRuleCondName , Route and Venue")
        self.ja_manager.compare_values({JavaApiFields.GatingRuleID.value: self.data_set.get_venue_gating_rule_id_by_name('main_rule_id')},
                                       act_res_2, 'Check that GatingRule has correct ID')

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_api_manager.send_post_request(self.modify_rule_message.set_default_param())
