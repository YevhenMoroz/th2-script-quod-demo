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
from test_framework.fix_wrappers.oms.FixMessageAllocationInstructionReportOMS import \
    FixMessageAllocationInstructionReportOMS
from test_framework.fix_wrappers.oms.FixMessageConfirmationReportOMS import FixMessageConfirmationReportOMS
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, ExecutionReportConst, \
    OrderReplyConst, SubmitRequestConst, ConfirmationReportConst, AllocationInstructionConst
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ComputeBookingFeesCommissionsRequestOMS import \
    ComputeBookingFeesCommissionsRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import \
    ForceAllocInstructionStatusRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
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


class QAP_T8458(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.bs_connectivity = self.fix_env.buy_side
        self.ss_connectivity = self.fix_env.sell_side
        self.qty = '1000'
        self.price = '99'
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.currency = self.data_set.get_currency_by_name('currency_3')
        self.currency_post_trade = self.data_set.get_currency_by_name('currency_2')
        self.venue_mic = self.data_set.get_mic_by_name('mic_2')
        self.client = self.data_set.get_client('client_fees_1')
        self.alloc_account = self.data_set.get_account_by_name('client_fees_1_acc_1')
        self.venue_client_name = self.data_set.get_venue_client_names_by_name('client_com_1_venue_1')
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.fix_verifier = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.submit_request = OrderSubmitOMS(self.data_set)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.trade_entry = TradeEntryOMS(self.data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.compute_booking_fee_commission_request = ComputeBookingFeesCommissionsRequestOMS(self.data_set)
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
        on_calculated_exec_scope = self.data_set.get_fee_exec_scope_by_name('on_calculated')
        self.rest_commission_sender.set_modify_fees_message(fee_type=agent_fee_type, comm_profile=commission_profile,
                                                            fee=fee)
        self.rest_commission_sender.change_message_params(
            {'commExecScope': on_calculated_exec_scope, 'instrType': instr_type, "venueID": venue_id})
        self.rest_commission_sender.send_post_request()
        # endregion

        # region set up configuration on BackEnd(precondition)
        self.ssh_client.send_command('~/quod/script/site_scripts/change_book_agent_misk_fee_type_on_Y')
        self.ssh_client.send_command("qrestart QUOD.ORS QUOD.CS QUOD.ESBUYTH2TEST")
        time.sleep(80)
        # endregion

        # region create CO order (step 1)
        self.submit_request.set_default_care_limit(recipient=self.environment.get_list_fe_environment()[0].user_1,
                                                   desk=self.environment.get_list_fe_environment()[0].desk_ids[0],
                                                   role=SubmitRequestConst.USER_ROLE_1.value)
        self.submit_request.update_fields_in_component('NewOrderSingleBlock',
                                                       {'OrdCapacity': SubmitRequestConst.OrdCapacity_Agency.value,
                                                        'OrdQty': self.qty,
                                                        'AccountGroupID': self.client,
                                                        'Price': self.price,
                                                        'ListingList': {'ListingBlock': [{'ListingID':
                                                            self.data_set.get_listing_id_by_name(
                                                                "listing_2")}]},
                                                        'InstrID': instrument_id
                                                        }
                                                       )
        self.submit_request.remove_fields_from_component('NewOrderSingleBlock', ['SettlCurrency'])
        responses = self.java_api_manager.send_message_and_receive_response(self.submit_request)
        print_message("Creating CO order (Step 1)", responses)
        order_reply_message = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        order_id = order_reply_message[JavaApiFields.OrdID.value]
        cl_ord_id = order_reply_message[JavaApiFields.ClOrdID.value]
        actually_sts_field = order_reply_message[JavaApiFields.TransStatus.value]
        self.java_api_manager.compare_values({JavaApiFields.TransStatus.value: OrderReplyConst.TransStatus_OPN.value},
                                             {JavaApiFields.TransStatus.value: actually_sts_field},
                                             'Comparing expected and actually results from step 1')
        # endregion

        # region trade CO order with ContraFirm (step 2)
        self.trade_entry.set_default_trade(order_id, self.price, self.qty)
        self.trade_entry.update_fields_in_component('TradeEntryRequestBlock',
                                                    {'CounterpartList': {'CounterpartBlock': [contra_firm]}})
        responses = self.java_api_manager.send_message_and_receive_response(self.trade_entry)
        print_message('Trade CO order (Step 2)', responses)
        execution_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
        exec_id = execution_report[JavaApiFields.ExecID.value]
        actually_exec_sts = execution_report[JavaApiFields.TransExecStatus.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value},
            {JavaApiFields.TransExecStatus.value: actually_exec_sts},
            'Comparing expected and actually results from step 2')
        # endregion

        # region complete CO order (step 3)
        self.complete_request.set_default_complete(order_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.complete_request)
        print_message('Completing CO order', responses)
        execution_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
        order_reply_message = self.java_api_manager.get_last_message(ORSMessageType.OrderReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        actually_post_trade_status = order_reply_message[JavaApiFields.PostTradeStatus.value]
        actually_done_for_day = order_reply_message[JavaApiFields.DoneForDay.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_RDY.value,
             JavaApiFields.DoneForDay.value: OrderReplyConst.DoneForDay_YES.value},
            {JavaApiFields.PostTradeStatus.value: actually_post_trade_status,
             JavaApiFields.DoneForDay.value: actually_done_for_day},
            'Comparing expected and actually results (step 3)')
        # endregion

        # region check that execution doesn`t have Agent Fee (step 4)
        misc_fee_rate = '5'
        execution_report[JavaApiFields.MiscFeesList.value][JavaApiFields.MiscFeesBlock.value][0][
            JavaApiFields.MiscFeeAmt.value] = str(round(float(
            execution_report[JavaApiFields.MiscFeesList.value][JavaApiFields.MiscFeesBlock.value][0][
                JavaApiFields.MiscFeeAmt.value]), 4))
        misc_fee_amount = float(misc_fee_rate) * float(self.qty) * float(self.price) / 10000
        self.java_api_manager.compare_values(
            {JavaApiFields.MiscFeeType.value: AllocationInstructionConst.COMM_AND_FEES_TYPE_AGE.value,
             JavaApiFields.MiscFeeBasis.value: AllocationInstructionConst.COMM_AND_FEES_BASIS_P.value,
             JavaApiFields.MiscFeeCurr.value: self.currency_post_trade,
             JavaApiFields.MiscFeeRate.value: str(float(misc_fee_rate)),
             JavaApiFields.MiscFeeAmt.value: str(misc_fee_amount)
             }, execution_report[JavaApiFields.MiscFeesList.value][JavaApiFields.MiscFeesBlock.value][0],
            'Check that Agent fee presents in Execution Report (step 4)')
        # endregion

        # region step 5

        # send ComputeBookingCommmissionFeesRequest (part of step 5)
        avg_px = str(float(self.price) / 100)
        self.compute_booking_fee_commission_request.set_list_of_exec_alloc_block(self.qty, exec_id, self.price,
                                                                                 actually_post_trade_status)
        self.compute_booking_fee_commission_request.set_list_of_order_alloc_block(cl_ord_id, order_id,
                                                                                  actually_post_trade_status)
        self.compute_booking_fee_commission_request.set_default_compute_booking_request(self.qty, avg_px)
        responses = self.java_api_manager.send_message_and_receive_response(self.compute_booking_fee_commission_request)
        print_message("send ComputeBookingCommissionFeesRequest (part of step 5)", responses)
        compute_booking_misc_fee_response = self.java_api_manager.get_last_message(
            ORSMessageType.ComputeBookingFeesCommissionsReply.value).get_parameters()[JavaApiFields.ComputeBookingFeesCommissionsReplyBlock.value]
        self.java_api_manager.key_is_absent(JavaApiFields.RootMiscFeesList.value, compute_booking_misc_fee_response,
                                            'Check that ComputeMiscFeeCommissionReply doesn`t have Agent Fees')
        # the end

        # book CO order (part of step 5)
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
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        self.java_api_manager.key_is_absent(JavaApiFields.RootMiscFeesList.value, allocation_report,
                                            'Check that Block doesn`t has Agent Fees')
        alloc_id = allocation_report[JavaApiFields.ClientAllocID.value]
        alloc_instruction_id = allocation_report[JavaApiFields.AllocInstructionID.value]
        # the end

        # endregion

        # region step 6

        # approve block (part of step 6)
        self.approve_block.set_default_approve(alloc_id=alloc_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.approve_block)
        print_message('Approve block (part of step 6)', responses)
        # the end

        # allocate block (part of step 6)
        self.confirmation_request.set_default_allocation(alloc_id)
        self.confirmation_request.update_fields_in_component("ConfirmationBlock", {
            "AllocAccountID": self.alloc_account,
            "InstrID": instrument_id,
            "AllocQty": self.qty,
            "AvgPx": avg_px})
        responses = self.java_api_manager.send_message_and_receive_response(self.confirmation_request)
        print_message(f' Allocate block step 6', responses)
        confirmation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ConfirmationReport.value).get_parameters()[
                JavaApiFields.ConfirmationReportBlock.value]
        self.java_api_manager.key_is_absent(JavaApiFields.MiscFeesList.value, confirmation_report,
                                            'Check that Agent Fees is absent for allocation')
        # the end

        # endregion

        # region unallocate block (step 7)
        self.unallocate_message.set_default(alloc_instruction_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.unallocate_message)
        print_message("Unallocate block ", responses)
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        confirmation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ConfirmationReport.value).get_parameters()[
                JavaApiFields.ConfirmationReportBlock.value]
        self.java_api_manager.key_is_absent(JavaApiFields.AllocSummaryStatus.value, allocation_report,
                                            'Check that SummaryStatus of block  is empty (step 7)')
        confirmation_status = confirmation_report[JavaApiFields.ConfirmStatus.value]
        confirmation_match_status = confirmation_report[JavaApiFields.MatchStatus.value]
        self.java_api_manager.compare_values({
            JavaApiFields.ConfirmStatus.value: ConfirmationReportConst.ConfirmStatus_CXL.value,
            JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_UNM.value}, {
            JavaApiFields.ConfirmStatus.value: confirmation_status,
            JavaApiFields.MatchStatus.value: confirmation_match_status
        }, 'Check expected and actually results from step 7')
        # endregion

        # region step 8
        # check that execution report doesn`t have Agent fee(part of step 8)
        params_of_execution_report_message = {
            "ExecType": "B",
            "OrdStatus": "B",
            "ClOrdID": cl_ord_id,
            'NoMiscFees': [
                {'MiscFeeAmt': str(round(misc_fee_amount, 4)),
                 'MiscFeeCurr': self.currency_post_trade,
                 'MiscFeeType': '12'}]
        }
        list_of_ignored_fields = ['Account', 'ExecID', 'OrderQtyData', 'LastQty', 'OrderID',
                                  'TransactTime', 'Side', 'AvgPx', 'QuodTradeQualifier', 'BookID',
                                  'SettlDate', 'TimeInForce', 'Currency', 'PositionEffect',
                                  'TradeDate', 'HandlInst', 'LeavesQty', 'CumQty', 'LastPx',
                                  'OrdType', 'tag5120', 'LastMkt', 'OrderCapacity',
                                  'QtyType', 'ExecBroker', 'Price', 'VenueType',
                                  'Instrument', 'NoParty', 'ExDestination', 'GrossTradeAmt',
                                  'AllocInstructionMiscBlock2',
                                  'OrderAvgPx', 'CommissionData', 'GatingRuleName', 'GatingRuleCondName']
        fix_execution_report = FixMessageExecutionReportOMS(self.data_set, params_of_execution_report_message)
        self.fix_verifier.check_fix_message_fix_standard(fix_execution_report, ignored_fields=list_of_ignored_fields)

        # the end

        # check that 35 = J (625 = 5) message does not have Agent Fee (part of step 8)
        list_of_ignored_fields.extend(['RootSettlCurrFxRateCalc', 'AllocID', 'NetMoney', 'TradeDate',
                                       'BookingType', 'RootSettlCurrency', 'AllocInstructionMiscBlock1',
                                       'Quantity', 'AllocTransType', 'RootSettlCurrFxRate', 'RootSettlCurrAmt',
                                       'GrossTradeAmt', 'AllocSettlCurrAmt', 'AllocSettlCurrency',
                                       'SettlCurrAmt', 'SettlCurrFxRate', 'SettlCurrFxRateCalc', 'ReportedPx'])
        params_of_allocation = {'NoOrders': [{
            'ClOrdID': cl_ord_id,
            'OrderID': order_id,
        }],
            'RootNoMiscFees': '#',
            'AllocType': '5',
            'NoMiscFees': '#'
        }
        fix_allocation_report = FixMessageAllocationInstructionReportOMS(params_of_allocation)
        self.fix_verifier.check_fix_message_fix_standard(fix_allocation_report, ignored_fields=list_of_ignored_fields)
        # the end

        # check that 35 = J (625 = 2) message does not have Agent Fee (part of step 8)
        fix_allocation_report.change_parameters({'AllocType': '2',
                                                 'NoAllocs': [{'AllocAccount': self.alloc_account,
                                                               'AllocQty': self.qty,
                                                               'IndividualAllocID': '*',
                                                               'AllocNetPrice': '*',
                                                               'AllocPrice': '*',
                                                               'AllocInstructionMiscBlock2': '*',
                                                               'NoMiscFees': '#'
                                                               }]
                                                 })
        self.fix_verifier.check_fix_message_fix_standard(fix_allocation_report, ignored_fields=list_of_ignored_fields)
        # endregion

        # check that 35 = AK messages (part of step 8)
        list_of_ignored_fields.extend(['ConfirmType', 'MatchStatus', 'ConfirmStatus',
                                       'CpctyConfGrp', 'ConfirmID', 'ConfirmTransType', 'AllocAccount', 'AllocQty',
                                       'OrderAvgPx', 'tag11245'])
        params_of_allocation.pop('AllocType')
        params_of_allocation.update({'ConfirmTransType': "0"})
        fix_confirmation = FixMessageConfirmationReportOMS(self.data_set, params_of_allocation)
        self.fix_verifier.check_fix_message_fix_standard(fix_confirmation, ignored_fields=list_of_ignored_fields)
        fix_confirmation.change_parameters({'ConfirmTransType': '2'})
        self.fix_verifier.check_fix_message_fix_standard(fix_confirmation, ignored_fields=list_of_ignored_fields)
        # the end

        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_commission_sender.clear_fees()
        self.ssh_client.send_command('~/quod/script/site_scripts/change_book_agent_misc_fee_type_on_N')
        self.ssh_client.send_command("qrestart QUOD.ORS QUOD.CS QUOD.ESBUYTH2TEST")
        time.sleep(80)
        self.ssh_client.close()
