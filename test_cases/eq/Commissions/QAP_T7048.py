import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageAllocationInstructionReportOMS import \
    FixMessageAllocationInstructionReportOMS
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.win_gui_wrappers.fe_trading_constant import MiddleOfficeColumns
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7048(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.bs_connectivity = self.fix_env.buy_side
        self.ss_connectivity = self.fix_env.sell_side
        self.dc_connectivity = self.fix_env.drop_copy
        self.client = self.data_set.get_client_by_name("client_com_1")
        self.cur = self.data_set.get_currency_by_name('currency_3')
        self.case_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit('instrument_3')
        self.qty = self.fix_message.get_parameter("OrderQtyData")['OrderQty']
        self.mic = self.data_set.get_mic_by_name("mic_2")
        self.price = self.fix_message.get_parameter("Price")
        self.venue = self.data_set.get_venue_by_name("venue_2")
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.case_id, self.data_set)
        self.client_for_rule = self.data_set.get_venue_client_names_by_name("client_com_1_venue_2")
        self.fix_manager = FixManager(self.ss_connectivity, self.case_id)
        self.mid_office = OMSMiddleOffice(self.case_id, self.session_id)
        self.rule_manager = RuleManager(Simulators.equity)
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.case_id)
        self.fix_verifier_dc = FixVerifier(self.dc_connectivity, self.case_id)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.fee = self.data_set.get_fee_by_name('fee1')
        self.comm_prof = self.data_set.get_comm_profile_by_name('abs_amt')
        self.fee_type = self.data_set.get_misc_fee_type_by_name('value_added_tax')
        self.params = {"ExDestination": self.mic, "Currency": self.cur, "Account": self.client}
        self.new_rate = '1'

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region send fees
        self.rest_commission_sender.clear_fees()
        self.rest_commission_sender.set_modify_fees_message(fee=self.fee, fee_type=self.fee_type, recalculate=False,
                                                            comm_profile=self.comm_prof)
        self.rest_commission_sender.change_message_params({"venueID": self.venue})
        self.rest_commission_sender.send_post_request()
        # endregion
        # region send order
        self.__send_fix_orders()
        # endregion
        # region check execution
        self.exec_report.set_default_filled(self.fix_message)
        self.exec_report.change_parameters(
            {'Currency': self.cur, 'SecondaryOrderID': '*', 'Text': '*', 'LastMkt': '*',
             "ReplyReceivedTime": "*", "CommissionData": "*",
             "Account": self.client,
             'MiscFeesGrp': "*"})
        self.exec_report.remove_parameter('SettlCurrency')
        self.fix_verifier.check_fix_message_fix_standard(self.exec_report)
        # endregion
        # region book order
        self.mid_office.book_order([MiddleOfficeColumns.order_id.value, self.order_id])
        self.mid_office.amend_block([MiddleOfficeColumns.order_id.value, self.order_id])
        # endregion
        # region check 35=J message
        no_misc_list = {'NoRootMiscFeesList': [
            {'RootMiscFeeBasis': '*', 'RootMiscFeeCurr': '*', 'RootMiscFeeType': '22', 'RootMiscFeeRate': '100',
             'RootMiscFeeAmt': '*'}]}
        allocation_report = FixMessageAllocationInstructionReportOMS()
        allocation_report.set_default_ready_to_book(self.fix_message)
        allocation_report.change_parameters({"AvgPx": "*", "Currency": "*",
                                             'tag5120': "*", 'RootSettlCurrAmt': '*', 'RootOrClientCommission': '*',
                                             'RootOrClientCommissionCurrency': '*', 'RootCommTypeClCommBasis': '*',
                                             'NoRootMiscFeesList': no_misc_list, "AllocInstructionMiscBlock1": "*"})
        self.fix_verifier_dc.check_fix_message_fix_standard(allocation_report)
        # endregion
        # region amend booking
        self.mid_office.set_modify_ticket_details(remove_fee=True, fee_type=self.fee_type,
                                                  fee_basis=self.data_set.get_commission_basis('comm_basis_1'),
                                                  fee_rate=self.new_rate)
        self.mid_office.amend_block([MiddleOfficeColumns.order_id.value, self.order_id])
        total_comm = self.mid_office.extract_list_of_block_fields([MiddleOfficeColumns.total_fees.value],
                                                                  [MiddleOfficeColumns.order_id.value, self.order_id])
        self.mid_office.compare_values({MiddleOfficeColumns.total_fees.value: self.new_rate}, total_comm,
                                       "Check Total Fees in booking")
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
            self.response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
            self.order_id = self.response[0].get_parameter("OrderID")
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(nos_rule)
            self.rule_manager.remove_rule(trade_rule)
