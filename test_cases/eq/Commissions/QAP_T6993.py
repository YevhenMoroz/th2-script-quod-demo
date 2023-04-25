import logging
from copy import deepcopy
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageAllocationInstructionReportOMS import \
    FixMessageAllocationInstructionReportOMS
from test_framework.fix_wrappers.oms.FixMessageConfirmationReportOMS import FixMessageConfirmationReportOMS
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, ExecutionReportConst, OrderReplyConst, \
    AllocationReportConst, ConfirmationReportConst, AllocationInstructionConst
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

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()


def print_message(message, responses):
    logger.info(message)
    for i in responses:
        logger.info(i)
        logger.info(i.get_parameters())


class QAP_T6993(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.bs_connectivity = self.fix_env.buy_side
        self.ss_connectivity = self.fix_env.sell_side
        self.qty = '6993'
        self.price = '10'
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.currency = self.data_set.get_currency_by_name('currency_3')
        self.currency_post_trade = self.data_set.get_currency_by_name('currency_2')
        self.venue_mic = self.data_set.get_mic_by_name('mic_2')
        self.client = self.data_set.get_client('client_com_1')
        self.alloc_account = self.data_set.get_account_by_name('client_com_1_acc_1')
        self.alloc_account_2 = self.data_set.get_account_by_name('client_com_1_acc_2')
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.fix_verifier = FixVerifier(self.fix_env.drop_copy, self.test_id)
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
        on_calculated_exec_scope = self.data_set.get_fee_exec_scope_by_name('on_calculated')
        self.rest_commission_sender.set_modify_fees_message(fee_type=agent_fee_type, comm_profile=commission_profile,
                                                            fee=fee)
        self.rest_commission_sender.change_message_params(
            {'commExecScope': on_calculated_exec_scope, 'instrType': instr_type, "venueID": venue_id})
        self.rest_commission_sender.send_post_request()
        instrument_id = self.data_set.get_instrument_id_by_name("instrument_3")
        # endregion

        # region create DMA order  precondition
        self.order_submit.set_default_dma_limit()
        self.order_submit.update_fields_in_component('NewOrderSingleBlock', {
            'ListingList': {'ListingBlock': [{'ListingID': self.data_set.get_listing_id_by_name("listing_2")}]},
            'InstrID': self.data_set.get_instrument_id_by_name("instrument_3"),
            'AccountGroupID': self.client,
            'OrdQty': self.qty,
            'Price': self.price,
        })
        responses = self.java_api_manager.send_message_and_receive_response(self.order_submit)
        print_message('Create DMA  order', responses)
        order_id = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value][JavaApiFields.OrdID.value]
        cl_ord_id = self.java_api_manager.get_last_message(ORSMessageType.OrdReply.value).get_parameters()[
            JavaApiFields.OrdReplyBlock.value][JavaApiFields.ClOrdID.value]
        # endregion

        # region partially trade DMA order (step 1)
        self.execution_report.set_default_trade(order_id)
        half_qty = int(int(self.qty) / 2)
        list_of_qty = [half_qty, str(int(self.qty) - half_qty)]
        self.execution_report.update_fields_in_component('ExecutionReportBlock',
                                                         {
                                                             "InstrumentBlock": self.data_set.get_java_api_instrument(
                                                                 "instrument_2"),
                                                             "Side": "Buy",
                                                             "LastTradedQty": half_qty,
                                                             "LastPx": self.price,
                                                             "OrdType": "Limit",
                                                             "Price": self.price,
                                                             "Currency": self.currency,
                                                             "ExecType": "Trade",
                                                             "TimeInForce": "Day",
                                                             "LeavesQty": half_qty,
                                                             "CumQty": half_qty,
                                                             "AvgPrice": self.price,
                                                             "LastMkt": self.venue_mic,
                                                             "OrdQty": self.qty
                                                         })
        responses = self.java_api_manager.send_message_and_receive_response(self.execution_report)
        print_message('Trade DMA  order (Partially filled)', responses)
        execution_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
        exec_id_first = execution_report[JavaApiFields.ExecID.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_PFL.value}, execution_report,
            'Compare actually and expected result from step 1')
        # endregion

        # region step 2 (Fully Trade DMA order)
        self.execution_report.update_fields_in_component('ExecutionReportBlock', {
            "LeavesQty": '0',
            "VenueExecID": bca.client_orderid(9),
            "CumQty": list_of_qty[1],
            "LastTradedQty": list_of_qty[1]
        })
        responses = self.java_api_manager.send_message_and_receive_response(self.execution_report)

        print_message('Trade DMA  order (Fully Filled)', responses)
        actually_result = dict()
        execution_report = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                                  ExecutionReportConst.ExecType_TRD.value).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value]
        actually_result.update(
            {JavaApiFields.TransExecStatus.value: execution_report[JavaApiFields.TransExecStatus.value]})
        exec_id_second = execution_report[JavaApiFields.ExecID.value]
        self.java_api_manager.compare_values(
            {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value}, actually_result,
            'Compare actually and expected result Execution from step 2')
        # endregion

        # region step 3
        misc_fee_rate = 5
        amount_of_fees = misc_fee_rate / 100 * int(self.qty) * int(self.price) / 100
        actually_result = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                                 ExecutionReportConst.ExecType_CAL.value).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value][JavaApiFields.MiscFeesList.value][
            JavaApiFields.MiscFeesBlock.value][0]
        expected_result = {JavaApiFields.MiscFeeRate.value: str(float(misc_fee_rate)),
                           JavaApiFields.MiscFeeBasis.value: AllocationInstructionConst.COMM_AND_FEES_BASIS_P.value,
                           JavaApiFields.MiscFeeCurr.value: self.currency_post_trade,
                           JavaApiFields.MiscFeeType.value: AllocationInstructionConst.COMM_AND_FEES_TYPE_AGE.value,
                           JavaApiFields.MiscFeeAmt.value: str(round(amount_of_fees, 3))}
        self.java_api_manager.compare_values(expected_result, actually_result,
                                             'Comparing expected and actually result from step 3')
        # endregion

        # region check 35=8 message step 4
        list_of_ignored_fields = ['Account', 'ExecID', 'OrderQtyData', 'LastQty', 'TransactTime', 'GrossTradeAmt',
                                  'ExDestination','ExecAllocGrp',
                                  'Side', 'AvgPx', 'SettlCurrency', 'SettlDate', 'TimeInForce',
                                  'PositionEffect', 'HandlInst', 'LeavesQty', 'CumQty',
                                  'LastPx', 'OrdType', 'SecondaryOrderID', 'OrderCapacity', 'QtyType',
                                  'Price', 'Instrument', 'BookID', 'QuodTradeQualifier', 'NoParty', 'ExDestination',
                                  'Side', 'GatingRuleCondName', 'GatingRuleName']
        execution_report = FixMessageExecutionReportOMS(self.data_set)
        execution_report.change_parameters({
            'ClOrdID': cl_ord_id,
            'OrderID': order_id,
            "ExecType": "B",
            "OrdStatus": "B"
        })
        execution_report.change_parameters({'Currency': self.currency, 'CommissionData': '*',
                                            'tag5120': '*', 'ExecBroker': '*',
                                            'NoMiscFees': [{
                                                'MiscFeeAmt': str(round(amount_of_fees, 3)),
                                                'MiscFeeCurr': self.currency_post_trade,
                                                'MiscFeeType': '12'
                                            }]})
        self.fix_verifier.check_fix_message_fix_standard(execution_report, ignored_fields=list_of_ignored_fields)
        # endregion

        # region step 5
        new_avg_px = str(float(self.price) / 100)
        post_trade_status = OrderReplyConst.PostTradeStatus_RDY.value
        self.compute_booking_fee_commission_request.set_list_of_order_alloc_block(cl_ord_id, order_id,
                                                                                  post_trade_status)
        self.compute_booking_fee_commission_request.set_list_of_exec_alloc_block(half_qty, exec_id_second, self.price,
                                                                                 post_trade_status)
        self.compute_booking_fee_commission_request.set_list_of_exec_alloc_block(half_qty, exec_id_first, self.price,
                                                                                 post_trade_status)
        self.compute_booking_fee_commission_request.set_default_compute_booking_request(self.qty, new_avg_px,
                                                                                        self.client)
        responses = self.java_api_manager.send_message_and_receive_response(self.compute_booking_fee_commission_request)
        print_message('Send ComputeBookingFeesCommissionsRequest', responses)
        compute_reply = self.java_api_manager.get_last_message(
            ORSMessageType.ComputeBookingFeesCommissionsReply.value).get_parameters()[
            JavaApiFields.ComputeBookingFeesCommissionsReplyBlock.value]
        fee_is_absent = not JavaApiFields.MiscFeesList.value in compute_reply
        self.java_api_manager.compare_values({"AgentFeesIsAbsent": True},
                                             {"AgentFeesIsAbsent": fee_is_absent},
                                             f'Check that Agent fee does not apply to {ORSMessageType.ComputeBookingFeesCommissionsReply.value} (step 5)')
        # endregion

        # region step 6
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
                                                                   'ExecAllocList': {
                                                                       'ExecAllocBlock': [{'ExecQty': self.qty,
                                                                                           'ExecID': exec_id_first,
                                                                                           'ExecPrice': self.price},
                                                                                          {'ExecQty': self.qty,
                                                                                           'ExecID': exec_id_second,
                                                                                           'ExecPrice': self.price}
                                                                                          ]},
                                                               })
        responses = self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        print_message("Allocation Instruction", responses)
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value, JavaApiFields.BookingAllocInstructionID.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        order_update = self.java_api_manager.get_last_message(ORSMessageType.OrdUpdate.value).get_parameters()[
            JavaApiFields.OrdUpdateBlock.value]
        alloc_id = deepcopy(allocation_report[JavaApiFields.ClientAllocID.value])
        expected_result = {
            JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_APP.value,
            JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_UNM.value,
            JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_BKD.value
        }
        actually_result = {JavaApiFields.AllocStatus.value: allocation_report[JavaApiFields.AllocStatus.value],
                           JavaApiFields.MatchStatus.value: allocation_report[JavaApiFields.MatchStatus.value],
                           JavaApiFields.PostTradeStatus.value: order_update[JavaApiFields.PostTradeStatus.value]}
        self.java_api_manager.compare_values(expected_result, actually_result, 'Check expected result for step 6')
        # endregion

        # region step 7
        fee_is_absent = not JavaApiFields.MiscFeesList.value in allocation_report
        self.java_api_manager.compare_values({"AgentFeesIsAbsent": True},
                                             {"AgentFeesIsAbsent": fee_is_absent},
                                             f'Check that Agent fee does not apply to {ORSMessageType.AllocationReport.value} (step 7)')
        # endregion

        # region step 8
        self.approve_block.set_default_approve(alloc_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.approve_block)
        print_message('Approve Block', responses)
        expected_result.update({JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_ACK.value,
                                JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_MAT.value})
        expected_result.pop(JavaApiFields.PostTradeStatus.value)
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value, JavaApiFields.BookingAllocInstructionID.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        actually_result = {JavaApiFields.AllocStatus.value: allocation_report[JavaApiFields.AllocStatus.value],
                           JavaApiFields.MatchStatus.value: allocation_report[JavaApiFields.MatchStatus.value]}
        self.java_api_manager.compare_values(expected_result, actually_result, 'Check expected result from step 8')
        # endregion

        # region step 9
        self.confirmation_request.set_default_allocation(alloc_id)
        list_of_security_accounts = [self.alloc_account, self.alloc_account_2]
        for sec_account in list_of_security_accounts:
            self.confirmation_request.update_fields_in_component("ConfirmationBlock", {
                "AllocAccountID": sec_account,
                "InstrID": instrument_id,
                "AllocQty": list_of_qty[list_of_security_accounts.index(sec_account)],
                "AvgPx": new_avg_px})
            responses = self.java_api_manager.send_message_and_receive_response(self.confirmation_request)
            print_message(f'Create Allocation for {sec_account}', responses)

            confirmation_report = \
                self.java_api_manager.get_last_message(ORSMessageType.ConfirmationReport.value).get_parameters()[
                    JavaApiFields.ConfirmationReportBlock.value]
            expected_result_confirmation = {
                JavaApiFields.ConfirmStatus.value: ConfirmationReportConst.ConfirmStatus_AFF.value,
                JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_MAT.value}
            actually_result = {
                JavaApiFields.ConfirmStatus.value: confirmation_report[JavaApiFields.ConfirmStatus.value],
                JavaApiFields.MatchStatus.value: confirmation_report[JavaApiFields.MatchStatus.value]}
            self.java_api_manager.compare_values(expected_result_confirmation, actually_result,
                                                 f'Check statuses of confirmation of {sec_account} step 9')
            fee_is_absent = not JavaApiFields.MiscFeesList.value in confirmation_report
            self.java_api_manager.compare_values({"AgentFeesIsAbsent": True},
                                                 {"AgentFeesIsAbsent": fee_is_absent},
                                                 f'Check that Agent fee does not apply to {ORSMessageType.ConfirmationReport.value} with {sec_account} (step 9)')

        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        expected_result.update(
            {JavaApiFields.AllocSummaryStatus.value: AllocationReportConst.AllocSummaryStatus_MAG.value})
        actually_result = {JavaApiFields.AllocStatus.value: allocation_report[JavaApiFields.AllocStatus.value],
                           JavaApiFields.MatchStatus.value: allocation_report[JavaApiFields.MatchStatus.value],
                           JavaApiFields.AllocSummaryStatus.value: allocation_report[
                               JavaApiFields.AllocSummaryStatus.value]}
        self.java_api_manager.compare_values(expected_result, actually_result,
                                             'Check expected result for allocation report from  step 10')
        # endregion

        # region step 10
        list_of_ignored_fields.extend(['RootSettlCurrFxRateCalc', 'AllocID', 'NetMoney', 'TradeDate',
                                       'BookingType', 'RootSettlCurrency', 'AllocInstructionMiscBlock1',
                                       'Quantity', 'AllocTransType', 'RootSettlCurrFxRate', 'RootSettlCurrAmt',
                                       'GrossTradeAmt', 'AllocSettlCurrAmt', 'AllocSettlCurrency',
                                       'SettlCurrAmt', 'SettlCurrFxRate', 'SettlCurrFxRateCalc', 'ReportedPx',
                                       'OrderAvgPx'])
        allocation_report = FixMessageAllocationInstructionReportOMS()
        allocation_report.change_parameters({'NoOrders': [{'ClOrdID': cl_ord_id, 'OrderID': order_id}],
                                             'AllocType': '5'})
        allocation_report.change_parameters({'AvgPx': new_avg_px, 'Currency': self.currency_post_trade,
                                             'tag5120': "*",
                                             })
        self.fix_verifier.check_fix_message_fix_standard(allocation_report, ignored_fields=list_of_ignored_fields)
        allocation_report.change_parameters({'NoMiscFees': '#',
                                             'AllocType': '2',
                                             'NoAllocs': [{'AllocAccount': self.alloc_account,
                                                           'AllocQty': list_of_qty[0],
                                                           'IndividualAllocID': '*',
                                                           'AllocNetPrice': '*',
                                                           'AllocPrice': '*',
                                                           }, {'AllocAccount': self.alloc_account_2,
                                                               'AllocQty': list_of_qty[1],
                                                               'IndividualAllocID': '*',
                                                               'AllocNetPrice': '*',
                                                               'AllocPrice': '*',
                                                               }]
                                             })
        self.fix_verifier.check_fix_message_fix_standard(allocation_report, ignored_fields=list_of_ignored_fields)
        confirmation_report = FixMessageConfirmationReportOMS(self.data_set)
        list_of_ignored_fields.extend(['ConfirmType', 'MatchStatus', 'ConfirmStatus',
                                       'CpctyConfGrp', 'ConfirmID', 'ConfirmTransType', 'tag11245'])
        confirmation_report.change_parameters({'NoOrders': [{
            'ClOrdID': cl_ord_id,
            'OrderID': order_id
        }]})
        for sec_account in list_of_security_accounts:
            confirmation_report.change_parameters(
                {'AvgPx': new_avg_px, 'Currency': self.currency_post_trade,
                 'tag5120': '*'})
            confirmation_report.change_parameters(
                {'AllocQty': list_of_qty[list_of_security_accounts.index(sec_account)],
                 'AllocAccount': sec_account,
                 'NoMiscFees': '#'})
            self.fix_verifier.check_fix_message_fix_standard(confirmation_report,
                                                             ['ClOrdID', 'AllocAccount', 'tag11245'],
                                                             ignored_fields=list_of_ignored_fields)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_commission_sender.clear_fees()
