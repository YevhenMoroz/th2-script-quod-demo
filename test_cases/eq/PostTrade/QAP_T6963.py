import logging
import os
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from custom.verifier import VerificationMethod
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import SubmitRequestConst
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import \
    ForceAllocInstructionStatusRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
seconds, nanos = timestamps()


class QAP_T6963(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.bo_connectivity = self.fix_env.drop_copy
        self.client = self.data_set.get_client_by_name('client_pt_1')
        self.client_acc = self.data_set.get_account_by_name('client_pt_1_acc_1')
        self.fix_verifier_dc = FixVerifier(self.bo_connectivity, self.test_id)
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.ord_sub_message = OrderSubmitOMS(self.data_set)
        self.trade_entry_message = TradeEntryOMS(self.data_set)
        self.complete_order = DFDManagementBatchOMS(self.data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.approve_message = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.confirmation_request = ConfirmationOMS(self.data_set)
        self.desk_id = self.environment.get_list_fe_environment()[0].desk_ids[1]
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create order
        self.ord_sub_message.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                    desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                    role=SubmitRequestConst.USER_ROLE_1.value, external_algo_twap=True)
        response = self.java_api_manager.send_message_and_receive_response(self.ord_sub_message)
        self.return_result(response, ORSMessageType.OrdReply.value)
        order_id = self.result.get_parameter('OrdReplyBlock')['OrdID']
        cl_order_id = self.result.get_parameter('OrdReplyBlock')['ClOrdID']
        qty = self.result.get_parameter('OrdReplyBlock')['OrdQty']
        price = self.result.get_parameter('OrdReplyBlock')['Price']
        # endregion
        # region trade order
        self.trade_entry_message.set_default_trade(order_id, price, qty)
        self.java_api_manager.send_message(self.trade_entry_message)
        # endregion
        # region complete order
        self.complete_order.set_default_complete(order_id)
        self.java_api_manager.send_message(self.complete_order)
        # endregion
        # region book order
        self.allocation_instruction.set_default_book(order_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        self.return_result(responses, ORSMessageType.AllocationReport.value)
        alloc_id = self.result.get_parameter('AllocationReportBlock')['ClientAllocID']
        # endregion
        # region approve order
        self.approve_message.set_default_approve(alloc_id)
        self.java_api_manager.send_message(self.approve_message)
        # endregion
        # region allocate order
        self.confirmation_request.set_default_allocation(alloc_id)
        self.confirmation_request.update_fields_in_component('ConfirmationBlock', {
            "AllocAccountID": self.client_acc, 'AllocQty': qty, 'AvgPx': price})
        responses = self.java_api_manager.send_message_and_receive_response(self.confirmation_request)
        self.return_result(responses, ORSMessageType.AllocationReport.value)
        # endregion
        # region Check Allocation Report
        self.ssh_client.send_command('cdl')
        self.ssh_client.send_command('egrep "serializing fix AllocationReport={.*.}" QUOD.ORS.log > logs.txt')
        self.ssh_client.send_command("sed -n '$'p logs.txt > logs2.txt")
        self.ssh_client.get_file('/Logs/quod317/logs2.txt', './logs.txt')
        exp_res = {
                'AlgoParameterName': 'AlgoParameterName="StrategyTag"', 'AlgoParameterValue':
                    'AlgoParameterValue="TWAP"', 'VenueScenarioParameterID': 'VenueScenarioParameterID="7505"'}
        with open('./logs.txt') as file:
            res = file.read()
            self.java_api_manager.compare_values(exp_res, {
                "AlgoParameterName": res, 'AlgoParameterValue': res, 'VenueScenarioParameterID': res},
                "Check fix allocation", VerificationMethod.CONTAINS)
        os.remove('./logs.txt')

        self.ssh_client.send_command('cdl')
        self.ssh_client.send_command('egrep "serializing fix Confirmation={.*.}" QUOD.ORS.log > logs.txt')
        self.ssh_client.send_command("sed -n '$'p logs.txt > logs2.txt")
        self.ssh_client.get_file('/Logs/quod317/logs2.txt', './logs.txt')
        with open('./logs.txt') as file:
            res = file.read()
            self.java_api_manager.compare_values(exp_res, {
                "AlgoParameterName": res, 'AlgoParameterValue': res, 'VenueScenarioParameterID': res},
                "Check fix confirmation", VerificationMethod.CONTAINS)
        os.remove('./logs.txt')
        # endregion

    def return_result(self, responses, message_type):
        for response in responses:
            if response.get_message_type() == message_type:
                self.result = response
