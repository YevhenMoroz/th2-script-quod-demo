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
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.java_api_constants import JavaApiFields, OrderReplyConst
from test_framework.java_api_wrappers.oms.ors_messges.AllocationInstructionOMS import AllocationInstructionOMS
from test_framework.java_api_wrappers.oms.ors_messges.ComputeBookingFeesCommissionsRequestOMS import \
    ComputeBookingFeesCommissionsRequestOMS
from test_framework.java_api_wrappers.oms.ors_messges.DFDManagementBatchOMS import DFDManagementBatchOMS
from test_framework.java_api_wrappers.oms.ors_messges.TradeEntryOMS import TradeEntryOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class QAP_T7028(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.response = None
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.java_api_connectivity = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.bs_connectivity = self.fix_env.buy_side
        self.ss_connectivity = self.fix_env.sell_side
        self.dc_connectivity = self.fix_env.drop_copy
        self.client = self.data_set.get_client_by_name("client_com_1")
        self.cur = self.data_set.get_currency_by_name('currency_3')
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit('instrument_3')
        self.java_api_manager = JavaApiManager(self.java_api_connectivity, self.test_id)
        self.qty = '200'
        self.mic = self.data_set.get_mic_by_name("mic_2")
        self.price = '10'
        self.venue = self.data_set.get_venue_by_name("venue_2")
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.rule_client = self.data_set.get_venue_client_names_by_name("client_com_1_venue_2")
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.mid_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.fix_verifier_dc = FixVerifier(self.dc_connectivity, self.test_id)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.comp_comm = ComputeBookingFeesCommissionsRequestOMS(self.data_set)
        self.fee1 = self.data_set.get_fee_by_name('fee1')
        self.fee2 = self.data_set.get_fee_by_name('fee2')
        self.fee_type1 = self.data_set.get_misc_fee_type_by_name('stamp')
        self.fee_type2 = self.data_set.get_misc_fee_type_by_name('value_added_tax')
        self.params = {"ExDestination": self.mic, "Currency": self.cur, "Account": self.client, 'Price': self.price,
                       'OrderQtyData': {'OrderQty': self.qty}}
        self.currency = self.data_set.get_currency_by_name('currency_2')  # GBP
        self.allocation_instruction = AllocationInstructionOMS(self.data_set)
        self.trade_entry_request = TradeEntryOMS(self.data_set)
        self.complete_order = DFDManagementBatchOMS(self.data_set)
        self.rule_manager = RuleManager(Simulators.equity)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region send fees
        self.rest_commission_sender.clear_commissions()
        self.rest_commission_sender.clear_fees()
        commission_profile_stamp = self.data_set.get_comm_profile_by_name('perc_amt')
        commission_profile_vat = self.data_set.get_comm_profile_by_name('bas_qty')
        self.rest_commission_sender.set_modify_fees_message(fee=self.fee1, fee_type=self.fee_type1,
                                                            comm_profile=commission_profile_stamp)
        self.rest_commission_sender.change_message_params({"venueID": self.venue})
        self.rest_commission_sender.send_post_request()
        self.rest_commission_sender.set_modify_fees_message(fee=self.fee2, fee_type=self.fee_type2,
                                                            comm_profile=commission_profile_vat)
        self.rest_commission_sender.change_message_params({"venueID": self.venue})
        self.rest_commission_sender.send_post_request()
        # endregion

        # region execute order
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.bs_connectivity,
                                                                                                  self.rule_client,
                                                                                                  self.mic,
                                                                                                  int(self.price))
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                            self.rule_client,
                                                                                            self.mic,
                                                                                            int(self.price),
                                                                                            int(self.qty), 2)
            self.fix_message.change_parameters(self.params)
            self.response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(nos_rule)
            self.rule_manager.remove_rule(trade_rule)
        time.sleep(5)
        exec_report = self.__get_fix_message({'ExecType': 'F'})
        order_id = exec_report["OrderID"]
        cl_order_id = exec_report['ClOrdID']
        vat_amt = str(float(self.qty) / 10000)
        stamp_rate = str(5)
        stamp_amount = str(int((float(self.qty) * float(self.price) * float(stamp_rate) / 10000)))
        exec_id = exec_report["ExecID"]

        self.java_api_manager.compare_values(
            {'ExecType': exec_report["ExecType"], 'OrdStatus': exec_report["OrdStatus"],
             'MiscFeesGrp': {'NoMiscFees': [{'MiscFeeAmt': stamp_amount, 'MiscFeeCurr': 'GBP', 'MiscFeeType': '5'}]}},
            exec_report,
            "Check the execution of order")
        # endregion

        # region get values from booking ticket
        instrument_id = self.data_set.get_instrument_id_by_name('instrument_3')
        gross_currency_amt = str(int(self.qty) * int(self.price))
        post_trade_sts = OrderReplyConst.PostTradeStatus_RDY.value
        self.comp_comm.set_list_of_order_alloc_block(cl_order_id, order_id, post_trade_sts)
        self.comp_comm.set_list_of_exec_alloc_block(self.qty, exec_id, self.price, post_trade_sts)
        self.comp_comm.set_default_compute_booking_request(self.qty)
        self.comp_comm.update_fields_in_component(JavaApiFields.ComputeBookingFeesCommissionsRequestBlock.value,
                                                  {'AccountGroupID': self.client, 'AvgPx': '0.100000000'})
        responses = self.java_api_manager.send_message_and_receive_response(self.comp_comm)
        self.__return_result(responses, ORSMessageType.ComputeBookingFeesCommissionsReply.value)
        fee_list_exp = {"RootMiscFeesBlock": [
            {
                "RootMiscFeeAmt": str(float(stamp_amount)),
                "RootMiscFeeRate": str(float(stamp_rate)),
                "RootMiscFeeCurr": "GBP",
                "RootMiscFeeType": "STA",
                "RootMiscFeeBasis": "P"
            },
            {
                "RootMiscFeeBasis": "B",
                "RootMiscFeeAmt": vat_amt,
                "RootMiscFeeCurr": "GBP",
                "RootMiscFeeType": "VAT",
                "RootMiscFeeRate": "1.0"
            }
        ]}
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
        alloc_report = self.java_api_manager.get_last_message(ORSMessageType.AllocationReport.value,
                                               JavaApiFields.BookingAllocInstructionID.value).get_parameter(
            JavaApiFields.AllocationReportBlock.value)
        common_fee_amount = str(float(vat_amt) + float(stamp_amount))
        total_fee = {'RootCommission': common_fee_amount, 'RootCommCurrency': 'GBP'}
        self.java_api_manager.compare_values(
            {'RootCommissionDataBlock': total_fee}, alloc_report,
            "Check values in the Alloc Report (TotalFees)")
        for fee in fee_list_exp[JavaApiFields.RootMiscFeesBlock.value]:
            self.java_api_manager.compare_values({
                'IsMiscFeeValuesPresent': True},
                {'IsMiscFeeValuesPresent': fee in alloc_report[JavaApiFields.RootMiscFeesList.value][
                    JavaApiFields.RootMiscFeesBlock.value]},
                f"Check values in the Alloc Report {fee}")
        # endregion

        # region check 35=J message
        no_misc_list = {'NoRootMiscFeesList': [
            {'RootMiscFeeBasis': '3',
             'RootMiscFeeCurr': self.currency,
             'RootMiscFeeType': '22', 'RootMiscFeeRate': '1',
             'RootMiscFeeAmt': vat_amt},
            {'RootMiscFeeBasis': '2', 'RootMiscFeeCurr': self.currency, 'RootMiscFeeType': '5',
             'RootMiscFeeRate': stamp_rate,
             'RootMiscFeeAmt': stamp_amount}]}
        ignored_list = ["AvgPx", "Currency", 'tag5120', 'RootSettlCurrAmt', 'RootOrClientCommission',
                        'RootOrClientCommissionCurrency', 'RootCommTypeClCommBasis', "AllocInstructionMiscBlock1",
                        'RootSettlCurrAmt', 'SettlType', 'Account', 'OrderAvgPx', 'ExecAllocGrp']
        allocation_report = FixMessageAllocationInstructionReportOMS()
        allocation_report.set_default_ready_to_book(self.fix_message)
        allocation_report.change_parameters({'NoRootMiscFeesList': no_misc_list})
        self.fix_verifier_dc.check_fix_message_fix_standard(allocation_report, ignored_fields=ignored_list)
        # endregion

    def __return_result(self, responses, message_type):
        for response in responses:
            if response.get_message_type() == message_type:
                self.result = response

    def __get_fix_message(self, parameter: dict):
        self.response.reverse()
        for i in range(len(self.response)):
            for j in parameter.keys():
                if self.response[i].get_parameters()[j] == parameter[j]:
                    return self.response[i].get_parameters()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_commission_sender.clear_fees()
