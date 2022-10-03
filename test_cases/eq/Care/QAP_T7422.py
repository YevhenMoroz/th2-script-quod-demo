import logging
import os
import time

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.ors_messages.UnMatchRequest import UnMatchRequest
from test_framework.win_gui_wrappers.fe_trading_constant import SecondLevelTabs, OrderBookColumns, TradeBookColumns, \
    TimeInForce, OrderType, MatchWindowsColumns
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket
from test_framework.win_gui_wrappers.oms.oms_trades_book import OMSTradesBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7422(TestCase):
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.trade_book = OMSTradesBook(self.test_id, self.session_id)
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.qty = '100'
        self.price = '10'
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.fix_message.set_default_dma_limit()
        self.fix_message.change_parameter('OrderQtyData', {'OrderQty': self.qty})
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)
        self.fix_message.change_parameter('Account', self.data_set.get_client_by_name('client_pt_1'))
        self.fix_message.change_parameter('Instrument', self.data_set.get_fix_instrument_by_name('instrument_1'))
        self.fix_message.change_parameter('Price', self.price)
        self.client_for_rule = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        self.exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.fix_message.change_parameter('ExDestination', self.exec_destination)
        self.lookup = self.data_set.get_lookup_by_name('lookup_1')

    # @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):

        # region create  DMA order
        dma_order_id = None
        try:
            rule_manager = RuleManager(Simulators.equity)
            nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.fix_env.buy_side,
                                                                                             self.client_for_rule,
                                                                                             self.exec_destination,
                                                                                             float(self.price))
            trade_rule = rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                                       self.client_for_rule,
                                                                                       self.exec_destination,
                                                                                       float(self.price),
                                                                                       int(self.qty),
                                                                                       delay=0)
            self.order_ticket.set_order_details(self.data_set.get_client_by_name('client_pt_1'), limit=self.price, qty=self.qty,
                                                order_type=OrderType.limit.value, tif=TimeInForce.DAY.value)
            self.order_ticket.create_order('DNX')
            dma_order_id = self.order_book.extract_field(OrderBookColumns.order_id.value)

        except Exception as e:
            logger.error(f'{e}')

        finally:
            time.sleep(5)
            rule_manager.remove_rule(nos_rule)
            rule_manager.remove_rule(trade_rule)
        # endregion

        # region create and accept CO order
        self.fix_message.change_parameter("HandlInst", '3')
        self.fix_manager.send_message_fix_standard(self.fix_message)
        self.client_inbox.accept_order(self.lookup, self.qty, self.price)
        care_order_id = self.order_book.extract_field(OrderBookColumns.order_id.value)
        # endregion

        # region extract execution from DMA order
        exec_id = self.order_book.extract_2lvl_fields(SecondLevelTabs.executions.value,
                                                      [TradeBookColumns.exec_id.value],
                                                      [1], {OrderBookColumns.order_id.value: dma_order_id})[0][OrderBookColumns.exec_id.value]
        # endregion

        # region match
        self.trade_book.manual_match(self.qty, [MatchWindowsColumns.order_id.value, care_order_id],
                                     [TradeBookColumns.exec_id.value, exec_id])
        # endregion

        # region verifying values of care order after match
        self.order_book.set_filter([OrderBookColumns.order_id.value, care_order_id])
        values_of_co_order = self.order_book.extract_fields_list(
            {OrderBookColumns.exec_sts.value: OrderBookColumns.exec_sts.value,
             OrderBookColumns.unmatched_qty.value: OrderBookColumns.unmatched_qty.value})
        self.order_book.compare_values({OrderBookColumns.exec_sts.value: 'Filled',
                                        OrderBookColumns.unmatched_qty.value: '0'}, values_of_co_order,
                                       'Comparing values at CO order(after match)')
        # endregion

        # region extraction execution from CO order
        exec_id_co_order = self.order_book.extract_2lvl_fields(SecondLevelTabs.executions.value,
                                                               [TradeBookColumns.exec_id.value],
                                                               [1], {OrderBookColumns.order_id.value: care_order_id})[
            0]['ExecID']
        # endregion

        # region unmatch order on half of qty
        order_un_match_params_first = UnMatchRequest({
            'SEND_SUBJECT': 'QUOD.ORS.FE',
            'UnMatchRequestBlock': {
                'UnMatchingList': {'UnMatchingBlock': [
                    {'VirtualExecID': exec_id_co_order, 'UnMatchingQty': str(int(self.qty) / 2),
                     'SourceAccountID': self.data_set.get_washbook_account_by_name('washbook_account_1'),
                     'PositionType': "N"}
                ]},
                'DestinationAccountID': self.data_set.get_account_by_name('client_pos_3_acc_3')
            }
        })
        self.java_api_manager.send_message(order_un_match_params_first)

        self.order_book.set_filter([OrderBookColumns.order_id.value, care_order_id])
        values_of_co_order = self.order_book.extract_fields_list(
            {OrderBookColumns.exec_sts.value: OrderBookColumns.exec_sts.value,
             OrderBookColumns.unmatched_qty.value: OrderBookColumns.unmatched_qty.value})
        self.order_book.compare_values({OrderBookColumns.exec_sts.value: 'Filled',
                                        OrderBookColumns.unmatched_qty.value: str(int(int(self.qty) / 2))},
                                       values_of_co_order,
                                       'Comparing values at CO order(after unmatch on half of qty)')

        exec_id_co_order = self.order_book.extract_2lvl_fields(SecondLevelTabs.executions.value,
                                                               [TradeBookColumns.exec_id.value],
                                                               [1], {OrderBookColumns.order_id.value: care_order_id})[
            0]['ExecID']
        # endregion
        order_un_match_params_second = UnMatchRequest({
            'SEND_SUBJECT': 'QUOD.ORS.FE',
            'UnMatchRequestBlock': {
                'UnMatchingList': {'UnMatchingBlock': [
                    {'VirtualExecID': exec_id_co_order, 'UnMatchingQty': str(int(self.qty) / 2),
                     'SourceAccountID': self.data_set.get_washbook_account_by_name('washbook_account_1'),
                     'PositionType': "N"}
                ]},
                'DestinationAccountID': self.data_set.get_account_by_name('client_pos_3_acc_3')
            }
        })
        self.java_api_manager.send_message(order_un_match_params_second)

        # region verifying values of care order after last unmatch
        self.order_book.set_filter([OrderBookColumns.order_id.value, care_order_id])
        values_of_co_order = self.order_book.extract_fields_list(
            {OrderBookColumns.exec_sts.value: OrderBookColumns.exec_sts.value,
             OrderBookColumns.unmatched_qty.value: OrderBookColumns.unmatched_qty.value})
        self.order_book.compare_values({OrderBookColumns.exec_sts.value: '',
                                        OrderBookColumns.unmatched_qty.value: self.qty}, values_of_co_order,
                                       'Comparing values at CO order(after last unmatch)')

        values_after_last_cancel = self.order_book.extract_2lvl_fields(SecondLevelTabs.executions.value,
                                                                       [
                                                                           TradeBookColumns.exec_type.value],
                                                                       [1],
                                                                       {OrderBookColumns.order_id.value: care_order_id})

        self.order_book.compare_values({TradeBookColumns.exec_type.value:
                                            'TradeCancel'}, values_after_last_cancel[0],
                                       'Verifying exec type of CO order execution')
        # endregion
