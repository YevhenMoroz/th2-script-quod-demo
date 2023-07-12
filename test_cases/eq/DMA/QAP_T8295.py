import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import Simulators, RuleManager
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T8295(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.rule_manager = RuleManager(Simulators.equity)
        self.venue_client_name = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        self.mic = self.data_set.get_mic_by_name('mic_1')
        self.fix_verifier = FixVerifier(self.fix_env.buy_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit()
        self.price = self.fix_message.get_parameter('Price')
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region  step 1: Send FIX order
        self.fix_message.change_parameter("OrdType", "I")
        nos_rule = None
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.fix_env.buy_side,
                                                                                                  self.venue_client_name,
                                                                                                  self.mic,
                                                                                                  int(self.price))
            response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        except Exception as e:
            logger.error(f'Something gone wrong : {e}', exc_info=True)
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(nos_rule)
        # endergion

        # region  step 1: Check execution report on the Buy Side
        ignored_fields = ['ReplyReceivedTime', 'GatingRuleCondName', 'GatingRuleName', 'SecondaryOrderID', 'LastMkt',
                          'Text']
        self.exec_report.set_default_new(self.fix_message)
        self.fix_verifier.check_fix_message_fix_standard(self.exec_report, ["ClOrdID"], ignored_fields=ignored_fields)
        # endergion
