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
class QAP_T8756(TestCase):
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
        half_qty = str(float(qty) / 2)
        self.modify_rule_message.set_default_param()
        param = self.modify_rule_message.get_parameter("gatingRuleCondition")
        param[0]["gatingRuleCondExp"] = "AND(AccountIDIS NULL)"
        param[0]["gatingRuleResult"][0]["gatingRuleResultAction"] = "CAR"
        param[0]["gatingRuleResult"][0]["gatingRuleResultIndice"] = '3'
        param[0]["gatingRuleResult"][0]["splitRatio"] = '0.5'
        value_result = {
            'alive': 'true',
            'deskID': desk_id,
            'gatingRuleResultAction': 'VAL',
            'gatingRuleResultIndice': '2',
            'gatingRuleResultProperty': 'DSK',
            'holdOrder': 'false',
            'splitRatio': '0',
        }
        dma_result = {
            'alive': 'true',
            'gatingRuleResultAction': 'DMA',
            'gatingRuleResultIndice': '1',
            'holdOrder': 'false',
            'splitRatio': '0.5',
            'venueID': venue_id
        }
        param[0]['gatingRuleResult'].insert(0, value_result)
        param[0]['gatingRuleResult'].insert(0, dma_result)
        self.modify_rule_message.update_parameters({"gatingRuleCondition": param})
        self.rest_api_manager.send_post_request(self.modify_rule_message)
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side, self.client_venue, self.exec_destination, float(price))
            self.ja_manager.send_message_and_receive_response(self.new_order_single, ExtractAllMessages.All.value)
            parent_order_reply = \
                self.ja_manager.get_last_message(ORSMessageType.OrdReply.value, cl_ord_id).get_parameters()[
                    JavaApiFields.OrdReplyBlock.value]
            self.ja_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value,
                                            JavaApiFields.GatingRuleCondName.value: 'All Orders',
                                            JavaApiFields.ClOrdID.value: cl_ord_id}, parent_order_reply,
                                           f'Verifying that Parent order with ClOrdID = {cl_ord_id} has correct values')
            child_order_reply_dma = self.ja_manager.get_last_message(ORSMessageType.OrdReply.value,
                                                                     ExecutionPolicyConst.DMA.value).get_parameters()[
                JavaApiFields.OrdReplyBlock.value]
            self.ja_manager.compare_values({JavaApiFields.ExecutionPolicy.value: ExecutionPolicyConst.DMA.value,
                                            JavaApiFields.OrdQty.value: half_qty}, child_order_reply_dma,
                                           'Verifying that child DMA order has correct values')
            child_order_notif_care = \
                self.ja_manager.get_last_message_by_multiple_filter(ORSMessageType.OrdNotification.value,
                                                                    [JavaApiFields.ParentOrdrList.value,
                                                                     ExecutionPolicyConst.CARE.value]).get_parameters()[
                    JavaApiFields.OrderNotificationBlock.value]
            self.ja_manager.compare_values(
                {JavaApiFields.OrdQty.value: half_qty, JavaApiFields.RecipientDeskID.value: str(desk_id)},
                child_order_notif_care, 'Verifying that child CO order has correct values')


        except Exception as e:
            logger.info(f'Your Exception is {e}')
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(nos_rule)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_api_manager.send_post_request(self.modify_rule_message.set_default_param())
