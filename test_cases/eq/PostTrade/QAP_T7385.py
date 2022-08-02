import logging
import os
import time
from pathlib import Path
from datetime import datetime
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.win_gui_wrappers.fe_trading_constant import MiddleOfficeColumns, OrderBookColumns, \
    AllocationsColumns
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7385(TestCase):
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
        account = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        first_alloc_account = self.data_set.get_account_by_name('client_pt_1_acc_1')
        trade_date = datetime.now().strftime('%m/%d/%Y')
        no_allocs: dict = {'NoAllocs': [
            {
                'AllocAccount': first_alloc_account,
                'AllocQty': qty
            },
        ]}
        self.fix_message.set_default_dma_limit()
        self.fix_message.change_parameter('OrderQtyData', {'OrderQty': qty})
        self.fix_message.change_parameter('Account', self.data_set.get_client_by_name('client_pt_1'))
        self.fix_message.change_parameter('Instrument', self.data_set.get_fix_instrument_by_name('instrument_1'))
        self.fix_message.change_parameter('Price', price)
        self.fix_message.change_parameter('PreAllocGrp', no_allocs)
        exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.fix_message.change_parameter('ExDestination', exec_destination)
        rule_manager = RuleManager(Simulators.equity)
        cl_ord_id = self.fix_message.get_parameter('ClOrdID')
        # endregion

        # region precondition,
        self.__creating_order(rule_manager, account, exec_destination, price, qty)
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id])
        post_trade_status = self.order_book.extract_field(OrderBookColumns.post_trade_status.value)
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id])
        exec_sts = self.order_book.extract_field(OrderBookColumns.exec_sts.value)
        self.order_book.compare_values({OrderBookColumns.post_trade_status.value: 'ReadyToBook',
                                        OrderBookColumns.exec_sts.value: 'Filled'},
                                       {OrderBookColumns.post_trade_status.value: post_trade_status,
                                        OrderBookColumns.exec_sts.value: exec_sts},
                                       'Comparing values after fully filled')
        # endregion

        # region step 2
        self.middle_office.book_order()
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id])
        post_trade_status = self.order_book.extract_field(OrderBookColumns.post_trade_status.value)
        self.order_book.compare_values({OrderBookColumns.post_trade_status.value: 'Booked'},
                                       {OrderBookColumns.post_trade_status.value: post_trade_status},
                                       'Comparing values after fully filled')
        block_id = self.middle_office.extract_block_field(MiddleOfficeColumns.block_id.value)
        filter_list = [MiddleOfficeColumns.block_id.value, block_id[MiddleOfficeColumns.block_id.value]]
        status = self.middle_office.extract_block_field(MiddleOfficeColumns.sts.value)
        self.middle_office.compare_values({MiddleOfficeColumns.sts.value: 'ApprovalPending'}, status,
                                          'Comparing status after book')
        # endregion

        # region step 3
        self.middle_office.clear_filter()
        self.middle_office.approve_block()
        extracted_values = self.middle_office.extract_list_of_block_fields([MiddleOfficeColumns.sts.value,
                                                                            MiddleOfficeColumns.match_status.value],
                                                                           filter_list)
        self.middle_office.compare_values({MiddleOfficeColumns.sts.value: 'Accepted',
                                           MiddleOfficeColumns.match_status.value: 'Matched'}, extracted_values,
                                          'Comparing status after approve')
        # endregion

        # region step 4, 5, 6
        self.middle_office.clear_filter()
        self.middle_office.allocate_block(filter=filter_list)
        extracted_values = self.middle_office.extract_list_of_block_fields([MiddleOfficeColumns.sts.value,
                                                                            MiddleOfficeColumns.match_status.value,
                                                                            MiddleOfficeColumns.summary_status.value,
                                                                            MiddleOfficeColumns.trade_date.value],
                                                                           filter_list)
        self.middle_office.compare_values({MiddleOfficeColumns.sts.value: 'Accepted',
                                           MiddleOfficeColumns.match_status.value: 'Matched',
                                           MiddleOfficeColumns.summary_status.value: 'MatchedAgreed',
                                           MiddleOfficeColumns.trade_date.value: trade_date}, extracted_values,
                                          'Comparing status after allocate')
        extraction_fields = [AllocationsColumns.sts.value, AllocationsColumns.match_status.value,
                             AllocationsColumns.trade_date.value]
        expected_results = [{AllocationsColumns.sts.value: 'Affirmed'},
                            {AllocationsColumns.match_status.value: 'Matched'},
                            {AllocationsColumns.trade_date.value: trade_date}]
        self.__verifying_allocation(extraction_fields, expected_results)
        # endregion

    def __creating_order(self, rule_manager: RuleManager, account, exec_destination, price, qty):
        trade_rule = None
        new_order_single_rule = None
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
            time.sleep(5)
            rule_manager.remove_rule(trade_rule)
            rule_manager.remove_rule(new_order_single_rule)

    def __comparing_values(self, expected_result, actually_result, verifier_message: str, eval_str):
        eval(eval_str)(expected_result, actually_result, verifier_message)

    def __verifying_allocation(self, extraction_fields, expected_result):
        count = 0
        for field in extraction_fields:
            value = self.middle_office.extract_allocate_value(field)
            self.__comparing_values(expected_result[count], value, f'Comparing for Allocation{value}',
                                    'self.middle_office.compare_values')
            count = count + 1
