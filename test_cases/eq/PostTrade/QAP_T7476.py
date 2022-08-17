import logging
import os
import time
from pathlib import Path
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageConfirmationReportOMS import FixMessageConfirmationReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, MiddleOfficeColumns, \
    AllocationsColumns
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7476(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.case_id = bca.create_event(os.path.basename(__file__), self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.order_book = OMSOrderBook(self.case_id, self.session_id)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.case_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.middle_office = OMSMiddleOffice(self.case_id, self.session_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        qty = '500'
        price = '50'
        negative_value = '-1'
        account = self.data_set.get_account_by_name('client_pt_1_acc_1')
        venue_client = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
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

        # region create DMA order (precondition)
        try:
            new_order_single_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side, account, exec_destination, float(price))
            trade_rule = rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                                       venue_client,
                                                                                       exec_destination,
                                                                                       float(price),
                                                                                       int(qty), 0)
            self.fix_manager.send_message_fix_standard(self.fix_message)
        except Exception as ex:
            logger.exception(f'{ex} - your exception')
            bca.create_event('Exception regarding rules', self.case_id, status='FAIL')

        finally:
            time.sleep(10)
            rule_manager.remove_rule(trade_rule)
            rule_manager.remove_rule(new_order_single_rule)
        # endregion

        # region book order (1 step)
        self.middle_office.set_modify_ticket_details(remove_fee=True, remove_comm=True)
        self.middle_office.book_order()
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id])
        post_trade_status = self.order_book.extract_field(OrderBookColumns.post_trade_status.value)
        self.__comparing_values({OrderBookColumns.post_trade_status.value: 'Booked'},
                                {OrderBookColumns.post_trade_status.value: post_trade_status},
                                'Comparing post trade status after book', 'self.order_book.compare_values')
        block_id = self.middle_office.extract_block_field(MiddleOfficeColumns.block_id.value)
        filter_list = [MiddleOfficeColumns.block_id.value, block_id[MiddleOfficeColumns.block_id.value]]
        extracted_list = [MiddleOfficeColumns.sts.value,
                          MiddleOfficeColumns.match_status.value]
        actually_result = self.__extracted_values(extracted_list, filter_list,
                                                  'self.middle_office.extract_list_of_block_fields')
        expected_result = {MiddleOfficeColumns.sts.value: 'ApprovalPending',
                           MiddleOfficeColumns.match_status.value: 'Unmatched'}
        self.__comparing_values(expected_result, actually_result,
                                'Comparing values after book for block of MiddleOffice',
                                'self.middle_office.compare_values')
        # endregion

        # region amend block (step 2)
        commission_fee_basis = self.data_set.get_commission_basis('comm_basis_1')
        self.middle_office.set_modify_ticket_details(comm_basis=commission_fee_basis, comm_rate=negative_value,
                                                     fee_basis=commission_fee_basis,
                                                     fee_rate=negative_value,
                                                     fee_type=self.data_set.get_misc_fee_type_by_name('tax'),
                                                     extract_book=True, toggle_manual=True)
        values = self.middle_office.amend_block(filter_list)
        self.middle_office.compare_values({'Fees': negative_value, 'Commission': negative_value},
                                          {'Fees': values['book.totalFees'], 'Commission': values['book.totalComm']},
                                          'Compare values Commission and Fees from Booking Ticket')
        # endregion

        # region approve block (step 3)
        self.middle_office.approve_block()
        extracted_list = [MiddleOfficeColumns.sts.value,
                          MiddleOfficeColumns.match_status.value]
        actually_result = self.__extracted_values(extracted_list, filter_list,
                                                  'self.middle_office.extract_list_of_block_fields')
        expected_result = {MiddleOfficeColumns.sts.value: 'Accepted',
                           MiddleOfficeColumns.match_status.value: 'Matched'}
        self.__comparing_values(expected_result, actually_result,
                                'Comparing values after approve for block of MiddleOffice',
                                'self.middle_office.compare_values')
        # endregion

        # region allocate block (step 4 , step 5, step 6)
        fix_verifier = FixVerifier(self.fix_env.drop_copy, self.case_id)
        confirmation_message = FixMessageConfirmationReportOMS(self.data_set)
        confirmation_message.set_default_confirmation_new(self.fix_message)
        confirmation_message.add_tag({'Account': '*'}).add_tag({'SettlCurrFxRate': '*'}). \
            add_tag({'AllocInstructionMiscBlock2': '*'}).add_tag({'tag5120': '*'}). \
            add_tag({'NoMiscFees': [{'MiscFeeAmt': negative_value, 'MiscFeeCurr': '*', 'MiscFeeType': '*'}]}). \
            add_tag({'CommissionData': {'CommissionType': '*', 'Commission': negative_value, 'CommCurrency': '*'}})
        arr_allocation_param = [{"Security Account": account, "Alloc Qty": qty}]
        self.middle_office.set_modify_ticket_details(arr_allocation_param=arr_allocation_param)
        self.middle_office.allocate_block(filter_list)
        fix_verifier.check_fix_message_fix_standard(confirmation_message)
        extracted_list = [MiddleOfficeColumns.sts.value,
                          MiddleOfficeColumns.match_status.value,
                          MiddleOfficeColumns.summary_status.value]
        actually_result = self.__extracted_values(extracted_list, filter_list,
                                                  'self.middle_office.extract_list_of_block_fields')
        expected_result = {MiddleOfficeColumns.sts.value: 'Accepted',
                           MiddleOfficeColumns.match_status.value: 'Matched',
                           MiddleOfficeColumns.summary_status.value: 'MatchedAgreed'}
        self.__comparing_values(expected_result, actually_result,
                                'Comparing values after allocate for block of MiddleOffice',
                                'self.middle_office.compare_values')
        extraction_fields = [AllocationsColumns.sts.value, AllocationsColumns.match_status.value,
                             AllocationsColumns.total_fees.value, AllocationsColumns.client_comm.value]
        expected_results = [{AllocationsColumns.sts.value: 'Affirmed'},
                            {AllocationsColumns.match_status.value: 'Matched'},
                            {AllocationsColumns.total_fees.value: negative_value},
                            {AllocationsColumns.client_comm.value: negative_value}]
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
