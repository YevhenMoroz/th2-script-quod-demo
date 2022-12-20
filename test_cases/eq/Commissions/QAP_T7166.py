import logging
import time
from datetime import datetime
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from custom.verifier import VerificationMethod
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.data_sets.oms_data_set.oms_const_enum import (
    OMSFee,
    OMSCommission,
    OmsVenues,
    OMSFeeType,
    OMSVenueID,
)
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields,\
    OrderReplyConst, AllocationReportConst, ConfirmationReportConst
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ComputeBookingFeesCommissionsRequestOMS import \
    ComputeBookingFeesCommissionsRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import \
    ForceAllocInstructionStatusRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


def print_message(message, responses):
    logger.info(message)
    for i in responses:
        logger.info(i)
        logger.info(i.get_parameters())


class QAP_T7166(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.qty = "100"
        self.price = "10"
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.venue_client_names = self.data_set.get_venue_client_names_by_name(
            "client_com_1_venue_2"
        )  # CLIENT_COMM_1_EUREX
        self.venue = self.data_set.get_mic_by_name("mic_2")  # EUREX
        self.currency_post_trade = self.data_set.get_currency_by_name('currency_2')
        self.client = self.data_set.get_client("client_com_1")  # CLIENT_COMM_1
        self.alloc_account = self.data_set.get_account_by_name("client_com_1_acc_1")  # CLIENT_COMM_1_SA1
        self.perc_amt = self.data_set.get_comm_profile_by_name("perc_amt")
        self.commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.submit_order = OrderSubmitOMS(self.data_set)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.compute_booking_fee_commission_request = ComputeBookingFeesCommissionsRequestOMS(self.data_set)
        self.confirmation_request = ConfirmationOMS(self.data_set)
        self.approve_block = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.complete_request = DFDManagementBatchOMS(self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Send commission and fees
        # Commissions
        self.commission_sender.clear_commissions()
        self.commission_sender.clear_fees()
        self.commission_sender.set_modify_client_commission_message(
            client=self.client, comm_profile=self.perc_amt, commission=OMSCommission.commission1
        )
        self.commission_sender.change_message_params(
            {"venueID": OmsVenues.venue_2.value, "commissionAmountType": "BRK"}
        )
        self.commission_sender.send_post_request()

        # Fees
        self.commission_sender.set_modify_fees_message(
            comm_profile=self.perc_amt, fee=OMSFee.fee1, fee_type=OMSFeeType.stamp.value
        )
        self.commission_sender.change_message_params({"venueID": OMSVenueID.eurex.value})
        self.commission_sender.send_post_request()
        # endregion

        # region Create CO order via FIX with automatic auto-accept ( part precondition)
        self.fix_message.set_default_care_limit(instr="instrument_3")
        self.fix_message.change_parameters(
            {
                "Side": "1",
                "OrderQtyData": {"OrderQty": self.qty},
                "Account": self.client,
                "ExDestination": self.venue,
                "Currency": self.data_set.get_currency_by_name("currency_3"),  # GBp
                "Price": self.price,
            }
        )
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)

        # get Client Order ID and Order ID
        cl_ord_id: str = response[0].get_parameters()["ClOrdID"]
        order_id: str = response[0].get_parameters()["OrderID"]
        # endregion

        # region step 1-2 - Split CO order and execute DMA order
        try:
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(
                self.bs_connectivity, self.venue_client_names, self.venue, float(self.price), int(self.qty), 0
            )
            self.submit_order.set_default_child_dma(order_id, cl_ord_id)
            self.submit_order.update_fields_in_component('NewOrderSingleBlock', {'AccountGroupID': self.client,
                                                                                 'ListingList': {'ListingBlock': [
                                                                                     {
                                                                                         'ListingID': self.data_set.get_listing_id_by_name(
                                                                                             "listing_2")}]},
                                                                                 'InstrID': self.data_set.get_instrument_id_by_name(
                                                                                     "instrument_3"),
                                                                                 'Price': self.price
                                                                                 })
            responses = self.java_api_manager.send_message_and_receive_response(self.submit_order)
            print_message('Split DMA order', responses)
        except Exception:
            logger.error("Error execution", exc_info=True)
        finally:
            time.sleep(3)
            self.rule_manager.remove_rule(trade_rule)
        # endregion

        # region step 3 - Checking Fees for EX Execution
        rate_of_fees_and_commission = '5.0'
        commission_amount = str(float(rate_of_fees_and_commission) / 10000 * float(self.price) * float(self.qty))
        execution_report_dma = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                                      filter_value='EX').get_parameters()[
            JavaApiFields.ExecutionReportBlock.value]
        fees_expected = {JavaApiFields.MiscFeeAmt.value: commission_amount,
                         JavaApiFields.MiscFeeRate.value: rate_of_fees_and_commission,
                         JavaApiFields.MiscFeeCurr.value: self.currency_post_trade}
        self.java_api_manager.compare_values(fees_expected,
                                             execution_report_dma[JavaApiFields.MiscFeesList.value][
                                                 JavaApiFields.MiscFeesBlock.value][0],
                                             'Check expected and actually fee for EX execution (part of step 3)',
                                             VerificationMethod.EQUALS)
        # endregion

        # region step 3 - Checking Commissions and Fees for EV Execution
        execution_report_care = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                                       filter_value='EV').get_parameters()[
            JavaApiFields.ExecutionReportBlock.value]
        exec_id = execution_report_care[JavaApiFields.ExecID.value]
        client_commission_expected = {JavaApiFields.CommissionAmount.value: commission_amount,
                                      JavaApiFields.CommissionRate.value: rate_of_fees_and_commission,
                                      JavaApiFields.CommissionCurrency.value: self.currency_post_trade}
        self.java_api_manager.compare_values(client_commission_expected,
                                             execution_report_care[JavaApiFields.ClientCommissionList.value][
                                                 JavaApiFields.ClientCommissionBlock.value][0],
                                             'Check expected and actually commission for EV execution (part of step 3)')
        self.java_api_manager.compare_values(fees_expected,
                                             execution_report_care[JavaApiFields.MiscFeesList.value][
                                                 JavaApiFields.MiscFeesBlock.value][0],
                                             'Check expected and actually fee for EV execution (part of step 3)')

        # endregion

        # region step 4 - check DayCumAmt and DayCumQty
        day_cum_amt_expected = str(float(self.price) * float(self.qty))
        self.java_api_manager.compare_values({JavaApiFields.DayCumAmt.value: day_cum_amt_expected,
                                              JavaApiFields.DayCumQty.value: str(float(self.qty))},
                                             {JavaApiFields.DayCumAmt.value: execution_report_care[
                                                 JavaApiFields.DayCumAmt.value],
                                              JavaApiFields.DayCumQty.value: execution_report_care[
                                                  JavaApiFields.DayCumQty.value
                                              ]},
                                             'Check expected and actually result from step 4')
        # endregion

        # region step 5 - Complete CO order
        self.complete_request.set_default_complete(order_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.complete_request)
        print_message("Completing CO order", responses)
        post_trade_status = OrderReplyConst.PostTradeStatus_RDY.value
        done_for_day = OrderReplyConst.DoneForDay_YES.value
        order_reply = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value]
        self.java_api_manager.compare_values({JavaApiFields.PostTradeStatus.value: post_trade_status,
                                              JavaApiFields.DoneForDay.value: done_for_day},
                                             order_reply, 'Check expected and actually result from step 5',
                                             VerificationMethod.EQUALS)
        # endregion

        # region step 6 (check that calculated execution)
        execution_report_care = \
            self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
        client_commission_expected.update({JavaApiFields.CommissionRate.value: commission_amount})
        self.java_api_manager.compare_values(client_commission_expected,
                                             execution_report_care[JavaApiFields.ClientCommissionList.value][
                                                 JavaApiFields.ClientCommissionBlock.value][0],
                                             'Check expected and actually commission for EV execution (part of step 6)',
                                             VerificationMethod.EQUALS)
        self.java_api_manager.compare_values(fees_expected,
                                             execution_report_care[JavaApiFields.MiscFeesList.value][
                                                 JavaApiFields.MiscFeesBlock.value][0],
                                             'Check expected and actually fee for EV Calculated execution (step 6)',
                                             VerificationMethod.EQUALS)
        # endregion

        # region step 7
        self.compute_booking_fee_commission_request.set_list_of_order_alloc_block(cl_ord_id, order_id,
                                                                                  OrderReplyConst.PostTradeStatus_RDY.value)
        self.compute_booking_fee_commission_request.set_list_of_exec_alloc_block(self.qty, exec_id, self.price,
                                                                                 OrderReplyConst.PostTradeStatus_RDY.value)
        self.compute_booking_fee_commission_request.set_default_compute_booking_request(self.qty)
        new_avg_px = str(int(self.price) / 100)
        self.compute_booking_fee_commission_request.update_fields_in_component(
            'ComputeBookingFeesCommissionsRequestBlock', {'AvgPx': new_avg_px, 'AccountGroupID': self.client})
        responses = self.java_api_manager.send_message_and_receive_response(self.compute_booking_fee_commission_request)
        print_message('Send ComputeBookingFeesCommissionsRequest', responses)
        compute_booking_fees_commission_reply = self.java_api_manager.get_last_message(
            ORSMessageType.ComputeBookingFeesCommissionsReply.value).get_parameters()[
            JavaApiFields.ComputeBookingFeesCommissionsReplyBlock.value]
        client_commission_expected.update({JavaApiFields.CommissionRate.value: rate_of_fees_and_commission})
        self.java_api_manager.compare_values(client_commission_expected, compute_booking_fees_commission_reply[
            JavaApiFields.ClientCommissionList.value][JavaApiFields.ClientCommissionBlock.value][0],
                                             'Check expected and actually result for client commission (part of step 7)')
        root_fee_expected = {JavaApiFields.RootMiscFeeAmt.value: commission_amount,
                             JavaApiFields.RootMiscFeeRate.value: rate_of_fees_and_commission,
                             JavaApiFields.RootMiscFeeCurr.value: self.currency_post_trade}
        self.java_api_manager.compare_values(root_fee_expected, compute_booking_fees_commission_reply[
            JavaApiFields.RootMiscFeesList.value][JavaApiFields.RootMiscFeesBlock.value][0],
                                             'Check expected and actually result for fee (part of step 7)')
        # endregion

        # region step 8
        root_misc_fees = compute_booking_fees_commission_reply[JavaApiFields.RootMiscFeesList.value]
        client_commission = compute_booking_fees_commission_reply[JavaApiFields.ClientCommissionList.value]
        instrument_id = self.data_set.get_instrument_id_by_name("instrument_3")
        gross_currency_amt = str(float(self.qty) * float(new_avg_px))
        self.allocation_instruction.set_default_book(order_id)
        self.allocation_instruction.update_fields_in_component('AllocationInstructionBlock',
                                                               {
                                                                   'GrossTradeAmt': gross_currency_amt,
                                                                   'AvgPx': self.price,
                                                                   'Qty': self.qty,
                                                                   'AccountGroupID': self.client,
                                                                   'Currency': self.currency_post_trade,
                                                                   "InstrID": instrument_id,
                                                                   'RootCommissionDataBlock': {
                                                                       'RootCommission': commission_amount,
                                                                       'RootCommType': 'A',
                                                                       'RootCommCurrency': self.currency_post_trade
                                                                   },
                                                                   JavaApiFields.RootMiscFeesList.value: root_misc_fees,
                                                                   JavaApiFields.ClientCommissionList.value: client_commission,
                                                                   'ExecAllocList': {
                                                                       'ExecAllocBlock': [{'ExecQty': self.qty,
                                                                                           'ExecID': exec_id,
                                                                                           'ExecPrice': self.price}]},

                                                               })
        responses = self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        print_message('Create Block', responses)
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        alloc_id = allocation_report[JavaApiFields.ClientAllocID.value]
        expected_result_for_block = {
            JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_APP.value,
            JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_UNM.value,
        }
        self.java_api_manager.compare_values(expected_result_for_block, allocation_report,
                                             'Check Status and MatchStatus (part of step 8)',
                                             VerificationMethod.EQUALS)
        self.java_api_manager.compare_values(root_fee_expected, allocation_report[JavaApiFields.RootMiscFeesList.value][
            JavaApiFields.RootMiscFeesBlock.value][0], 'Check that block has correctly fee (part of step 8)')
        self.java_api_manager.compare_values(client_commission_expected,
                                             allocation_report[JavaApiFields.ClientCommissionList.value][
                                                 JavaApiFields.ClientCommissionBlock.value][0],
                                             'Check that block has correctly client commission (part of step 8)')
        # endregion

        # region step 9 - Approve Block
        self.approve_block.set_default_approve(alloc_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.approve_block)
        print_message("Approve block", responses)
        allocation_report = self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[JavaApiFields.AllocationReportBlock.value]
        expected_result_for_block.update({JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_ACK.value,
                                          JavaApiFields.MatchStatus.value: AllocationReportConst.MatchStatus_MAT.value})
        self.java_api_manager.compare_values(expected_result_for_block, allocation_report,
                                             'Check Status and MatchStatus (step 9)',
                                             VerificationMethod.EQUALS)
        # endregion

        # region step 10 - Allocate block
        self.confirmation_request.set_default_allocation(alloc_id)
        self.confirmation_request.update_fields_in_component('ConfirmationBlock', {
            "AllocAccountID": self.alloc_account,
            'AllocQty': self.qty,
            'AvgPx': new_avg_px,
            "InstrID": instrument_id
        })
        responses = self.java_api_manager.send_message_and_receive_response(self.confirmation_request)
        print_message('Allocate block', responses)
        confirmation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ConfirmationReport.value).get_parameters()[
                JavaApiFields.ConfirmationReportBlock.value]
        self.java_api_manager.compare_values(client_commission_expected, confirmation_report[JavaApiFields.ClientCommissionList.value][JavaApiFields.ClientCommissionBlock.value][0],
                                             'Check client commission (part of step 10)', VerificationMethod.EQUALS)

        self.java_api_manager.compare_values(fees_expected, confirmation_report[JavaApiFields.MiscFeesList.value][JavaApiFields.MiscFeesBlock.value][0],
                                             'Check fee (part of step 10)', VerificationMethod.EQUALS)
        expected__statuses_for_confirmation = {
            JavaApiFields.ConfirmStatus.value: ConfirmationReportConst.ConfirmStatus_AFF.value,
            JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_MAT.value}
        self.java_api_manager.compare_values(expected__statuses_for_confirmation, confirmation_report,
                                             'Check ConfirmStatus and MatchStatus (part of step 10)',
                                             VerificationMethod.EQUALS)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.commission_sender.clear_commissions()
        self.commission_sender.clear_fees()

        logger.info(f"Case {self.test_id} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
