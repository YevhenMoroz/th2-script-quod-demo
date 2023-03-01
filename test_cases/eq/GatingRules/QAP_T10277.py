import logging
import os
import time
import xml.etree.ElementTree as ET
from pathlib import Path

from pkg_resources import resource_filename

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.oms.RestApiModifyGatingRuleMessage import RestApiModifyGatingRuleMessage
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T10277(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.rest_api_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_api_manager = RestApiManager(session_alias=self.rest_api_connectivity, case_id=self.test_id)
        self.ja_manager = JavaApiManager(environment.get_list_java_api_environment()[0].java_api_conn_user2,
                                         self.test_id)
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.modify_rule_message = RestApiModifyGatingRuleMessage(self.data_set)
        self.client_venue = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        self.exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.rule_manager = RuleManager(Simulators.equity)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1: Send Algo order
        price = '10'
        qty = '10000'
        self.order_submit.set_default_dma_limit()
        external_algo_parameters_block = {"ExternalAlgoParameterBlock": [
                                                                  {
                                                                      'AlgoParameterName': "StrategyTag",
                                                                      "AlgoParamString": "TWAP",
                                                                      'VenueScenarioParameterID': "7505"}]}
        self.order_submit.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value,
                                                     {JavaApiFields.Price.value: price,
                                                      JavaApiFields.OrdQty.value: qty,
                                                      'RouteList': {'RouteBlock': [{
                                                          'RouteID': self.data_set.get_route_id_by_name('route_1')
                                                      }]},
                                                      "AlgoParametersBlock": {"AlgoType": "External",
                                                                              "ScenarioID": "101",
                                                                              "AlgoPolicyID": "1000131"},
                                                      "ExternalAlgoParametersBlock": {
                                                          "ExternalAlgoParameterListBlock":external_algo_parameters_block,
                                                          'ScenarioID': "101",
                                                          "ScenarioIdentifier": "8031",
                                                          "VenueScenarioID": "TWAP",
                                                          "VenueScenarioVersionID": "9682",
                                                          "VenueScenarioVersionValue": "ATDLEQ5.3.1"},
                                                      })
        self.modify_rule_message.set_default_param()
        param = self.modify_rule_message.get_parameter("gatingRuleCondition")
        param[0]["gatingRuleCondExp"] = "OrdQty=10000"
        param[0]["gatingRuleResult"][0]["gatingRuleResultAction"] = "DMA"
        param[0]["gatingRuleResult"][0]["routeID"] = self.data_set.get_route_id_by_name('route_1')
        self.modify_rule_message.update_parameters({"gatingRuleCondition": param})
        self.rest_api_manager.send_post_request(self.modify_rule_message)
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side, self.client_venue, self.exec_destination, float(price))
            self.ja_manager.send_message_and_receive_response(self.order_submit)
            order_reply = self.ja_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
                JavaApiFields.OrdReplyBlock.value]
            self.ja_manager.compare_values(external_algo_parameters_block,
                                           order_reply[JavaApiFields.ExternalAlgoParametersBlock.value][JavaApiFields.ExternalAlgoParameterListBlock.value],
                                           f'Check that {JavaApiFields.ExternalAlgoParameterListBlock.value} presents')
        except Exception as e:
            logger.info(f'Your Exception is {e}')
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(nos_rule)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_api_manager.send_post_request(self.modify_rule_message.set_default_param())
