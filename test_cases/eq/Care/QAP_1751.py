import logging
import os
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.SessionAlias import SessionAliasOMS
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.ors_messages.TradeEntryRequest import TradeEntryRequest
from test_framework.win_gui_wrappers.fe_trading_constant import SecondLevelTabs, OrderBookColumns, OrderType, ExecSts, \
    DiscloseExec
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True



class QAP_1751(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set=None, environment=None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.qty = "30000"
        self.price = "5"
        self.first_split_qty = "20000"
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit()
        self.fix_message.change_parameter('OrderQtyData', {'OrderQty': self.qty})
        self.fix_message.change_parameter("Price", self.price)
        self.rule_manager = RuleManager()
        self.client_for_rule = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        self.exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)


    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        # region create CO order
        self.fix_manager.send_message_fix_standard(self.fix_message)
        order_id = self.order_book.extract_field(OrderBookColumns.order_id.value)
        # endregion
        # region accept order
        self.client_inbox.accept_order()
        # endregion
        # region check order open status
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).check_order_fields_list(
            {OrderBookColumns.sts.value: ExecSts.open.value})
        # endregion
        # region set "manual" disclise flag
        self.order_book.set_disclose_flag_via_order_book("manual")
        # endregion
        # region check disclose execution
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id]).check_order_fields_list(
            {OrderBookColumns.disclose_exec.value: DiscloseExec.manual.value})
        # endregion
        # region split order
        try:
            nos_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.fix_env.buy_side,
                                                                                             self.client_for_rule,
                                                                                             self.exec_destination,
                                                                                             float(self.price))
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                                       self.client_for_rule,
                                                                                       self.exec_destination,
                                                                                       float(self.price),
                                                                                       int(self.first_split_qty),
                                                                                       delay=0)
            # endregion
            # region split order
            self.order_ticket.set_order_details(qty=self.first_split_qty)
            self.order_ticket.split_order()
        except Exception:
            logger.setLevel(logging.DEBUG)
            logging.debug('RULE WORK CORRECTLY. (: NOT :)')
        finally:
            time.sleep(10)
            self.rule_manager.remove_rule(trade_rule)
            self.rule_manager.remove_rule(nos_rule)
        # endregion
        self.order_book.exe

        #
        #
        # fix_verifier = FixVerifier(ss_connectivity, self.case_id)
        # fix_manager = FixManager(ss_connectivity)
        # new_qty = '30000'
        # first_split_qty = '20000'
        # second_split_qty = '10000'
        # type_of_split_order = OrderType.limit.value
        # fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        # fix_message.set_default_care_limit()
        # fix_message.change_parameter('OrderQtyData', {'OrderQty': new_qty})
        # fix_execution_message = FixMessageExecutionReportOMS(fix_message.get_parameters())
        # fix_execution_message.change_parameter('ExecType', 'B')
        # fix_execution_message.change_parameter('OrdStatus', 'B')
        # fix_execution_message_second = FixMessageExecutionReportOMS(fix_message.get_parameters())
        # fix_execution_message_second.change_parameter('ExecType', 'B')
        # fix_execution_message_second.change_parameter('OrdStatus', 'B')
        # client = fix_message.get_parameter('Account')
        # client_for_rule = self.data_set.get_venue_client_names_by_name('client_1_venue_1')
        # exec_destination = self.data_set.get_mic_by_name('mic1')
        # price = fix_message.get_parameter('Price')
        # lookup = fix_message.get_parameter('Instrument')
        # price_first_split = '5'
        #
        # # endregion
        #
        # # region create CO order
        # fix_manager.send_message_fix_standard(fix_message)
        # order_id = order_book.extract_field('Order ID')
        # # endregion
        #
        # # region accept CO order
        # order_inbox = OMSClientInbox(self.case_id, self.session_id)
        # order_inbox.accept_order(lookup, new_qty, price)
        # order_book.set_filter([OrderBookColumns.order_id.value, order_id])
        # order_book.set_disclose_flag_via_order_book('manual')
        # # endregion
        #
        # rule_manager = RuleManager()
        # # region Split  order
        # order_book.set_filter([OrderBookColumns.order_id.value, order_id])
        # try:
        #     nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(bs_connectivity,
        #                                                                                      client_for_rule,
        #                                                                                      exec_destination,
        #                                                                                      float(price_first_split))
        #     trade_rule = rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(bs_connectivity,
        #                                                                                client_for_rule,
        #                                                                                exec_destination,
        #                                                                                float(price_first_split),
        #                                                                                int(first_split_qty),
        #                                                                                delay=0)
        #     order_book.set_order_ticket_details(qty=first_split_qty, type=type_of_split_order, price=price_first_split)
        #     order_book.split_limit_order()
        # except Exception:
        #     logger.setLevel(logging.DEBUG)
        #     logging.debug('RULE WORK CORRECTLY. (: NOT :)')
        # finally:
        #     time.sleep(10)
        #     rule_manager.remove_rule(trade_rule)
        #     rule_manager.remove_rule(nos_rule)
        # # endregion
        #
        # # region  execution summary order
        # trade_entry_request_message = TradeEntryRequest()
        # trade_entry_request_message.set_default(self.data_set, order_id, price_first_split
        #                                         , first_split_qty)
        # trade_entry_request_message.get_parameter('TradeEntryRequestBlock')['TradeEntryTransType'] = 'CAL'
        # execid = order_book.extract_2lvl_fields(SecondLevelTabs.execution_tab.value, ['ExecID'], rows=[1],
        #                                         filter_dict={OrderBookColumns.order_id.value: order_id})
        # trade_entry_request_message.update_fields_in_component('TradeEntryRequestBlock',
        #                                                        {'ExecToDiscloseList': {'ExecToDiscloseBlock': [
        #                                                            execid[0]
        #                                                        ]}})
        # java_api_sender = JavaApiManager(java_api_connectivity, self.case_id)
        # java_api_sender.send_message(trade_entry_request_message)
        # # endregion
        #
        # # region fix_verifier
        # fix_execution_message.add_tag({'LastQty': first_split_qty})
        # fix_execution_message.add_tag(
        #     {'CumQty': first_split_qty, 'LeavesQty': second_split_qty, 'LastPx': price_first_split})
        # fix_execution_message.add_tag(
        #     {'OrderID': order_id, 'Parties': '*', 'SettlDate': '*', 'TradeDate': '*', 'ExecID': execid[0],
        #      'QtyType': '*', 'VenueType': 'O', 'GrossTradeAmt': '*', 'TradeReportingIndicator': '*',
        #      'AvgPx': price_first_split})
        # fix_execution_message.change_parameter('TransactTime', '*')
        # fix_verifier.check_fix_message_fix_standard(fix_execution_message)
        # # endregion
        #
        # #  region split second order
        # order_book.set_filter([OrderBookColumns.order_id.value, order_id])
        # try:
        #     nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(bs_connectivity,
        #                                                                                      client_for_rule,
        #                                                                                      exec_destination,
        #                                                                                      float(price_first_split))
        #     trade_rule = rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(bs_connectivity,
        #                                                                                client_for_rule,
        #                                                                                exec_destination,
        #                                                                                float(price_first_split),
        #                                                                                int(second_split_qty),
        #                                                                                delay=0)
        #     order_book.set_order_ticket_details(qty=second_split_qty, type=type_of_split_order, price=price_first_split)
        #     order_book.split_limit_order()
        # except Exception:
        #     logger.setLevel(logging.DEBUG)
        #     logging.debug('RULE WORK CORRECTLY. (: NOT :)')
        # finally:
        #     time.sleep(10)
        #     rule_manager.remove_rule(trade_rule)
        #     rule_manager.remove_rule(nos_rule)
        # #  endregion
        #
        # # region  execution summary order
        # trade_entry_request_message_second = TradeEntryRequest()
        # trade_entry_request_message_second.set_default(self.data_set, order_id, price
        #                                                , second_split_qty)
        # trade_entry_request_message_second.get_parameter('TradeEntryRequestBlock')['TradeEntryTransType'] = 'CAL'
        # execid_second = order_book.extract_2lvl_fields(SecondLevelTabs.execution_tab.value, ['ExecID'], rows=[3],
        #                                                filter_dict={OrderBookColumns.order_id.value: order_id})
        # trade_entry_request_message_second.update_fields_in_component('TradeEntryRequestBlock',
        #                                                               {'ExecToDiscloseList': {'ExecToDiscloseBlock': [
        #                                                                   execid_second[0]
        #                                                               ]}})
        # java_api_sender.send_message(trade_entry_request_message_second)
        # # endregion
        #
        # # region fix_verifier
        # time.sleep(10)
        # fix_execution_message_second.add_tag({'LastQty': second_split_qty})
        # fix_execution_message_second.add_tag(
        #     {'CumQty': new_qty, 'LeavesQty': '0', 'LastPx': price})
        # fix_execution_message_second.add_tag({'OrderID': order_id, 'Parties': '*', 'SettlDate': '*', 'TradeDate': '*',
        #                                       'QtyType': '*', 'VenueType': 'O', 'GrossTradeAmt': '*', 'AvgPx': '10',
        #                                       'TradeReportingIndicator': '*', })
        # fix_execution_message_second.change_parameter('TransactTime', '*')
        # fix_verifier.check_fix_message_fix_standard(fix_execution_message_second, ['ClOrdID', 'OrdStatus', 'ExecType',
        #                                                                            'AvgPx'])
        # # endregion
