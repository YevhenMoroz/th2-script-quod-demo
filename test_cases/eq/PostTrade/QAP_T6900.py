import logging
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.oms.RestApiModifyInstitutionMessage import RestApiModifyInstitutionMessage
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, DoneForDays, \
    PostTradeStatuses, ExecSts, MiddleOfficeColumns, SecondLevelTabs, ChildOrderBookColumns, AllocationsColumns
from test_framework.win_gui_wrappers.oms.oms_booking_window import OMSBookingWindow
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T6900(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.rest_api_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.qty = '6900'
        self.price = '10'
        self.check_qty = self.qty[0]+','+self.qty[1:4]
        self.client = self.data_set.get_client('client_pt_1')
        self.venue_client_name = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        self.ex_destination = self.data_set.get_mic_by_name('mic_1')
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.middle_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.fix_verifier = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.execution_report = FixMessageExecutionReportOMS(self.data_set)
        self.booking_blotter = OMSBookingWindow(self.test_id, self.session_id)
        self.rest_api_manager = RestApiManager(session_alias=self.rest_api_connectivity, case_id=self.test_id)
        self.rule_manager = RuleManager(Simulators.equity)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # # region update Institution via RestApi(Precondition)
        # rest_api_message = RestApiModifyInstitutionMessage(self.data_set)
        # rest_api_message.set_default_param()
        # rest_api_message.modify_enable_unknown_accounts(True)
        # self.rest_api_manager.send_post_request(rest_api_message)
        # # endregion

        # region create  DMA order via fix and trade it (step 1 and step 2)
        self.fix_message.set_default_dma_limit()
        alt_acount = 'AltAccount'
        self.fix_message.change_parameters(
            {'Side': '1', 'OrderQtyData': {'OrderQty': self.qty}, 'Account': self.client, 'Price': self.price})
        self.fix_message.add_tag({'PreAllocGrp': {'NoAllocs': [{'AllocAccount': alt_acount, 'AllocQty': self.qty}]}})
        trade_rule = new_order_single_rule = False
        try:
            new_order_single_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side, self.venue_client_name, self.ex_destination, float(self.price))
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                                            self.venue_client_name,
                                                                                            self.ex_destination,
                                                                                            float(self.price),
                                                                                            int(self.qty), delay=0
                                                                                            )
            response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
            order_id = response[0].get_parameters()['OrderID']
        except Exception as e:
            logger.error(f'{e}', exc_info=True)

        finally:
            time.sleep(3)
            self.rule_manager.remove_rule(new_order_single_rule)
            self.rule_manager.remove_rule(trade_rule)

        # endregion

        # region check expected result from step 1
        filter_list = [OrderBookColumns.order_id.value, order_id]
        filter_dict = {OrderBookColumns.order_id.value: order_id}
        values = self.order_book.extract_2lvl_fields(SecondLevelTabs.pre_trade_alloc_tab.value,
                                                     [ChildOrderBookColumns.id_allocation.value,
                                                      ChildOrderBookColumns.qty_alloc.value,
                                                      ChildOrderBookColumns.percent.value], rows=[1],
                                                     filter_dict=filter_dict)
        expected_result = {ChildOrderBookColumns.id_allocation.value: alt_acount+',',
                           ChildOrderBookColumns.qty_alloc.value: self.check_qty+',',
                           ChildOrderBookColumns.percent.value: '100'}
        self.order_book.compare_values(expected_result, values[0], 'Comparing values on Pre Trade Allocations from step1')

        # endregion

        # region check  expected result from step 2
        expected_result={OrderBookColumns.exec_sts.value: ExecSts.filled.value,
                                OrderBookColumns.done_for_day.value: DoneForDays.yes.value,
                                OrderBookColumns.post_trade_status.value: PostTradeStatuses.ready_to_book.value}
        column_dict={OrderBookColumns.exec_sts.value: OrderBookColumns.exec_sts.value,
                            OrderBookColumns.done_for_day.value: OrderBookColumns.done_for_day.value,
                            OrderBookColumns.post_trade_status.value: OrderBookColumns.post_trade_status.value}
        self.__check_expected_result_of_order(column_dict,
                                              filter_list, expected_result,
                                              '2')
        # endregion

        # region book DMA order (step 3)
        self.middle_office.book_order(filter_list)
        # endregion

        # region check expected result from step 3
        """
        Order
        """
        column_dict.pop(OrderBookColumns.exec_sts.value)
        expected_result.pop(OrderBookColumns.exec_sts.value)
        expected_result.update({OrderBookColumns.post_trade_status.value: PostTradeStatuses.booked.value})
        self.__check_expected_result_of_order(column_dict,
                                              filter_list, expected_result,
                                              '3')
        '''
        Block
        '''
        filter_list_for_block = [MiddleOfficeColumns.order_id.value, order_id]
        list_extraction = [MiddleOfficeColumns.sts.value, MiddleOfficeColumns.match_status.value]
        self.middle_office.clear_filter()
        values = self.middle_office.extract_list_of_block_fields(list_extraction, filter_list_for_block)
        expected_result = {MiddleOfficeColumns.sts.value: MiddleOfficeColumns.appr_pending_sts.value,
                           MiddleOfficeColumns.match_status.value: MiddleOfficeColumns.unmatched_sts.value}
        self.middle_office.compare_values(expected_result, values, 'Comparing values from expected result of step 3')
        # endregion

        # region step 4
        self.middle_office.approve_block()
        self.middle_office.allocate_block(filter_list_for_block)
        # endregion

        # region check expected result of step 4
        # Block
        list_extraction.append(MiddleOfficeColumns.summary_status.value)
        self.middle_office.clear_filter()
        values = self.middle_office.extract_list_of_block_fields(list_extraction, filter_list_for_block)
        expected_result.update({MiddleOfficeColumns.sts.value: MiddleOfficeColumns.accepted_sts.value,
                                MiddleOfficeColumns.match_status.value: MiddleOfficeColumns.matched_sts.value,
                                MiddleOfficeColumns.summary_status.value: MiddleOfficeColumns.matched_agreed_sts.value})
        self.middle_office.compare_values(expected_result, values,
                                          'Comparing values from expected result of step 4 for Block')
        # Allocation
        list_extraction.clear()
        list_extraction.extend([AllocationsColumns.alt_account.value, AllocationsColumns.alloc_qty.value])
        expected_result.clear()
        filter_dict_block = {filter_list_for_block[0]: filter_list_for_block[1]}
        values = self.middle_office.extract_list_of_allocate_fields(list_extraction,
                                                                    filter_dict_block=filter_dict_block,
                                                                    clear_filter_from_block=True)
        expected_result.update(
            {AllocationsColumns.alt_account.value: alt_acount, AllocationsColumns.alloc_qty.value: self.check_qty+','})
        self.middle_office.compare_values(expected_result, values,
                                          'Comparing values from expected result of step 4 for Allocation')
        # endregion

    def __check_expected_result_of_order(self, column_of_extraction: dict, filter_list, expected_result,
                                         step_number: str):
        self.order_book.set_filter(filter_list)
        value = self.order_book.extract_fields_list(column_of_extraction)
        self.order_book.compare_values(expected_result, value, f'Comparing expected result of step{step_number}')
