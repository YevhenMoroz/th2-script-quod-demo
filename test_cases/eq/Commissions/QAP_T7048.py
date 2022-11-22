import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
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
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import OrderReplyConst, JavaApiFields
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ComputeBookingFeesCommissionsRequestOMS import \
    ComputeBookingFeesCommissionsRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.ConfirmationOMS import ConfirmationOMS
from test_framework.java_api_wrappers.oms.ors_messges.ForceAllocInstructionStatusRequestOMS import \
    ForceAllocInstructionStatusRequestOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7048(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.bs_connectivity = self.fix_env.buy_side
        self.ss_connectivity = self.fix_env.sell_side
        self.dc_connectivity = self.fix_env.drop_copy
        self.client = self.data_set.get_client_by_name("client_com_1")  # CLIENT_COMM
        self.cur = self.data_set.get_currency_by_name('currency_3')  # GBp
        self.com_cur = self.data_set.get_currency_by_name('currency_2')
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit('instrument_3')
        self.qty = self.fix_message.get_parameter("OrderQtyData")['OrderQty']
        self.mic = self.data_set.get_mic_by_name("mic_2")  # XEUR
        self.price = self.fix_message.get_parameter("Price")
        self.venue = self.data_set.get_venue_by_name("venue_2")  # EUREX
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.client_for_rule = self.data_set.get_venue_client_names_by_name("client_com_1_venue_2")
        self.client_acc = self.data_set.get_account_by_name('client_com_1_acc_1')  # CLIENT_COMM_1_SA1
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.rule_manager = RuleManager(Simulators.equity)
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.fix_verifier_dc = FixVerifier(self.dc_connectivity, self.test_id)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.fee = self.data_set.get_fee_by_name('fee1')
        self.comm_prof = self.data_set.get_comm_profile_by_name('perc_qty')
        self.fee_type = self.data_set.get_misc_fee_type_by_name('value_added_tax')
        self.params = {"ExDestination": self.mic, "Currency": self.cur, "Account": self.client}
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.comp_comm = ComputeBookingFeesCommissionsRequestOMS(self.data_set)
        self.force_alloc_instr = ForceAllocInstructionStatusRequestOMS(self.data_set)
        self.confirmation = ConfirmationOMS(self.data_set)
        self.alloc_report = FixMessageAllocationInstructionReportOMS()
        self.conf_report = FixMessageConfirmationReportOMS(self.data_set)
        self.fix_verifier_dc = FixVerifier(self.dc_connectivity, self.test_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region send fees
        self.rest_commission_sender.clear_commissions()
        self.rest_commission_sender.clear_fees()
        self.rest_commission_sender.set_modify_fees_message(fee=self.fee, fee_type=self.fee_type,
                                                            comm_profile=self.comm_prof)
        self.rest_commission_sender.change_message_params({"venueID": self.venue})
        self.rest_commission_sender.send_post_request()
        # endregion

        # region send order
        response = self.__send_fix_orders()
        order_id = response[0].get_parameter("OrderID")
        cl_order_id = response[0].get_parameter("ClOrdID")
        exec_id = response[5].get_parameters()["ExecID"]
        # endregion

        # region get values from booking ticket
        instrument_id = self.data_set.get_instrument_id_by_name('instrument_3')
        gross_currency_amt = str(int(self.qty) * int(self.price))
        post_trade_sts = OrderReplyConst.PostTradeStatus_RDY.value
        new_avg_px = str(float(self.price) / 100)
        self.comp_comm.set_list_of_order_alloc_block(cl_order_id, order_id, post_trade_sts)
        self.comp_comm.set_list_of_exec_alloc_block(self.qty, exec_id, self.price, post_trade_sts)
        self.comp_comm.set_default_compute_booking_request(self.qty, new_avg_px, self.client)
        responses = self.java_api_manager.send_message_and_receive_response(self.comp_comm)
        self.__return_result(responses, ORSMessageType.ComputeBookingFeesCommissionsReply.value)
        fee_list = self.result.get_parameter(JavaApiFields.ComputeBookingFeesCommissionsReplyBlock.value)[
            'RootMiscFeesList']
        # endregion

        # region book order
        self.allocation_instruction.set_default_book(order_id)
        self.allocation_instruction.update_fields_in_component('AllocationInstructionBlock',
                                                               {
                                                                   'GrossTradeAmt': gross_currency_amt,
                                                                   'AvgPx': self.price,
                                                                   'Qty': self.qty,
                                                                   'InstrID': instrument_id,
                                                                   "Currency": self.cur,
                                                                   "AccountGroupID": self.client,
                                                                   'RootMiscFeesList': fee_list
                                                               })
        responses = self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        # endregion

        # region check block values
        fee_list_exp = {'RootMiscFeesBlock': [
            {'RootMiscFeeBasis': 'P', 'RootMiscFeeAmt': '10.0', 'RootMiscFeeType': 'VAT', 'RootMiscFeeCurr': 'GBP',
             'RootMiscFeeRate': '10.0'}]}
        self.__return_result(responses, ORSMessageType.AllocationReport.value)
        alloc_report = self.result.get_parameter('AllocationReportBlock')
        alloc_inst_id = alloc_report['ClientAllocID']
        # endregion

        # region check ready to book message
        no_misc_fees = {'NoRootMiscFeesList': [{"RootMiscFeeBasis": '2', "RootMiscFeeCurr": self.com_cur,
                                                "RootMiscFeeType": "22", 'RootMiscFeeRate': '10',
                                                'RootMiscFeeAmt': '10'}]}
        alloc_ignored_fields = ['Account', 'tag5120', 'AvgPx', 'Currency', 'RootCommTypeClCommBasis',
                                'RootOrClientCommission', 'RootOrClientCommissionCurrency', 'RootSettlCurrAmt']
        self.alloc_report.set_default_ready_to_book(self.fix_message)
        self.alloc_report.change_parameters({"NoRootMiscFeesList": no_misc_fees})
        self.fix_verifier_dc.check_fix_message_fix_standard(self.alloc_report, ignored_fields=alloc_ignored_fields)
        # endregion

        # region amend booking
        fee_list['RootMiscFeesBlock'][0]['RootMiscFeeRate'] = '5.0'
        fee_list['RootMiscFeesBlock'][0]['RootMiscFeeAmt'] = '5.0'
        self.allocation_instruction.set_amend_book(alloc_inst_id, exec_id, self.qty, new_avg_px)
        self.allocation_instruction.update_fields_in_component('AllocationInstructionBlock',
                                                               {
                                                                   'GrossTradeAmt': gross_currency_amt,
                                                                   'AvgPx': self.price,
                                                                   'Qty': self.qty,
                                                                   'InstrID': instrument_id,
                                                                   "Currency": self.cur,
                                                                   "AccountGroupID": self.client,
                                                                   'RootMiscFeesList': fee_list
                                                               })
        responses = self.java_api_manager.send_message_and_receive_response(self.allocation_instruction)
        self.__return_result(responses, ORSMessageType.AllocationReport.value)
        alloc_report = self.result.get_parameter('AllocationReportBlock')
        self.java_api_manager.compare_values({'RootMiscFeeRate':
                                                  fee_list['RootMiscFeesBlock'][0]['RootMiscFeeRate']},
                                              {'RootMiscFeeRate': alloc_report['RootMiscFeesList']['RootMiscFeesBlock'][0][
                                                   'RootMiscFeeRate']},
                                             'Check fees after amending booking')
        self.java_api_manager.compare_values({'RootMiscFeeAmt':
                                                  fee_list['RootMiscFeesBlock'][0]['RootMiscFeeRate']},
                                              {'RootMiscFeeAmt': alloc_report['RootMiscFeesList']['RootMiscFeesBlock'][0][
                                                   'RootMiscFeeAmt']},
                                             'Check fees after amending booking')
        # endregion

        # region approve block
        self.force_alloc_instr.set_default_approve(alloc_inst_id)
        self.java_api_manager.send_message(self.force_alloc_instr)
        # endregion

        # region allocate block
        self.confirmation.set_default_allocation(alloc_inst_id)
        self.confirmation.update_fields_in_component('ConfirmationBlock',
                                                     {'AllocAccountID': self.client_acc, "InstrID": instrument_id,
                                                      "AvgPx": new_avg_px})
        self.java_api_manager.send_message(self.confirmation)
        # endregion

        time.sleep(8)
        # region check ready to book message
        no_misc_fees = {'NoMiscFees': [{"MiscFeeAmt": '5', "MiscFeeCurr": self.com_cur,
                                                "MiscFeeType": "22"}]}
        alloc_ignored_fields = ['AvgPx', 'tag5120', 'CommissionData']
        self.conf_report.set_default_confirmation_new(self.fix_message)
        self.conf_report.change_parameters({'NoMiscFees': no_misc_fees})
        self.fix_verifier_dc.check_fix_message_fix_standard(self.conf_report, ignored_fields=alloc_ignored_fields)
        # endregion

    def __send_fix_orders(self):
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.bs_connectivity,
                self.client_for_rule,
                self.mic,
                int(self.price))
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                            self.client_for_rule,
                                                                                            self.mic,
                                                                                            int(self.price),
                                                                                            int(self.qty), 2)
            self.fix_message.change_parameters(self.params)
            response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(nos_rule)
            self.rule_manager.remove_rule(trade_rule)
        return response

    def __return_result(self, responses, message_type):
        for response in responses:
            if response.get_message_type() == message_type:
                self.result = response

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_commission_sender.clear_fees()
        self.rest_commission_sender.clear_commissions()
