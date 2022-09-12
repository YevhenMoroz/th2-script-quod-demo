import logging
import os
import time
from pathlib import Path

from th2_grpc_act_gui_quod.middle_office_pb2 import PanelForExtraction

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns,  \
    ExecSts, MiddleOfficeColumns
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket
from test_framework.win_gui_wrappers.oms.oms_trades_book import OMSTradesBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()


class QAP_T8339(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.bs_connectivity = self.fix_env.buy_side
        self.ss_connectivity = self.fix_env.sell_side
        self.qty = '7777'
        self.price = '10'
        self.rule_manager = RuleManager(sim=Simulators.equity)
        self.currency = self.data_set.get_currency_by_name('currency_3')
        self.venue_client_names = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        self.venue = self.data_set.get_mic_by_name('mic_2')
        self.client = self.data_set.get_client('client_pt_1')
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.middle_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.trade_book = OMSTradesBook(self.test_id, self.session_id)
        self.fix_verifier = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.pset = self.data_set.get_pset('pset_3')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region create CO  and partially fill it step 1
        self.fix_message.set_default_care_limit(instr='instrument_3')
        self.fix_message.change_parameters(
            {'Side': '1', 'OrderQtyData': {'OrderQty': self.qty}, 'Account': self.client, 'Price': self.price,
             'Currency': self.currency, 'ExDestination': 'XEUR'})
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = response[0].get_parameters()['OrderID']
        self.client_inbox.accept_order({OrderBookColumns.order_id.value: order_id})
        filter_list = [OrderBookColumns.order_id.value, order_id]
        # endregion

        # region check actually  result from step 1
        dict_of_extraction = {OrderBookColumns.sts.value: OrderBookColumns.sts.value}
        expected_result = {OrderBookColumns.sts.value: ExecSts.open.value}
        message = "Check values from expecter result of step 1"
        self.__check_expected_result_from_order_book(filter_list, expected_result, dict_of_extraction, message)
        # endregion

        # region execute order (step 2)
        self.order_book.manual_execution(qty=self.qty)
        # endregion

        # region check actually  result from step 2
        dict_of_extraction = {OrderBookColumns.exec_sts.value: OrderBookColumns.exec_sts.value}
        expected_result = {OrderBookColumns.exec_sts.value: ExecSts.filled.value}
        message = message.replace('1', '2')
        self.__check_expected_result_from_order_book(filter_list, expected_result, dict_of_extraction, message)
        # endregion

        # region book order (step 3)
        self.order_book.complete_order(filter_list=filter_list)
        self.middle_office.book_order(filter_list)
        # endregion

        # region check actually result from step 3
        filter_list = [MiddleOfficeColumns.order_id.value, order_id]
        list_of_column = [MiddleOfficeColumns.pset.value, MiddleOfficeColumns.pset_bic.value]
        expected_result = {MiddleOfficeColumns.pset.value: self.pset[0],
                           MiddleOfficeColumns.pset_bic.value: self.pset[1]}
        message.replace('2', '3')
        self.__extract_and_check_value_from_block(list_of_column, filter_list, expected_result, message)
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
