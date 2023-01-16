import logging
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


class QAP_T7375(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit()
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.bs_connectivity = self.fix_env.buy_side
        self.venue_client_name = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')  # MOClient_PARIS
        self.mic = self.data_set.get_mic_by_name('mic_1')  # XPAR
        self.price = self.fix_message.get_parameter("Price")
        self.qty = self.fix_message.get_parameter("OrderQtyData")["OrderQty"]

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        client = self.data_set.get_client_by_name("client_pt_1")
        account = self.data_set.get_washbook_account_by_name('washbook_account_1')
        no_allocs = {"NoAllocs": [{'AllocAccount': account, 'AllocQty': self.qty}]}
        self.fix_message.change_parameters({"Account": client, "PreAllocGrp": no_allocs})
        self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        exec_rep = self.fix_manager.get_last_message("ExecutionReport").get_parameters()
        self.fix_manager.compare_values({"OrdStatus": "8"}, exec_rep, "Check OrdStatus")
        self.fix_manager.compare_values({"Text": "Unknown account"}, exec_rep, "Check reason",
                                        VerificationMethod.CONTAINS)
        # endregion
