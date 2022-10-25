import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageAllocationInstructionReportOMS import \
    FixMessageAllocationInstructionReportOMS
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import OrderReplyConst, JavaApiFields
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ComputeBookingFeesCommissionsRequestOMS import \
    ComputeBookingFeesCommissionsRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7105(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.bs_connectivity = self.fix_env.buy_side
        self.ss_connectivity = self.fix_env.sell_side
        self.dc_connectivity = self.fix_env.drop_copy
        self.java_api_connectivity = self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.client = self.data_set.get_client_by_name("client_com_1")  # CLIENT_COMM_1
        self.cur = self.data_set.get_currency_by_name('currency_3')  # GBp
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit("instrument_3")
        self.qty = self.fix_message.get_parameter('OrderQtyData')['OrderQty']
        self.mic = self.data_set.get_mic_by_name("mic_2")  # XEUR
        self.venue = self.data_set.get_venue_by_name("venue_2")  # EUREX
        self.price = self.fix_message.get_parameter('Price')
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.fix_verifier_dc = FixVerifier(self.dc_connectivity, self.test_id)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.fee = self.data_set.get_fee_by_name('fee1')
        self.comm_profile = self.data_set.get_comm_profile_by_name("perc_amt")
        self.com_cur = self.data_set.get_currency_by_name('currency_2')
        self.fee_type = self.data_set.get_misc_fee_type_by_name('agent')
        self.fee_route_id = self.data_set.get_route_id_by_name('route_1')
        self.exec_scope = self.data_set.get_fee_exec_scope_by_name('all_exec')
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.comp_comm = ComputeBookingFeesCommissionsRequestOMS(self.data_set)
        self.trade_entry_request = TradeEntryOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region send fees and commission
        self.rest_commission_sender.clear_fees()
        self.rest_commission_sender.set_modify_fees_message(comm_profile=self.comm_profile).change_message_params(
            {'venueID': self.venue}).send_post_request()
        self.rest_commission_sender.clear_commissions()
        self.rest_commission_sender.set_modify_client_commission_message(
            comm_profile=self.comm_profile).change_message_params(
            {'venueID': self.venue}).send_post_request()
        # endregion
        # region send order
        self.__send_fix_orders()
        order_id = self.response[0].get_parameter("OrderID")
        cl_order_id = self.response[0].get_parameter("ClOrdID")
        # endregion
        # region Execute order
        self.trade_entry_request.set_default_trade(order_id, exec_price=self.price, exec_qty=self.qty)
        responses = self.java_api_manager.send_message_and_receive_response(self.trade_entry_request)
        self.__return_result(responses, ORSMessageType.ExecutionReport.value)
        exec_id = self.result.get_parameter(JavaApiFields.ExecutionReportBlock.value)['ExecID']
        # endregion
        # region check order ExecutionReports
        no_misc = {"MiscFeeAmt": '1', "MiscFeeCurr": self.com_cur,
                   "MiscFeeType": "4"}
        comm_data = {"Commission": "1", "CommType": "3"}
        execution_report = FixMessageExecutionReportOMS(self.data_set).set_default_filled(self.fix_message)
        ignore_fields = ['ReplyReceivedTime', 'LastMkt', 'Text', 'SettlCurrency', 'LastExecutionPolicy',
                         'SecondaryOrderID', 'SettlType', 'VenueType', 'SecondaryExecID']
        execution_report.change_parameters(
            {'Currency': self.cur,
             "Account": self.client, "MiscFeesGrp": {"NoMiscFees": [no_misc]}, "CommissionData": comm_data})
        self.fix_verifier.check_fix_message_fix_standard(execution_report, ignored_fields=ignore_fields)
        # endregion
        # region book order
        self.allocation_instruction.set_default_book(order_id)
        post_trade_sts = OrderReplyConst.PostTradeStatus_RDY.value
        self.comp_comm.set_list_of_order_alloc_block(cl_order_id, order_id, post_trade_sts)
        self.comp_comm.set_list_of_exec_alloc_block(self.qty, exec_id, self.price, post_trade_sts)
        self.comp_comm.set_default_compute_booking_request(self.qty)
        self.comp_comm.update_fields_in_component(JavaApiFields.ComputeBookingFeesCommissionsRequestBlock.value,
                                                  {'AccountGroupID': self.client, 'AvgPx': '0.100000000'})
        responses = self.java_api_manager.send_message_and_receive_response(self.comp_comm)
        self.__return_result(responses, ORSMessageType.ComputeBookingFeesCommissionsReply.value)
        clcomm_list = self.result.get_parameter(JavaApiFields.ComputeBookingFeesCommissionsReplyBlock.value)[
            'ClientCommissionList']
        comm_list = self.result.get_parameter(JavaApiFields.ComputeBookingFeesCommissionsReplyBlock.value)[
            'RootMiscFeesList']
        # endregion
        # region book order
        instrument_id = self.data_set.get_instrument_id_by_name('instrument_3')
        gross_currency_amt = str(int(self.qty) * int(self.price))
        self.allocation_instruction.update_fields_in_component('AllocationInstructionBlock',
                                                               {
                                                                   'GrossTradeAmt': gross_currency_amt,
                                                                   'AvgPx': self.price,
                                                                   'Qty': self.qty,
                                                                   'InstrID': instrument_id,
                                                                   "Currency": self.cur,
                                                                   "AccountGroupID": self.client,
                                                                   'ClientCommissionList': clcomm_list,
                                                                   'RootMiscFeesList': comm_list
                                                               })
        responses = self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        # endregion
        # region check actual PostTradeStatus of order
        self.__return_result(responses, ORSMessageType.OrdUpdate.value)
        self.java_api_manager.compare_values(
            {JavaApiFields.PostTradeStatus.value: OrderReplyConst.PostTradeStatus_BKD.value},
            self.result.get_parameter(JavaApiFields.OrdUpdateBlock.value),
            'Check order Post Trade sts')
        # region check booked order
        alloc_report = FixMessageAllocationInstructionReportOMS().set_default_ready_to_book(
            self.fix_message)
        no_root_misc = {"RootMiscFeeBasis": "2", "RootMiscFeeCurr": self.com_cur,
                        "RootMiscFeeType": no_misc['MiscFeeType'],
                        "RootMiscFeeRate": '5', "RootMiscFeeAmt": "0.5"}
        alloc_report.change_parameters(
            {"AvgPx": "*", "Currency": "*", "tag5120": "*",
             'RootOrClientCommission': "0.5", 'RootCommTypeClCommBasis': "2",
             "RootOrClientCommissionCurrency": self.com_cur,
             'NoRootMiscFeesList': {"NoRootMiscFeesList": [no_root_misc]}, "RootSettlCurrAmt": "*"})
        self.fix_verifier_dc.check_fix_message_fix_standard(alloc_report, ignored_fields=['Account'])
        # endregion

    def __send_fix_orders(self):
        self.fix_message.change_parameters(
            {"Account": self.client,
             "ExDestination": self.mic,
             "Currency": self.data_set.get_currency_by_name("currency_3")})
        self.response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)

    def __return_result(self, responses, message_type):
        for response in responses:
            if response.get_message_type() == message_type:
                self.result = response
