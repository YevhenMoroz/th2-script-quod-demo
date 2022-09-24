import logging
import time
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, PostTradeStatuses, MiddleOfficeColumns
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7383(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.mid_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.fix_verifier_dc = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit("instrument_3")
        self.client = self.data_set.get_client_by_name("client_com_1")
        self.cur = self.data_set.get_currency_by_name('currency_3')
        self.com_cur = self.data_set.get_currency_by_name('currency_2')
        self.client_acc = self.data_set.get_account_by_name("client_com_1_acc_1")
        self.mic = self.data_set.get_mic_by_name("mic_2")
        self.change_params = {'Account': self.client, "Currency": self.cur, "ExDestination": self.mic}
        self.fix_message.change_parameters(self.change_params)
        self.qty = self.fix_message.get_parameter('OrderQtyData')['OrderQty']
        self.price = self.fix_message.get_parameter("Price")
        self.venue = self.data_set.get_venue_by_name("venue_2")
        self.rule_manager = RuleManager(Simulators.equity)
        self.client_for_rule = self.data_set.get_venue_client_names_by_name("client_com_1_venue_2")
        self.cl_ord_id = self.fix_message.get_parameter('ClOrdID')
        self.comm_profile = self.data_set.get_comm_profile_by_name("perc_amt")
        self.comm = self.data_set.get_commission_by_name("commission1")
        self.fee = self.data_set.get_fee_by_name('fee1')

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        self.rest_commission_sender.clear_fees()
        self.rest_commission_sender.set_modify_fees_message(fee=self.fee,
                                                            comm_profile=self.comm_profile).change_message_params(
            {'venueID': self.venue}).send_post_request()
        self.rest_commission_sender.clear_commissions()
        self.rest_commission_sender.set_modify_client_commission_message(commission=self.comm,
                                                                         comm_profile=self.comm_profile).send_post_request()
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.fix_env.buy_side,
                                                                                                  self.client_for_rule,
                                                                                                  self.mic,
                                                                                                  int(self.price))
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                                            self.client_for_rule,
                                                                                            self.mic, int(self.price),
                                                                                            int(self.qty), 2)

            self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(nos_rule)
            self.rule_manager.remove_rule(trade_rule)
        # endregion
        # region check exec
        no_misc = {"MiscFeeAmt": '1', "MiscFeeCurr": self.com_cur,
                   "MiscFeeType": "4"}
        comm_data = {"Commission": "1", "CommType": "3"}
        execution_report = FixMessageExecutionReportOMS(self.data_set).set_default_filled(self.fix_message)
        execution_report.change_parameters(
            {'ReplyReceivedTime': "*", 'Currency': self.cur, 'LastMkt': "*", 'Text': "*",
             "Account": self.client, "MiscFeesGrp": {"NoMiscFees": [no_misc]}, "CommissionData": comm_data})
        execution_report.remove_parameters(
            ['SettlCurrency'])
        self.fix_verifier.check_fix_message_fix_standard(execution_report)
        # endregion
        # region check ready_to_book order sts
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, self.cl_ord_id]).check_order_fields_list(
            {OrderBookColumns.post_trade_status.value: PostTradeStatuses.ready_to_book.value})
        # endregion
        # region book order
        self.mid_office.set_modify_ticket_details(remove_comm=True, remove_fee=True)
        self.mid_office.book_order([OrderBookColumns.cl_ord_id.value, self.cl_ord_id])
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, self.cl_ord_id]).check_order_fields_list(
            {OrderBookColumns.post_trade_status.value: PostTradeStatuses.booked.value})
        # endregion
        # region check total fees
        total_fees = self.mid_office.extract_block_field(MiddleOfficeColumns.total_fees.value)
        self.mid_office.compare_values({MiddleOfficeColumns.total_fees.value: ''}, total_fees, "Check Total Fees")
        # endregion
        # region check total fees
        total_comm = self.mid_office.extract_block_field(MiddleOfficeColumns.client_comm.value)
        self.mid_office.compare_values({MiddleOfficeColumns.client_comm.value: ''}, total_comm,
                                       "Check Total Comm")
        # endregion
