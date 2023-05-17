import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.verifier import VerificationMethod
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
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst, \
    ExecutionReportConst, AllocationInstructionConst, AllocationReportConst, ConfirmationReportConst
from test_framework.java_api_wrappers.oms.es_messages.ExecutionReportOMS import ExecutionReportOMS
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ComputeBookingFeesCommissionsRequestOMS import \
    ComputeBookingFeesCommissionsRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import \
    ForceAllocInstructionStatusRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.OrderSubmitOMS import OrderSubmitOMS
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.oms.RestApiManageSecurityBlock import RestApiManageSecurityBlock
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def print_message(message, responses):
    logger.info(message)
    for i in responses:
        logger.info(i)
        logger.info(i.get_parameters())


class QAP_T7021(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.bs_connectivity = self.fix_env.buy_side
        self.dc_connectivity = self.fix_env.drop_copy
        self.client = self.data_set.get_client_by_name("client_com_1")
        self.client_acc = self.data_set.get_account_by_name("client_com_1_acc_1")
        self.currency = self.data_set.get_currency_by_name('currency_2')
        self.currency_GBp = self.data_set.get_currency_by_name('currency_3')
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.qty = "100"
        self.price = "20"
        self.mic = self.data_set.get_mic_by_name("mic_2")
        self.venue = self.data_set.get_venue_by_name("venue_2")
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.rest_api_manager = RestApiManager(session_alias=self.wa_connectivity, case_id=self.test_id)
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.client_for_rule = self.data_set.get_venue_client_names_by_name("client_com_1_venue_2")
        self.fix_verifier = FixVerifier(self.dc_connectivity, self.test_id)
        self.fee1 = self.data_set.get_fee_by_name('fee1')
        self.fee2 = self.data_set.get_fee_by_name('fee2')
        self.fee3 = self.data_set.get_fee_by_name('fee3')
        self.fee_type1 = self.data_set.get_misc_fee_type_by_name('stamp')
        self.fee_type2 = self.data_set.get_misc_fee_type_by_name('levy')
        self.fee_type3 = self.data_set.get_misc_fee_type_by_name('per_transac')
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.execution_report = ExecutionReportOMS(self.data_set)
        self.submit_request = OrderSubmitOMS(self.data_set)
        self.complete_message = DFDManagementBatchOMS(self.data_set)
        self.compute_request = ComputeBookingFeesCommissionsRequestOMS(self.data_set)
        self.alloc_instr = AllocationInstructionOMS(self.data_set)
        self.force_alloc = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.confirm = ConfirmationOMS(self.data_set)
        self.manage_security_block = RestApiManageSecurityBlock(self.data_set)
        self.pertransac_commission_profile = self.data_set.get_comm_profile_by_name('perc_amt')
        self.bas_amt = self.data_set.get_comm_profile_by_name('bas_amt')
        self.fix_execution_report = FixMessageExecutionReportOMS(self.data_set)
        self.allocation_instruction_fix = FixMessageAllocationInstructionReportOMS()
        self.confirmation_report = FixMessageConfirmationReportOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region send fees
        self.rest_commission_sender.clear_fees()
        self.rest_commission_sender.set_modify_fees_message(fee=self.fee1, fee_type=self.fee_type1,
                                                            comm_profile=self.bas_amt)
        self.rest_commission_sender.change_message_params({"venueID": self.venue})
        self.rest_commission_sender.send_post_request()
        self.rest_commission_sender.set_modify_fees_message(fee=self.fee2, fee_type=self.fee_type2,
                                                            comm_profile=self.bas_amt)
        self.rest_commission_sender.change_message_params({"venueID": self.venue})
        self.rest_commission_sender.send_post_request()
        self.rest_commission_sender.set_modify_fees_message(fee=self.fee3, fee_type=self.fee_type3,
                                                            comm_profile=self.pertransac_commission_profile)
        self.rest_commission_sender.change_message_params({"venueID": self.venue})
        self.rest_commission_sender.send_post_request()
        self.manage_security_block.set_fee_exemption(True, True, False)
        self.rest_api_manager.send_post_request(self.manage_security_block)
        # endregion

        # region step 1
        self.submit_request.set_default_dma_limit()
        instrument_id = self.data_set.get_instrument_id_by_name("instrument_3")
        self.submit_request.update_fields_in_component('NewOrderSingleBlock', {
            'ListingList': {'ListingBlock': [{'ListingID': self.data_set.get_listing_id_by_name("listing_2")}]},
            'InstrID': instrument_id,
            'AccountGroupID': self.client,
            'OrdQty': self.qty,
            'Price': self.price,
        })
        responses = self.java_api_manager.send_message_and_receive_response(self.submit_request)
        print_message("Create DMA order", responses)
        order_id = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameter(
            JavaApiFields.OrderNotificationBlock.value)["OrdID"]
        cl_order_id = self.java_api_manager.get_last_message(ORSMessageType.OrdNotification.value).get_parameter(
            JavaApiFields.OrderNotificationBlock.value)["ClOrdID"]
        # endregion

        # region step 2
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
                                                             "Currency": self.currency_GBp,
                                                             "ExecType": "Trade",
                                                             "TimeInForce": "Day",
                                                             "LeavesQty": self.qty,
                                                             "CumQty": self.qty,
                                                             "AvgPrice": self.price,
                                                             "LastMkt": self.mic,
                                                             "OrdQty": self.qty
                                                         })
        responses = self.java_api_manager.send_message_and_receive_response(self.execution_report)
        print_message('Execute DMA order', responses)
        execution_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value,
                                                   ExecutionReportConst.ExecType_TRD.value).get_parameters()[
                JavaApiFields.ExecutionReportBlock.value]
        actually_trans_exec_status = execution_report[JavaApiFields.TransExecStatus.value]
        exec_id = execution_report[JavaApiFields.ExecID.value]
        expected_result = {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value}
        self.java_api_manager.compare_values(expected_result,
                                             {JavaApiFields.TransExecStatus.value: actually_trans_exec_status},
                                             'Check ExecSts from step 2')
        self.java_api_manager.compare_values({'Count of Fee group': 1}, {'Count of Fee group': len(
            execution_report['MiscFeesList'][JavaApiFields.MiscFeesBlock.value])},
                                             'Check that execution has unique commission')
        actually_result = execution_report[JavaApiFields.MiscFeesList.value][JavaApiFields.MiscFeesBlock.value][0]
        expected_result.clear()
        fee_rate = float(5)
        fee_amount = float(fee_rate * float(self.qty) * float(self.price) / 10000)
        expected_result = {
            JavaApiFields.MiscFeeRate.value: str(fee_rate),
            JavaApiFields.MiscFeeAmt.value: str(fee_amount),
            JavaApiFields.MiscFeeCurr.value: self.currency,
            JavaApiFields.MiscFeeType.value: AllocationInstructionConst.COMM_AND_FEE_TYPE_TRA.value
        }
        self.java_api_manager.compare_values(expected_result, actually_result,
                                             'Check that Fee is PerTransac for execution from step 2')

        # region step 3
        new_avg_px = float(self.price) / 100
        post_trd_sts = OrderReplyConst.PostTradeStatus_RDY.value
        self.compute_request.set_list_of_order_alloc_block(cl_order_id, order_id, post_trd_sts)
        self.compute_request.set_list_of_exec_alloc_block(self.qty, exec_id, self.price, post_trd_sts)
        self.compute_request.set_default_compute_booking_request(self.qty, new_avg_px, self.client)
        responses = self.java_api_manager.send_message_and_receive_response(self.compute_request)
        print_message("ComputeRequest", responses)
        compute_reply = self.java_api_manager.get_last_message(
            ORSMessageType.ComputeBookingFeesCommissionsReply.value).get_parameters()[
            "ComputeBookingFeesCommissionsReplyBlock"]
        expected_levy = {'ExpectedFee': AllocationInstructionConst.COMM_AND_FEE_TYPE_LEV.value}
        expected_stamp = {'ExpectedFee': AllocationInstructionConst.COMM_AND_FEE_TYPE_STA.value}
        expected_per_trans = {'ExpectedFee': AllocationInstructionConst.COMM_AND_FEE_TYPE_TRA.value}

        expected_result_calculated = {
            JavaApiFields.RootMiscFeeRate.value: str(fee_rate),
            JavaApiFields.RootMiscFeeAmt.value: str(fee_amount),
            JavaApiFields.RootMiscFeeCurr.value: self.currency,
            JavaApiFields.RootMiscFeeType.value: AllocationInstructionConst.COMM_AND_FEE_TYPE_TRA.value
        }
        self.java_api_manager.compare_values(expected_per_trans,
                                             {"ExpectedFee": str(
                                                 compute_reply[JavaApiFields.RootMiscFeesList.value][
                                                     JavaApiFields.RootMiscFeesBlock.value])},
                                             "Check Per Transac", VerificationMethod.CONTAINS)
        self.java_api_manager.compare_values(expected_result_calculated,
                                             compute_reply[JavaApiFields.RootMiscFeesList.value][
                                                 JavaApiFields.RootMiscFeesBlock.value][0],
                                             'Check that PerTransac Fee properly calculated for ComputeMiscFeeCommissionReply (part of step 3)')
        # endregion

        # region step 3
        gross_amt = float(new_avg_px) * float(self.qty)
        self.alloc_instr.set_default_book(order_id)
        self.alloc_instr.update_fields_in_component("AllocationInstructionBlock",
                                                    {"RootMiscFeesList": compute_reply["RootMiscFeesList"],
                                                     "AccountGroupID": self.client,
                                                     "AvgPx": new_avg_px,
                                                     'GrossTradeAmt': gross_amt,
                                                     "InstrID": self.data_set.get_instrument_id_by_name(
                                                         "instrument_3")})
        self.java_api_manager.send_message_and_receive_response(self.alloc_instr)
        alloc_report = self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value,
                                                              JavaApiFields.BookingAllocInstructionID.value).get_parameter(
            JavaApiFields.AllocationReportBlock.value)
        self.java_api_manager.compare_values(expected_per_trans,
                                             {"ExpectedFee": str(
                                                 alloc_report["RootMiscFeesList"]["RootMiscFeesBlock"])},
                                             "Check Per Transac", VerificationMethod.CONTAINS)
        alloc_id = alloc_report["AllocInstructionID"]
        order_update = self.java_api_manager.get_last_message(ORSMessageType.OrdUpdate.value).get_parameters()[
            JavaApiFields.OrdUpdateBlock.value]
        expected_result = {
            JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_APP.value,
            JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_UNM.value,
            JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_BKD.value,
            JavaApiFields.DoneForDay.value: OrderReplyConst.DoneForDay_YES.value
        }
        actually_result = {JavaApiFields.AllocStatus.value: alloc_report[JavaApiFields.AllocStatus.value],
                           JavaApiFields.MatchStatus.value: alloc_report[JavaApiFields.MatchStatus.value],
                           JavaApiFields.PostTradeStatus.value: order_update[JavaApiFields.PostTradeStatus.value],
                           JavaApiFields.DoneForDay.value: order_update[JavaApiFields.DoneForDay.value]}
        self.java_api_manager.compare_values(expected_result, actually_result,
                                             'Check  Middle Office Statuses (part os step 3)')
        self.java_api_manager.compare_values(expected_result_calculated,
                                             alloc_report[JavaApiFields.RootMiscFeesList.value][
                                                 JavaApiFields.RootMiscFeesBlock.value][0],
                                             'Check that PerTransac Fee properly calculated for AllocInstruction (part of step 3)')
        # endregion

        # region step 4
        self.force_alloc.set_default_approve(alloc_id)
        responses = self.java_api_manager.send_message_and_receive_response(self.force_alloc)
        print_message('Approve Block', responses)
        alloc_report = self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameter(
            JavaApiFields.AllocationReportBlock.value)
        expected_result.pop(JavaApiFields.DoneForDay.value)
        expected_result.pop(JavaApiFields.PostTradeStatus.value)
        expected_result.update({JavaApiFields.AllocStatus.value: AllocationReportConst.AllocStatus_ACK.value,
                                JavaApiFields.MatchStatus.value: ConfirmationReportConst.MatchStatus_MAT.value})
        actually_result.clear()
        actually_result.update({JavaApiFields.AllocStatus.value: alloc_report[JavaApiFields.AllocStatus.value],
                                JavaApiFields.MatchStatus.value: alloc_report[JavaApiFields.MatchStatus.value]})
        self.java_api_manager.compare_values(expected_result, actually_result,
                                             'Check Middle Office Statuses (part of step 4)')
        # endregion

        # region step 5
        self.confirm.set_default_allocation(alloc_id)
        self.confirm.update_fields_in_component("ConfirmationBlock", {"AllocAccountID": self.client_acc,
                                                                      'AvgPx': new_avg_px,
                                                                      "InstrID": self.data_set.get_instrument_id_by_name(
                                                                          "instrument_3")})
        responses = self.java_api_manager.send_message_and_receive_response(self.confirm)
        print_message('Confirmation', responses)
        confirm_report = \
            self.java_api_manager.get_last_message(ORSMessageType.ConfirmationReport.value).get_parameters()[
                JavaApiFields.ConfirmationReportBlock.value]
        self.java_api_manager.compare_values(expected_per_trans,
                                             {"ExpectedFee": str(
                                                 confirm_report["MiscFeesList"]["MiscFeesBlock"])},
                                             "Check Per Transac", VerificationMethod.CONTAINS)
        gross_amt = float(new_avg_px) * float(self.qty)
        net_amt = gross_amt + fee_amount
        expected_result.clear()
        expected_result = {'NetAmount': str(net_amt), "NetPrice": str(float(net_amt) / float(self.qty))}
        actually_result = {'NetAmount': confirm_report[JavaApiFields.NetMoney.value],
                           "NetPrice": confirm_report[JavaApiFields.NetPrice.value]}
        self.java_api_manager.compare_values(expected_result, actually_result,
                                             'Check NetAmt and NetPrice of allocation (part of step 5)')
        # region step 6
        fee_amount_fix = str(int(fee_amount))
        fee_rate_fix = str(int(fee_rate))
        no_misc_fee = [{'MiscFeeAmt': fee_amount_fix, 'MiscFeeCurr': self.currency, 'MiscFeeType': '10'}]
        # pre step check 35 = 8 message
        list_of_ignored_fields = ['Account', 'ExecID', 'OrderQtyData', 'LastQty',
                                  'OrderID', 'TransactTime', 'Side', 'AvgPx', 'ExecAllocGrp',
                                  'QuodTradeQualifier', 'BookID', 'SettlCurrency',
                                  'SettlDate', 'Currency', 'TimeInForce', 'PositionEffect',
                                  'TradeDate', 'HandlInst', 'LeavesQty', 'NoParty', 'CumQty', 'LastPx',
                                  'OrdType', 'tag5120', 'LastMkt', 'OrderCapacity', 'QtyType',
                                  'ExecBroker', 'Price', 'VenueType', 'Instrument',
                                  'ExDestination', 'GrossTradeAmt', 'CommissionData',
                                  'SecondaryOrderID', 'LastExecutionPolicy', 'SecondaryExecID', 'OrderAvgPx',
                                  'GatingRuleName', 'GatingRuleCondName']

        self.fix_execution_report.change_parameters({"ExecType": "F", "OrdStatus": "2", "ClOrdID": cl_order_id,
                                                     'NoMiscFees': no_misc_fee})
        self.fix_verifier.check_fix_message_fix_standard(self.fix_execution_report,
                                                         ignored_fields=list_of_ignored_fields)

        # end region
        # pre step check 35=J message (626 = 5)
        list_of_ignored_fields.extend(['RootCommTypeClCommBasis', 'AllocID',
                                       'NetMoney', 'BookingType', 'AllocInstructionMiscBlock1',
                                       'Quantity', 'RootOrClientCommission', 'AllocTransType',
                                       'ReportedPx', 'ConfirmStatus', 'MatchStatus', 'ConfirmID',
                                       'RootOrClientCommissionCurrency',
                                       'RootSettlCurrAmt'])
        self.allocation_instruction_fix.change_parameters(
            {'NoOrders': [{'ClOrdID': cl_order_id, 'OrderID': order_id}], "AllocType": '5',
             'NoRootMiscFeesList': [{
                 'RootMiscFeeBasis': '2',
                 'RootMiscFeeCurr': self.currency,
                 'RootMiscFeeType': '10',
                 'RootMiscFeeRate': fee_rate_fix,
                 'RootMiscFeeAmt': fee_amount_fix
             }]})
        self.fix_verifier.check_fix_message_fix_standard(self.allocation_instruction_fix,
                                                         ignored_fields=list_of_ignored_fields)
        # end region
        # pre step check 35=J message (626 = 2)
        list_of_ignored_fields.extend(['IndividualAllocID', 'AllocNetPrice', 'AllocQty', 'AllocPrice', 'tag11245'])
        self.allocation_instruction_fix.remove_parameter('NoRootMiscFeesList')
        self.allocation_instruction_fix.change_parameters({'NoAllocs': [{
            'NoMiscFees': no_misc_fee,
            'AllocAccount': self.client_acc
        }]})
        self.allocation_instruction_fix.change_parameters(
            {'NoOrders': [{'ClOrdID': cl_order_id, 'OrderID': order_id}], "AllocType": '2'})
        self.fix_verifier.check_fix_message_fix_standard(self.allocation_instruction_fix,
                                                         ignored_fields=list_of_ignored_fields)
        # end region
        # pre step check 35=AK message
        list_of_ignored_fields.extend(['CpctyConfGrp', 'ConfirmID', 'ConfirmType', 'AllocAccount', 'tag11245'])
        self.confirmation_report.change_parameters(
            {'NoOrders': [{'ClOrdID': cl_order_id, 'OrderID': order_id}],
             'ConfirmTransType': "0",
             'NoMiscFees': no_misc_fee})
        self.fix_verifier.check_fix_message_fix_standard(self.confirmation_report,
                                                         ignored_fields=list_of_ignored_fields)
        # end region

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_commission_sender.clear_fees()
        self.manage_security_block.set_fee_exemption(False, False, False)
        self.rest_api_manager.send_post_request(self.manage_security_block)
