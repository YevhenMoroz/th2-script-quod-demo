import logging
import os
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, MiddleOfficeColumns
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7517(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.middle_office = OMSMiddleOffice(self.test_id, self.session_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        qty = '300'
        price = '30'
        account = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        self.fix_message.set_default_dma_limit()
        self.fix_message.change_parameter('OrderQtyData', {'OrderQty': qty})
        self.fix_message.change_parameter('Account', self.data_set.get_client_by_name('client_pt_1'))
        self.fix_message.change_parameter('Instrument', self.data_set.get_fix_instrument_by_name('instrument_1'))
        self.fix_message.change_parameter('Price', price)
        exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.fix_message.change_parameter('ExDestination', exec_destination)
        rule_manager = RuleManager(Simulators.equity)
        trade_rule = None
        new_order_single_rule = None
        cl_ord_id = self.fix_message.get_parameter('ClOrdID')
        # endregion

        # region create order
        try:
            new_order_single_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side, account, exec_destination, float(price))
            trade_rule = rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side, account,
                                                                                       exec_destination, float(price),
                                                                                       int(qty), 0)
            self.fix_manager.send_message_fix_standard(self.fix_message)
        except Exception as ex:
            logger.exception(f'{ex} - your exception')
            bca.create_event('Exception regarding rules', self.test_id, status='FAIL')

        finally:
            time.sleep(10)
            rule_manager.remove_rule(trade_rule)
            rule_manager.remove_rule(new_order_single_rule)
        # endregion

        # region verify value of fields after trade (precondition)
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id])
        post_trade_status = self.order_book.extract_field(OrderBookColumns.post_trade_status.value)
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id])
        value_done_for_day = self.order_book.extract_field(OrderBookColumns.done_for_day.value)
        expected_result = {OrderBookColumns.post_trade_status.value: 'ReadyToBook',
                           OrderBookColumns.done_for_day.value: 'Yes'}
        actually_result = {OrderBookColumns.post_trade_status.value: post_trade_status,
                           OrderBookColumns.done_for_day.value: value_done_for_day}
        comparing_message = 'Comparing values after trade'
        self.__comparing_values(expected_result, actually_result, comparing_message, 'self.order_book.compare_values')
        # endregion

        # region book order and verify values after it at order book (step 1)
        self.middle_office.book_order()
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value,  cl_ord_id])
        value = self.order_book.extract_field(OrderBookColumns.post_trade_status.value)
        self.order_book.compare_values({OrderBookColumns.post_trade_status.value: 'Booked'},
                                       {OrderBookColumns.post_trade_status.value: value},
                                       'Compare PostTradeStatus after Book')
        # endregion

        # region check value at middle office
        block_id = self.middle_office.extract_block_field(MiddleOfficeColumns.block_id.value)
        self.middle_office.clear_filter()
        list_of_extraction = [MiddleOfficeColumns.conf_service.value, MiddleOfficeColumns.sts.value,
                              MiddleOfficeColumns.match_status.value, MiddleOfficeColumns.summary_status.value]
        filter_list = [MiddleOfficeColumns.block_id.value, block_id[MiddleOfficeColumns.block_id.value]]
        actually_result = self.__extracted_values(list_of_extraction, filter_list,
                                                  'self.middle_office.extract_list_of_block_fields')
        expected_result = {MiddleOfficeColumns.conf_service.value: 'Manual',
                           MiddleOfficeColumns.sts.value: 'ApprovalPending',
                           MiddleOfficeColumns.match_status.value: 'Unmatched',
                           MiddleOfficeColumns.summary_status.value: ''}
        self.__comparing_values(expected_result, actually_result,
                                'Comparing values after book for block of MiddleOffice',
                                'self.middle_office.compare_values')
        # endregion

        # region unbook block (step 2)
        self.middle_office.un_book_order()
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id])
        value = self.order_book.extract_field(OrderBookColumns.post_trade_status.value)
        self.order_book.compare_values({OrderBookColumns.post_trade_status.value: 'ReadyToBook'},
                                       {OrderBookColumns.post_trade_status.value: value},
                                       'Compare PostTradeStatus after Book')
        actually_result = self.__extracted_values(list_of_extraction, filter_list,
                                                  'self.middle_office.extract_list_of_block_fields')
        expected_result = {MiddleOfficeColumns.conf_service.value: 'Manual',
                           MiddleOfficeColumns.sts.value: 'Canceled',
                           MiddleOfficeColumns.match_status.value: 'Unmatched',
                           MiddleOfficeColumns.summary_status.value: ''}
        self.__comparing_values(expected_result, actually_result,
                                'Comparing values after book for block of MiddleOffice',
                                'self.middle_office.compare_values')

    def __comparing_values(self, expected_result, actually_result, verifier_message: str, eval_str):
        eval(eval_str)(expected_result, actually_result, verifier_message)

    def __extracted_values(self, fields, filter, method_for_eval):
        return eval(method_for_eval)(fields, filter)
