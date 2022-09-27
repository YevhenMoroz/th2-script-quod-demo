import logging
import os
import typing
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, MiddleOfficeColumns, \
    AllocationsColumns
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7475(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.middle_office = OMSMiddleOffice(self.test_id, self.session_id)

    # @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        qty = '1000'
        price = '10'
        exec_price = '2'
        client_name = self.data_set.get_client_by_name('client_pt_4')
        no_allocs: dict = {'NoAllocs': [
            {
                'AllocAccount': self.data_set.get_account_by_name('client_pt_4_acc_1'),
                'AllocQty': qty
            }]}
        self.fix_message.set_default_care_limit()
        self.fix_message.change_parameter('OrderQtyData', {'OrderQty': qty})
        self.fix_message.change_parameter('Account', client_name)
        self.fix_message.change_parameter('Instrument', self.data_set.get_fix_instrument_by_name('instrument_1'))
        self.fix_message.change_parameter('Price', price)
        self.fix_message.change_parameter('PreAllocGrp', no_allocs)
        exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.fix_message.change_parameter('ExDestination', exec_destination)
        compare_eval = 'self.middle_office.compare_values'
        orders_id = list()
        # endregion

        # region_create_orders(precondition)
        for i in range(3):
            self.fix_manager.send_message_fix_standard(self.fix_message)
            self.client_inbox.accept_order(filter={'ClientName': client_name})
            self.order_book.set_filter([OrderBookColumns.qty.value, qty])
            orders_id.append(self.order_book.extract_field(OrderBookColumns.order_id.value, 1))

        # endregion

        # region mass manual execution and  verify expected result(step 1 , 2)
        self.order_book.mass_manual_execution(exec_price, len(orders_id))
        self.order_book.complete_order(row_count=len(orders_id), filter_list=[OrderBookColumns.qty.value, qty])
        self.__verifying_value_of_orders(orders_id, [OrderBookColumns.post_trade_status.value,
                                                     OrderBookColumns.exec_sts.value], ['ReadyToBook', 'Filled'])
        # endregion

        # region book order and approve block (step 3)
        self.middle_office.set_modify_ticket_details(selected_row_count=len(orders_id))
        self.middle_office.book_order()
        block_id = self.middle_office.extract_block_field(MiddleOfficeColumns.block_id.value)
        self.__verifying_value_of_orders(orders_id, [OrderBookColumns.post_trade_status.value], ['Booked'])
        self.middle_office.set_filter(
            [MiddleOfficeColumns.block_id.value, block_id[MiddleOfficeColumns.block_id.value]])
        self.middle_office.clear_filter()
        value_of_block = self.middle_office.extract_list_of_block_fields([MiddleOfficeColumns.sts.value,
                                                                          MiddleOfficeColumns.match_status.value],
                                                                         row_number=1)
        expected_result = {MiddleOfficeColumns.sts.value: 'ApprovalPending',
                           MiddleOfficeColumns.match_status.value: 'Unmatched'}
        self.__comparing_values(expected_result, value_of_block, 'Comparing value after book',
                                compare_eval)
        # endregion

        # region step 4
        self.middle_office.approve_block()
        filter_list = [MiddleOfficeColumns.block_id.value, '122000000034']
        extracted_list = [MiddleOfficeColumns.sts.value,
                          MiddleOfficeColumns.match_status.value,
                          MiddleOfficeColumns.summary_status.value]
        actually_result = self.__extracted_values(extracted_list, filter_list,
                                                  'self.middle_office.extract_list_of_block_fields')
        expected_result = {MiddleOfficeColumns.summary_status.value: 'MatchedAgreed',
                           MiddleOfficeColumns.sts.value: 'Accepted',
                           MiddleOfficeColumns.match_status.value: 'Matched'}
        self.__comparing_values(expected_result, actually_result,
                                'Comparing values after approve for block of MiddleOffice',
                                compare_eval)
        extraction_fields = [AllocationsColumns.alloc_qty.value]
        expected_results = [{AllocationsColumns.alloc_qty.value: str(int(qty) * 3).replace('0', ',', 1).__add__('0')}]
        self.__verifying_allocation(extraction_fields, expected_results)
        # endregion

    def __comparing_values(self, expected_result, actually_result, verifier_message: str, eval_str):
        eval(eval_str)(expected_result, actually_result, verifier_message)

    def __extracted_values(self, fields, filter_values, method_for_eval):
        return eval(method_for_eval)(fields, filter_values)

    def __verifying_allocation(self, extraction_fields, expected_result):
        count = 0
        for field in extraction_fields:
            value = self.middle_office.extract_allocate_value(field)
            self.__comparing_values(expected_result[count], value, f'Comparing for Allocation{value}',
                                    'self.middle_office.compare_values')
            count = count+1

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
