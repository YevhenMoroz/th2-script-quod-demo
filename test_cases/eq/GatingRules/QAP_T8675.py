import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager, ExtractAllMessages
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst, ExecutionPolicyConst
from test_framework.java_api_wrappers.oms.ors_messges.FixNewOrderSingleOMS import FixNewOrderSingleOMS
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.oms.RestApiModifyGatingRuleMessage import RestApiModifyGatingRuleMessage

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T8675(TestCase):
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.rest_api_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_api_manager = RestApiManager(session_alias=self.rest_api_connectivity, case_id=self.test_id)
        self.ja_manager = JavaApiManager(environment.get_list_java_api_environment()[0].java_api_conn_user2,
                                         self.test_id)
        self.new_order_single = FixNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.modify_rule_message = RestApiModifyGatingRuleMessage(self.data_set)
        self.client_venue = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        self.exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.rule_manager = RuleManager(Simulators.equity)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        price = '10'
        desk_id = self.environment.get_list_fe_environment()[0].desk_ids[1]
        self.new_order_single.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value,
                                                         {JavaApiFields.Price.value: price})
        venue_id = self.data_set.get_venue_by_name('venue_1')
        cl_ord_id = self.new_order_single.get_parameters()[JavaApiFields.NewOrderSingleBlock.value][
            JavaApiFields.ClOrdID.value]
        qty = self.new_order_single.get_parameters()[JavaApiFields.NewOrderSingleBlock.value][
            JavaApiFields.OrdQty.value]
        self.modify_rule_message.set_default_param()
        param = self.modify_rule_message.get_parameter("gatingRuleCondition")
        param[0]["gatingRuleCondExp"] = "AND(AccountIDIS NULL)"
        param[0]["gatingRuleResult"][0]["gatingRuleResultAction"] = "DMA"
        param[0]["gatingRuleResult"][0]["gatingRuleResultIndice"] = '1'
        param[0]["gatingRuleResult"][0]["splitRatio"] = '0.6'
        set_value_params: dict = {"alive": 'true',
                                  "gatingRuleResultIndice": 2,
                                  "splitRatio": '0.4',
                                  "holdOrder": 'false',
                                  "gatingRuleResultAction": "REJ",
                                  "gatingRuleResultRejectType": "SFT"}
        param[0]['gatingRuleResult'].insert(1, set_value_params)

        self.modify_rule_message.update_parameters({"gatingRuleCondition": param})
        self.rest_api_manager.send_post_request(self.modify_rule_message)
        list_of_ord_qty = ['60.0', '40.0']
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side, self.client_venue, self.exec_destination, float(price))
            self.ja_manager.send_message_and_receive_response(self.new_order_single, ExtractAllMessages.All.value)
            child_ord_reply_dma_open = \
                self.ja_manager.get_last_message_by_multiple_filter(ORSMessageType.OrdReply.value,
                                                                    [ExecutionPolicyConst.DMA.value,
                                                                     OrderReplyConst.TransStatus_OPN.value,
                                                                     list_of_ord_qty[0]]).get_parameters()[
                    JavaApiFields.OrdReplyBlock.value]
            self.ja_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value,
                                            JavaApiFields.OrdQty.value: list_of_ord_qty[0],
                                            JavaApiFields.ExecutionPolicy.value: ExecutionPolicyConst.DMA.value},
                                           child_ord_reply_dma_open,
                                           f'Verifying that first DMA order has properly values (step 2)')
            child_ord_notification_dma_hld = \
                self.ja_manager.get_last_message_by_multiple_filter(ORSMessageType.OrdNotification.value,
                                                                    [ExecutionPolicyConst.DMA.value,
                                                                     OrderReplyConst.OrdStatus_HLD.value,
                                                                     list_of_ord_qty[1]]).get_parameters()[
                    JavaApiFields.OrderNotificationBlock.value]
            self.ja_manager.compare_values({JavaApiFields.OrdStatus.value: OrderReplyConst.OrdStatus_HLD.value,
                                            JavaApiFields.OrdQty.value: list_of_ord_qty[1],
                                            JavaApiFields.ExecutionPolicy.value: ExecutionPolicyConst.DMA.value},
                                           child_ord_notification_dma_hld,
                                           f'Verifying that second DMA order has properly values (step 2)')

        except Exception as e:
            logger.info(f'Your Exception is {e}')
        finally:
            time.sleep(5)
            self.rule_manager.remove_rule(nos_rule)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_api_manager.send_post_request(self.modify_rule_message.set_default_param())
