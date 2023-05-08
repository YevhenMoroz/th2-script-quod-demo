import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.verifier import VerificationMethod
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ComputeBookingFeesCommissionsRequestOMS import \
    ComputeBookingFeesCommissionsRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import \
    ForceAllocInstructionStatusRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.oms.RestApiManageSecurityBlock import RestApiManageSecurityBlock
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class QAP_T6994(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.ss_connectivity = self.fix_env.sell_side
        self.client = self.data_set.get_client_by_name("client_com_1")
        self.client_acc1 = self.data_set.get_account_by_name('client_com_1_acc_1')
        self.client_acc2 = self.data_set.get_account_by_name('client_com_1_acc_2')
        self.client_for_rule = self.data_set.get_venue_client_names_by_name("client_com_1_venue_2")
        self.mic = self.data_set.get_mic_by_name("mic_2")
        self.cur = self.data_set.get_currency_by_name('currency_3')
        self.comm_cur = self.data_set.get_currency_by_name('currency_2')
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.submit_request = OrderSubmitOMS(self.data_set).set_default_dma_limit()
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.rule_manager = RuleManager(Simulators.equity)
        self.qty = '100'
        self.price = '20'
        self.qty_first_alloc = '75'
        self.qty_second_alloc = str(int(self.qty) - int(self.qty_first_alloc))
        self.listing_id = self.data_set.get_listing_id_by_name("listing_2")
        self.instr_id = self.data_set.get_instrument_id_by_name("instrument_3")
        self.venue = self.data_set.get_venue_by_name("venue_2")
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.rest_api_manager = RestApiManager(session_alias=self.wa_connectivity, case_id=self.test_id)
        self.compute_request = ComputeBookingFeesCommissionsRequestOMS(self.data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.force_alloc = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.confirm = ConfirmationOMS(self.data_set)
        self.fee_charge_type = self.data_set.get_misc_fee_type_by_name('local_comm')
        self.instr_type = self.data_set.get_instr_type('equity')
        self.perc_amt = self.data_set.get_comm_profile_by_name("perc_amt")
        self.fee_type = self.data_set.get_misc_fee_type_by_name('levy')
        self.manage_security_block = RestApiManageSecurityBlock(self.data_set)
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region send fee
        self.manage_security_block.set_default_param()
        self.rest_api_manager.send_post_request(self.manage_security_block)
        params = {"venueID": self.venue, 'miscFeeCategory': self.fee_charge_type, 'instrType': self.instr_type}
        self.rest_commission_sender.clear_commissions()
        self.rest_commission_sender.clear_fees()
        self.rest_commission_sender.set_modify_fees_message(comm_profile=self.perc_amt, recalculate=True,
                                                            fee_type=self.fee_type)
        self.rest_commission_sender.change_message_params(params)
        self.rest_commission_sender.send_post_request()
        self.ssh_client.send_command("qrestart ORS")
        time.sleep(30)
        # endregion

        # region send dma order
        self.submit_request.update_fields_in_component('NewOrderSingleBlock', {'AccountGroupID': self.client,
                                                                               'ListingList': {'ListingBlock': [{
                                                                                   'ListingID': self.listing_id}]},
                                                                               'InstrID': self.instr_id,
                                                                               'OrdQty': self.qty, "Price": self.price})
        trade_rule = None
        try:
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                                            self.client_for_rule,
                                                                                            self.mic, float(self.price),
                                                                                            int(self.qty), 2)

            self.java_api_manager.send_message_and_receive_response(self.submit_request)
            exec_report = self.java_api_manager.get_first_message(ORSMessageType.ExecutionReport.value).get_parameter(
                JavaApiFields.ExecutionReportBlock.value)
            order_id = exec_report[JavaApiFields.OrdID.value]
        finally:
            time.sleep(3)
            self.rule_manager.remove_rule(trade_rule)
        # endregion

        # region Step 2 - Check that Execution of DMA doesn`t have Fee
        exec_reply = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()
        self.java_api_manager.compare_values(
            {JavaApiFields.ExecutionReportBlock.value: JavaApiFields.MiscFeesList.value}, exec_reply,
            "Check execution doesn't contain fee", VerificationMethod.NOT_CONTAINS)
        # endregion

        # region step 3 - Book order
        gross_amt = float(self.price) * float(self.qty)
        self.allocation_instruction.set_default_book(order_id)
        self.allocation_instruction.update_fields_in_component("AllocationInstructionBlock",
                                                               {"AccountGroupID": self.client,
                                                                "AvgPx": self.price,
                                                                'GrossTradeAmt': gross_amt,
                                                                "InstrID": self.instr_id, 'Currency': self.cur,
                                                                "Qty": self.qty})
        self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)

        # region step 3 - Check commission
        alloc_report = self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameter(
            JavaApiFields.AllocationReportBlock.value)
        order_update_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdUpdate.value).get_parameter(
            JavaApiFields.OrdUpdateBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_BKD.value},
            order_update_reply,
            "Comparing PostTradeStatus after Book",
        )
        alloc_id = alloc_report[JavaApiFields.ClAllocID.value]
        # endregion

        expected_result_comm = {
            JavaApiFields.MiscFeeBasis.value: "P",
            JavaApiFields.MiscFeeRate.value: '5.0',
            JavaApiFields.MiscFeeCurr.value: self.comm_cur,
            JavaApiFields.MiscFeeType.value: self.fee_type,
            JavaApiFields.MiscFeeAmt.value: '0.75'
        }
        # region step 4 - Approve block
        self.force_alloc.set_default_approve(alloc_id)
        self.java_api_manager.send_message_and_receive_response(self.force_alloc)
        # endregion

        # region step 4 - Allocate block
        # 1
        self.confirm.set_default_allocation(alloc_id)
        self.confirm.update_fields_in_component("ConfirmationBlock", {"AllocAccountID": self.client_acc1,
                                                                      "InstrID": self.instr_id,
                                                                      "AllocQty": self.qty_first_alloc,
                                                                      "AvgPx": self.price})
        self.java_api_manager.send_message_and_receive_response(self.confirm)
        confirm_report = \
            self.java_api_manager.get_first_message(ORSMessageType.ConfirmationReport.value).get_parameters()[
                JavaApiFields.ConfirmationReportBlock.value]
        self.java_api_manager.compare_values(expected_result_comm,
                                             confirm_report[JavaApiFields.MiscFeesList.value][
                                                 JavaApiFields.MiscFeesBlock.value][0],
                                             "Check fee after first allocation")
        conf_id1 = confirm_report['ConfirmationID']
        # endregion

        # 2
        expected_result_comm.update({JavaApiFields.MiscFeeAmt.value: '0.25'})
        self.confirm.update_fields_in_component("ConfirmationBlock", {"AllocAccountID": self.client_acc2,
                                                                      "AllocQty": self.qty_second_alloc})
        self.java_api_manager.send_message_and_receive_response(self.confirm)
        confirm_report = \
            self.java_api_manager.get_first_message(ORSMessageType.ConfirmationReport.value).get_parameters()[
                JavaApiFields.ConfirmationReportBlock.value]
        self.java_api_manager.compare_values(expected_result_comm,
                                             confirm_report[JavaApiFields.MiscFeesList.value][
                                                 JavaApiFields.MiscFeesBlock.value][0],
                                             "Check commission after second allocation")
        conf_id2 = confirm_report['ConfirmationID']
        # endregion

        # region step 6
        comm_list = {
            JavaApiFields.MiscFeeBasis.value: "P",
            JavaApiFields.MiscFeeRate.value: '10.0',
            JavaApiFields.MiscFeeCurr.value: self.comm_cur,
            JavaApiFields.MiscFeeType.value: self.fee_type,
            JavaApiFields.MiscFeeAmt.value: '1.5'
        }
        self.confirm.set_default_amend_allocation(conf_id1, alloc_id, qty_to_allocate=self.qty_first_alloc,
                                                  price=self.price)
        self.confirm.update_fields_in_component('ConfirmationBlock', {"AllocAccountID": self.client_acc1,
                                                                      "InstrID": self.instr_id,
                                                                      JavaApiFields.MiscFeesList.value: {
                                                                          JavaApiFields.MiscFeesBlock.value: [
                                                                              comm_list]}})
        self.java_api_manager.send_message_and_receive_response(self.confirm)
        confirmation = self.java_api_manager.get_last_message(ORSMessageType.ConfirmationReport.value).get_parameters()[
            JavaApiFields.ConfirmationReportBlock.value]
        self.java_api_manager.compare_values(
            comm_list,
            confirmation[JavaApiFields.MiscFeesList.value][
                JavaApiFields.MiscFeesBlock.value][0],
            'Check fee after Amended Confirmation')
        # endregion

        self.confirm.set_default_amend_allocation(conf_id2, alloc_id, qty_to_allocate=self.qty_second_alloc,
                                                  price=self.price)
        self.confirm.update_fields_in_component('ConfirmationBlock', {"AllocAccountID": self.client_acc2,
                                                                      "InstrID": self.instr_id,
                                                                      JavaApiFields.MiscFeesList.value: {
                                                                          JavaApiFields.MiscFeesBlock.value: [
                                                                              comm_list]}})
        self.java_api_manager.send_message_and_receive_response(self.confirm)
        confirmation = self.java_api_manager.get_last_message(ORSMessageType.ConfirmationReport.value).get_parameters()[
            JavaApiFields.ConfirmationReportBlock.value]
        self.java_api_manager.compare_values(
            comm_list,
            confirmation[JavaApiFields.MiscFeesList.value][
                JavaApiFields.MiscFeesBlock.value][0],
            'Check fee after Amended Confirmation')

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_commission_sender.clear_fees()
        self.manage_security_block.set_default_param()
        self.rest_api_manager.send_post_request(self.manage_security_block)
        self.ssh_client.send_command("qrestart ORS")
        time.sleep(30)
