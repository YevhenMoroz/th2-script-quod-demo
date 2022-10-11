import logging
import time
from pathlib import Path
from custom import basic_custom_actions as bca
from rule_management import Simulators, RuleManager
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, DiscloseExec
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7399(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.rule_manager = RuleManager(Simulators.equity)
        self.client_for_rule = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        self.qty = self.fix_message.get_parameter('OrderQtyData')['OrderQty']
        self.price = self.fix_message.get_parameter('Price')
        self.exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.account = self.fix_message.get_parameter('Account')
        self.price_sum = "22.2"
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declarations
        # region create CO orders
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id1 = response[0].get_parameter("OrderID")
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id2 = response[0].get_parameter("OrderID")
        # endregion
        # region accept orders
        self.client_inbox.accept_order()
        self.client_inbox.accept_order()
        # endregion
        # region set manual disclose flag
        self.order_book.set_disclose_flag_via_order_book("manual", [1, 2])
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id1]).check_order_fields_list(
            {OrderBookColumns.disclose_exec.value: DiscloseExec.manual.value})
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id2]).check_order_fields_list(
            {OrderBookColumns.disclose_exec.value: DiscloseExec.manual.value})
        nos_rule = None
        trade_rule = None
        # endregion
        # region split and exec order
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.fix_env.buy_side,
                                                                                                  self.client_for_rule,
                                                                                                  self.exec_destination,
                                                                                                  float(self.price))
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                                            self.client_for_rule,
                                                                                            self.exec_destination,
                                                                                            float(self.price),
                                                                                            int(self.qty),
                                                                                            delay=0)
            self.order_ticket.split_order(filter_list=[OrderBookColumns.order_id.value, order_id1])
            self.order_ticket.split_order(filter_list=[OrderBookColumns.order_id.value, order_id2])
        except Exception:
            logger.error("Error execution", exc_info=True)
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(nos_rule)
            self.rule_manager.remove_rule(trade_rule)
        # endregion
        # region mass exec
        self.order_book.mass_execution_summary(2, self.price_sum)
        # endregion
        # verify LastPX by minifix gtw
        time.sleep(5)
        self.exec_report.set_default_calculated(self.fix_message)
        self.exec_report.change_parameters({"LastPx": self.price_sum, "VenueType":"*", 'OrderID': order_id1})
        self.fix_verifier.check_fix_message(self.exec_report, ['OrderID', 'ExecType'])
        self.exec_report.change_parameters({'OrderID': order_id2})
        self.fix_verifier.check_fix_message(self.exec_report, ['OrderID', 'ExecType'])
        # endregion
