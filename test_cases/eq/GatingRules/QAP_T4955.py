import logging
import time
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.oms.RestApiDisableGatingRuleMessage import RestApiDisableGatingRuleMessage
from test_framework.rest_api_wrappers.oms.RestApiModifyGatingRuleMessage import RestApiModifyGatingRuleMessage

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T4955(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.rest_api_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_api_manager = RestApiManager(session_alias=self.rest_api_connectivity, case_id=self.test_id)
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.venue_client_names = self.data_set.get_venue_client_names_by_name("client_1_venue_1")  # XPAR_CLIENT1
        self.exec_destination = self.data_set.get_mic_by_name("mic_1")  # XPAR
        self.modify_rule_message = RestApiModifyGatingRuleMessage(self.data_set).set_default_param()
        self.disable_rule_message = RestApiDisableGatingRuleMessage(self.data_set).set_default_param()
        self.qty = "15000"
        self.price = "20"
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Enabling GatingRule
        # Set condition to GatingRule
        param = self.modify_rule_message.get_parameter("gatingRuleCondition")
        param[0]["gatingRuleCondExp"] = "OrdQty>10000"
        self.modify_rule_message.update_parameters({"gatingRuleCondition": param})
        self.rest_api_manager.send_post_request(self.modify_rule_message)
        # endregion

        # region Create DMA order via FIX
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.bs_connectivity, self.venue_client_names, self.exec_destination, float(self.price)
            )

            self.fix_message.set_default_dma_limit()
            self.fix_message.change_parameters({"Side": "1", "OrderQtyData": {"OrderQty": self.qty}})
            self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        except Exception as e:
            logger.info(f"Your Exception is {e}")
        finally:
            time.sleep(0)
            self.rule_manager.remove_rule(nos_rule)
        # endregion

        # region Check ExecutionReports
        self.exec_report.set_default_new(self.fix_message)
        self.exec_report.change_parameters(
            {
                "ReplyReceivedTime": "*",
                "SecondaryOrderID": "*",
                "Text": "*",
                "LastMkt": "*",
                "GatingRuleName": "GTRULE_RECOVERY",
                "GatingRuleCondName": "Cond1",
            }
        )
        self.fix_verifier.check_fix_message_fix_standard(self.exec_report)
        # endregion

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_api_manager.send_post_request(self.disable_rule_message)
