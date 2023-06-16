import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, AllocationReportConst, \
    ConfirmationReportConst
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T7243(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.qty = '100'
        self.price = '10'
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.client = self.data_set.get_client('client_pt_1')  # MOClient7 Fully manual with one account
        self.account1 = self.data_set.get_account_by_name("client_pt_1_acc_1")
        self.client_for_rule = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')  # MOClient7_PARIS
        self.exec_destination = self.data_set.get_mic_by_name('mic_1')  # XPAR
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.all_instr = AllocationInstructionOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Create DMA order via FIX
        try:
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                            self.client_for_rule,
                                                                                            self.exec_destination,
                                                                                            float(self.price),
                                                                                            int(self.qty), delay=0)
            self.fix_message.set_default_dma_limit()
            self.fix_message.change_parameters(
                {'Side': '1', 'OrderQtyData': {'OrderQty': self.qty}, 'Account': self.client, 'Price': self.price})
            response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(trade_rule)
        # endregion
        # region Split Booking
        order_id = response[0].get_parameters()['OrderID']
        exec_id = self.fix_manager.get_last_message("ExecutionReport", "EV").get_parameters()['ExecID']
        self.all_instr.set_split_book(order_id)
        self.all_instr.update_fields_in_component("AllocationInstructionBlock",
                                                  {"InstrID": self.data_set.get_instrument_id_by_name(
                                                      "instrument_2"),
                                                      "AccountGroupID": self.client})
        self.java_api_manager.send_message_and_receive_response(self.all_instr)
        allocation_report1 = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        alloc_id1 = allocation_report1[JavaApiFields.ClAllocID.value]
        booking_id = allocation_report1[JavaApiFields.ClientAllocID.value]
        expected_result = ({JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_APP.value,
                            JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_UNM.value})
        actually_result = {JavaApiFields.AllocStatus.value: allocation_report1[JavaApiFields.AllocStatus.value],
                           JavaApiFields.MatchStatus.value: allocation_report1[JavaApiFields.MatchStatus.value]}
        self.java_api_manager.compare_values(expected_result, actually_result, 'Check booking')

        allocation_report2 = \
            self.java_api_manager.get_first_message(ORSMessageType.AllocationReport.value, "APP").get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        alloc_id2 = allocation_report2[JavaApiFields.ClAllocID.value]
        expected_result = ({JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_APP.value,
                            JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_UNM.value})
        actually_result = {JavaApiFields.AllocStatus.value: allocation_report2[JavaApiFields.AllocStatus.value],
                           JavaApiFields.MatchStatus.value: allocation_report2[JavaApiFields.MatchStatus.value]}
        self.java_api_manager.compare_values(expected_result, actually_result, 'Check booking 2')
        # endregion
        # region Amend Block
        self.all_instr.set_amend_book(alloc_id1, exec_id, self.qty, self.price)
        param = {'Qty': '50', 'ClientCommissionList': {'ClientCommissionBlock': [
                    {'CommissionAmount': '5.0', 'CommissionAmountSubType': 'OTH', 'CommissionAmountType': 'BRK',
                     'CommissionBasis': 'ABS', 'CommissionCurrency': 'EUR', 'CommissionRate': '5.0'}]}}

        self.all_instr.update_fields_in_component('AllocationInstructionBlock', param)
        self.java_api_manager.send_message_and_receive_response(self.all_instr)
        alloc_rep = self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
            JavaApiFields.AllocationReportBlock.value]
        param.pop('Qty')
        exp_res = param['ClientCommissionList']['ClientCommissionBlock'][0]
        self.java_api_manager.compare_values(exp_res,alloc_rep['ClientCommissionList']['ClientCommissionBlock'][0],
                                             "Check that block modified")
        # endregion
