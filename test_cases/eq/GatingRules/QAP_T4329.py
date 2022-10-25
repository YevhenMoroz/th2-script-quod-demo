import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca, basic_custom_actions
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.oms.RestApiDisableGatingRuleMessage import RestApiDisableGatingRuleMessage
from test_framework.rest_api_wrappers.oms.RestApiModifyGatingRuleMessage import RestApiModifyGatingRuleMessage
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T4329(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.rest_api_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_api_manager = RestApiManager(session_alias=self.rest_api_connectivity, case_id=self.test_id)
        self.ja_manager = JavaApiManager(environment.get_list_java_api_environment()[0].java_api_conn, self.test_id)
        self.order_submit = OrderSubmitOMS(data_set).set_default_dma_limit()
        self.disable_rule_message = RestApiDisableGatingRuleMessage(self.data_set).set_default_param()
        self.buy_side = self.environment.get_list_fix_environment()[0].buy_side
        self.rule_manager = RuleManager(Simulators.equity)
        self.client_venue_paris = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        self.client_venue_eurex = self.data_set.get_venue_client_names_by_name('client_1_venue_2')
        self.exec_destination_paris = self.data_set.get_mic_by_name('mic_1')
        self.exec_destination_eurex = self.data_set.get_mic_by_name('mic_2')
        self.class_name = QAP_T4329

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        try:
            price = self.order_submit.get_parameter("NewOrderSingleBlock")['Price']
            nos_rule_paris = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.buy_side, self.client_venue_paris, self.exec_destination_paris, float(price))
            nos_rule_eurex = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.buy_side, self.client_venue_eurex, self.exec_destination_eurex, float(price)
            )
            self.order_submit.update_fields_in_component("NewOrderSingleBlock", {"OrdQty": "200"})
            modify_rule_message = RestApiModifyGatingRuleMessage(self.data_set)
            modify_rule_message.set_default_param()
            param = modify_rule_message.get_parameter("gatingRuleCondition")
            param[0]["gatingRuleCondExp"] = "OR(VenueID IN(PARIS),VenueID NOT IN(PARIS))"
            param[0]["gatingRuleCondName"] = "Conflicting_rules"
            param[0]['holdOrder'] = 'true'
            modify_rule_message.update_parameters({"gatingRuleCondition": param})
            self.rest_api_manager.send_post_request(modify_rule_message)
            self.send_submit_message_and_check_result(self.order_submit)
            self.order_submit.update_fields_in_component('NewOrderSingleBlock', {
                'ListingList': {'ListingBlock': [{'ListingID': self.data_set.get_listing_id_by_name("listing_2")}]},
                'InstrID': self.data_set.get_instrument_id_by_name("instrument_3"),
                "ClOrdID": basic_custom_actions.client_orderid(9) + Path(__file__).name[:-3]})
            self.send_submit_message_and_check_result(self.order_submit)
        except Exception as e:
            logger.error(f"Exception is {e}")
        finally:
            time.sleep(3)
            self.rule_manager.remove_rule(nos_rule_paris)
            self.rule_manager.remove_rule(nos_rule_eurex)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_api_manager.send_post_request(self.disable_rule_message)

    @staticmethod
    def print_message(message, responses):
        logger.info(message)
        for i in responses:
            logger.info(i)
            logger.info(i.get_parameters())

    def send_submit_message_and_check_result(self, order_submit):
        responses = self.ja_manager.send_message_and_receive_response(order_submit)
        self.class_name.print_message('Message After Creation of order', responses)
        act_res_rule: dict = self.ja_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameters()[
            JavaApiFields.OrderNotificationBlock.value]
        self.ja_manager.compare_values({"GatingRuleCondName": "Conflicting_rules",
                                        JavaApiFields.OrdStatus.value: OrderReplyConst.OrdStatus_HLD.value},
                                       act_res_rule,
                                       "check GatingRuleCondName")
