import logging
import time
from pathlib import Path

from ctm_rules_management import CTMRuleManager
from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import AllocationReportConst, JavaApiFields, \
    ConfirmationReportConst
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import \
    ForceAllocInstructionStatusRequestOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T9126(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.qty = '100'
        self.price = '10'
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.ctm_rule_manager = CTMRuleManager()
        self.venue_client_names = self.data_set.get_venue_client_names_by_name('client_pt_9_venue_1')
        self.mic = self.data_set.get_mic_by_name('mic_1')  # XPAR
        self.client = self.data_set.get_client_by_name("client_pt_9")
        self.account = self.data_set.get_account_by_name("client_pt_9_acc_1")
        self.account2 = self.data_set.get_account_by_name("client_pt_9_acc_2")
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.comm_profile = self.data_set.get_comm_profile_by_name("abs_amt")
        self.venue = self.data_set.get_venue_by_name("venue_1")
        self.pset = self.data_set.get_pset('pset_by_id_1')
        self.comm = self.data_set.get_commission_by_name("commission2")
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.approve_message = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.log_rule = self.ctm_rule_manager.add_login_rule()
        self.del_rule = self.ctm_rule_manager.add_delete_rule()
        self.ans_rule = self.ctm_rule_manager.add_autoresponder_with_2_acc(self.account, self.account2)
        time.sleep(30)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Create DMA order via FIX
        try:
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                            self.venue_client_names,
                                                                                            self.mic,
                                                                                            float(self.price),
                                                                                            int(self.qty), 0)
            self.fix_message.set_default_dma_limit()
            self.fix_message.change_parameters(
                {'OrderQtyData': {'OrderQty': self.qty}, 'Price': self.price, 'Account': self.client})
            response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
            # get Client Order ID and Order ID
            order_id = response[0].get_parameters()['OrderID']
            exec_id = response[-1].get_parameters()['ExecID']
        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(trade_rule)
        # endregion
        # region step 1
        self.allocation_instruction.set_default_book(order_id)
        instrument_id = self.data_set.get_instrument_id_by_name('instrument_2')
        comm_block = {'ClientCommissionBlock': [
            {'CommissionAmountType': 'Broker',
             'CommissionAmount': '1',
             'CommissionBasis': 'Absolute',
             'CommissionCurrency': "EUR",
             'CommissionRate': '1'},
            {'CommissionAmountType': 'ClearingBroker',
             'CommissionAmount': '1',
             'CommissionBasis': 'Absolute',
             'CommissionCurrency': "EUR",
             'CommissionRate': '1'}
        ]}
        self.allocation_instruction.update_fields_in_component('AllocationInstructionBlock',
                                                               {"InstrID": instrument_id, "AccountGroupID": self.client,
                                                                "SettlementModelID": "2", "SettlLocationID": "1",
                                                                'ExecAllocList': {
                                                                    'ExecAllocBlock': [{'ExecQty': self.qty,
                                                                                        'ExecID': exec_id,
                                                                                        'ExecPrice': self.price}]},
                                                                'ClientCommissionList': comm_block
                                                                })
        self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        alloc_id = allocation_report[JavaApiFields.ClientAllocID.value]
        # endregion

        # region step 2
        self.approve_message.set_default_approve(alloc_id)
        self.java_api_manager.send_message_and_receive_response(self.approve_message)
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_ACK.value,
             JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_MAT.value,
             JavaApiFields.ConfirmationService.value: AllocationReportConst.ConfirmationService_EXT.value},
            allocation_report, 'Checking that block matched (step 2)')
        conf_report = self.java_api_manager.get_last_message(ORSMessageType.ConfirmationReport.value,
                                                             self.account).get_parameters()[
            JavaApiFields.ConfirmationReportBlock.value]
        alloc_report = self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
            JavaApiFields.AllocationReportBlock.value]
        alloc_report_comm = alloc_report['ClientCommissionList']['ClientCommissionBlock']
        if alloc_report_comm[0]['CommissionAmountType'] == "CLB":
            alloc_report_comm[0], alloc_report_comm[1] = alloc_report_comm[1], alloc_report_comm[0]
        self.java_api_manager.compare_values({'CommissionAmountType': "BRK"}, alloc_report_comm[0],
                                             "Check allocation comm 1(step 2)")
        self.java_api_manager.compare_values({'CommissionAmountType': "CLB"}, alloc_report_comm[1],
                                             "Check allocation comm 2(step 2)")
        conf_report_comm = conf_report['ClientCommissionList']['ClientCommissionBlock']
        if conf_report_comm[0]['CommissionAmountType'] == "CLB":
            conf_report_comm[0], conf_report_comm[1] = conf_report_comm[1], conf_report_comm[0]
        self.java_api_manager.compare_values({'CommissionAmountType': "BRK"}, conf_report_comm[0],
                                             "Check confirmation comm 1(step 3)")
        self.java_api_manager.compare_values({'CommissionAmountType': "CLB"}, conf_report_comm[1],
                                             "Check confirmation comm 2(step 3)")

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.ctm_rule_manager.remove_rules([self.log_rule, self.del_rule, self.ans_rule])
