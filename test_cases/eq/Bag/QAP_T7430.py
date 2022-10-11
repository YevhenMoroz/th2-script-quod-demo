import logging
import os
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from stubs import Stubs
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBagColumn, OrderBookColumns, WaveColumns, \
    BagStatuses, PostTradeStatuses, DoneForDays
from test_framework.win_gui_wrappers.oms.oms_bag_order_book import OMSBagOrderBook
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7430(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.bag_order_book = OMSBagOrderBook(self.test_id, self.session_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.rule_manager = RuleManager(Simulators.equity)
        self.middle_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.act_java_api = Stubs.act_java_api

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        qty = '3881'
        qty_of_wave = str(int(int(qty) * 2))
        price = '10'
        client_for_rule = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        self.fix_message.set_default_dma_limit()
        self.fix_message.change_parameter('OrderQtyData', {'OrderQty': qty})
        self.fix_message.change_parameter('Account', self.data_set.get_client_by_name('client_pt_1'))
        self.fix_message.change_parameter('Instrument', self.data_set.get_fix_instrument_by_name('instrument_1'))
        self.fix_message.change_parameter('Price', price)
        exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.fix_message.change_parameter('ExDestination', exec_destination)
        lookup = self.data_set.get_lookup_by_name('lookup_1')
        self.fix_message.change_parameter("HandlInst", '3')
        new_order_single_rule = trade_rule = None
        orders_id = []
        name_of_bag = 'QAP_T7430'

        # endregion

        # region step 1 , step 2 and step 3
        self.fix_message.change_parameter("HandlInst", '3')
        for i in range(2):
            self.fix_manager.send_message_fix_standard(self.fix_message)
            self.client_inbox.accept_order(lookup, qty, price)
            self.order_book.set_filter([OrderBookColumns.qty.value, qty])
            orders_id.append(self.order_book.extract_field(OrderBookColumns.order_id.value, 1))
        self.order_book.set_filter([OrderBookColumns.qty.value, qty])
        self.bag_order_book.create_bag_details([1, 2], name_of_bag=name_of_bag)
        self.bag_order_book.create_bag()
        self.__extracting_and_comparing_value_for_bag_order([OrderBagColumn.ord_bag_name.value,
                                                             OrderBagColumn.bag_status.value
                                                             ], [name_of_bag, BagStatuses.new.value],
                                                            False, 'creating')
        complete_filter = {OrderBagColumn.ord_bag_name.value: name_of_bag}
        # endregion

        # region step 4 and step 5
        try:
            new_order_single_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side,
                client_for_rule, exec_destination,
                float(price))
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                                            client_for_rule,
                                                                                            exec_destination,
                                                                                            float(price),
                                                                                            traded_qty=int(qty),
                                                                                            delay=0)
            self.bag_order_book.set_order_bag_wave_details(tif=self.data_set.get_time_in_force('time_in_force_1'),
                                                           price=price, qty=qty_of_wave)
            self.bag_order_book.wave_bag()
        except Exception as e:
            logger.error(f'{e}')
        finally:
            time.sleep(5)
            self.rule_manager.remove_rule(new_order_single_rule)
            self.rule_manager.remove_rule(trade_rule)
        fields = self.bag_order_book.extract_from_order_bag_book_and_other_tab('1',
                                                                               extraction_fields=[
                                                                                   OrderBagColumn.id.value],
                                                                               sub_extraction_fields=[
                                                                                   WaveColumns.status.value])
        self.bag_order_book.compare_values(
            {WaveColumns.status.value: BagStatuses.terminated.value},
            {WaveColumns.status.value:
                 fields[WaveColumns.status.value]}, 'Comparing Status of Wave')
        # endregion

        # region complete bag(step 6)
        self.bag_order_book.complete_or_un_complete_bag(complete_filter)
        # endregion

        # region book bag order(step 7 and step 8)
        modify_ticket_details = self.middle_office.set_modify_ticket_details(agreed_price='2')
        self.bag_order_book.book_bag(modify_ticket_details)
        self.__checking_post_trade_status(orders_id, expected_post_trade_status=PostTradeStatuses.booked.value,
                                          expected_done_for_day=DoneForDays.yes.value)
        # endregion

        # region un-complete bag (step 9)
        self.bag_order_book.complete_or_un_complete_bag(complete_filter, False)
        self.__checking_post_trade_status(orders_id, expected_post_trade_status='',
                                          expected_done_for_day='')
        # endregion

        # region re-complete bag (step 10)
        self.bag_order_book.complete_or_un_complete_bag(complete_filter, True)
        self.__checking_post_trade_status(orders_id, expected_post_trade_status=PostTradeStatuses.ready_to_book.value,
                                          expected_done_for_day=DoneForDays.yes.value)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def __extracting_and_comparing_value_for_bag_order(self, bag_column_extraction: list, expected_values: list,
                                                       return_order_bag_id: bool, action: str):
        fields = self.bag_order_book.extract_order_bag_book_details('1', bag_column_extraction)
        expected_values_bag = dict()
        order_bag_id = None
        if return_order_bag_id:
            order_bag_id = fields.pop(OrderBagColumn.id.value)
            bag_column_extraction.remove(OrderBagColumn.id.value)
        for count in range(len(bag_column_extraction)):
            expected_values_bag.update({bag_column_extraction[count]: expected_values[count]})
        self.bag_order_book.compare_values(expected_values_bag,
                                           fields, f'Compare values from bag_book after{action}')
        if return_order_bag_id:
            return order_bag_id

    @try_except(test_id=Path(__file__).name[:-3])
    def __checking_post_trade_status(self, orders_id: list, expected_done_for_day, expected_post_trade_status):
        post_trade_column = OrderBookColumns.post_trade_status.value
        done_for_day_column = OrderBookColumns.done_for_day.done_for_day.value
        for index in range(len(orders_id)):
            self.order_book.set_filter([OrderBookColumns.order_id.value, orders_id[index]])
            fields = self.order_book.extract_fields_list({post_trade_column: post_trade_column,
                                                          done_for_day_column: done_for_day_column})
            self.order_book.compare_values({post_trade_column: expected_post_trade_status,
                                            done_for_day_column: expected_done_for_day},
                                           fields,
                                           'Comparing values')
