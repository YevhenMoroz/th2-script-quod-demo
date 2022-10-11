import logging
import os
import time
from custom import basic_custom_actions as bca
from pathlib import Path
from test_framework.core.try_exept_decorator import try_except
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import SecondLevelTabs, OrderBookColumns
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket
from test_framework.win_gui_wrappers.oms.oms_trades_book import OMSTradesBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7420(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__), self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.trade_book = OMSTradesBook(self.test_id, self.session_id)
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.qty = '100'
        self.price = '10'
        self.exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.fix_message_dma = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit()
        self.fix_message_dma.change_parameter('OrderQtyData', {'OrderQty': self.qty})
        self.fix_message_dma.change_parameter('Account', self.data_set.get_client_by_name('client_co_1'))
        self.fix_message_dma.change_parameter('Price', self.price)
        self.fix_message_care = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.fix_message_care.change_parameter('OrderQtyData', {'OrderQty': self.qty})
        self.fix_message_care.change_parameter('Account', self.data_set.get_client_by_name('client_co_1'))
        self.fix_message_care.change_parameter('Price', self.price)
        self.client_for_rule = self.data_set.get_venue_client_names_by_name('client_co_1_venue_1')
        self.lookup = self.data_set.get_lookup_by_name('lookup_1')
        self.rule_manager = RuleManager(Simulators.equity)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # endregion
        # region create CO
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message_care)
        care_order_id = response[0].get_parameters()['OrderID']
        self.client_inbox.accept_order()
        # region create  DMA order
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
            dma_order_id = response[0].get_parameters()['OrderID']
        except Exception as e:
            logger.error(f'{e}')

        finally:
            time.sleep(5)
            self.rule_manager.remove_rule(nos_rule)
            self.rule_manager.remove_rule(trade_rule)
        exec_order_dma_id = self.order_book.set_filter(
            [OrderBookColumns.order_id.value, dma_order_id]).extract_2lvl_fields(
            SecondLevelTabs.executions.value, ["ExecID"], [1])
        # endregion
        # region manual match execution
        self.trade_book.manual_match(self.qty, order_filter_list=["OrderId", care_order_id],
                                     trades_filter_list=["ExecID", exec_order_dma_id[0]['ExecID']])
        exec_order_care_id = self.order_book.extract_2lvl_fields(
            SecondLevelTabs.executions.value, ["ExecID"], [1], filter_dict={OrderBookColumns.order_id.value: care_order_id})
        # endregion
        # region check unmatch qty
        self.order_book.set_filter([OrderBookColumns.order_id.value, care_order_id]).check_order_fields_list(
            {OrderBookColumns.unmatched_qty.value: "0"})
        # endregion
        # region unmatch execution
        self.trade_book.un_match(trades_filter_list=["ExecID", exec_order_care_id[0]['ExecID']])
        # endregion
        # region check unmatch qty
        self.order_book.set_filter([OrderBookColumns.order_id.value, care_order_id]).check_order_fields_list(
            {OrderBookColumns.unmatched_qty.value: self.qty})
        # endregion
        # region manual match execution
        self.trade_book.manual_match(self.qty, order_filter_list=["OrderId", care_order_id],
                                     trades_filter_list=["ExecID", exec_order_dma_id[0]['ExecID']])
        # endregion
        # region check unmatch qty
        self.order_book.set_filter([OrderBookColumns.order_id.value, care_order_id]).check_order_fields_list(
            {OrderBookColumns.unmatched_qty.value: "0"})
        # endregion
