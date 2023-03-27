import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.oms.RestApiDisableGatingRuleMessage import RestApiDisableGatingRuleMessage
from test_framework.rest_api_wrappers.oms.RestApiModifyGatingRuleMessage import RestApiModifyGatingRuleMessage

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T4931(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.rest_api_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_api_manager = RestApiManager(session_alias=self.rest_api_connectivity, case_id=self.test_id)
        self.ja_manager = JavaApiManager(environment.get_list_java_api_environment()[0].java_api_conn, self.test_id)
        self.order_submit = OrderSubmitOMS(data_set).set_default_dma_limit()
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.rule_manager = RuleManager(Simulators.equity)
        self.client_venue = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        self.exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.modify_rule_message = RestApiModifyGatingRuleMessage(self.data_set).set_default_param()
        self.disable_rule_message = RestApiDisableGatingRuleMessage(self.data_set).set_default_param()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        qty = str(float('200'))
        price = str(float('10'))
        self.order_submit.update_fields_in_component("NewOrderSingleBlock", {"OrdQty": qty,
                                                                             'Price': price})
        param = self.modify_rule_message.get_parameter("gatingRuleCondition")
        set_value_params: dict = {"alive": 'true',
                                  "gatingRuleResultIndice": 1,
                                  "splitRatio": 0,
                                  "holdOrder": 'true',
                                  "gatingRuleResultProperty": "APP",
                                  "gatingRuleResultAction": "VAL",
                                  "gatingRuleResultRejectType": "HRD"}
        param[0]["gatingRuleResult"].insert(0, set_value_params)  # Set Action=SetValue above
        param[0]["gatingRuleResult"][1]["gatingRuleResultIndice"] = 2
        param[0]["gatingRuleResult"][1]["gatingRuleResultAction"] = "DMA"
        param[0]["gatingRuleCondExp"] = "AND(ExecutionPolicy=DMA,OrdQty<1000)"
        self.modify_rule_message.update_parameters({"gatingRuleCondition": param})
        self.rest_api_manager.send_post_request(self.modify_rule_message)
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side, self.client_venue, self.exec_destination, float(price))
            self.ja_manager.send_message_and_receive_response(self.order_submit)
        except Exception as e:
            logger.info(f'Your Exception is {e}')
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(nos_rule)

        act_res = self.ja_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameters()[
            JavaApiFields.OrderNotificationBlock.value]
        self.ja_manager.compare_values(
            {JavaApiFields.GatingRuleCondName.value: "All Orders", JavaApiFields.OrdStatus.value: "HLD",
             JavaApiFields.GatingRuleID.value: self.data_set.get_venue_gating_rule_id_by_name('main_rule_id'),
             JavaApiFields.OrdQty.value: qty, JavaApiFields.Price.value: price}, act_res,
            "check GatingRuleCondName")
        act_res_2 = self.ja_manager.get_last_message(ORSMessageType.OrderSubmitReply.value).get_parameters()[
            JavaApiFields.NewOrderReplyBlock.value][JavaApiFields.Ord.value]
        self.ja_manager.compare_values({JavaApiFields.FreeNotes.value: 'order held as per gating rule instruction'},
                                       act_res_2, 'Verifying FreeNotes has correct value')

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_api_manager.send_post_request(self.modify_rule_message.set_default_param())
