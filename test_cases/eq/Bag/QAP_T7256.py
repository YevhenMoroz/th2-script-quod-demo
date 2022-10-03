import logging
import os
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBagColumn, OrderBookColumns
from test_framework.win_gui_wrappers.oms.oms_bag_order_book import OMSBagOrderBook
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7256(TestCase):
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

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        qty = '5321'
        price = '10'
        client_name = self.data_set.get_client_by_name('client_pt_1')
        client_name_2 = self.data_set.get_client_by_name('client_pt_2')
        client_desk = self.data_set.get_client_desk('client_desk_1')
        self.fix_message.set_default_dma_limit()
        self.fix_message.change_parameter('OrderQtyData', {'OrderQty': qty})
        self.fix_message.change_parameter('Account', client_name)
        self.fix_message.change_parameter('Instrument', self.data_set.get_fix_instrument_by_name('instrument_1'))
        self.fix_message.change_parameter('Price', price)
        exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.fix_message.change_parameter('ExDestination', exec_destination)
        lookup = self.data_set.get_lookup_by_name('lookup_1')
        self.fix_message.change_parameter("HandlInst", '3')
        qty_of_bag = self._adjustment_of_value(str(int(qty) * 2))
        orders_id = []
        name_of_bag = 'QAP_T7256'
        inbox_filter = {'ClientName': client_name}
        # endregion

        # region create 2 CO order (precondition)
        for i in range(2):
            if i == 1:
                self.fix_message.change_parameter('Account', client_name_2)
            self.fix_manager.send_message_fix_standard(self.fix_message)
            self.client_inbox.accept_order(lookup, qty, price,
                                           filter=inbox_filter)
            self.order_book.set_filter([OrderBookColumns.qty.value, qty])
            orders_id.append(self.order_book.extract_field(OrderBookColumns.order_id.value, 1))
        # endregion

        # region create Bag and check Client Name (step 1, step 2, step 3)
        self.bag_order_book.create_bag_details([1, 2], name_of_bag=name_of_bag, price=price)
        self.bag_order_book.create_bag()
        self._extracting_and_comparing_value_for_bag_order([OrderBagColumn.order_bag_qty.value,
                                                            OrderBagColumn.ord_bag_name.value,
                                                            OrderBagColumn.unmatched_qty.value,
                                                            OrderBagColumn.leaves_qty.value,
                                                            OrderBagColumn.client_name.value,
                                                            OrderBagColumn.client_desk.value
                                                            ],
                                                           [
                                                               qty_of_bag,
                                                               name_of_bag,
                                                               qty_of_bag,
                                                               qty_of_bag,
                                                               '',
                                                               ''
                                                           ], False, 'creation')

        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def _extracting_and_comparing_value_for_bag_order(self, bag_column_extraction: list, expected_values: list,
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
                                           fields, f'Compare values from bag_book after {action}')
        if return_order_bag_id:
            return order_bag_id

    @staticmethod
    @try_except(test_id=Path(__file__).name[:-3])
    def _adjustment_of_value(string_value: str):
        new_value = str()
        for i in range(len(string_value)):
            if i == 2:
                new_value = new_value + ',' + string_value[i]
            else:
                new_value = new_value + string_value[i]
        return new_value
