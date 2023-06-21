import logging
import time
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, SubmitRequestConst
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.oms.RestApiModifyGatingRuleMessage import RestApiModifyGatingRuleMessage

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


def print_message(message, responses):
    logger.info(message)
    for i in responses:
        logger.info(i)
        logger.info(i.get_parameters())


class QAP_T9272(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.rest_api_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_api_manager = RestApiManager(session_alias=self.rest_api_connectivity, case_id=self.test_id)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.order_submit = OrderSubmitOMS(data_set)
        self.modify_rule_message = RestApiModifyGatingRuleMessage(self.data_set).set_default_param()
        self.client = self.data_set.get_client_by_name("client_1")  # CLIENT1
        self.qty = "100"
        self.price = "20"
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.venue_client_names = self.data_set.get_venue_client_names_by_name("client_1_venue_1")  # XPAR_CLIENT1
        self.exec_destination = self.data_set.get_mic_by_name("mic_1")  # XPAR
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Enabling GatingRule
        param = self.modify_rule_message.get_parameter("gatingRuleCondition")
        param[0]["gatingRuleCondExp"] = "AND(Origin=FIX,AccountGroupID=CLIENT1)"
        param[0]["gatingRuleResult"][0]["gatingRuleResultAction"] = "DMA"
        self.modify_rule_message.update_parameters({"gatingRuleCondition": param})
        self.rest_api_manager.send_post_request(self.modify_rule_message)
        # endregion

        # region Step 1 - Create Care order via FIX
        nos_rule = None
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.bs_connectivity, self.venue_client_names, self.exec_destination, float(self.price)
            )
            self.fix_message.set_default_care_limit()
            self.fix_message.change_parameters({"OrderQtyData": {"OrderQty": self.qty}, "Account": self.client})
            response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
            gating_rule_name = response[0].get_parameters()["GatingRuleName"]
            gating_rule_cond_name = response[0].get_parameters()["GatingRuleCondName"]
            exec_policy = response[0].get_parameters()["HandlInst"]
        except Exception as e:
            logger.info(f"Your Exception is {e}")
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(nos_rule)
        # endregion

        # region Step 1 - Check that the Gating rule is applied to the FIX Care order
        self.java_api_manager.compare_values(
            {
                JavaApiFields.GatingRuleCondName.value: "All Orders",
                JavaApiFields.GatingRuleID.value: "Main Rule",
                JavaApiFields.ExecutionPolicy.value: "1",
            },
            {
                JavaApiFields.GatingRuleCondName.value: gating_rule_cond_name,
                JavaApiFields.GatingRuleID.value: gating_rule_name,
                JavaApiFields.ExecutionPolicy.value: exec_policy,
            },
            "Step 1 - Check the GatingRule is applied to the FIX CO, ExecPcy = DMA",
        )
        # endregion

        # region Step 2 - Create Care order
        self.order_submit.set_default_care_limit(
            recipient=self.environment.get_list_fe_environment()[0].user_1,
            desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
            role=SubmitRequestConst.USER_ROLE_1.value,
        )
        self.order_submit.update_fields_in_component(
            "NewOrderSingleBlock", {"OrdQty": "100", "AccountGroupID": self.client}
        )
        responses = self.java_api_manager.send_message_and_receive_response(self.order_submit)
        print_message("CREATE", responses)
        # endregion

        # region Step 2 - Check that the Gating rule is not applied to the order
        order_notification = self.java_api_manager.get_last_message(
            ORSMessageType.OrdNotification.value,
        ).get_parameters()[JavaApiFields.OrderNotificationBlock.value]

        self.java_api_manager.compare_values(
            {
                JavaApiFields.GatingRuleCondName.value: "Default Result",
                JavaApiFields.GatingRuleID.value: self.data_set.get_venue_gating_rule_id_by_name("main_rule_id"),
                JavaApiFields.ExecutionPolicy.value: "C",
            },
            order_notification,
            "Step 2 - Check that the Gating rule is not applied to the order, ExecPcy = Care",
        )
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_api_manager.send_post_request(self.modify_rule_message.set_default_param())
