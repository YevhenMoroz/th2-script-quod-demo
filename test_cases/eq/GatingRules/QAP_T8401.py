import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.oms.RestApiDisableGatingRuleMessage import RestApiDisableGatingRuleMessage
from test_framework.rest_api_wrappers.oms.RestApiModifyGatingRuleMessage import RestApiModifyGatingRuleMessage
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst, SubmitRequestConst, \
    ExecutionPolicyConst

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T8401(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.file_name = Path(__file__).name[:-3]
        self.test_id = bca.create_event(self.file_name, self.report_id)
        self.rest_api_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_api_manager = RestApiManager(session_alias=self.rest_api_connectivity, case_id=self.test_id)
        self.ja_manager = JavaApiManager(environment.get_list_java_api_environment()[0].java_api_conn, self.test_id)
        self.order_submit = OrderSubmitOMS(data_set).set_default_dma_limit()
        self.disable_rule_message = RestApiDisableGatingRuleMessage(self.data_set).set_default_param()
        self.buy_side = self.environment.get_list_fix_environment()[0].buy_side
        self.rule_manager = RuleManager(Simulators.equity)
        self.client_venue_paris = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        self.exec_destination_paris = self.data_set.get_mic_by_name('mic_1')
        self.modify_rule_message = RestApiModifyGatingRuleMessage(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        try:
            client = self.order_submit.get_parameters()[JavaApiFields.NewOrderSingleBlock.value][
                JavaApiFields.AccountGroupID.value]
            price = self.order_submit.get_parameter("NewOrderSingleBlock")['Price']
            nos_rule_paris = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.buy_side, self.client_venue_paris, self.exec_destination_paris, float(price))
            self.order_submit.update_fields_in_component("NewOrderSingleBlock", {"OrdQty": "200"})
            self.modify_rule_message.set_default_param()
            param = self.modify_rule_message.get_parameter("gatingRuleCondition")
            param[0]["gatingRuleCondExp"] = f"AND(AccountGroupID={client},Side=Buy)"
            set_value_params: dict = {"alive": 'true',
                                      "gatingRuleResultIndice": 1,
                                      "splitRatio": 1,
                                      "holdOrder": 'false',
                                      "gatingRuleResultAction": "REJ",
                                      "gatingRuleResultRejectType": "HRD"}
            param[0]["gatingRuleResult"][0] = set_value_params
            self.modify_rule_message.update_parameters({"gatingRuleCondition": param})
            self.rest_api_manager.send_post_request(self.modify_rule_message)
            self.send_submit_message_and_check_result(self.order_submit, ExecutionPolicyConst.DMA.value)
            self.order_submit.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                     desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                     role=SubmitRequestConst.USER_ROLE_1.value)
            self.order_submit.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value, {
                JavaApiFields.ClOrdID.value: f"CARE{self.file_name}" + bca.client_orderid(9)
            })
            self.send_submit_message_and_check_result(self.order_submit, ExecutionPolicyConst.CARE.value)
        except Exception as e:
            logger.error(f"Exception is {e}")
        finally:
            time.sleep(3)
            self.rule_manager.remove_rule(nos_rule_paris)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_api_manager.send_post_request(self.modify_rule_message.set_default_param())

    def send_submit_message_and_check_result(self, order_submit, exec_policy, ):
        self.ja_manager.send_message_and_receive_response(order_submit)
        act_res_rule = self.ja_manager.get_last_message(ORSMessageType.OrderSubmitReply.value).get_parameters()[
            JavaApiFields.NewOrderReplyBlock.value][JavaApiFields.Ord.value]
        self.ja_manager.compare_values({JavaApiFields.GatingRuleCondName.value: "All Orders",
                                        JavaApiFields.OrdStatus.value: OrderReplyConst.OrdStatus_REJ.value,
                                        JavaApiFields.GatingRuleID.value: self.data_set.get_venue_gating_rule_id_by_name(
                                            'main_rule_id'),
                                        JavaApiFields.ExecutionPolicy.value: exec_policy},
                                       act_res_rule,
                                       f"check GatingRuleCondName for {exec_policy} order")
