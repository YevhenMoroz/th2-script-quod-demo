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
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, ExecutionReportConst, \
    OrderReplyConst, SubmitRequestConst
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ComputeBookingFeesCommissionsRequestOMS import \
    ComputeBookingFeesCommissionsRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import \
    ForceAllocInstructionStatusRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.ors_messages.BlockUnallocateRequest import BlockUnallocateRequest
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.ssh_wrappers.ssh_client import SshClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()


def print_message(message, responses):
    logger.info(message)
    for i in responses:
        logger.info(i)
        logger.info(i.get_parameters())


class QAP_T7038(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.bs_connectivity = self.fix_env.buy_side
        self.ss_connectivity = self.fix_env.sell_side
        self.qty = '999'
        self.price = '99'
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.currency = self.data_set.get_currency_by_name('currency_3')
        self.currency_post_trade = self.data_set.get_currency_by_name('currency_2')
        self.venue_mic = self.data_set.get_mic_by_name('mic_2')
        self.client = self.data_set.get_client('client_com_1')
        self.alloc_account = self.data_set.get_account_by_name('client_com_1_acc_4')
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.fix_verifier = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.submit_request = OrderSubmitOMS(self.data_set)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.execution_report = ExecutionReportOMS(self.data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.compute_booking_fee_commission_request = ComputeBookingFeesCommissionsRequestOMS(self.data_set)
        self.allocation_instruction_message = AllocationInstructionOMS(self.data_set)
        self.confirmation_request = ConfirmationOMS(self.data_set)
        self.approve_block = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.complete_request = DFDManagementBatchOMS(self.data_set)
        self.contra_firm = self.data_set.get_contra_firm('contra_firm_1')
        self.unallocate_message = BlockUnallocateRequest()
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region set agent_fees precondition
        agent_fee_type = self.data_set.get_misc_fee_type_by_name('agent')
        instrument_id = self.data_set.get_instrument_id_by_name("instrument_3")
        commission_profile = self.data_set.get_comm_profile_by_name('perc_amt')
        fee = self.data_set.get_fee_by_name('fee3')
        instr_type = self.data_set.get_instr_type('equity')
        venue_id = self.data_set.get_venue_id('eurex')
        contra_firm = self.data_set.get_counterpart_id_java_api('counterpart_contra_firm')
        self.rest_commission_sender.clear_fees()
        all_exec_scope = self.data_set.get_fee_exec_scope_by_name('all_exec')
        self.rest_commission_sender.set_modify_fees_message(fee_type=agent_fee_type, comm_profile=commission_profile,
                                                            fee=fee)
        self.rest_commission_sender.change_message_params(
            {'commExecScope': all_exec_scope, 'instrType': instr_type, "venueID": venue_id})
        self.rest_commission_sender.send_post_request()
        # endregion

        # region set up configuration on BackEnd(precondition)
        self.ssh_client.send_command('~/quod/script/site_scripts/change_book_agent_misk_fee_type_on_Y')
        self.ssh_client.send_command("qrestart QUOD.ORS QUOD.CS QUOD.ESBUYTH2TEST")
        time.sleep(90)
        # endregion

        # region create DMA order (precondition)
        self.submit_request.set_default_dma_limit()
        self.submit_request.update_fields_in_component('NewOrderSingleBlock',
                                                       {'OrdCapacity': SubmitRequestConst.OrdCapacity_Agency.value,
                                                        'OrdQty': self.qty,
                                                        'AccountGroupID': self.client,
                                                        'Price': self.price,
                                                        'ListingList': {'ListingBlock': [{'ListingID':
                                                            self.data_set.get_listing_id_by_name(
                                                                "listing_2")}]},
                                                        'InstrID': instrument_id,
                                                        "PreTradeAllocationBlock": {
                                                            "PreTradeAllocationList": {"PreTradeAllocAccountBlock": [
                                                                {"AllocAccountID": self.alloc_account,
                                                                 "AllocQty": self.qty}]}},
                                                        }
                                                       )
        self.submit_request.remove_fields_from_component('NewOrderSingleBlock', ['SettlCurrency'])
        responses = self.java_api_manager.send_message_and_receive_response(self.submit_request)
        print_message("Creating DMA order (Precondition)", responses)
        order_reply_message = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        order_id = order_reply_message[JavaApiFields.OrdID.value]
        cl_ord_id = order_reply_message[JavaApiFields.ClOrdID.value]
        # endregion

        # region trade DMA order (step 1)
        self.execution_report.set_default_trade(order_id)
        self.execution_report.update_fields_in_component('ExecutionReportBlock',
                                                         {
                                                             "InstrumentBlock": self.data_set.get_java_api_instrument(
                                                                 "instrument_2"),
                                                             "Side": "Buy",
                                                             "LastTradedQty": self.qty,
                                                             "LastPx": self.price,
                                                             "OrdType": "Limit",
                                                             "Price": self.price,
                                                             "Currency": self.currency,
                                                             "ExecType": "Trade",
                                                             "TimeInForce": "Day",
                                                             "LeavesQty": '0',
                                                             "CumQty": self.qty,
                                                             "AvgPrice": self.price,
                                                             "LastMkt": self.venue_mic,
                                                             "OrdQty": self.qty
                                                         })
        responses = self.java_api_manager.send_message_and_receive_response(self.execution_report)
        print_message('Trade DMA order (Step 1)', responses)
        execution_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value, ExecutionReportConst.ExecType_TRD.value).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
        exec_id = execution_report[JavaApiFields.ExecID.value]
        actually_exec_sts = execution_report[JavaApiFields.TransExecStatus.value]
        # the end

        # send ComputeBookingCommmissionFeesRequest (part of step 1)
        avg_px = str(float(self.price) / 100)
        post_trade_status = OrderReplyConst.PostTradeStatus_RDY.value
        self.compute_booking_fee_commission_request.set_list_of_exec_alloc_block(self.qty, exec_id, self.price,
                                                                                 post_trade_status)
        self.compute_booking_fee_commission_request.set_list_of_order_alloc_block(cl_ord_id, order_id,
                                                                                  post_trade_status)
        self.compute_booking_fee_commission_request.set_default_compute_booking_request(self.qty, avg_px)
        responses = self.java_api_manager.send_message_and_receive_response(self.compute_booking_fee_commission_request)
        print_message("send ComputeBookingCommissionFeesRequest (part of step 1)", responses)
        compute_booking_misc_fee_response = self.java_api_manager.get_last_message(
            ORSMessageType.ComputeBookingFeesCommissionsReply.value).get_parameters()
        root_misc_fee_list_is_absent = not JavaApiFields.RootMiscFeesList.value in compute_booking_misc_fee_response
        self.java_api_manager.compare_values({JavaApiFields.RootMiscFeesList.value:True},
                                             {JavaApiFields.RootMiscFeesList.value:root_misc_fee_list_is_absent},
                                            'Check that ComputeMiscFeeCommissionReply doesn`t have Agent Fees (part of step 1)')
        # the end

        # book CO order (part of step 1)
        gross_amt = str(float(avg_px) * float(self.qty))
        self.allocation_instruction.set_default_book(order_id)
        self.allocation_instruction.update_fields_in_component('AllocationInstructionBlock',
                                                               {
                                                                   'GrossTradeAmt': gross_amt,
                                                                   'AvgPx': avg_px,
                                                                   'Qty': self.qty,
                                                                   'AccountGroupID': self.client,
                                                                   'Currency': self.currency_post_trade,
                                                                   "InstrID": instrument_id,
                                                                   'ExecAllocList': {
                                                                       'ExecAllocBlock': [{'ExecQty': self.qty,
                                                                                           'ExecID': exec_id,
                                                                                           'ExecPrice': self.price}]},
                                                               })
        responses = self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        print_message("Allocation Instruction", responses)
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value, JavaApiFields.BookingAllocInstructionID.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        order_update = self.java_api_manager.get_last_message(ORSMessageType.OrdUpdate.value).get_parameters()[
            JavaApiFields.OrdUpdateBlock.value]
        actually_post_trade_status = order_update[JavaApiFields.PostTradeStatus.value]
        alloc_id = allocation_report[JavaApiFields.ClientAllocID.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value,
             JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_BKD.value},
            {JavaApiFields.TransExecStatus.value: actually_exec_sts,
             JavaApiFields.PostTradeStatus.value: actually_post_trade_status},
            'Comparing expected and actually results from step 1')
        root_misc_fee_list_is_absent = not JavaApiFields.RootMiscFeesList.value in allocation_report
        self.java_api_manager.compare_values({JavaApiFields.RootMiscFeesList.value: True},
                                             {JavaApiFields.RootMiscFeesList.value: root_misc_fee_list_is_absent},
                                            'Check that Block doesn`t has Agent Fees (part of step 1)')
        # the end
        # endregion

        # region step 2
        # approve block (part of step 2)
        self.approve_block.set_default_approve(alloc_id=alloc_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.approve_block)
        print_message('Approve block (part of step 2)', responses)
        # the end

        # allocate block (part of step 2)
        self.confirmation_request.set_default_allocation(alloc_id)
        self.confirmation_request.update_fields_in_component("ConfirmationBlock", {
            "AllocAccountID": self.alloc_account,
            "InstrID": instrument_id,
            "AllocQty": self.qty,
            "AvgPx": avg_px})
        responses = self.java_api_manager.send_message_and_receive_response(self.confirmation_request)
        print_message(f' Allocate block (part of step 2)', responses)
        confirmation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ConfirmationReport.value).get_parameters()[
                JavaApiFields.ConfirmationReportBlock.value]
        root_misc_fee_list_is_absent = not JavaApiFields.RootMiscFeesList.value in confirmation_report
        self.java_api_manager.compare_values({JavaApiFields.RootMiscFeesList.value: True},
                                             {JavaApiFields.RootMiscFeesList.value: root_misc_fee_list_is_absent},
                                            'Check that Agent Fees is absent for confirmation (step 2)')
        # the end

        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_commission_sender.clear_fees()
        self.ssh_client.send_command('~/quod/script/site_scripts/change_book_agent_misc_fee_type_on_N')
        self.ssh_client.send_command("qrestart QUOD.ORS QUOD.CS QUOD.ESBUYTH2TEST")
        time.sleep(90)
        self.ssh_client.close()
