import logging
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
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


class QAP_T8827(TestCase):
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
        self.order_submit = OrderSubmitOMS(data_set).set_default_care_limit(
            recipient=self.environment.get_list_fe_environment()[0].user_1,
            desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
            role=SubmitRequestConst.USER_ROLE_1.value,
        )
        self.modify_rule_message = RestApiModifyGatingRuleMessage(self.data_set).set_default_param()
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Enabling GatingRule
        self.order_submit.update_fields_in_component("NewOrderSingleBlock", {"OrdQty": "100"})
        price = self.order_submit.get_parameter("NewOrderSingleBlock")["Price"]
        param = self.modify_rule_message.get_parameter("gatingRuleCondition")
        param[0]["gatingRuleCondExp"] = "Side=Buy"
        send_strategy_params: dict = {
            "algoPolicyID": "1000069",
            "gatingRuleResultAction": "ALG",
            "scenarioID": "39",
        }
        param[0]["gatingRuleResult"][0].update(send_strategy_params)
        self.modify_rule_message.update_parameters({"gatingRuleCondition": param})
        self.rest_api_manager.send_post_request(self.modify_rule_message)
        # endregion

        # region Create Care order
        responses = self.java_api_manager.send_message_and_receive_response(self.order_submit)
        print_message("CREATE", responses)
        # endregion

        # region Check that the Gating rule is applied to the order
        order_notification = self.java_api_manager.get_last_message(
            ORSMessageType.OrdNotification.value
        ).get_parameters()[JavaApiFields.OrderNotificationBlock.value]
        self.java_api_manager.compare_values(
            {
                JavaApiFields.GatingRuleCondName.value: "All Orders",
                JavaApiFields.GatingRuleID.value: self.data_set.get_venue_gating_rule_id_by_name("main_rule_id"),
                JavaApiFields.ExecutionPolicy.value: "S",
            },
            order_notification,
            "Check GatingRuleID and ExecutionPolicy",
        )

        self.java_api_manager.compare_values(
            {
                "AlgoPolicyID": "1000069",
                "AlgoType": "PDM",
                "ScenarioID": "39",
            },
            order_notification["AlgoParametersBlock"],
            "Check AlgoParametersBlock",
        )
        # endregion

        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value
        ]
        self.java_api_manager.compare_values(
            {
                JavaApiFields.GatingRuleCondName.value: "All Orders",
                JavaApiFields.TransStatus.value: "OPN",
                JavaApiFields.OrdQty.value: "100.0",
                JavaApiFields.ExecutionPolicy.value: "S",
            },
            order_reply,
            "Check that the Gating rule is applied to the order",
        )
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_api_manager.send_post_request(self.modify_rule_message.set_default_param())
