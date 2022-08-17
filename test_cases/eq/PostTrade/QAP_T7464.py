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
from test_framework.read_log_wrappers.ReadLogVerifier import ReadLogVerifier
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, PostTradeStatuses, ExecSts, \
    MiddleOfficeColumns, AllocationsColumns
from test_framework.win_gui_wrappers.oms.oms_booking_window import OMSBookingWindow
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T7464(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.rest_api_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.client = self.data_set.get_client('client_pt_1')
        self.alloc_account = self.data_set.get_account_by_name('client_pt_1_acc_1')
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.middle_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.fix_verifier = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.execution_report = FixMessageExecutionReportOMS(self.data_set)
        self.booking_blotter = OMSBookingWindow(self.test_id, self.session_id)
        self.rest_api_manager = RestCommissionsSender(self.rest_api_connectivity, self.test_id, self.data_set)
        self.ors_report = self.environment.get_list_read_log_environment()[0].read_log_conn_ors
        self.read_log_verifier = ReadLogVerifier(self.ors_report, self.test_id)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        global order_id
        qty = '7464'
        price = '10'
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
        indicators_list = [self.data_set.get_net_gross_ind_type('gross_ind'),
                           self.data_set.get_net_gross_ind_type('net_ind')]
        # endregion

        # region create order step 1
        for indicator in indicators_list:
            try:
                new_order_single_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                    self.fix_env.buy_side, account, exec_destination, float(price))
                trade_rule = rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side, account,
                                                                                           exec_destination, float(price),
                                                                                           int(qty), 0)
                response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
                order_id = response[0].get_parameters()['OrderID']
            except Exception as ex:
                logger.exception(f'{ex} - your exception')

            finally:
                time.sleep(10)
                rule_manager.remove_rule(trade_rule)
                rule_manager.remove_rule(new_order_single_rule)

            # endregion

            # region check expected result from precondition
            filter_list = [OrderBookColumns.order_id.value, order_id]
            dict_of_extraction = {OrderBookColumns.post_trade_status.value: OrderBookColumns.post_trade_status.value,
                                  OrderBookColumns.exec_sts.value: OrderBookColumns.exec_sts.value}
            expected_result = {OrderBookColumns.post_trade_status.value: PostTradeStatuses.ready_to_book.value,
                               OrderBookColumns.exec_sts.value: ExecSts.filled.value}
            message = "Comparing expected and actual result from precondition"
            self.__check_expected_result_from_order_book(filter_list, expected_result, dict_of_extraction, message)
            # endregion

            # region step 1 and step 2
            self.middle_office.set_modify_ticket_details(net_gross_ind=indicator)
            self.middle_office.book_order(filter_list)
            # endregion

            # region check expected result from step 2
            expected_result.pop(OrderBookColumns.exec_sts.value)
            dict_of_extraction.pop(OrderBookColumns.exec_sts.value)
            expected_result.update({OrderBookColumns.post_trade_status.value: PostTradeStatuses.booked.value})
            message = "Comparing expected and actual values after book for order"
            self.__check_expected_result_from_order_book(filter_list, expected_result, dict_of_extraction, message)
            list_of_column = [MiddleOfficeColumns.sts.value, MiddleOfficeColumns.match_status.value]
            expected_result.clear()
            filter_list = [MiddleOfficeColumns.order_id.value, order_id]
            expected_result.update({MiddleOfficeColumns.sts.value: MiddleOfficeColumns.appr_pending_sts.value,
                                    MiddleOfficeColumns.match_status.value: MiddleOfficeColumns.unmatched_sts.value})
            message = message.replace('order', 'block')
            self.__extract_and_check_value_from_block(list_of_column, filter_list, expected_result, message)
            # endregion

            # region allocate block step 3
            allocation_param = [
                {AllocationsColumns.security_acc.value: self.data_set.get_account_by_name("client_pt_1_acc_1"),
                 AllocationsColumns.alloc_qty.value: qty}]
            self.middle_office.set_modify_ticket_details(arr_allocation_param=allocation_param)
            self.middle_office.allocate_block(filter_list)
            # endregion

            # region check actual result with expected result  from step 3
            expected_result.update({MiddleOfficeColumns.sts.value: MiddleOfficeColumns.accepted_sts.value,
                                    MiddleOfficeColumns.match_status.value: MiddleOfficeColumns.matched_sts.value,
                                    MiddleOfficeColumns.summary_status.value: MiddleOfficeColumns.matched_agreed_sts.value})
            list_of_column.append(MiddleOfficeColumns.summary_status.value)
            message = "Comparing expected and actual values after allocation for block"
            self.__extract_and_check_value_from_block(list_of_column, filter_list, expected_result, message)
            filter_dict = {filter_list[0]: filter_list[1]}
            actually_result_from_allocation = self.middle_office.extract_list_of_allocate_fields(
                [AllocationsColumns.sts.value, AllocationsColumns.match_status.value, AllocationsColumns.alloc_id.value], filter_dict_block=filter_dict,
                clear_filter_from_block=True)
            allocation_id = actually_result_from_allocation.pop(AllocationsColumns.alloc_id.value)
            self.middle_office.compare_values({AllocationsColumns.sts.value: AllocationsColumns.affirmed_sts.value,
                                               AllocationsColumns.match_status.value: AllocationsColumns.matced_sts.value},
                                              actually_result_from_allocation,
                                              'Comparing actual and expected result from alllocation')
            # endregion

            # region Check ALS logs Status New
            als_message = dict()
            als_message.update({"ConfirmationID": allocation_id, "NetGrossInd": indicator})
            self.read_log_verifier.check_read_log_message(als_message, ["ConfirmationID"], timeout=50000)
            # endregion

    def __check_expected_result_from_order_book(self, filter_list, expected_result, dict_of_extraction, message):
        self.order_book.set_filter(filter_list=filter_list)
        actual_result = self.order_book.extract_fields_list(
            dict_of_extraction)
        self.order_book.compare_values(expected_result, actual_result,
                                       message)

    def __extract_and_check_value_from_block(self, list_of_column, filter_list, expected_result, message):
        self.middle_office.clear_filter()
        actual_result = self.middle_office.extract_list_of_block_fields(list_of_column=list_of_column,
                                                                        filter_list=filter_list)
        self.middle_office.compare_values(expected_result, actual_result, message)
