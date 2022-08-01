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
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, PostTradeStatuses, ExecSts, \
    SecondLevelTabs
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time


class QAP_T6972(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.client = self.data_set.get_client('client_pt_1')
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.middle_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.rule_manager = RuleManager(Simulators.equity)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region create order via fix (step 1)
        qty = '1500'
        price = '33.8'
        self.fix_message.set_default_care_limit('instrument_1')
        self.fix_message.change_parameters(
            {'Side': '1', 'OrderQtyData': {'OrderQty': qty}, 'Account': self.client, 'Price': price})
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = response[0].get_parameters()['OrderID']
        filter_dict = {OrderBookColumns.order_id.value: order_id}
        filter_list = [OrderBookColumns.order_id.value, order_id]
        self.client_inbox.accept_order(filter=filter_dict)
        # endregion

        # region check expected result from step 1
        order_book_sts_column = OrderBookColumns.sts.value
        expected_result = {OrderBookColumns.sts.value: ExecSts.open.value}
        self.order_book.set_filter(filter_list)
        actually_result = self.order_book.extract_fields_list({order_book_sts_column: order_book_sts_column})
        self.order_book.compare_values(expected_result, actually_result, 'Comparing status from step 1')
        # endregion

        # region split CO order(step 2 and step 3)
        self.__split_co_order('1', '32.7', filter_list)
        # endregion

        # region check expected_result of step 3
        actually_result = self.order_book.extract_2lvl_fields(SecondLevelTabs.child_tab.value,
                                                              [OrderBookColumns.sts.value], [1], filter_dict)[0]
        expected_result = {OrderBookColumns.sts.value: ExecSts.terminated.value}

        self.order_book.compare_values(expected_result, actually_result, 'Comparing status of child order from step 3')
        # endregion

        # region step 4
        account_destination = self.data_set.get_account_by_name('client_pos_3_acc_3')
        self.order_book.unmatch_and_transfer(account_destination, filter_dict)
        # endregion

        # region check expected result of step 4
        expected_result = {OrderBookColumns.exec_type.value: ExecSts.trade_cancel.value}
        actually_result = self.order_book.extract_2lvl_fields(SecondLevelTabs.executions.value,
                                                              [OrderBookColumns.exec_type.value], [1], filter_dict)[0]
        self.order_book.compare_values(expected_result, actually_result, "Comparing results of step 4")
        # endregion

        # region step 5 and step 6
        qty_of_child_order = str(int(int(qty) / 3))
        self.__split_co_order(qty_of_child_order, '34', filter_list)
        self.__split_co_order(qty_of_child_order, '33.8', filter_list)
        self.__split_co_order(qty_of_child_order, '34.2', filter_list)
        # endregion

        # region expected result from 6 step
        actually_result = self.order_book.extract_2lvl_fields(SecondLevelTabs.child_tab.value,
                                                              [OrderBookColumns.sts.value],
                                                              [1, 2, 3], filter_dict)
        expected_result = {OrderBookColumns.sts.value: ExecSts.terminated.value}
        for index in range(3):
            self.order_book.compare_values(expected_result, actually_result[index],
                                           f'Comparing values of {index + 1} child order')
        # endregion

        # region step 7
        self.order_book.complete_order(filter_list=filter_list)
        # endregion

        # region check expected result  from step 7
        self.order_book.set_filter(filter_list)
        actually_result = self.order_book.extract_fields_list({OrderBookColumns.post_trade_status.value:
                                                                   OrderBookColumns.post_trade_status.value,
                                                               OrderBookColumns.done_for_day.value:
                                                                   OrderBookColumns.done_for_day.value})
        expected_result = {OrderBookColumns.post_trade_status.value: PostTradeStatuses.ready_to_book.value}
        self.order_book.compare_values(expected_result, actually_result,
                                       f'Comparing calue of {order_id} after complete')
        # endregion

        # region extract values from book step 8
        checking_values = self.order_book.extracting_values_from_booking_ticket(
            [PanelForExtraction.MAIN_PANEL], filter_dict=filter_dict, count_of_rows=1)
        values = self.order_book.split_main_tab(checking_values)
        self.order_book.compare_values({'Agreed Price': ' 34'}, values[-6], 'Comparing agreed price from book')

        # endregion

    def __split_co_order(self, qty: str, price: str, filter_list: list):
        new_order_rule = trade_rule = None
        venue = self.data_set.get_mic_by_name('mic_1')
        client = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        try:
            new_order_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side, client, venue, float(price))
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                                            client, venue, float(price),
                                                                                            int(qty), delay=0
                                                                                            )
            self.order_ticket.set_order_details(qty=qty, limit=price)
            self.order_ticket.split_order(filter_list)
        except Exception as e:
            logger.error(f"{e}", exc_info=True, stack_info=True)
        finally:
            time.sleep(3)
            self.rule_manager.remove_rule(new_order_rule)
            self.rule_manager.remove_rule(trade_rule)
