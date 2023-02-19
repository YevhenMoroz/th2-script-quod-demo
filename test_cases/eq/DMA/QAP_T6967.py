import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.fix_wrappers.oms.FixMessageOrderCancelRequestOMS import FixMessageOrderCancelRequestOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T6967(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.nos = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit()
        self.ocr = FixMessageOrderCancelRequestOMS()
        self.rule_manager = RuleManager(Simulators.equity)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.mic = self.data_set.get_mic_by_name("mic_1")
        self.venue_client_names = self.data_set.get_venue_client_names_by_name("client_1_venue_1")
        self.price = self.nos.get_parameter("Price")

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        params = {"TargetStrategy": "1024",
                  "StrategyParametersGrp": {"NoStrategyParameters": [
                      {
                          'StrategyParameterName': 'Urgency',
                          'StrategyParameterType': '14',
                          'StrategyParameterValue': 'LOW'
                      }
                  ]}
                  }
        self.nos.add_tag(params)
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.bs_connectivity,
                                                                                                  self.venue_client_names,
                                                                                                  self.mic,
                                                                                                  int(self.price))
            self.fix_manager.send_message_and_receive_response_fix_standard(self.nos)
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(nos_rule)

        exec_rep = self.fix_manager.get_last_message("ExecutionReport").get_parameters()
        self.fix_manager.compare_values({"TargetStrategy": "1024", "OrdStatus": "0"}, exec_rep, "Check Step 1")
        # endregion
        # region Step 2
        try:
            cancel_rule = self.rule_manager.add_OrderCancelRequest(self.bs_connectivity, self.venue_client_names,
                                                                   self.mic, True)
            self.ocr.set_default(self.nos)
            self.fix_manager.send_message_and_receive_response_fix_standard(self.ocr)
        except Exception as E:
            logger.error(f"Error is {E}", exc_info=True)
        finally:
            time.sleep(3)
            self.rule_manager.remove_rule(cancel_rule)
        exec_rep = self.fix_manager.get_last_message("ExecutionReport").get_parameters()
        self.fix_manager.compare_values({"OrdStatus": "4", "TargetStrategy": "1024"}, exec_rep, "Check Step 2")
        # endregion
