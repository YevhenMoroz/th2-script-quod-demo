import logging
import os
import time
from pathlib import Path
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.ors_messages.UnMatchRequest import UnMatchRequest
from test_framework.win_gui_wrappers.fe_trading_constant import SecondLevelTabs, OrderBookColumns, TradeBookColumns, \
    TimeInForce, OrderType, MatchWindowsColumns, ExecSts
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket
from test_framework.win_gui_wrappers.oms.oms_trades_book import OMSTradesBook
from test_framework.core.try_exept_decorator import try_except

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7421(TestCase):
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
        self.client_for_rule = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        self.exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.fix_message_care = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.fix_message_care.change_parameters(
            {'Account': self.data_set.get_client_by_name('client_pt_1'), 'OrderQtyData': {'OrderQty': self.qty},
             'Instrument':
                 self.data_set.get_fix_instrument_by_name('instrument_1'), 'Price': self.price, 'ExDestination':
                 self.exec_destination})
        self.fix_message_dma = FixMessageNewOrderSingleOMS(self.data_set).set_default_dma_limit()
        self.fix_message_dma.change_parameters(
            {'Account': self.data_set.get_client_by_name('client_pt_1'), 'OrderQtyData': {'OrderQty': self.qty},
             'Instrument':
                 self.data_set.get_fix_instrument_by_name('instrument_1'), 'Price': self.price, 'ExDestination':
                 self.exec_destination})
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)
        self.lookup = self.data_set.get_lookup_by_name('lookup_1')
        self.rule_manager = RuleManager(Simulators.equity)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region create  DMA order
        dma_order_id = None
        nos_rule = None
        trade_rule1 = None
        trade_rule2 = None
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.fix_env.buy_side,
                                                                                                  self.client_for_rule,
                                                                                                  self.exec_destination,
                                                                                                  float(self.price))
            trade_rule1 = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                                             self.client_for_rule,
                                                                                             self.exec_destination,
                                                                                             float(self.price),
                                                                                             int("50"),
                                                                                             delay=0)
            trade_rule2 = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                                             self.client_for_rule,
                                                                                             self.exec_destination,
                                                                                             float(self.price),
                                                                                             int("50"),
                                                                                             delay=0)

            response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message_dma)
            dma_order_id = response[0].get_parameters()['OrderID']
            self.rule_manager.remove_rules([nos_rule, trade_rule1, trade_rule2])
            print(dma_order_id)
        except Exception as e:
            logger.error(f'{e}')

        finally:
            self.rule_manager.remove_rules([nos_rule, trade_rule1, trade_rule2])
        # endregion
        # region check dma is filled
        self.order_book.set_filter([OrderBookColumns.order_id.value, dma_order_id]).check_order_fields_list(
            {OrderBookColumns.exec_sts.value: ExecSts.filled.value})
        # endregion
        # region create and accept CO order
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message_care)
        care_order_id = response[0].get_parameters()['OrderID']
        self.client_inbox.accept_order()
        # endregion
        # region extract execution from DMA order
        exec_id = self.order_book.extract_2lvl_fields(SecondLevelTabs.executions.value,
                                                      [TradeBookColumns.exec_id.value],
                                                      [1], {OrderBookColumns.order_id.value: dma_order_id})[0][
            OrderBookColumns.exec_id.value]
        # endregion
        # region match
        self.trade_book.manual_match_n_to_1(care_order_id, [1, 2],
                                            [TradeBookColumns.exec_id.value, exec_id[:-1]])
        # endregion
        # region check dma is filled
        self.order_book.set_filter([OrderBookColumns.order_id.value, care_order_id]).check_order_fields_list(
            {OrderBookColumns.exec_sts.value: ExecSts.filled.value, OrderBookColumns.unmatched_qty.value: "0"})
        # endregion
