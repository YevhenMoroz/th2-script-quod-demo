import logging
import time
from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from test_framework.fix_wrappers.FixManager import FixManager
from rule_management import RuleManager, Simulators
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7398(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.qty = "100"
        self.price1 = "50"
        self.price2 = "40"
        self.account1 = self.data_set.get_client_by_name('client_1')
        self.account2 = self.data_set.get_client_by_name('client_2')
        self.venue = self.data_set.get_mic_by_name('mic_1')
        self.fix_message_1 = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.fix_message_1.change_parameters({'OrderQtyData': {'OrderQty': self.qty}, "Price": self.price1,
                                              "Account": self.account1, 'ExDestination': self.venue,
                                              "Side": "2"})
        self.fix_message_2 = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.fix_message_2.change_parameters({'OrderQtyData': {'OrderQty': self.qty}, "Price": self.price2,
                                              "Account": self.account2, 'ExDestination': self.venue,
                                              "Side": "1"})
        self.client_for_rule1 = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        self.client_for_rule2 = self.data_set.get_venue_client_names_by_name('client_2_venue_1')
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.rule_manager = RuleManager(Simulators.equity)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.cl_ord_id = self.fix_message_1.get_parameter("ClOrdID")



    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create CO order
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message_1)
        order_id_1 = response[0].get_parameter("OrderID")
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message_2)
        order_id_2 = response[0].get_parameter("OrderID")
        # endregion
        # region accept CO order
        self.client_inbox.accept_order()
        self.client_inbox.accept_order()
        # endregion
        # region set up disclose flag
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, self.cl_ord_id[:-1]]).set_disclose_flag_via_order_book('manual', [1,2])
        # region split first order
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.fix_env.buy_side,
                                                                                 self.client_for_rule1,
                                                                                 self.venue,
                                                                                 float(self.price1))
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                           self.client_for_rule1, self.venue,
                                                                           float(self.price1), int(self.qty), delay=0)
            self.order_ticket.split_order([OrderBookColumns.order_id.value, order_id_1])
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(nos_rule)
            self.rule_manager.remove_rule(trade_rule)
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.fix_env.buy_side,
                                                                                                  self.client_for_rule2,
                                                                                                  self.venue,
                                                                                                  float(self.price2))
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                                            self.client_for_rule2,
                                                                                            self.venue,
                                                                                            float(self.price2),
                                                                                            int(self.qty), delay=0)
            self.order_ticket.split_order([OrderBookColumns.order_id.value, order_id_2])
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(nos_rule)
            self.rule_manager.remove_rule(trade_rule)

        # region mass execution
        self.order_book.complete_order(2, [OrderBookColumns.cl_ord_id.value, self.cl_ord_id[:-1]])
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, self.cl_ord_id[:-1]]).mass_execution_summary_at_average_price(2)
        # endregion
        # verify tags by minifix gtw
        self.exec_report.set_default_calculated(self.fix_message_1)
        self.exec_report.change_parameters({"AvgPx": self.price1, "Account": self.account1, "Side":"2", "VenueType":"*"})
        self.fix_verifier.check_fix_message(self.exec_report)
        self.exec_report.set_default_calculated(self.fix_message_2)
        self.exec_report.change_parameters({"AvgPx": self.price2, "Account": self.account2, "Side":"1", "VenueType":"*"})
        self.fix_verifier.check_fix_message(self.exec_report)
        # endregion
