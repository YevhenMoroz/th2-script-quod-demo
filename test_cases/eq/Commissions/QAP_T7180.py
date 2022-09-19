import logging
import time

from pathlib import Path
from th2_grpc_act_gui_quod.middle_office_pb2 import PanelForExtraction
from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, PostTradeStatuses, \
    MiddleOfficeColumns, AllocationsColumns, ExecSts
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()


class QAP_T7180(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.bs_connectivity = self.fix_env.buy_side
        self.qty = '7180'
        self.price = '10'
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.currency = self.data_set.get_currency_by_name('currency_3')  # GBp
        self.venue_client_names = self.data_set.get_venue_client_names_by_name('client_com_1_venue_2')  # MOClient_EUREX
        self.venue = self.data_set.get_mic_by_name('mic_2')  # XEUR
        self.client = self.data_set.get_client('client_com_1')  #
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.middle_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region set client_commission precondition
        trade_rule = order_id = new_order_single = None
        self.rest_commission_sender.clear_commissions()
        self.rest_commission_sender.set_modify_client_commission_message(
            comm_profile=self.data_set.get_comm_profile_by_name('commission_with_minimal_value'))
        self.rest_commission_sender.send_post_request()
        # endregion

        # region create DMA order (precondition)
        try:
            new_order_single = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.bs_connectivity,
                self.venue_client_names,
                self.venue,
                float(self.price))
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.bs_connectivity,
                                                                                            self.venue_client_names,
                                                                                            self.venue,
                                                                                            float(self.price),
                                                                                            int(self.qty), 0)
            self.fix_message.set_default_dma_limit(instr='instrument_3')
            self.fix_message.change_parameters(
                {'Side': '1', 'OrderQtyData': {'OrderQty': self.qty}, 'Account': self.client, 'Price': self.price,
                 'Currency': self.currency, 'ExDestination': 'XEUR'})
            response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
            order_id = response[0].get_parameters()['OrderID']

        except Exception:
            logger.error('Error execution', exc_info=True)
        finally:
            time.sleep(2)
            self.rule_manager.remove_rule(new_order_single)
            self.rule_manager.remove_rule(trade_rule)
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

        # region step 1
        filter_list = [MiddleOfficeColumns.order_id.value, order_id]
        self.middle_office.book_order(filter_list)
        # endregion

        # region check actual result from step 1
        expected_result = {OrderBookColumns.post_trade_status.value: PostTradeStatuses.booked.value}
        dict_of_extraction = {OrderBookColumns.post_trade_status.value: OrderBookColumns.post_trade_status.value}
        message = "Comparing expected and actual values after book of order(step 1)"
        self.__check_expected_result_from_order_book(filter_list, expected_result, dict_of_extraction, message)
        list_of_column = [MiddleOfficeColumns.conf_service.value]
        expected_result.clear()
        filter_list = [MiddleOfficeColumns.order_id.value, order_id]
        expected_result.update({MiddleOfficeColumns.conf_service.value: MiddleOfficeColumns.manual.value})
        message = message.replace('order', 'block')
        self.__extract_and_check_value_from_block(list_of_column, filter_list, expected_result, message)
        # endregion

        # region step 2
        self.middle_office.approve_block()
        # endregion

        # region check actual result from step 2
        expected_result.clear()
        expected_result.update({MiddleOfficeColumns.sts.value: MiddleOfficeColumns.accepted_sts.value,
                                MiddleOfficeColumns.match_status.value: MiddleOfficeColumns.matched_sts.value})
        list_of_column.clear()
        list_of_column.extend([MiddleOfficeColumns.sts.value, MiddleOfficeColumns.match_status.value])
        message = "Comparing value after approve(step 2)"
        self.__extract_and_check_value_from_block(list_of_column, filter_list, expected_result, message)
        filter_dict = {filter_list[0]: filter_list[1]}
        # endregion

        # region step 3 and step 4
        values = self.middle_office.extracting_values_from_allocation_ticket([PanelForExtraction.COMMISSION],
                                                                             filter_dict)
        values_splited = self.middle_office.split_fees(values)
        expected_result_for_fees = {'Basis': 'Absolute,', 'Rate': '100,', 'Amount': '100,', 'Currency': 'GBP'}
        self.middle_office.compare_values(expected_result_for_fees, values_splited[0],
                                          'Comparing minimum Client commission from allovation Ticket')
        # endregion

        # region step 5
        allocation_param = [
            {AllocationsColumns.security_acc.value: self.data_set.get_account_by_name("client_com_1_acc_1"),
             AllocationsColumns.alloc_qty.value: self.qty}]
        self.middle_office.set_modify_ticket_details(arr_allocation_param=allocation_param)
        self.middle_office.allocate_block(filter_list)
        # endregion

        # check result after step 5
        expected_result.update({MiddleOfficeColumns.sts.value: MiddleOfficeColumns.accepted_sts.value,
                                MiddleOfficeColumns.match_status.value: MiddleOfficeColumns.matched_sts.value,
                                MiddleOfficeColumns.summary_status.value: MiddleOfficeColumns.matched_agreed_sts.value})
        list_of_column.append(MiddleOfficeColumns.summary_status.value)
        message = "Comparing expected and actual values after allocation for block (step 5)"
        self.__extract_and_check_value_from_block(list_of_column, filter_list, expected_result, message)
        actually_result_from_allocation = self.middle_office.extract_list_of_allocate_fields(
            [AllocationsColumns.sts.value, AllocationsColumns.match_status.value],
            filter_dict_block=filter_dict,
            clear_filter_from_block=True)
        self.middle_office.compare_values({AllocationsColumns.sts.value: AllocationsColumns.affirmed_sts.value,
                                           AllocationsColumns.match_status.value: AllocationsColumns.matced_sts.value},
                                          actually_result_from_allocation,
                                          'Comparing actual and expected result from allocation (step 5)')
        # endregion

        # region step 6
        values = self.middle_office.extract_values_from_amend_allocation_ticket([PanelForExtraction.COMMISSION],
                                                                                block_filter_dict=filter_dict)
        result = self.middle_office.split_fees(values)
        self.middle_office.compare_values(expected_result_for_fees, result[0],
                                          'Comparing minimum Client commission from amend allocation Ticket')
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

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_commission_sender.clear_commissions()
