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
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, SubmitRequestConst
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import \
    ForceAllocInstructionStatusRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T8664(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.qty = '100'
        self.price = '10'
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.ctm_rule_manager = CTMRuleManager()
        self.venue_client_names = self.data_set.get_venue_client_names_by_name('client_pt_9_venue_1')
        self.mic = self.data_set.get_mic_by_name('mic_1')  # XPAR
        self.client = self.data_set.get_client_by_name("client_pt_9")
        self.account = self.data_set.get_account_by_name("client_pt_9_acc_1")
        self.account2 = self.data_set.get_account_by_name("client_pt_9_acc_2")
        self.comm_profile = self.data_set.get_comm_profile_by_name("abs_amt")
        self.venue = self.data_set.get_venue_by_name("venue_1")
        self.pset = self.data_set.get_pset('pset_by_id_1')
        self.comm = self.data_set.get_commission_by_name("commission2")
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.order_submit = OrderSubmitOMS(data_set)
        self.trade_entry = TradeEntryOMS(self.data_set)
        self.complete_request = DFDManagementBatchOMS(self.data_set)
        self.desk = self.environment.get_list_fe_environment()[0].desk_ids[1]
        self.approve_message = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.log_rule = self.ctm_rule_manager.add_login_rule()
        self.del_rule = self.ctm_rule_manager.add_delete_rule()
        self.ans_rule = self.ctm_rule_manager.add_autoresponder_with_2_acc(self.account, self.account2)
        time.sleep(30)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Create and execute order
        self.order_submit.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                 desk=self.desk,
                                                 role=SubmitRequestConst.USER_ROLE_1.value)
        self.java_api_manager.send_message_and_receive_response(self.order_submit)
        order_id = self.java_api_manager.get_last_message(ORSMessageType.OrderReply.value).get_parameter(
            JavaApiFields.OrdReplyBlock.value)["OrdID"]
        self.trade_entry.set_default_trade(order_id)
        self.java_api_manager.send_message_and_receive_response(self.trade_entry)
        exec_id =self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)[JavaApiFields.ExecID.value]
        self.complete_request.set_default_complete(order_id)
        self.java_api_manager.send_message(self.complete_request)
        # endregion
        # region step 1
        self.allocation_instruction.set_default_book(order_id)
        self.allocation_instruction.update_fields_in_component('AllocationInstructionBlock',
                                                               {"AccountGroupID": self.client,
                                                                "SettlementModelID": "2", "SettlLocationID": "1",
                                                                "BrokerClCommProfileID": "1",
                                                                'ExecAllocList': {
                                                                    'ExecAllocBlock': [{'ExecQty': self.qty,
                                                                                        'ExecID': exec_id,
                                                                                        'ExecPrice': self.price}]}})
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
            self.java_api_manager.get_last_message(ORSMessageType.GatewayAllocationInstruction.value).get_parameters()[
                JavaApiFields.AllocationInstructionBlock.value]
        self.java_api_manager.compare_values({"BIC": "QUODTESTGW3"}, allocation_report, "Check BIC")

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.ctm_rule_manager.remove_rules([self.log_rule, self.del_rule, self.ans_rule])
