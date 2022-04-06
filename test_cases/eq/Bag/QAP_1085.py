import logging
import os
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.ors_messages.ModifyBagOrderRequest import ModifyBagOrderRequest
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBagColumn, OrderBookColumns
from test_framework.win_gui_wrappers.oms.oms_bag_order_book import OMSBagOrderBook
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_1085(TestCase):
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.case_id = bca.create_event(os.path.basename(__file__), self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.case_id)
        self.order_book = OMSOrderBook(self.case_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.case_id, self.session_id)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.case_id)
        self.bag_order_book = OMSBagOrderBook(self.case_id, self.session_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        qty = '300'
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
        qty_of_bag = str(int(qty) * 3)
        qty_of_bag_after_modification = str(int(qty) * 2)
        orders_id = []
        name_of_bag = 'Bag_B'
        # endregion
        # region create 3 CO order
        self.fix_message.change_parameter("HandlInst", '3')
        for i in range(3):
            self.fix_manager.send_message_fix_standard(self.fix_message)
            self.client_inbox.accept_order(lookup, qty, price,)
            orders_id.append(self.order_book.extract_field(OrderBookColumns.order_id.value, 1))
        # endregion

        # region create Bag and extract values from it
        self.bag_order_book.create_bag_details([1, 2, 3], name_of_bag=name_of_bag, price='5')
        self.bag_order_book.create_bag()
        fields = self.bag_order_book.extract_order_bag_book_details('1', [OrderBagColumn.order_bag_qty.value,
                                                                          OrderBagColumn.ord_bag_name.value,
                                                                          OrderBagColumn.id.value,
                                                                          OrderBagColumn.unmatched_qty.value,
                                                                          OrderBagColumn.leaves_qty.value
                                                                          ])
        order_bag_id = fields.pop('order_bag.' + OrderBagColumn.id.value)
        expected_values_first = {'order_bag.' + OrderBagColumn.order_bag_qty.value: qty_of_bag,
                                 'order_bag.' + OrderBagColumn.ord_bag_name.value: name_of_bag,
                                 'order_bag.' + OrderBagColumn.unmatched_qty.value: qty_of_bag,
                                 'order_bag.' + OrderBagColumn.leaves_qty.value: qty_of_bag,
                                 }
        self.bag_order_book.compare_values(expected_values_first,
                                           fields, 'Compare values from bag_book before modification')

        # endregion

        # region modify bag_order and verifying bag_order after modify
        java_api_message = ModifyBagOrderRequest()
        java_api_message.set_default(order_bag_id, '10', name_of_bag)
        java_api_message.add_components_into_repeating_group('OrderBagOrderList', 'OrderBagOrderBlock', 'OrdID',
                                                             orders_id[:-1])
        self.java_api_manager.send_message(java_api_message)
        # endregion

        fields_2 = self.bag_order_book.extract_order_bag_book_details('1', [OrderBagColumn.order_bag_qty.value,
                                                                            OrderBagColumn.ord_bag_name.value,
                                                                            OrderBagColumn.id.value,
                                                                            OrderBagColumn.unmatched_qty.value,
                                                                            OrderBagColumn.leaves_qty.value
                                                                            ])
        expected_values_second = {'order_bag.' + OrderBagColumn.order_bag_qty.value: qty_of_bag_after_modification,
                                  'order_bag.' + OrderBagColumn.ord_bag_name.value: name_of_bag,
                                  'order_bag.' + OrderBagColumn.id.value: order_bag_id,
                                  'order_bag.' + OrderBagColumn.unmatched_qty.value: qty_of_bag_after_modification,
                                  'order_bag.' + OrderBagColumn.leaves_qty.value: qty_of_bag_after_modification
                                  }
        self.bag_order_book.compare_values(expected_values_second,
                                           fields_2, 'Compare values from bag_book after modification')
