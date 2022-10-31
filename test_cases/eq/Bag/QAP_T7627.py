import logging
import os
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBagColumn, OrderBookColumns, BagStatuses, \
    SecondLevelTabs
from test_framework.win_gui_wrappers.oms.oms_bag_order_book import OMSBagOrderBook
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7627(TestCase):
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
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        qty = '1442'
        qty_for_verifying_order = qty[0] + ',' + qty[1:4]
        new_qty_of_order = '1'
        qty_of_bag = str(int(int(qty) * 2))
        new_qty_of_bag_for_verifying = qty[0]+','+qty[1:3]+'3'
        qty_for_verifying_bag = qty_of_bag[0] + ',' + qty_of_bag[1:4]
        price = '10'
        self.fix_message.set_default_dma_limit()
        self.fix_message.change_parameter('OrderQtyData', {'OrderQty': qty})
        self.fix_message.change_parameter('Account', self.data_set.get_client_by_name('client_pt_1'))
        self.fix_message.change_parameter('Instrument', self.data_set.get_fix_instrument_by_name('instrument_1'))
        self.fix_message.change_parameter('Price', price)
        exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.fix_message.change_parameter('ExDestination', exec_destination)
        lookup = self.data_set.get_lookup_by_name('lookup_1')
        self.fix_message.change_parameter("HandlInst", '3')
        orders_id = []
        name_of_bag = 'QAP_1442'

        # endregion

        # region step 1
        self.fix_message.change_parameter("HandlInst", '3')
        for i in range(2):
            self.fix_manager.send_message_fix_standard(self.fix_message)
            self.client_inbox.accept_order(lookup, qty, price)
            self.order_book.set_filter([OrderBookColumns.qty.value, qty])
            orders_id.append(self.order_book.extract_field(OrderBookColumns.order_id.value, 1))
        self.order_book.set_filter([OrderBookColumns.qty.value, qty])
        self.bag_order_book.create_bag_details([1, 2], name_of_bag=name_of_bag)
        self.bag_order_book.create_bag()

        sub_filter_list = [OrderBookColumns.order_id.value, orders_id[0]]
        sub_filter_dict = {OrderBookColumns.order_id.value: orders_id[0]}
        filter_list = [OrderBagColumn.ord_bag_name.value, name_of_bag]
        filter_dict = {OrderBagColumn.ord_bag_name.value: name_of_bag}
        expected_result_1 = {OrderBookColumns.qty.value: qty_for_verifying_order,
                             OrderBagColumn.order_bag_qty.value: qty_for_verifying_bag,
                             OrderBagColumn.unmatched_qty.value: qty_for_verifying_bag,
                             OrderBagColumn.ord_bag_name.value: name_of_bag}
        expected_result_2 = {OrderBookColumns.qty.value: new_qty_of_order,
                             OrderBagColumn.order_bag_qty.value: new_qty_of_bag_for_verifying,
                             OrderBagColumn.unmatched_qty.value: new_qty_of_bag_for_verifying,
                             OrderBagColumn.ord_bag_name.value: name_of_bag}
        self.__verifying_values(sub_filter_list, filter_list, expected_result_1)
        # endregion

        # region modify_order_details in sub level tab
        order_details = self.order_ticket.set_order_details(qty='1').order_details
        self.bag_order_book.set_modify_sub_level_order_details(filter_dict, order_details, sub_filter_dict)
        self.__verifying_values(sub_filter_list, filter_list, expected_result_2)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def __verifying_values(self, sub_filter_list, filter_list, expected_result):
        fields = self.bag_order_book.extract_from_order_bag_book_and_other_tab('1', [OrderBagColumn.ord_bag_name.value,
                                                                                     OrderBagColumn.unmatched_qty.value,
                                                                                     OrderBagColumn.leaves_qty.value,
                                                                                     OrderBagColumn.order_bag_qty.value],
                                                                               [OrderBookColumns.qty.value],
                                                                               sub_filter_list,
                                                                               filter_list,
                                                                               table_name=SecondLevelTabs.orders_tab.value)
        self.order_book.compare_values(expected_result, fields, 'Comparing values')
