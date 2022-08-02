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
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, MiddleOfficeColumns, \
    AllocationsColumns
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7547(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.case_id = bca.create_event(os.path.basename(__file__), self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.case_id)
        self.order_book = OMSOrderBook(self.case_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.case_id, self.session_id)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.case_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.middle_office = OMSMiddleOffice(self.case_id, self.session_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        qty = '200'
        price = '10'
        account_first = self.data_set.get_account_by_name('client_pt_1_acc_1')
        account_second = self.data_set.get_account_by_name('client_pt_1_acc_2')
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

        finally:
            time.sleep(10)
            rule_manager.remove_rule(trade_rule)
            rule_manager.remove_rule(new_order_single_rule)

        # endregion

        # region verify value of fields after trade
        self.order_book.set_filter([OrderBookColumns.qty.value, qty])
        post_trade_status = self.order_book.extract_field(OrderBookColumns.post_trade_status.value)
        self.order_book.set_filter([OrderBookColumns.qty.value, qty])
        value_exec_sts = self.order_book.extract_field(OrderBookColumns.exec_sts.value)
        self.order_book.compare_values(
            {OrderBookColumns.post_trade_status.value: 'ReadyToBook', OrderBookColumns.done_for_day.value: 'Filled'},
            {OrderBookColumns.post_trade_status.value: post_trade_status,
             OrderBookColumns.done_for_day.value: value_exec_sts}, 'Comparing values after trade')
        # endregion

        # region book order and verify values after it at order book (step 1)
        self.middle_office.book_order()
        self.order_book.set_filter([OrderBookColumns.qty.value, qty])
        value = self.order_book.extract_field(OrderBookColumns.post_trade_status.value)
        self.order_book.compare_values({OrderBookColumns.post_trade_status.value: 'Booked'},
                                       {OrderBookColumns.post_trade_status.value: value},
                                       'Compare PostTradeStatus after Book')
        # endregion

        # region check value at middle office (step 1)
        block_id = self.middle_office.extract_block_field(MiddleOfficeColumns.block_id.value)
        values = self.middle_office.extract_list_of_block_fields([MiddleOfficeColumns.conf_service.value,
                                                                  MiddleOfficeColumns.sts.value,
                                                                  MiddleOfficeColumns.match_status.value,
                                                                  MiddleOfficeColumns.summary_status.value
                                                                  ])
        self.middle_office.compare_values({MiddleOfficeColumns.conf_service.value: 'Manual',
                                           MiddleOfficeColumns.sts.value: 'ApprovalPending',
                                           MiddleOfficeColumns.match_status.value: 'Unmatched',
                                           MiddleOfficeColumns.summary_status.value: ''}, values,
                                          'Comparing values after book for block of MiddleOffice')
        # endregion

        # region approve order and verify values after that (step 2)
        self.middle_office.approve_block()
        values_of_middle_office = self.middle_office.extract_list_of_block_fields([
            MiddleOfficeColumns.sts.value,
            MiddleOfficeColumns.match_status.value,
            MiddleOfficeColumns.summary_status.value],
            [MiddleOfficeColumns.block_id.value, block_id[MiddleOfficeColumns.block_id.value]])
        self.middle_office.compare_values({MiddleOfficeColumns.summary_status.value: '',
                                           MiddleOfficeColumns.sts.value: 'Accepted',
                                           MiddleOfficeColumns.match_status.value: 'Matched'}, values_of_middle_office,
                                          'Comparing values after approve for block of MiddleOffice')
        # endregion

        # region allocate block on 2 account (step 3)
        allocation_param = [{"Security Account": account_first, "Alloc Qty": str(int(int(qty) / 2))},
                            {"Security Account": account_second, "Alloc Qty": str(int(int(qty) / 2))}]
        self.middle_office.set_modify_ticket_details(arr_allocation_param=allocation_param)
        self.middle_office.allocate_block()
        values_of_middle_office = self.middle_office.extract_list_of_block_fields([
            MiddleOfficeColumns.sts.value,
            MiddleOfficeColumns.match_status.value,
            MiddleOfficeColumns.summary_status.value],
            [MiddleOfficeColumns.block_id.value, block_id[MiddleOfficeColumns.block_id.value]])
        self.middle_office.compare_values({MiddleOfficeColumns.summary_status.value: 'MatchedAgreed',
                                           MiddleOfficeColumns.sts.value: 'Accepted',
                                           MiddleOfficeColumns.match_status.value: 'Matched'}, values_of_middle_office,
                                          'Comparing values after allocate for block of MiddleOffice')
        # endregion

        # region verifying values of allocations (step 4)
        self.__comparing_allocations_value(account_first, str(int(int(qty) / 2)), price)
        self.__comparing_allocations_value(account_second, str(int(int(qty) / 2)), price)
        # endregion

    def __comparing_allocations_value(self, account, qty, price):
        allocation_status = self.middle_office.extract_allocate_value(AllocationsColumns.sts.value,
                                                                      account=account)
        allocation_match_status = self.middle_office.extract_allocate_value(AllocationsColumns.match_status.value,
                                                                            account=account)
        allocation_qty = self.middle_office.extract_allocate_value(AllocationsColumns.alloc_qty.value,
                                                                   account=account)
        allocation_avg_px = self.middle_office.extract_allocate_value(AllocationsColumns.avg_px.value,
                                                                      account=account)
        self.middle_office.compare_values({AllocationsColumns.sts.value: 'Affirmed'}, allocation_status,
                                          f'Comparing allocation status for {account}')
        self.middle_office.compare_values({AllocationsColumns.match_status.value: 'Matched'}, allocation_match_status,
                                          f'Comparing allocation match_status for {account}')
        self.middle_office.compare_values({AllocationsColumns.alloc_qty.value: str(int(int(qty) / 2))}, allocation_qty,
                                          f'Comparing allocation qty for {account}')
        self.middle_office.compare_values({AllocationsColumns.avg_px.value: price}, allocation_avg_px,
                                          f'Comparing allocation avg_px for {account}')
