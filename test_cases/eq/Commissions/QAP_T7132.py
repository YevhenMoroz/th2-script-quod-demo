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
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7132(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.bs_connectivity = self.fix_env.buy_side
        self.ss_connectivity = self.fix_env.sell_side
        self.dc_connectivity = self.fix_env.drop_copy
        self.client = self.data_set.get_client_by_name("client_com_1")
        self.client_acc = self.data_set.get_account_by_name("client_com_1_acc_1")
        self.cur = self.data_set.get_currency_by_name('currency_3')
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit("instrument_3")
        self.qty = self.fix_message.get_parameter('OrderQtyData')['OrderQty']
        self.mic = self.data_set.get_mic_by_name("mic_2")
        self.venue = self.data_set.get_venue_by_name("venue_2")
        self.price = "10"
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.client_for_rule = self.data_set.get_venue_client_names_by_name("client_com_1_venue_2")
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.mid_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.fix_verifier_dc = FixVerifier(self.dc_connectivity, self.test_id)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.comm = self.data_set.get_commission_by_name("commission1")
        self.fee = self.data_set.get_fee_by_name('fee1')
        self.comm_profile = self.data_set.get_comm_profile_by_name("perc_amt")
        self.com_cur = self.data_set.get_currency_by_name('currency_2')

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        self.rest_commission_sender.clear_fees()
        self.rest_commission_sender.set_modify_fees_message(fee=self.fee,
                                                            comm_profile=self.comm_profile).change_message_params(
            {'venueID': self.venue}).send_post_request()
        self.rest_commission_sender.clear_commissions()
        self.rest_commission_sender.set_modify_client_commission_message(commission=self.comm, account=self.client_acc,
                                                                         comm_profile=self.comm_profile).send_post_request()
        # endregion
        # region send order
        self.__send_fix_orders("1")
        order_id1 = self.response[0].get_parameter("OrderID")
        self.__send_fix_orders("2")
        order_id2 = self.response[0].get_parameter("OrderID")
        # endregion
        # region check ExecutionReports of first order
        self.exec_report.set_default_filled(self.fix_message)
        no_misc = {"MiscFeeAmt": '0.5', "MiscFeeCurr": self.com_cur,
                   "MiscFeeType": "4"}
        comm_data = {"Commission": "0.5", "CommType": "3"}
        self.exec_report.change_parameters(
            {'Side': "1", 'Currency': self.cur, 'SecondaryOrderID': '*', 'Text': '*', 'LastMkt': '*',
             "ReplyReceivedTime": "*", "Account": self.client_acc, "MiscFeesGrp": {"NoMiscFees": [no_misc]},
             "CommissionData": comm_data})
        self.exec_report.remove_parameter('SettlCurrency')
        self.fix_verifier.check_fix_message_fix_standard(self.exec_report, ["Side", "ExecType"])
        # region check ExecutionReports of second order
        self.exec_report.change_parameters(
            {'Side': "2"})
        self.fix_verifier.check_fix_message_fix_standard(self.exec_report, ["Side", "ExecType"])
        # endregion
        # region mass book order
        self.order_book.mass_book([1, 2])
        # endregion
        # region check commission and fee in booking of first order
        alloc_report = FixMessageAllocationInstructionReportOMS().set_default_ready_to_book(
            self.fix_message)
        no_root_misc = {"RootMiscFeeBasis": "0", "RootMiscFeeCurr": self.com_cur,
                        "RootMiscFeeType": no_misc['MiscFeeType'],
                        "RootMiscFeeRate": no_misc['MiscFeeAmt'], "RootMiscFeeAmt": no_misc['MiscFeeAmt']}
        alloc_report.change_parameters(
            {"Account": self.client, "AvgPx": "*", "Currency": "*", "tag5120": "*",
             'RootOrClientCommission': comm_data['Commission'], 'RootCommTypeClCommBasis': comm_data['CommType'],
             "RootOrClientCommissionCurrency": self.com_cur,
             'NoRootMiscFeesList': {"NoRootMiscFeesList": [no_root_misc]}})
        alloc_report.remove_parameters(["BookingType", 'AllocInstructionMiscBlock1'])
        self.fix_verifier_dc.check_fix_message_fix_standard(alloc_report, ["Side"])
        # endregion
        # region check commission and fee in booking of first order
        alloc_report.change_parameters(
            {"Account": self.client, "Side": "1"})
        self.fix_verifier_dc.check_fix_message_fix_standard(alloc_report, ["Side"])
        # endregion

    def __send_fix_orders(self, side: str):
        try:
            nos_rule = self.rule_manager. \
                add_NewOrdSingleExecutionReportTradeByOrdQty_FIXStandard(self.bs_connectivity,
                                                                         self.client_for_rule,
                                                                         self.mic,
                                                                         float(self.price), float(self.price),
                                                                         int(self.qty), int(self.qty), 1)
            self.fix_message.change_parameters(
                {"Side": side, "Price": self.price, "Account": self.client,
                 "ExDestination": self.mic,
                 "Currency": self.data_set.get_currency_by_name("currency_3"),
                 'PreAllocGrp': {'NoAllocs': [{'AllocAccount': self.client_acc,
                                               'AllocQty': self.qty}]}})
            self.response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(nos_rule)
