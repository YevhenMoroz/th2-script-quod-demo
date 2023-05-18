import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageAllocationInstructionReportOMS import \
    FixMessageAllocationInstructionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, ExecutionReportConst
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ComputeBookingFeesCommissionsRequestOMS import \
    ComputeBookingFeesCommissionsRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T7927(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.dc_connectivity = self.fix_env.drop_copy
        self.client = self.data_set.get_client("client_com_1")  # CLIENT_COMM_1
        self.perc_amt = self.data_set.get_comm_profile_by_name("perc_amt")
        self.cur = self.data_set.get_currency_by_name('currency_1')
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.fix_message.change_parameters({"Account": self.client})
        self.fix_verifier = FixVerifier(self.dc_connectivity, self.test_id)
        self.qty = self.fix_message.get_parameter('OrderQtyData')['OrderQty']
        self.price = self.fix_message.get_parameter('Price')
        self.venue = self.data_set.get_venue_by_name('venue_1')
        self.commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.trade_request = TradeEntryOMS(self.data_set)
        self.complete_message = DFDManagementBatchOMS(self.data_set)
        self.compute_request = ComputeBookingFeesCommissionsRequestOMS(self.data_set)
        self.alloc_instr = AllocationInstructionOMS(self.data_set)
        self.alloc_report = FixMessageAllocationInstructionReportOMS()
        self.instr_id = self.data_set.get_instrument_id_by_name("instrument_2")
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Send commission and fees
        self.commission_sender.clear_commissions()
        self.commission_sender.clear_fees()
        self.commission_sender.set_modify_fees_message(comm_profile=self.perc_amt)
        self.commission_sender.change_message_params({"venueID": self.venue})
        self.commission_sender.send_post_request()
        self.commission_sender.set_modify_client_commission_message(comm_profile=self.perc_amt)
        self.commission_sender.change_message_params({"venueID": self.venue})
        self.commission_sender.send_post_request()
        # endregion

        # region create order (precondition)
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = response[0].get_parameter("OrderID")
        cl_order_id = response[0].get_parameter("ClOrdID")
        # endregion

        expected_result_comm = {JavaApiFields.CommissionCurrency.value: 'EUR',
                                JavaApiFields.CommissionBasis.value: 'PCT', JavaApiFields.CommissionRate.value: '5.0',
                                JavaApiFields.CommissionAmount.value: '100.0',
                                JavaApiFields.CommissionAmountType.value: 'BRK',
                                JavaApiFields.CommissionAmountSubType.value: 'OTH'}
        expected_result_fee = {JavaApiFields.MiscFeeBasis.value: 'P', JavaApiFields.MiscFeeType.value: 'EXC',
                               JavaApiFields.MiscFeeCurr.value: 'EUR',
                               JavaApiFields.MiscFeeRate.value: '5.0', JavaApiFields.MiscFeeAmt.value: '100.0'}

        # region manual execute order (precondition)
        self.trade_request.set_default_trade(order_id, self.price)
        self.java_api_manager.send_message_and_receive_response(self.trade_request)
        exec_reply = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameters()[
            JavaApiFields.ExecutionReportBlock.value]
        exec_id = exec_reply[JavaApiFields.ExecID.value]
        expected_result = {JavaApiFields.TransExecStatus.value: ExecutionReportConst.TransExecStatus_FIL.value,
                           JavaApiFields.MiscFeesList.value: {JavaApiFields.MiscFeesBlock.value: [expected_result_fee]},
                           JavaApiFields.ClientCommissionList.value: {
                               JavaApiFields.ClientCommissionBlock.value: [expected_result_comm]}}
        self.java_api_manager.compare_values(expected_result, exec_reply,
                                             "Check commissions after Execution")
        # endregion

        # region complete order (precondition)
        self.complete_message.set_default_complete(order_id)
        self.java_api_manager.send_message_and_receive_response(self.complete_message)
        exec_reply = self.java_api_manager.get_last_message(ORSMessageType.ExecutionReport.value).get_parameter(
            JavaApiFields.ExecutionReportBlock.value)
        post_trd_sts = exec_reply["PostTradeStatus"]
        self.java_api_manager.compare_values({JavaApiFields.ExecType.value: ExecutionReportConst.ExecType_CAL.value},
                                             exec_reply, "Check order is completed")
        # endregion

        expected_result_comm = {JavaApiFields.CommissionCurrency.value: 'EUR',
                                JavaApiFields.CommissionBasis.value: 'PCT', JavaApiFields.CommissionRate.value: '5.0',
                                JavaApiFields.CommissionAmount.value: '2.0',
                                JavaApiFields.CommissionAmountType.value: 'BRK'}
        expected_result_fee = {JavaApiFields.RootMiscFeeBasis.value: 'P', JavaApiFields.RootMiscFeeType.value: 'EXC',
                               JavaApiFields.RootMiscFeeCurr.value: 'EUR',
                               JavaApiFields.RootMiscFeeRate.value: '5.0', JavaApiFields.RootMiscFeeAmt.value: '2.0'}

        # region get commission and fee from Booking Ticket(precondition)
        cross_price = (int(self.price) / 100) * 2
        self.compute_request.set_list_of_order_alloc_block(cl_order_id, order_id, post_trd_sts)
        self.compute_request.set_list_of_exec_alloc_block(self.qty, exec_id, self.price, post_trd_sts)
        self.compute_request.set_default_compute_booking_request(self.qty, cross_price, self.client)
        self.java_api_manager.send_message_and_receive_response(self.compute_request)
        compute_reply = self.java_api_manager.get_last_message(
            ORSMessageType.ComputeBookingFeesCommissionsReply.value).get_parameter(
            JavaApiFields.ComputeBookingFeesCommissionsReplyBlock.value)

        self.java_api_manager.compare_values(
            {JavaApiFields.RootMiscFeesList.value: {JavaApiFields.RootMiscFeesBlock.value: [expected_result_fee]},
             JavaApiFields.ClientCommissionList.value: {
                 JavaApiFields.ClientCommissionBlock.value: [expected_result_comm]}},
            compute_reply,
            "Check comissions in the booking ticket")
        # endregion

        # region book order (precondition)
        self.alloc_instr.set_default_book(order_id)
        self.alloc_instr.update_fields_in_component("AllocationInstructionBlock",
                                                    {"ClientCommissionList": compute_reply[
                                                        JavaApiFields.ClientCommissionList.value],
                                                     "RootMiscFeesList": compute_reply[
                                                         JavaApiFields.RootMiscFeesList.value],
                                                     "AccountGroupID": self.client,
                                                     "InstrID": self.instr_id, "AvgPx": self.price,
                                                     "GrossTradeAmt": '2000'})
        self.java_api_manager.send_message_and_receive_response(self.alloc_instr)
        alloc_report = self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value).get_parameter(
            JavaApiFields.AllocationReportBlock.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.RootMiscFeesList.value: {JavaApiFields.RootMiscFeesBlock.value: [expected_result_fee]},
             JavaApiFields.ClientCommissionList.value: {
                 JavaApiFields.ClientCommissionBlock.value: [expected_result_comm]}},
            alloc_report,
            "Check comissions after booking")
        # endregion

        # region check Allocation Report (step 1)
        ignored_firelds = ['Account', 'ExecAllocGrp', 'tag5120', 'RootSettlCurrAmt']
        self.alloc_report.set_default_ready_to_book(self.fix_message)
        self.alloc_report.change_parameters({'RootCommTypeClCommBasis': '3', "RootOrClientCommission": '100',
                                             'RootOrClientCommissionCurrency': self.cur, 'NoRootMiscFeesList': {
                'NoRootMiscFeesList': [{'RootMiscFeeBasis': '2', 'RootMiscFeeCurr': self.cur, 'RootMiscFeeType': '4',
                                        'RootMiscFeeRate': '5', 'RootMiscFeeAmt': '100'}]}})
        self.fix_verifier.check_fix_message_fix_standard(self.alloc_report, ignored_fields=ignored_firelds)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.commission_sender.clear_commissions()
        self.commission_sender.clear_fees()
