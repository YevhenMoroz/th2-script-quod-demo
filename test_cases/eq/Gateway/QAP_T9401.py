import logging
import os
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from custom.verifier import VerificationMethod
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import ExecutionReportConst, JavaApiFields
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import \
    ForceAllocInstructionStatusRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
seconds, nanos = timestamps()


class QAP_T9401(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.fix_verifier = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.client = self.data_set.get_client('client_pt_1')
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.approve_message = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.confirmation_request = ConfirmationOMS(self.data_set)
        self.execution_report = ExecutionReportOMS(self.data_set)
        self.dma_washbook = self.data_set.get_washbook_account_by_name('washbook_account_1')
        self.qty = '300'
        self.price = '10'
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1 : create DMA  order
        self.order_submit.set_default_dma_limit()
        self.order_submit.update_fields_in_component(JavaApiFields.NewOrderSingleBlock.value, {
            JavaApiFields.AccountGroupID.value: self.client,
            JavaApiFields.WashBookAccountID.value: self.dma_washbook,
            JavaApiFields.OrdQty.value: self.qty,
            JavaApiFields.Price.value: self.price,
        })
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        order_id = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value][JavaApiFields.OrdID.value]
        # endregion

        # region step 2: Trade DMA order
        self.execution_report.set_default_trade(order_id)
        self.execution_report.update_fields_in_component(JavaApiFields.ExecutionReportBlock.value,
                                                         {
                                                             JavaApiFields.LastTradedQty.value: self.qty,
                                                             JavaApiFields.LastPx.value: self.price,
                                                             JavaApiFields.Price.value: self.price,
                                                             JavaApiFields.CumQty.value: self.qty,
                                                             JavaApiFields.AvgPrice.value: self.price,
                                                             JavaApiFields.OrdQty.value: self.qty
                                                         })
        self.java_api_manager.send_message_and_receive_response(self.execution_report)
        actually_result = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                                 ExecutionReportConst.ExecType_TRD.value).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value]
        exec_id = actually_result[JavaApiFields.ExecID.value]
        exec_id_calculated = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                                 ExecutionReportConst.ExecType_CAL.value).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value][JavaApiFields.ExecID.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value}, actually_result,
            'Verifying that order fully filled (step 2)')
        # endregion

        # region step 3: Check that all 35=8 message has WashBook:
        self._check_that_wash_book_presents(f'.*.fix ExecutionReport.*.ExecID=.{exec_id}.*',
                                            'trade execution step 3')
        self._check_that_wash_book_presents(f'.*.fix ExecutionReport.*.ExecID=.{exec_id_calculated}.*',
                                            'calculated execution step 3')
        # endregion

        # region book CO order step 4: Book DMA order
        self.allocation_instruction.set_default_book(order_id)
        self.allocation_instruction.update_fields_in_component(JavaApiFields.AllocationInstructionBlock.value,
                                                               {
                                                                   JavaApiFields.AvgPx.value: self.price,
                                                                   JavaApiFields.Qty.value: self.qty
                                                               })
        self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        allocation_report = self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value,
                                                                   JavaApiFields.BookingAllocInstructionID.value).get_parameters()[
            JavaApiFields.AllocationReportBlock.value]
        alloc_id = allocation_report[JavaApiFields.ClAllocID.value]
        # endregion

        # region step 5 : Check 35=J (626 = 5 message)
        self._check_that_wash_book_presents(f'.*.fix AllocationReport.*.OrdID=.{order_id}.*.AllocType=ReadyToBook.*',
                                            'AllocationReport  step 5')
        # endregion

        # region step 6: Approve block and allocate block
        # part 1: Approve block
        self.approve_message.set_default_approve(alloc_id)
        self.java_api_manager.send_message_and_receive_response(self.approve_message)
        # end_of_part

        # part 2: Allocate block
        self.confirmation_request.set_default_allocation(alloc_id)
        sec_acc_1 = self.data_set.get_account_by_name('client_pt_1_acc_1')
        self.confirmation_request.update_fields_in_component(JavaApiFields.ConfirmationBlock.value, {
            JavaApiFields.AllocAccountID.value: sec_acc_1,
            JavaApiFields.AllocQty.value: self.qty,
            JavaApiFields.AvgPx.value: self.price,
        })
        self.java_api_manager.send_message_and_receive_response(self.confirmation_request)
        # end_of_part

        # endregion

        # region step 7: Check ConfirmationReport in logs
        self._check_that_wash_book_presents(f'.*.fix Confirmation.*.OrdID=.{order_id}.*',
                                            'Confirmation Report  step 7')
        # endregion

        # region step 8: Check Allocation Report (Preliminary)
        self._check_that_wash_book_presents(f'.*.fix AllocationReport.*.OrdID=.{order_id}.*.AllocType=Preliminary.*',
                                            'AllocationReport  step 8')
        # endregion

    def _check_that_wash_book_presents(self, pattern, step):
        self.ssh_client.send_command('cdl')
        self.ssh_client.send_command(f'egrep "{pattern}" QUOD.FIXBACKOFFICE_TH2.log > logs.txt')
        self.ssh_client.send_command("sed -n '$'p logs.txt > logs2.txt")
        self.ssh_client.get_file('/Logs/quod317/logs2.txt', './logs.txt')
        with open('./logs.txt') as file:
            res: list = file.readlines()
            print(res)
            print('-----------------------------------------------------------')
            self.java_api_manager.compare_values({'WashBookPresent': self.dma_washbook},
                                                 {'WashBookPresent': res[-1]}, f'Verify that WashBook presents ({step})',VerificationMethod.CONTAINS)
        os.remove('./logs.txt')
