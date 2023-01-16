import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.verifier import VerificationMethod
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageConfirmationReportOMS import FixMessageConfirmationReportOMS
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst, \
    AllocationInstructionConst, AllocationReportConst, ConfirmationReportConst
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ComputeBookingFeesCommissionsRequestOMS import \
    ComputeBookingFeesCommissionsRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import \
    ForceAllocInstructionStatusRequestOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def print_message(message, responses):
    logger.info(message)
    for i in responses:
        logger.info(i)
        logger.info(i.get_parameters())


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7023(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.bs_connectivity = self.fix_env.buy_side
        self.ss_connectivity = self.fix_env.sell_side
        self.dc_connectivity = self.fix_env.drop_copy
        self.client = self.data_set.get_client_by_name("client_pt_4")
        self.client_acc1 = self.data_set.get_account_by_name("client_pt_4_acc_1")
        self.client_acc2 = self.data_set.get_account_by_name("client_pt_4_acc_2")
        self.cur = self.data_set.get_currency_by_name('currency_3')
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit('instrument_3')
        self.qty = '10000'
        self.fix_message.change_parameters({'OrderQtyData': {'OrderQty': self.qty}})
        self.mic = self.data_set.get_mic_by_name("mic_2")
        self.price = self.fix_message.get_parameter("Price")
        self.currency_post_trade = self.data_set.get_currency_by_name('currency_2')
        self.venue = self.data_set.get_venue_by_name("venue_2")
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.client_for_rule = self.data_set.get_venue_client_names_by_name("client_pt_4_venue_2")
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.mid_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.rule_manager = RuleManager(Simulators.equity)
        self.fix_verifier = FixVerifier(self.dc_connectivity, self.test_id)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.fee1 = self.data_set.get_fee_by_name('fee1')
        self.fee2 = self.data_set.get_fee_by_name('fee2')
        self.fee3 = self.data_set.get_fee_by_name('fee3')
        self.fee_type1 = self.data_set.get_misc_fee_type_by_name('stamp')
        self.fee_type2 = self.data_set.get_misc_fee_type_by_name('levy')
        self.fee_type3 = self.data_set.get_misc_fee_type_by_name('per_transac')
        self.params = {"ExDestination": self.mic, "Currency": self.cur, "Account": self.client}
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.compute_booking_fee_commission_request = ComputeBookingFeesCommissionsRequestOMS(self.data_set)
        self.confirmation_request = ConfirmationOMS(self.data_set)
        self.approve_block = ForceAllocInstructionStatusRequestOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region send fees precondition
        self.rest_commission_sender.clear_fees()
        comm_profile_fee_1 = self.data_set.get_comm_profile_by_name('bas_qty')
        comm_profile_fee_2 = self.data_set.get_comm_profile_by_name('bas_amt')
        comm_profile_fee_3 = self.data_set.get_comm_profile_by_name('perc_amt')
        self.rest_commission_sender.set_modify_fees_message(fee=self.fee1, fee_type=self.fee_type1,
                                                            comm_profile=comm_profile_fee_1)
        self.rest_commission_sender.change_message_params({"venueID": self.venue})
        self.rest_commission_sender.send_post_request()
        self.rest_commission_sender.set_modify_fees_message(fee=self.fee2, fee_type=self.fee_type2,
                                                            comm_profile=comm_profile_fee_2)
        self.rest_commission_sender.change_message_params({"venueID": self.venue})
        self.rest_commission_sender.send_post_request()
        self.rest_commission_sender.set_modify_fees_message(fee=self.fee3, fee_type=self.fee_type3,
                                                            comm_profile=comm_profile_fee_3)
        self.rest_commission_sender.change_message_params({"venueID": self.venue})
        self.rest_commission_sender.send_post_request()
        # endregion

        # region create and trade DMA order (step 1 and step 2)
        self.__send_fix_orders()
        expected_result = {'OrdStatus': '0'}
        last_response = self.__get_fix_message(expected_result)
        self.java_api_manager.compare_values(expected_result, last_response,
                                             'Check actually and expected result from step 1')
        expected_result.clear()
        expected_result.update({'ExecType': 'F'})
        last_response = self.__get_fix_message(expected_result)
        self.java_api_manager.compare_values(expected_result, last_response,
                                             'Check actually and expected result for ExecType (part of step 2')

        basis_fee_amount = str(float(self.qty) * float(self.price) / 1000000)
        perc_rate = 5.0
        perc_fee_amount = str(int(float(self.qty) * float(self.price) / 10000 * perc_rate))
        expected_levy_fee_dimensions = {
            JavaApiFields.MiscFeeAmt.value: basis_fee_amount,
            JavaApiFields.MiscFeeCurr.value: self.currency_post_trade,
            JavaApiFields.MiscFeeType.value: '6'
        }
        expected_per_transac_fee_dimensions = {
            JavaApiFields.MiscFeeAmt.value: perc_fee_amount,
            JavaApiFields.MiscFeeCurr.value: self.currency_post_trade,
            JavaApiFields.MiscFeeType.value: '10'
        }
        exec_id = last_response['ExecID']
        list_of_expected_fees = [expected_levy_fee_dimensions, expected_per_transac_fee_dimensions]
        for index in range(2):
            if last_response['NoMiscFees']['NoMiscFees'][index][
                JavaApiFields.MiscFeeType.value] == '6':
                self.java_api_manager.compare_values(expected_levy_fee_dimensions,
                                                     last_response['NoMiscFees']['NoMiscFees'][index],
                                                     f'Check expected and actually results of fees with FeeType '
                                                     f'{expected_levy_fee_dimensions[JavaApiFields.MiscFeeType.value]}')
            else:
                self.java_api_manager.compare_values(expected_per_transac_fee_dimensions,
                                                     last_response['NoMiscFees']['NoMiscFees'][index],
                                                     f'Check expected and actually results of fees with FeeType '
                                                     f'{expected_per_transac_fee_dimensions[JavaApiFields.MiscFeeType.value]}')

        self.java_api_manager.compare_values({'Count groups of fees': len(list_of_expected_fees)},
                                             {'Count groups of fees': len(last_response['NoMiscFees']['NoMiscFees'])},
                                             f'Check that only{len(list_of_expected_fees)} groups of fees present (step 2)')
        # endregion

        # region step 3 - Book order

        # Send ComputeCommissionFeesRequest (part of step 3)
        self.compute_booking_fee_commission_request.set_list_of_order_alloc_block(self.cl_ord_id, self.order_id,
                                                                                  OrderReplyConst.PostTradeStatus_RDY.value)
        self.compute_booking_fee_commission_request.set_list_of_exec_alloc_block(self.qty, exec_id, self.price,
                                                                                 OrderReplyConst.PostTradeStatus_RDY.value)
        self.compute_booking_fee_commission_request.set_default_compute_booking_request(self.qty)
        new_avg_px = str(float(self.price) / 100)
        self.compute_booking_fee_commission_request.update_fields_in_component(
            'ComputeBookingFeesCommissionsRequestBlock', {'AvgPx': new_avg_px, 'AccountGroupID': self.client})
        responses = self.java_api_manager.send_message_and_receive_response(self.compute_booking_fee_commission_request)
        print_message('Send ComputeBookingFeesCommissionsRequest', responses)
        compute_booking_fees_commission_reply = self.java_api_manager.get_last_message(
            ORSMessageType.ComputeBookingFeesCommissionsReply.value).get_parameters()[
            JavaApiFields.ComputeBookingFeesCommissionsReplyBlock.value]
        expected_levy_root_fee_dimensions = {
            JavaApiFields.RootMiscFeeAmt.value: basis_fee_amount,
            JavaApiFields.RootMiscFeeCurr.value: self.currency_post_trade,
            JavaApiFields.RootMiscFeeType.value: AllocationInstructionConst.COMM_AND_FEE_TYPE_LEV.value
        }
        expected_per_transac_root_fee_dimensions = {
            JavaApiFields.RootMiscFeeAmt.value: str(float(perc_fee_amount)),
            JavaApiFields.RootMiscFeeCurr.value: self.currency_post_trade,
            JavaApiFields.RootMiscFeeType.value: AllocationInstructionConst.COMM_AND_FEE_TYPE_TRA.value
        }
        list_of_expected_root_fees = [expected_levy_root_fee_dimensions, expected_per_transac_root_fee_dimensions]
        for root_fee_expected in list_of_expected_root_fees:
            self.java_api_manager.compare_values(root_fee_expected, compute_booking_fees_commission_reply[
                JavaApiFields.RootMiscFeesList.value][JavaApiFields.RootMiscFeesBlock.value][
                list_of_expected_root_fees.index(root_fee_expected)],
                                                 'Check expected and actually result for fee (Compute Request) (part of step 3)')
        self.java_api_manager.compare_values({'Count groups of fees': len(list_of_expected_fees)},
                                             {'Count groups of fees': len(compute_booking_fees_commission_reply[
                                                                              JavaApiFields.RootMiscFeesList.value][
                                                                              JavaApiFields.RootMiscFeesBlock.value])},
                                             f'Check that only{len(list_of_expected_fees)} groups of fees present (part of step 3)')
        # the end

        # book order (part of step 3)
        common_fee_amount = float(basis_fee_amount) + float(perc_fee_amount)
        instrument_id = self.data_set.get_instrument_id_by_name("instrument_3")
        gross_currency_amt = str(float(self.qty) * float(new_avg_px))
        root_misc_fees = compute_booking_fees_commission_reply[JavaApiFields.RootMiscFeesList.value]
        self.allocation_instruction.set_default_book(self.order_id)
        self.allocation_instruction.update_fields_in_component('AllocationInstructionBlock',
                                                               {
                                                                   'GrossTradeAmt': gross_currency_amt,
                                                                   'AvgPx': self.price,
                                                                   'Qty': self.qty,
                                                                   'AccountGroupID': self.client,
                                                                   'Currency': self.currency_post_trade,
                                                                   "InstrID": instrument_id,
                                                                   'RootCommissionDataBlock': {
                                                                       'RootCommission': str(common_fee_amount),
                                                                       'RootCommType': 'A',
                                                                       'RootCommCurrency': self.currency_post_trade
                                                                   },
                                                                   JavaApiFields.RootMiscFeesList.value: root_misc_fees,
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
        order_update = self.java_api_manager.get_last_message(ORSMessageType.OrdUpdate.value).get_parameters()[
            JavaApiFields.OrdUpdateBlock.value]
        expected_result_for_block = {
            JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_APP.value,
            JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_UNM.value,
        }
        expected_result_for_order = {JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_BKD.value,
                                     JavaApiFields.DoneForDay.value: OrderReplyConst.DoneForDay_YES.value}
        self.java_api_manager.compare_values(expected_result_for_block, allocation_report,
                                             'Check Status and MatchStatus (part of step 3)')
        self.java_api_manager.compare_values(expected_result_for_order, order_update,
                                             'Check PostTradeStatus and DoneForDay(part of step 3)')
        # the end

        # endregion

        # region approve block
        self.approve_block.set_default_approve(alloc_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.approve_block)
        print_message('Approve block', responses)
        allocation_report = \
            self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameters()[
                JavaApiFields.AllocationReportBlock.value]
        expected_result_for_block.update({JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_ACK.value,
                                          JavaApiFields.MatchStatus.value: AllocationReportConst.MatchStatus_MAT.value})
        self.java_api_manager.compare_values(expected_result_for_block, allocation_report,
                                             'Check Status and MatchStatus (step 4)')
        # endregion

        # region step 5 - Allocate block
        list_of_security_accounts = [self.client_acc1, self.client_acc2]
        half_qty = str(float(self.qty) / 2)
        for sec_account in list_of_security_accounts:
            self.confirmation_request.set_default_allocation(alloc_id)
            self.confirmation_request.update_fields_in_component('ConfirmationBlock', {
                "AllocAccountID": sec_account,
                'AllocQty': half_qty,
                'AvgPx': new_avg_px,
                "InstrID": instrument_id
            })
            responses = self.java_api_manager.send_message_and_receive_response(self.confirmation_request)
            print_message(f'Allocate block for {sec_account}', responses)
            confirmation_report = \
                self.java_api_manager.get_last_message(ORSMessageType.ConfirmationReport.value).get_parameters()[
                    JavaApiFields.ConfirmationReportBlock.value]
            net_amt = str(float(half_qty) * float(new_avg_px) + float(perc_fee_amount) / 2)
            net_price = str(float(net_amt) / float(half_qty))
            if list_of_security_accounts.index(sec_account) == 1:
                net_amt = str(float(half_qty) * float(new_avg_px) + float(perc_fee_amount) / 2 +
                              float(basis_fee_amount) / 2)
                net_price = str(float(net_amt) / float(half_qty))
            self.java_api_manager.compare_values({JavaApiFields.NetMoney.value: net_amt,
                                                  JavaApiFields.NetPrice.value: net_price}, confirmation_report,
                                                 f'Check that confirmation with {sec_account} has properly NetMoney and NetPrice')
            for commission in confirmation_report[JavaApiFields.MiscFeesList.value][JavaApiFields.MiscFeesBlock.value]:
                self.java_api_manager.compare_values(
                    {JavaApiFields.MiscFeeType.value: AllocationInstructionConst.COMM_AND_FEE_TYPE_STA.value},
                    commission,
                    'Check that fee isn`t Stamp', VerificationMethod.NOT_CONTAINS)
        # endregion
        time.sleep(10)

        # region step 6 - Verify that 35 = AK message of first account doesn`t have Stamp and Levy fees
        list_of_ignore_fields = ['SecondaryOrderID', 'LastExecutionPolicy', 'TradeDate', 'SecondaryExecID', 'OrderID',
                                 'ExDestination', 'GrossTradeAmt', 'SettlCurrency', 'Instrument', 'TimeInForce',
                                 'OrdType', "TradeReportingIndicator", 'SettlDate', 'Side', 'HandlInst', 'OrderQtyData',
                                 'SecondaryExecID', 'ExecID', 'LastQty', 'TransactTime', 'AvgPx', 'QuodTradeQualifier',
                                 'BookID', 'Currency', 'PositionEffect', 'TrdType', 'LeavesQty', 'NoParty', 'CumQty',
                                 'LastPx', 'LastCapacity', 'tag5120', 'LastMkt', 'OrderCapacity''QtyType', 'ExecBroker',
                                 'QtyType', 'Price', 'OrderCapacity', 'VenueType', 'CommissionData', 'Text',
                                 'AllocQty', 'ConfirmType', 'ConfirmID',
                                 'AllocID', 'NetMoney', 'MatchStatus',
                                 'ConfirmStatus', 'AllocInstructionMiscBlock1',
                                 'CpctyConfGrp', 'ReportedPx','OrderAvgPx']
        params = {'ConfirmTransType': "0",
                  'AllocAccount': self.client_acc1,
                  'NoOrders': [{
                      'ClOrdID': self.cl_ord_id,
                      'OrderID': '*'
                  }],
                  'NoMiscFees': [
                      {'MiscFeeAmt': int(int(perc_fee_amount) / 2),
                       'MiscFeeCurr': '*',
                       'MiscFeeType': '10'}]
                  }
        fix_confirmation_report = FixMessageConfirmationReportOMS(self.data_set, params)
        self.fix_verifier.check_fix_message_fix_standard(fix_confirmation_report,
                                                         ['ConfirmTransType', 'NoOrders', 'AllocAccount'],
                                                         ignored_fields=list_of_ignore_fields)
        # endregion

        # region step 7 - Verify that 35 = AK of second account doesn`t have Stamp fees
        fix_confirmation_report.change_parameters({'AllocAccount': self.client_acc2,
                                                   'NoMiscFees': [
                                                       {'MiscFeeAmt': int(int(perc_fee_amount) / 2),
                                                        'MiscFeeCurr': '*',
                                                        'MiscFeeType': '10'},
                                                       {'MiscFeeAmt': float(basis_fee_amount) / 2,
                                                        'MiscFeeCurr': '*',
                                                        'MiscFeeType': '6'}
                                                   ]
                                                   })
        self.fix_verifier.check_fix_message_fix_standard(fix_confirmation_report,
                                                         ['ConfirmTransType', 'NoOrders', 'AllocAccount'],
                                                         ignored_fields=list_of_ignore_fields)
        # endregion

        # region step 8
        params.clear()
        params = {
            "ExecType": "F",
            "OrdStatus": "2",
            "Account": self.client,
            "ClOrdID": self.cl_ord_id,
            'NoMiscFees': [
                {'MiscFeeAmt': perc_fee_amount,
                 'MiscFeeCurr': '*',
                 'MiscFeeType': '10'},
                {'MiscFeeAmt': basis_fee_amount,
                 'MiscFeeCurr': '*',
                 'MiscFeeType': '6'}
            ]
        }
        fix_execution_report = FixMessageExecutionReportOMS(self.data_set, params)
        self.fix_verifier.check_fix_message_fix_standard(fix_execution_report, ignored_fields=list_of_ignore_fields)
        # endregion

    def __send_fix_orders(self):
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.bs_connectivity,
                                                                                                  self.client_for_rule,
                                                                                                  self.mic,
                                                                                                  int(self.price))
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                            self.client_for_rule,
                                                                                            self.mic, int(self.price),
                                                                                            int(self.qty), 2)
            self.fix_message.change_parameters(self.params)
            self.response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
            self.order_id = self.response[0].get_parameter("OrderID")
            self.cl_ord_id = self.response[0].get_parameter("ClOrdID")
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(nos_rule)
            self.rule_manager.remove_rule(trade_rule)

    def __get_fix_message(self, parameter: dict):
        for i in range(len(self.response)):
            for j in parameter.keys():
                if self.response[i].get_parameters()[j] == parameter[j]:
                    return self.response[i].get_parameters()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_commission_sender.clear_fees()
