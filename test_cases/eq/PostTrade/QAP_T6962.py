import logging
import os
import random
from datetime import datetime, timedelta
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.verifier import VerificationMethod
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType, FIXMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageAllocationOMS import FixMessageAllocationOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, AllocationReportConst, \
    ConfirmationReportConst
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import \
    ForceAllocInstructionStatusRequestOMS
from test_framework.java_api_wrappers.ors_messages.BlockChangeConfirmationServiceRequest import \
    BlockChangeConfirmationServiceRequest
from test_framework.java_api_wrappers.ors_messages.BlockUnallocateRequest import BlockUnallocateRequest
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T6962(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.bs_connectivity = self.fix_env.buy_side
        self.fix_manager42 = FixManager(self.fix_env.sell_side_fix42, self.test_id)
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.all_instr = AllocationInstructionOMS(self.data_set)
        self.confirm = ConfirmationOMS(self.data_set)
        self.approve_block = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.fix_alloc = FixMessageAllocationOMS()
        self.unallocate_message = BlockUnallocateRequest()
        self.confirm = ConfirmationOMS(self.data_set)
        self.change_confirm = BlockChangeConfirmationServiceRequest()
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Create and execute DMA
        client = self.data_set.get_client_by_name("client_pt_8")
        account1 = self.data_set.get_account_by_name("client_pt_8_acc_1")
        venue_client = self.data_set.get_venue_client_names_by_name("client_pt_8_venue_1")
        mic = self.data_set.get_mic_by_name("mic_1")
        price = str(random.randint(10, 200))
        self.params = {
            "TargetStrategy": "1024",
            "StrategyParametersGrp": {"NoStrategyParameters": [
                {
                    'StrategyParameterName': 'Urgency',
                    'StrategyParameterType': '14',
                    'StrategyParameterValue':"MEDIUM"
                }
            ]}
        }
        change_params = {'Account': client, "Price": price}
        nos = FixMessageNewOrderSingleOMS(self.data_set).set_fix42_dma_limit().change_parameters(change_params)
        nos.add_tag(self.params)
        qty = nos.get_parameters()["OrderQty"]

        try:
            rule_manager = RuleManager(Simulators.equity)
            trade_rele = rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                       venue_client, mic,
                                                                                       int(price), int(qty), 0)
            response = self.fix_manager42.send_message_and_receive_response_fix_standard(nos)
        finally:
            rule_manager.remove_rule(trade_rele)
        # endregion
        # region Send FIX alloc
        self.fix_alloc.set_fix42_preliminary(nos, account1)
        self.fix_manager42.send_message_and_receive_response_fix_standard(self.fix_alloc)
        alloc_ack = self.fix_manager42.get_last_message(FIXMessageType.AllocationACK.value).get_parameters()
        self.fix_manager42.compare_values({"AllocStatus": "3"}, alloc_ack, "Check FIX alloc")
        # endregion
        # region Book Order
        order_id = response[0].get_parameters()['OrderID']
        self.all_instr.set_default_book(order_id)
        self.all_instr.update_fields_in_component("AllocationInstructionBlock",
                                                  {"InstrID": self.data_set.get_instrument_id_by_name(
                                                      "instrument_2"), "AvgPx": price,
                                                      "AccountGroupID": client})
        self.java_api_manager.send_message_and_receive_response(self.all_instr)
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        alloc_id = allocation_report[JavaApiFields.ClientAllocID.value]
        expected_result = ({JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_APP.value,
                            JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_UNM.value})
        self.java_api_manager.compare_values(expected_result, allocation_report, 'Check Block')
        # endregion
        # region Approve order
        self.approve_block.set_default_approve(alloc_id)
        self.java_api_manager.send_message_and_receive_response(self.approve_block)
        conf_report = self.java_api_manager.get_last_message(ORSMessageType.ConfirmationReport.value).get_parameter(
            JavaApiFields.ConfirmationReportBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_MAT.value,
             JavaApiFields.ConfirmStatus.value: ConfirmationReportConst.ConfirmStatus_AFF.value}, conf_report, 'Check Alloc')
        # endregion
        # region Check ALS logs Status New
        self.ssh_client.send_command('cdl')
        self.ssh_client.send_command('egrep "serializing fix AllocationReport={.*.}" QUOD.ORS.log > logs.txt')
        self.ssh_client.send_command("sed -n '$'p logs.txt > logs2.txt")
        self.ssh_client.get_file('/Logs/quod317/logs2.txt', './logs.txt')
        with open('./logs.txt') as file:
            res = file.read()
            self.java_api_manager.compare_values({
                'AlgoParameters': 'AlgoParameterName="Urgency" AlgoParameterType=String AlgoParameterValue="MEDIUM"'}, {
                "AlgoParameters": res}, "Check fix allocation",
                VerificationMethod.CONTAINS)
        os.remove('./logs.txt')

        self.ssh_client.send_command('cdl')
        self.ssh_client.send_command('egrep "serializing fix Confirmation={.*.}" QUOD.ORS.log > logs.txt')
        self.ssh_client.send_command("sed -n '$'p logs.txt > logs2.txt")
        self.ssh_client.get_file('/Logs/quod317/logs2.txt', './logs.txt')
        with open('./logs.txt') as file:
            res = file.read()
            self.java_api_manager.compare_values({
               'AlgoParameters': 'AlgoParameterName="Urgency" AlgoParameterType=String AlgoParameterValue="MEDIUM"'}, {
                "AlgoParameters": res}, "Check fix confirmation",
                VerificationMethod.CONTAINS)
        os.remove('./logs.txt')
        # endregion