import logging
import os
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T10954(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.new_order_single = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit()
        self.fix_verifier_back_office = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.fix_exec_report = FixMessageExecutionReportOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region create orders (step 1)
        self.fix_manager.send_message_and_receive_response_fix_standard(self.new_order_single)
        # endregion

        # region check PendingOpen message on the Drop Copy
        ignored_fields = ['GatingRuleCondName', 'GatingRuleName', 'Parties', 'QuodTradeQualifier', 'BookID', 'NoParty',
                          'tag5120', 'LastMkt', 'ExecBroker', 'trailer', 'header']
        self.fix_exec_report.set_default_new(self.new_order_single)
        self.fix_exec_report.change_parameters({"OrdStatus": "A", "ExecType": "A"})
        self.fix_verifier_back_office.check_fix_message(self.fix_exec_report, ignored_fields=ignored_fields)
        # endregion
