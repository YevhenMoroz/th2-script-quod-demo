import logging
import os
import time
import typing
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, MiddleOfficeColumns
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_3360(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.case_id = bca.create_event(os.path.basename(__file__), self.report_id)
        self.order_book = OMSOrderBook(self.case_id, self.session_id)
        self.middle_office = OMSMiddleOffice(self.case_id, self.session_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.case_id)
        self.qty = '1000'
        self.price = '10'
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.fix_message.set_default_dma_limit()
        self.fix_message.change_parameter('OrderQtyData', {'OrderQty': self.qty})
        self.fix_message.change_parameter('Account', self.data_set.get_client_by_name('client_pt_8'))
        self.fix_message.change_parameter('Price', self.price)
        self.client_for_rule = self.data_set.get_venue_client_names_by_name('client_pt_7_venue_1')
        self.exec_destination = self.data_set.get_mic_by_name('mic_1')

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        qty_of_second_block = '100'
        qty_of_first_block = '-1'
        orders_id = list()

        # region create  DMA order (precondition)
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
            self.fix_manager.send_message_fix_standard(self.fix_message)
            orders_id.append(self.order_book.extract_field(OrderBookColumns.order_id.value))

        except Exception as e:
            logger.error(f'{e}')

        finally:
            time.sleep(5)
            rule_manager.remove_rule(nos_rule)
            rule_manager.remove_rule(trade_rule)
            self.__verifying_value_of_orders(orders_id, [OrderBookColumns.post_trade_status.value,
                                                         OrderBookColumns.exec_sts.value], ['ReadyToBook', 'Filled'])
        # endregion

        # region split book (step 1 2, 3, 4)
        self.order_book.set_filter([OrderBookColumns.order_id.value, orders_id[0]])
        split_param_1 = self.order_book.create_split_booking_parameter(qty_of_first_block)
        split_param_2 = self.order_book.create_split_booking_parameter(qty_of_second_block)
        result = self.order_book.split_book([split_param_1, split_param_2], row_numbers=[1, 2], error_expected=True)
        expected_result = {
            'Footer Value': 'Error - sum of the split booking quantity does not equal to Total Alloc Qty.'}
        comparing_message = 'Comparing_error message'
        self.__comparing_values(expected_result, result, comparing_message,
                                'self.order_book.compare_values')
        # endregion

    def __comparing_values(self, expected_result, actually_result, verifier_message: str, eval_str):
        eval(eval_str)(expected_result, actually_result, verifier_message)

    def __verifying_value_of_orders(self, orders_id: list, fields: typing.List[str], expected_values: typing.List[str]):
        for order in range(len(orders_id)):
            for count in range(len(fields)):
                self.order_book.set_filter([OrderBookColumns.order_id.value, orders_id[order]])
                value = self.order_book.extract_field(fields[count])
                expected_result = {fields[count]: expected_values[count]}
                actually_result = {fields[count]: value}
                comparing_message = f'Comparing values of order {orders_id[order]}'
                self.__comparing_values(expected_result, actually_result, comparing_message,
                                        'self.order_book.compare_values')
