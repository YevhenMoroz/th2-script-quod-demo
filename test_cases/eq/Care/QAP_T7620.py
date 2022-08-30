import logging
import time
from pathlib import Path
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, ExecSts, \
    DiscloseExec, TradeBookColumns, SecondLevelTabs
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket
from test_framework.win_gui_wrappers.oms.oms_trades_book import OMSTradesBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7620(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.qty = "30000"
        self.price = "5"
        self.price_for_second_exec_sum = "20"
        self.first_split_qty = "20000"
        self.second_split_qty = "10000"
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.fix_message.change_parameter('OrderQtyData', {'OrderQty': self.qty})
        self.fix_message.change_parameter("Price", self.price)
        self.fix_message.change_parameter("Side", "2")
        self.fix_execution_message = FixMessageExecutionReportOMS(self.data_set).set_default_calculated(
            self.fix_message)
        self.trade_book = OMSTradesBook(self.test_id, self.session_id)
        self.rule_manager = RuleManager(Simulators.equity)
        self.client_for_rule = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        self.exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side, self.test_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create CO order
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = response[0].get_parameter("OrderID")
        # endregion
        # region accept order
        self.client_inbox.accept_order()
        # endregion
        # region check order open status
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).check_order_fields_list(
            {OrderBookColumns.sts.value: ExecSts.open.value})
        # endregion
        # region set manual disclise flag
        self.order_book.set_disclose_flag_via_order_book("manual")
        # endregion
        # region check disclose execution
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).check_order_fields_list(
            {OrderBookColumns.disclose_exec.value: DiscloseExec.manual.value})
        # endregion
        # region split order
        self.__split_order_and_execute(self.first_split_qty)
        # endregion
        # region  execution summary order
        self.order_book.exec_summary(price=self.price, filter_dict={OrderBookColumns.order_id.value: order_id})
        execid = self.order_book.extract_2lvl_fields(SecondLevelTabs.executions.value,
            [OrderBookColumns.exec_id.value], [2], {OrderBookColumns.order_id.value: order_id})
        print(execid)
        # endregion
        # region fix_verifier
        self.fix_execution_message.change_parameters(
            {'TradeDate': '*', 'LastMkt': '*', "VenueType": "*", "LastPx": self.price, "AvgPx": "5", "ExecID": execid[0]['ExecID']})
        self.fix_verifier.check_fix_message_fix_standard(self.fix_execution_message)
        # endregion
        # region split order
        self.__split_order_and_execute(self.second_split_qty)
        self.order_book.exec_summary(price=self.price_for_second_exec_sum,
                                     filter_dict={OrderBookColumns.order_id.value: order_id})
        execid = self.order_book.extract_2lvl_fields(SecondLevelTabs.executions.value,
                                                     [OrderBookColumns.exec_id.value], [4],
                                                     {OrderBookColumns.order_id.value: order_id})
        # endregion
        # region fix_verifier
        sec = FixMessageExecutionReportOMS(self.data_set).set_default_calculated(
            self.fix_message).change_parameters(
            {'TradeDate': '*', 'LastMkt': '*', "VenueType": "*", "LastPx": self.price_for_second_exec_sum,
             "AvgPx": "10", "ExecID": execid[0]['ExecID'], "LastQty":self.second_split_qty, "LeavesQty":"0"})
        self.fix_verifier.check_fix_message_fix_standard(sec, key_parameters=["ExecID", "LastPx", "AvgPx"])

    def __split_order_and_execute(self, qty: str):
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.fix_env.buy_side,
                                                                                                  self.client_for_rule,
                                                                                                  self.exec_destination,
                                                                                                  float(self.price))
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                                            self.client_for_rule,
                                                                                            self.exec_destination,
                                                                                            float(self.price),
                                                                                            int(qty),
                                                                                            delay=0)
            # endregion
            # region split order
            self.order_ticket.set_order_details(qty=qty)
            self.order_ticket.split_order()
        except Exception:
            logger.setLevel(logging.DEBUG)
            logging.debug('RULE WORK CORRECTLY. (: NOT :)')
        finally:
            time.sleep(10)
            self.rule_manager.remove_rule(trade_rule)
            self.rule_manager.remove_rule(nos_rule)
