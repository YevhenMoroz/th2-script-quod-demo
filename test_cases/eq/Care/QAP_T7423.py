import logging
import time
from pathlib import Path
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from test_framework.fix_wrappers.FixManager import FixManager
from rule_management import RuleManager, Simulators
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, ExecSts, SecondLevelTabs, \
    TradeBookColumns, MatchWindowsColumns, ExecType
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket
from test_framework.win_gui_wrappers.oms.oms_trades_book import OMSTradesBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7423(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.qty = "100"
        self.qty_match = "50"
        self.price = "10"
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message_care = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.fix_message_care.change_parameter('OrderQtyData', {'OrderQty': self.qty})
        self.fix_message_care.change_parameter("Price", self.price)
        self.fix_message_dma = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit()
        self.exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.fix_message_dma.change_parameter('OrderQtyData', {'OrderQty': self.qty})
        self.fix_message_dma.change_parameter("Price", self.price)
        self.fix_message_dma.change_parameter('Account', self.data_set.get_client_by_name("client_co_1"))
        self.client_for_rule = self.data_set.get_venue_client_names_by_name('client_co_1_venue_1')
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.rule_manager = RuleManager(Simulators.equity)
        self.trade_book = OMSTradesBook(self.test_id, self.session_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create CO order
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message_care)
        order_id_care = response[0].get_parameters()['OrderID']
        # endregion
        # region accept CO order
        self.client_inbox.accept_order()
        # endregion
        # region create DMA order
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
            response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message_dma)
            order_id_dma = response[0].get_parameters()['OrderID']
        except Exception:
            logger.error("Error execution", exc_info=True)
        finally:
            time.sleep(1)
            self.rule_manager.remove_rule(nos_rule)
            self.rule_manager.remove_rule(trade_rule)
        exec_order_dma_id = self.order_book.set_filter(
            [OrderBookColumns.order_id.value, order_id_dma]).extract_2lvl_fields(
            SecondLevelTabs.executions.value, [OrderBookColumns.exec_id.value], [1])
        ex_type_dma = self.order_book.set_filter([OrderBookColumns.order_id.value, order_id_dma]).extract_2lvl_fields(
            SecondLevelTabs.executions.value, [OrderBookColumns.exec_type.value], [1])
        print(ex_type_dma)
        self.order_book.compare_values({OrderBookColumns.exec_type.value: ExecType.trade.value}, ex_type_dma[0],
                                       "Check execution")
        # endregion
        # region manual match execution
        self.trade_book.manual_match(self.qty_match,
                                     order_filter_list=[MatchWindowsColumns.order_id.value, order_id_care],
                                     trades_filter_list=[TradeBookColumns.exec_id.value,
                                                         exec_order_dma_id[0][OrderBookColumns.exec_id.value]])
        # exec_order_care_id = self.order_book.set_filter(
        #     [OrderBookColumns.order_id.value, order_id_care]).extract_2lvl_fields(
        #     SecondLevelTabs.executions.value, ["ExecID"], [1])
        # endregion
        # region check unmatch qty
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id_care]).check_order_fields_list(
            {OrderBookColumns.unmatched_qty.value: self.qty_match,
             OrderBookColumns.exec_sts.value: ExecSts.partially_filled.value})
        # endregion
        # region second manual match execution
        self.trade_book.manual_match(self.qty_match,
                                     order_filter_list=[MatchWindowsColumns.order_id.value, order_id_care],
                                     trades_filter_list=[TradeBookColumns.exec_id.value,
                                                         exec_order_dma_id[0][OrderBookColumns.exec_id.value]])
        # endregion
        # region check unmatch qty and exec sts
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id_care]).check_order_fields_list(
            {OrderBookColumns.unmatched_qty.value: "0",
             OrderBookColumns.exec_sts.value: ExecSts.filled.value})
        # self.order_book.set_filter([OrderBookColumns.order_id.value, order_id_care]).check_second_lvl_fields_list(
        #     {"ExecType": "Trade",
        #      OrderBookColumns.exec_sts.value: ExecSts.filled.value})
        ex_type_care = self.order_book.set_filter([OrderBookColumns.order_id.value, order_id_care]).extract_2lvl_fields(
            SecondLevelTabs.executions.value, [OrderBookColumns.exec_type.value], [1])
        print(ex_type_care)
        self.order_book.compare_values({OrderBookColumns.exec_type.value: ExecType.trade.value}, ex_type_care[0],
                                       "Check execution")
        exec_sts_care = self.order_book.set_filter(
            [OrderBookColumns.order_id.value, order_id_care]).extract_2lvl_fields(
            SecondLevelTabs.executions.value, [OrderBookColumns.exec_sts.value], [1])
        print(exec_sts_care)
        self.order_book.compare_values({OrderBookColumns.exec_type.value: ExecType.trade.value}, exec_sts_care[0],
                                       "Check execution")
        # endregion
