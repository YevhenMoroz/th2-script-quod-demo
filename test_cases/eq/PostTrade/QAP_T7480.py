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
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, MiddleOfficeColumns, \
    AllocationsColumns
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7480(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.middle_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.client_for_rule = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        self.pset = self.data_set.get_pset('pset_1')
        self.pset_2 = self.data_set.get_pset('pset_2')
        self.exec_destination = self.data_set.get_mic_by_name('mic_1')

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        nos_rule = None
        trade_rule = None
        qty = '300'
        price = '10'
        account_first = self.data_set.get_account_by_name('client_pt_1_acc_1')
        no_allocs: typing.Dict[str, list] = {'NoAllocs': [
            {
                'AllocAccount': account_first,
                'AllocQty': qty,
            }]}
        self.fix_message.change_parameter('PreAllocGrp', no_allocs)
        self.fix_message.set_default_dma_limit()
        self.fix_message.change_parameter('OrderQtyData', {'OrderQty': qty})
        self.fix_message.change_parameter('Account', self.data_set.get_client_by_name('client_pt_1'))
        self.fix_message.change_parameter('Price', price)

        cl_ord_id = self.fix_message.get_parameter('ClOrdID')
        rule_manager = RuleManager(Simulators.equity)
        # region create  DMA order
        try:
            nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(self.fix_env.buy_side,
                                                                                             self.client_for_rule,
                                                                                             self.exec_destination,
                                                                                             float(price))
            trade_rule = rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                                       self.client_for_rule,
                                                                                       self.exec_destination,
                                                                                       float(price),
                                                                                       int(qty),
                                                                                       delay=0)
            self.fix_manager.send_message_fix_standard(self.fix_message)
        except Exception as e:
            logger.error(f'{e}')

        finally:
            time.sleep(10)
            rule_manager.remove_rule(nos_rule)
            rule_manager.remove_rule(trade_rule)
        # endregion

        # region Book order and verify value after that (step 1, step 2)
        order_id_first = self.order_book.extract_field(OrderBookColumns.order_id.value)
        self.middle_office.set_modify_ticket_details(pset=self.pset[0])
        self.middle_office.book_order()
        block_id = self.middle_office.extract_block_field(MiddleOfficeColumns.block_id.value)
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id])
        post_trade_status = self.order_book.extract_field(OrderBookColumns.post_trade_status.value)
        self.__comparing_values({OrderBookColumns.post_trade_status.value: 'Booked'},
                                {OrderBookColumns.post_trade_status.value: post_trade_status},
                                'Comparing post trade status after book', 'self.order_book.compare_values')
        filter_list = [MiddleOfficeColumns.block_id.value, block_id[MiddleOfficeColumns.block_id.value]]
        extracted_list = [MiddleOfficeColumns.sts.value,
                          MiddleOfficeColumns.match_status.value,
                          MiddleOfficeColumns.pset.value,
                          MiddleOfficeColumns.pset_bic.value]
        actually_result = self.__extracted_values(extracted_list, filter_list,
                                                  'self.middle_office.extract_list_of_block_fields')
        expected_result = {MiddleOfficeColumns.sts.value: 'ApprovalPending',
                           MiddleOfficeColumns.match_status.value: 'Unmatched',
                           MiddleOfficeColumns.pset.value: self.pset[0],
                           MiddleOfficeColumns.pset_bic.value: self.pset[1]}
        self.__comparing_values(expected_result, actually_result,
                                'Comparing values after book for block of MiddleOffice',
                                'self.middle_office.compare_values')
        # endregion

        # region amend PSET for block (step 3, step 4)
        self.middle_office.set_modify_ticket_details(pset=self.pset_2[0])
        self.middle_office.amend_block(filter_list)
        extracted_list = [MiddleOfficeColumns.pset.value,
                          MiddleOfficeColumns.pset_bic.value]
        actually_result = self.__extracted_values(extracted_list, filter_list,
                                                  'self.middle_office.extract_list_of_block_fields')
        expected_result = {MiddleOfficeColumns.pset.value: self.pset_2[0],
                           MiddleOfficeColumns.pset_bic.value: self.pset_2[1]}
        self.__comparing_values(expected_result, actually_result,
                                'Comparing values after amend  block of MiddleOffice',
                                'self.middle_office.compare_values')
        # endregion

        # region approve block (step 5)
        self.middle_office.approve_block()
        extracted_list = [MiddleOfficeColumns.sts.value,
                          MiddleOfficeColumns.match_status.value]
        actually_result = self.__extracted_values(extracted_list, filter_list,
                                                  'self.middle_office.extract_list_of_block_fields')
        expected_result = {MiddleOfficeColumns.sts.value: 'Accepted',
                           MiddleOfficeColumns.match_status.value: 'Matched'}
        self.__comparing_values(expected_result, actually_result,
                                'Comparing values after approve  block of MiddleOffice',
                                'self.middle_office.compare_values')
        # endregion

        # region allocate block (step 6)
        self.middle_office.allocate_block(filter=filter_list)
        extraction_fields = [AllocationsColumns.pset.value, AllocationsColumns.pset_bic.value]
        expected_results = [{AllocationsColumns.pset.value: self.pset_2[0]},
                            {AllocationsColumns.pset_bic.value: self.pset_2[1]}]
        self.__verifying_allocation(extraction_fields, expected_results)
        # endregion

        # region amend allocation and verifying value after that (step 7, step 8)
        self.middle_office.set_modify_ticket_details(is_alloc_amend=True, pset=self.pset[0])
        self.middle_office.amend_allocate(filter=filter_list)
        extraction_fields = [AllocationsColumns.pset.value, AllocationsColumns.pset_bic.value]
        expected_results = [{AllocationsColumns.pset.value: self.pset_2[0]},
                            {AllocationsColumns.pset_bic.value: self.pset_2[1]}]
        self.__verifying_allocation(extraction_fields, expected_results)
        # endregion

    def __comparing_values(self, expected_result, actually_result, verifier_message: str, eval_str):
        eval(eval_str)(expected_result, actually_result, verifier_message)

    def __extracted_values(self, fields, filter, method_for_eval):
        return eval(method_for_eval)(fields, filter)

    def __verifying_allocation(self, extraction_fields, expected_result):
        count = 0
        for field in extraction_fields:
            value = self.middle_office.extract_allocate_value(field)
            self.__comparing_values(expected_result[count], value, f'Comparing for Allocation{value}',
                                    'self.middle_office.compare_values')
            count = count + 1
