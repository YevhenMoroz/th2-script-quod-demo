import logging
import time
from copy import deepcopy
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, ExecutionReportConst, OrderReplyConst,\
    AllocationInstructionConst
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ComputeBookingFeesCommissionsRequestOMS import \
    ComputeBookingFeesCommissionsRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import \
    ForceAllocInstructionStatusRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
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


class QAP_T8328(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.bs_connectivity = self.fix_env.buy_side
        self.ss_connectivity = self.fix_env.sell_side
        self.qty = '8328'
        self.price = '10'
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.currency = self.data_set.get_currency_by_name('currency_3')
        self.currency_post_trade = self.data_set.get_currency_by_name('currency_2')
        self.venue_mic = self.data_set.get_mic_by_name('mic_2')
        self.client = self.data_set.get_client('client_com_1')
        self.alloc_account = self.data_set.get_account_by_name('client_com_1_acc_1')
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.fix_verifier = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.ssh_client_env = self.environment.get_list_ssh_client_environment()[0]
        self.ssh_client = SshClient(self.ssh_client_env.host, self.ssh_client_env.port, self.ssh_client_env.user,
                                    self.ssh_client_env.password, self.ssh_client_env.su_user,
                                    self.ssh_client_env.su_password)
        self.order_submit = OrderSubmitOMS(self.data_set)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.trade_entry = TradeEntryOMS(self.data_set)
        self.complete_request = DFDManagementBatchOMS(self.data_set)
        self.compute_booking_fee_commission_request = ComputeBookingFeesCommissionsRequestOMS(self.data_set)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.approve_block = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.confirmation_request = ConfirmationOMS(self.data_set)
        self.execution_report = ExecutionReportOMS(self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region set agent fees precondition
        agent_fee_type = self.data_set.get_misc_fee_type_by_name('agent')
        commission_profile = self.data_set.get_comm_profile_by_name('perc_amt')
        fee = self.data_set.get_fee_by_name('fee3')
        instr_type = self.data_set.get_instr_type('equity')
        venue_id = self.data_set.get_venue_id('eurex')
        self.rest_commission_sender.clear_fees()
        on_calculated_exec_scope = self.data_set.get_fee_exec_scope_by_name('all_exec')
        self.rest_commission_sender.set_modify_fees_message(fee_type=agent_fee_type, comm_profile=commission_profile,
                                                            fee=fee)
        self.rest_commission_sender.change_message_params(
            {'commExecScope': on_calculated_exec_scope, 'instrType': instr_type, "venueID": venue_id})
        self.rest_commission_sender.send_post_request()
        instrument_id = self.data_set.get_instrument_id_by_name("instrument_3")
        # endregion

        # region set up configuration on BackEnd(precondition)
        self.ssh_client.send_command('~/quod/script/site_scripts/change_book_agent_misk_fee_type_on_Y')
        self.ssh_client.send_command("qrestart QUOD.ORS QUOD.CS QUOD.ESBUYTH2TEST")
        time.sleep(120)
        # endregion

        # region create DMA order  step 1
        self.order_submit.set_default_dma_limit()
        self.order_submit.update_fields_in_component('NewOrderSingleBlock', {
            'ListingList': {'ListingBlock': [{'ListingID': self.data_set.get_listing_id_by_name("listing_2")}]},
            'InstrID': self.data_set.get_instrument_id_by_name("instrument_3"),
            'AccountGroupID': self.client,
            'OrdQty': self.qty,
            'Price': self.price,
            "ClOrdID": bca.client_orderid(9) + Path(__file__).name[:-3],
        })
        responses = self.java_api_manager.send_message_and_receive_response(self.order_submit)
        print_message('Create DMA  order', responses)
        order_id = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value][JavaApiFields.OrdID.value]
        cl_ord_id = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value][JavaApiFields.ClOrdID.value]
        # endregion

        # region fully trade DMA order (step 2)
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
                                                             "LeavesQty": 0,
                                                             "CumQty": self.qty,
                                                             "AvgPrice": self.price,
                                                             "LastMkt": self.venue_mic,
                                                             "OrdQty": self.qty
                                                         })
        responses = self.java_api_manager.send_message_and_receive_response(self.execution_report)
        print_message("Trade DMA order (step 2)", responses)
        misc_fee_rate = 5
        amount_of_fees = misc_fee_rate / 100 * int(self.qty) * int(self.price) / 100
        execution_report = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                                  ExecutionReportConst.ExecType_TRD.value).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value]
        exec_id = execution_report[JavaApiFields.ExecID.value]
        actually_result = execution_report[JavaApiFields.MiscFeesList.value][JavaApiFields.MiscFeesBlock.value][0]
        expected_result = {JavaApiFields.MiscFeeRate.value: str(float(misc_fee_rate)),
                           JavaApiFields.MiscFeeBasis.value: AllocationInstructionConst.COMM_AND_FEES_BASIS_P.value,
                           JavaApiFields.MiscFeeCurr.value: self.currency_post_trade,
                           JavaApiFields.MiscFeeType.value: AllocationInstructionConst.COMM_AND_FEES_TYPE_AGE.value,
                           JavaApiFields.MiscFeeAmt.value: str(round(amount_of_fees, 3))}
        self.java_api_manager.compare_values(expected_result, actually_result,
                                             'Checking results from step 2')
        # endregion

        # region step 3
        new_avg_px = str(float(self.price) / 100)
        post_trade_status = OrderReplyConst.PostTradeStatus_RDY.value
        self.compute_booking_fee_commission_request.set_list_of_order_alloc_block(cl_ord_id, order_id,
                                                                                  post_trade_status)
        self.compute_booking_fee_commission_request.set_list_of_exec_alloc_block(self.qty, exec_id, self.price,
                                                                                 post_trade_status)
        self.compute_booking_fee_commission_request.set_default_compute_booking_request(self.qty, new_avg_px,
                                                                                        self.client)
        responses = self.java_api_manager.send_message_and_receive_response(self.compute_booking_fee_commission_request)
        print_message('Send ComputeBookingFeesCommissionsRequest  step 3', responses)
        compute_reply = self.java_api_manager.get_last_message(
            ORSMessageType.ComputeBookingFeesCommissionsReply.value).get_parameters()[
            JavaApiFields.ComputeBookingFeesCommissionsReplyBlock.value]
        agent_fee_on_compute_booking_fee_commission_reply = compute_reply[JavaApiFields.RootMiscFeesList.value]
        expected_result.clear()
        expected_result = {JavaApiFields.RootMiscFeeRate.value: str(round(amount_of_fees, 3)),
                           JavaApiFields.RootMiscFeeBasis.value: AllocationInstructionConst.COMM_AND_FEES_BASIS_A.value,
                           JavaApiFields.RootMiscFeeCurr.value: self.currency_post_trade,
                           JavaApiFields.RootMiscFeeType.value: AllocationInstructionConst.COMM_AND_FEES_TYPE_AGE.value,
                           JavaApiFields.RootMiscFeeAmt.value: str(round(amount_of_fees, 3))}
        actually_result = agent_fee_on_compute_booking_fee_commission_reply[JavaApiFields.RootMiscFeesBlock.value][0]
        self.java_api_manager.compare_values(expected_result, actually_result,
                                             'Check agent fee on ComputeBookingFeesCommissionsReply. Part of step 3')

        gross_currency_amt = str(float(self.qty) * float(new_avg_px))
        self.allocation_instruction.set_default_book(order_id)
        self.allocation_instruction.update_fields_in_component('AllocationInstructionBlock',
                                                               {
                                                                   'GrossTradeAmt': gross_currency_amt,
                                                                   'AvgPx': new_avg_px,
                                                                   'Qty': self.qty,
                                                                   'AccountGroupID': self.client,
                                                                   'Currency': self.currency_post_trade,
                                                                   "InstrID": instrument_id,
                                                                   JavaApiFields.RootMiscFeesList.value: agent_fee_on_compute_booking_fee_commission_reply,
                                                                   'ExecAllocList': {
                                                                       'ExecAllocBlock': [{'ExecQty': self.qty,
                                                                                           'ExecID': exec_id,
                                                                                           'ExecPrice': self.price},
                                                                                          ]},
                                                               })
        responses = self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        print_message("Allocation Instruction", responses)
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value, JavaApiFields.BookingAllocInstructionID.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        alloc_id = deepcopy(allocation_report[JavaApiFields.ClientAllocID.value])
        actually_result = \
        allocation_report[JavaApiFields.RootMiscFeesList.value][JavaApiFields.RootMiscFeesBlock.value][0]
        self.java_api_manager.compare_values(expected_result, actually_result,
                                             'Check that block has agent fee. Part of step 4')
        # endregion

        # region step 5-6
        self.approve_block.set_default_approve(alloc_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.approve_block)
        print_message('Approve Block. Part of step 4', responses)

        self.confirmation_request.set_default_allocation(alloc_id)
        self.confirmation_request.update_fields_in_component("ConfirmationBlock", {
            "AllocAccountID": self.alloc_account,
            "InstrID": instrument_id,
            "AllocQty": self.qty,
            "AvgPx": new_avg_px})
        responses = self.java_api_manager.send_message_and_receive_response(self.confirmation_request)
        print_message('Allocate block step 5', responses)
        confirmation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ConfirmationReport.value).get_parameters()[
                JavaApiFields.ConfirmationReportBlock.value]
        expected_result.clear()
        expected_result = {JavaApiFields.MiscFeeRate.value: str(round(amount_of_fees, 3)),
                           JavaApiFields.MiscFeeBasis.value: AllocationInstructionConst.COMM_AND_FEES_BASIS_A.value,
                           JavaApiFields.MiscFeeCurr.value: self.currency_post_trade,
                           JavaApiFields.MiscFeeType.value: AllocationInstructionConst.COMM_AND_FEES_TYPE_AGE.value,
                           JavaApiFields.MiscFeeAmt.value: str(round(amount_of_fees, 3))}
        actually_result = \
        confirmation_report[JavaApiFields.MiscFeesList.value][JavaApiFields.MiscFeesBlock.value][0]
        self.java_api_manager.compare_values(expected_result, actually_result,
                                             "Check that confirmation report has agent fee. Part of step 6")

        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.ssh_client.send_command('~/quod/script/site_scripts/change_book_agent_misc_fee_type_on_N')
        self.ssh_client.send_command("qrestart QUOD.ORS QUOD.CS QUOD.ESBUYTH2TEST")
        time.sleep(80)
        self.rest_commission_sender.clear_fees()
        self.ssh_client.close()
