import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.verifier import VerificationMethod
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7446(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit()
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.bs_connectivity = self.fix_env.buy_side
        self.venue_client_name = self.data_set.get_venue_client_names_by_name('client_1_venue_1')  # MOClient_PARIS
        self.mic = self.data_set.get_mic_by_name('mic_1')  # XPAR
        self.price = self.fix_message.get_parameter("Price")
        self.qty = self.fix_message.get_parameter("OrderQtyData")["OrderQty"]

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1 2
        client = self.data_set.get_client_by_name("client_1")
        self.fix_message.change_parameters({"Account": client})
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                          self.venue_client_name,
                                                                                          self.mic, float(self.price),
                                                                                          int(self.qty), 0)
            response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(nos_rule)
        # endregion
        # region Step 3
        for i, res in enumerate(response):
            if res.get_message_type() == "ExecutionReport":
                self.fix_manager.compare_values({"ExecType": "3"}, res.get_parameters(),
                                              f"Check ExecType from {i} ExecutionReport", VerificationMethod.NOT_EQUALS)
        # endregion
