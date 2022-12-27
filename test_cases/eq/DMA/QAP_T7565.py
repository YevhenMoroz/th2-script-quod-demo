import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from custom.verifier import VerificationMethod
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T7565(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Create DMA order via FIX
        self.fix_message.set_default_dma_limit("instrument_1")
        self.fix_message.change_parameter("Price", "1.00001")
        self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        exec_rep = self.fix_manager.get_last_message("ExecutionReport").get_parameters()
        self.fix_manager.compare_values({"OrdStatus": "8"}, exec_rep, "Check OrdStatus")
        self.fix_manager.compare_values({"Text": "tick size"}, exec_rep, "Check reject reason",
                                        VerificationMethod.CONTAINS)
        # endregion
