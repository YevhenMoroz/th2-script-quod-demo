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
from test_framework.fix_wrappers.oms.FixMessageAllocationInstructionReportOMS import \
    FixMessageAllocationInstructionReportOMS
from test_framework.fix_wrappers.oms.FixMessageConfirmationReportOMS import FixMessageConfirmationReportOMS
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T8089(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.qty = '8089'
        self.price = '10'
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.venue = self.data_set.get_mic_by_name('mic_1')
        self.client = self.data_set.get_client('client_pt_2')
        self.client_for_rule = self.data_set.get_venue_client_names_by_name('client_pt_2_venue_1')
        self.alloc_account = self.data_set.get_account_by_name('client_pt_2_acc_1')
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit()
        self.fix_verifier = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.execution_report = FixMessageExecutionReportOMS(self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region create order via fix (step 1)
        try:
            nos_rule = self.rule_manager. \
                add_NewOrdSingleExecutionReportTradeByOrdQty_FIXStandard(self.bs_connectivity,
                                                                         self.client_for_rule,
                                                                         self.venue,
                                                                         float(self.price), float(self.price),
                                                                         int(self.qty), int(self.qty), 1)
            self.fix_message.change_parameters(
                {'Side': '5', 'OrderQtyData': {'OrderQty': self.qty}, 'Account': self.client, 'Price': self.price,
                 'PreAllocGrp': {'NoAllocs': [{'AllocAccount': self.alloc_account,
                                               'AllocQty': self.qty}]}})
            response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
            order_id = response[0].get_parameter("OrderID")
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(nos_rule)
        # endregion

        # region check message 35=8 54=5 150 = 0
        ignored_list_new = ['Parties', 'QuodTradeQualifier', 'BookID', 'NoParty', 'SecondaryOrderID', 'tag5120', 'LastMkt',
                        'Text', 'ExecBroker', "GatingRuleName"]
        self.execution_report.set_default_new(self.fix_message)
        self.execution_report.change_parameters({'Side': '5', 'OrderID': order_id})
        self.fix_verifier.check_fix_message_fix_standard(self.execution_report, ignored_fields=ignored_list_new)
        # endregion

        # region check messgae 35=8 54=5 150=F
        ignored_list_exec = ['M_PreAllocGrp', 'Parties', 'QuodTradeQualifier', 'BookID', 'SettlCurrency',
                             'TradeReportingIndicator', 'NoParty', 'tag5120', 'LastMkt',
                             'Text', 'ExecBroker', 'SecurityDesc', "GatingRuleName"]
        self.execution_report.set_default_filled(self.fix_message)
        self.execution_report.change_parameters({'Side': '5', 'OrderID': order_id})
        self.fix_verifier.check_fix_message_fix_standard(self.execution_report, ignored_fields=ignored_list_exec)
        # endregion

        # check 35=J 54=5 626=5 message
        ignored_list_alloc = ['Account', 'tag5120', 'OrderAvgPx', 'IndividualAllocID', "tag11245"]
        allocation_report = FixMessageAllocationInstructionReportOMS()
        allocation_report.set_default_ready_to_book(self.fix_message)
        allocation_report.change_parameters({'Side': '5'})
        self.fix_verifier.check_fix_message_fix_standard(allocation_report, ignored_fields=ignored_list_alloc)
        # endregion

        # region check 35=AK message
        ignored_list_conf = ['OrderAvgPx', 'tag5120', "tag11245"]
        confirmation_message = FixMessageConfirmationReportOMS(self.data_set)
        confirmation_message.set_default_confirmation_new(self.fix_message)
        confirmation_message.change_parameters({'Side': '5'})
        self.fix_verifier.check_fix_message_fix_standard(confirmation_message, ignored_fields=ignored_list_conf)
        # endregion

        # region check 35=J message
        allocation_report.set_default_preliminary(self.fix_message)
        allocation_report.change_parameters({'Side': '5'})
        self.fix_verifier.check_fix_message_fix_standard(allocation_report, ignored_fields=ignored_list_alloc)
        # endregion
