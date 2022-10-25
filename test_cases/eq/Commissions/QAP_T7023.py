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
from test_framework.fix_wrappers.oms.FixMessageConfirmationReportOMS import FixMessageConfirmationReportOMS
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, MiddleOfficeColumns, \
    AllocationsColumns
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


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
        self.qty = self.fix_message.get_parameter("OrderQtyData")['OrderQty']
        self.mic = self.data_set.get_mic_by_name("mic_2")
        self.price = self.fix_message.get_parameter("Price")
        self.venue = self.data_set.get_venue_by_name("venue_2")
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.client_for_rule = self.data_set.get_venue_client_names_by_name("client_pt_4_venue_2")
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.mid_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.rule_manager = RuleManager(Simulators.equity)
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.fix_verifier_dc = FixVerifier(self.dc_connectivity, self.test_id)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.fee1 = self.data_set.get_fee_by_name('fee1')
        self.fee2 = self.data_set.get_fee_by_name('fee2')
        self.fee3 = self.data_set.get_fee_by_name('fee3')
        self.fee_type1 = self.data_set.get_misc_fee_type_by_name('stamp')
        self.fee_type2 = self.data_set.get_misc_fee_type_by_name('levy')
        self.fee_type3 = self.data_set.get_misc_fee_type_by_name('per_transac')
        self.params = {"ExDestination": self.mic, "Currency": self.cur, "Account": self.client}

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region send fees
        self.rest_commission_sender.clear_fees()
        self.rest_commission_sender.set_modify_fees_message(fee=self.fee1, fee_type=self.fee_type1)
        self.rest_commission_sender.change_message_params({"venueID": self.venue})
        self.rest_commission_sender.send_post_request()
        self.rest_commission_sender.set_modify_fees_message(fee=self.fee2, fee_type=self.fee_type2)
        self.rest_commission_sender.change_message_params({"venueID": self.venue})
        self.rest_commission_sender.send_post_request()
        self.rest_commission_sender.set_modify_fees_message(fee=self.fee3, fee_type=self.fee_type3)
        self.rest_commission_sender.change_message_params({"venueID": self.venue})
        self.rest_commission_sender.send_post_request()
        # endregion
        # region send order
        self.__send_fix_orders()
        filter_list_order = [OrderBookColumns.order_id.value, self.order_id]
        # endregion
        no_misc = {'NoMiscFees': [{'MiscFeeAmt': "*", 'MiscFeeCurr': '*', 'MiscFeeType': "10"},
                                  {'MiscFeeAmt': "*", 'MiscFeeCurr': '*', 'MiscFeeType': "6"}]}
        self.exec_report.set_default_filled(self.fix_message)
        self.exec_report.change_parameters(
            {'Currency': self.cur, 'SecondaryOrderID': '*', 'Text': '*', 'LastMkt': '*',
             "ReplyReceivedTime": "*", "CommissionData": "*",
             "Account": self.client,
             'MiscFeesGrp': no_misc})
        self.exec_report.remove_parameter('SettlCurrency')
        self.fix_verifier.check_fix_message_fix_standard(self.exec_report)
        # endregion
        # region  book order
        self.mid_office.book_order(filter_list_order)
        # endregion
        # region check 35=J message
        no_misc_list = {'NoRootMiscFeesList': [
            {'RootMiscFeeBasis': '*', 'RootMiscFeeCurr': '*', 'RootMiscFeeType': '10', 'RootMiscFeeRate': '*',
             'RootMiscFeeAmt': '*'}]}
        allocation_report = FixMessageAllocationInstructionReportOMS()
        allocation_report.set_default_ready_to_book(self.fix_message)
        allocation_report.change_parameters({"AvgPx": "*", "Currency": "*",
                                             'tag5120': "*", 'RootSettlCurrAmt': '*', 'RootOrClientCommission': '*',
                                             'RootOrClientCommissionCurrency': '*', 'RootCommTypeClCommBasis': '*',
                                             'NoRootMiscFeesList': no_misc_list})
        allocation_report.remove_parameters(["AllocInstructionMiscBlock1"])
        self.fix_verifier_dc.check_fix_message_fix_standard(allocation_report)
        # endregion
        # region book order
        qty_to_alloc = str(int(int(self.qty) / 2))
        self.mid_office.approve_block([MiddleOfficeColumns.order_id.value, self.order_id])
        alloc_block = [{AllocationsColumns.security_acc.value: self.client_acc1,
                        AllocationsColumns.alloc_qty.value: qty_to_alloc},
                       {AllocationsColumns.security_acc.value: self.client_acc2,
                        AllocationsColumns.alloc_qty.value: qty_to_alloc}]
        self.mid_office.set_modify_ticket_details(arr_allocation_param=alloc_block, is_alloc_amend=True)
        self.mid_office.allocate_block([MiddleOfficeColumns.order_id.value, self.order_id])
        # endregion
        # region check Allocation Report
        self.mid_office.extract_allocation_sub_lvl()
        # no_misc_list_acc1 = {'NoRootMiscFeesList': [
        #     {'RootMiscFeeBasis': '*', 'RootMiscFeeCurr': '*', 'RootMiscFeeType': '5', 'RootMiscFeeRate': '*',
        #      'RootMiscFeeAmt': '*'}]}
        # allocation_report2 = FixMessageAllocationInstructionReportOMS().set_default_preliminary(self.fix_message)
        # allocation_report2.change_parameters({'AllocAccount': self.client_acc1,
        #                                      'AllocQty': qty_to_alloc, 'NoRootMiscFeesList': no_misc_list_acc1,
        #                                      'RootCommTypeClCommBasis': "*", 'AvgPx': "*", 'Currency': '*',
        #                                      "RootOrClientCommission": "*", "AllocType": "*",
        #                                      "AllocInstructionMiscBlock1": "*", "tag5120": "*",
        #                                      "RootOrClientCommissionCurrency": "*", "RootSettlCurrAmt": "*"})
        # self.fix_verifier_dc.check_fix_message_fix_standard(allocation_report2, ['AllocType', "AllocAccount"])
        # allocation_report2.change_parameters({"AllocAccount": self.client_acc2})
        # allocation_report2.remove_parameter('NoRootMiscFeesList')
        # self.fix_verifier_dc.check_fix_message_fix_standard(allocation_report2, ["AllocAccount", 'AllocType'])
        # endregion
        # region check Confirmation Report for first account
        conf_report = FixMessageConfirmationReportOMS(self.data_set).set_default_confirmation_new(self.fix_message)
        conf_report.change_parameters(
            {"Account": self.client, "AllocAccount": self.client_acc1, "AvgPx": "*", "AllocQty": qty_to_alloc,
             "Currency": "*", "tag5120": "*", 'NoMiscFees': no_misc, 'CommissionData': "*"})
        conf_report.remove_parameters(["AllocInstructionMiscBlock1"])
        self.fix_verifier_dc.check_fix_message_fix_standard(conf_report,
                                                            ["OrderID", "ConfirmTransType", "AllocAccount"])
        # endregion
        # region check Confirmation Report for second account
        conf_report.change_parameters(
            {"AllocAccount": self.client_acc2})
        self.fix_verifier_dc.check_fix_message_fix_standard(conf_report,
                                                            ["OrderID", "ConfirmTransType", "AllocAccount"])
        # endregion
        self.exec_report.change_parameters(
            {'NoMiscFees': no_misc, 'QuodTradeQualifier': "*", 'BookID': "*", "NoParty": "*", "tag5120": "*",
             "ExecBroker": "*"})
        self.exec_report.remove_parameters(['ReplyReceivedTime', 'MiscFeesGrp', 'Parties', 'TradeReportingIndicator'])
        self.fix_verifier_dc.check_fix_message_fix_standard(self.exec_report)

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
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(nos_rule)
            self.rule_manager.remove_rule(trade_rule)


    def __check_allocation_sub_tab(self):
        self.mid_office.extract_allocation_sub_lvl()