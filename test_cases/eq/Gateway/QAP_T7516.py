import logging
import time
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

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
seconds, nanos = timestamps()


class QAP_T7516(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.dc_connectivity = self.fix_env.drop_copy
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.fix_verifier_dc = FixVerifier(self.dc_connectivity, self.test_id)
        self.client = self.data_set.get_client_by_name("client_counterpart_1")
        self.rule_manager = RuleManager(Simulators.equity)
        self.mic = self.data_set.get_mic_by_name("mic_1")
        self.rule_client = self.data_set.get_venue_client_names_by_name("client_counterpart_1_venue_1")
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit()
        self.fix_message.change_parameters({'Account': self.client})
        self.params = {"TargetStrategy": "1024",
            "StrategyParametersGrp": {"NoStrategyParameters": [
                {
                    'StrategyParameterName': 'Urgency',
                    'StrategyParameterType': '14',
                    'StrategyParameterValue': 'LOW'
                }
            ]}
        }
        self.fix_message.add_tag(self.params)
        self.price = self.fix_message.get_parameter('Price')
        self.qty = self.fix_message.get_parameter('OrderQtyData')['OrderQty']
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create order with algo param execute it
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.bs_connectivity,
                                                                                                  self.rule_client,
                                                                                                  self.mic,
                                                                                                  int(self.price))
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                            self.rule_client,
                                                                                            self.mic,
                                                                                            int(self.price),
                                                                                            int(self.qty), 2)
            response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(nos_rule)
            self.rule_manager.remove_rule(trade_rule)
        # endregion
        # region check exec report
        list_of_ignore_fields = ['SecurityDesc', 'Text', 'LastMkt', 'SettlCurrency', 'StrategyParametersGrp',
                                 'ReplyReceivedTime', 'GatingRuleCondName', 'GatingRuleName']
        fix_execution_report = FixMessageExecutionReportOMS(self.data_set)
        fix_execution_report.set_default_filled(self.fix_message)
        fix_execution_report.change_parameters({'TargetStrategy': self.params["TargetStrategy"]})
        self.fix_verifier.check_fix_message_fix_standard(fix_execution_report, ignored_fields=list_of_ignore_fields)
        # endregion

