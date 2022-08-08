import logging
import time
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, ExecSts, SecondLevelTabs
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T6966(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.client = self.data_set.get_client_by_name("client_co_1")
        self.client_acc = self.data_set.get_account_by_name("client_co_1_acc_1")
        self.change_params = {'Account': self.client}
        self.qty = self.fix_message.get_parameter("OrderQtyData")['OrderQty']
        self.price = self.fix_message.get_parameter("Price")
        self.fix_message.change_parameters(self.change_params)
        self.rule_manager = RuleManager(Simulators.equity)
        self.mic = self.data_set.get_mic_by_name("mic_1")
        self.cl_ord_id = self.fix_message.get_parameter('ClOrdID')
        self.client_for_rule = self.data_set.get_venue_client_names_by_name("client_co_1_venue_1")
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.qty_to_split = "50"
        self.qty_to_exec = "25"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create and accept order
        self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        self.client_inbox.accept_order()
        # endregion
        # region split and execute order
        nos_rule = None
        trade_rule = None
        try:

            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.fix_env.buy_side,
                                                                                                  self.client_for_rule,
                                                                                                  self.mic,
                                                                                                  int(self.price))
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                                            self.client_for_rule,
                                                                                            self.mic, int(self.price),
                                                                                            int(self.qty_to_exec), 2)
            self.order_ticket.set_order_details(qty=self.qty_to_split)
            self.order_ticket.split_order([OrderBookColumns.cl_ord_id.value, self.cl_ord_id])
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(nos_rule)
            self.rule_manager.remove_rule(trade_rule)
            # endregion
            # region split and execute order
            self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, self.cl_ord_id]).check_second_lvl_fields_list(
                {OrderBookColumns.exec_sts.value: ExecSts.partially_filled.value})
            expect_res = self.order_book.extract_2lvl_fields(SecondLevelTabs.executions.value,
                                                             [OrderBookColumns.unmatched_qty.value], [1],
                                                             {OrderBookColumns.cl_ord_id.value: self.cl_ord_id})
            print(expect_res)
            self.order_book.compare_values({OrderBookColumns.unmatched_qty.value: "0"},
                                         expect_res[0],
                                           "Check Ummatched qty in Electronic Execution ")
            # endregion
