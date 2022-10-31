import logging
import os
import time
from datetime import datetime
from pathlib import Path
from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.ors_messages.OrderModificationRequest import OrderModificationRequest
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBagColumn, OrderBookColumns
from test_framework.win_gui_wrappers.oms.oms_bag_order_book import OMSBagOrderBook
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7648(TestCase):
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
        qty = '1087'
        new_qty_for_one_order = '1090'
        price = '10'
        client = self.data_set.get_client_by_name('client_pt_1')
        self.fix_message.set_default_dma_limit()
        self.fix_message.change_parameter('OrderQtyData', {'OrderQty': qty})
        self.fix_message.change_parameter('Account', client)
        self.fix_message.change_parameter('Instrument', self.data_set.get_fix_instrument_by_name('instrument_1'))
        self.fix_message.change_parameter('Price', price)
        exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.fix_message.change_parameter('ExDestination', exec_destination)
        self.fix_message.change_parameter("HandlInst", '3')
        qty_of_bag = str(int(qty) * 2)
        qty_of_bag_after_modification = str(int(qty_of_bag) + 3)
        qty_of_bag = QAP_T7648.__adjustment_of_value(qty_of_bag)
        qty_of_bag_after_modification = QAP_T7648.__adjustment_of_value(qty_of_bag_after_modification)
        orders_id = []
        name_of_bag = 'Bag_QAP_1087'
        filter_for_client_inbox = {OrderBookColumns.qty.value: qty}
        # endregion

        # region create 3 CO order (precondition)
        for i in range(2):
            self.fix_manager.send_message_fix_standard(self.fix_message)
            self.client_inbox.accept_order(filter=filter_for_client_inbox)
            self.order_book.set_filter([OrderBookColumns.qty.value, qty])
            orders_id.append(self.order_book.extract_field(OrderBookColumns.order_id.value, 1))
        # endregion

        # region create Bag and extract values from it
        self.bag_order_book.create_bag_details([1, 2], name_of_bag=name_of_bag, price=price)
        self.bag_order_book.create_bag()
        self.__extracting_and_comparing_value_for_bag_order([OrderBagColumn.order_bag_qty.value,
                                                             OrderBagColumn.ord_bag_name.value,
                                                             OrderBagColumn.unmatched_qty.value,
                                                             OrderBagColumn.leaves_qty.value
                                                             ], [
                                                                qty_of_bag,
                                                                name_of_bag,
                                                                qty_of_bag,
                                                                qty_of_bag],
                                                            False, ' creating')
        # endregion

        # region modification bag order and check value after modification
        order_modification_message_java_api = {
            'SEND_SUBJECT': 'QUOD.ORS.FE',
            'REPLY_SUBJECT': 'QUOD.FE.ORS',
            'OrderModificationRequestBlock': {
                'OrdID': orders_id[0],
                'OrdType': 'LMT',
                'Price': price,
                'TimeInForce': 'DAY',
                'PositionEffect': 'O',
                'OrdQty': new_qty_for_one_order,
                'OrdCapacity': 'A',
                'TransactTime': (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y-%m-%dT%H:%M:%S'),
                'MaxPriceLevels': '1',
                'BookingType': 'REG',
                'SettlCurrency': self.data_set.get_currency_by_name('currency_1'),
                'CancelChildren': 'N',
                'ModifyChildren': 'N',
                'RouteID': 1,
                'ExecutionPolicy': 'C',
                'AccountGroupID': client,
                'WashBookAccountID': self.data_set.get_washbook_account_by_name('washbook_account_3')
            }
        }
        java_api_message = OrderModificationRequest(order_modification_message_java_api)
        self.java_api_manager.send_message(java_api_message)
        time.sleep(3)
        self.client_inbox.accept_modify_plus_child(filter=filter_for_client_inbox)
        # endregion

        # extracting and comparing values after modification
        self.__extracting_and_comparing_value_for_bag_order([OrderBagColumn.order_bag_qty.value,
                                                             OrderBagColumn.ord_bag_name.value,
                                                             OrderBagColumn.unmatched_qty.value,
                                                             OrderBagColumn.leaves_qty.value
                                                             ], [
                                                                qty_of_bag_after_modification,
                                                                name_of_bag,
                                                                qty_of_bag_after_modification,
                                                                qty_of_bag_after_modification],
                                                            False, ' modification')
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

    @staticmethod
    def __adjustment_of_value(string_value: str):
        new_value = str()
        for i in range(len(string_value)):
            if i is 1:
                new_value = new_value + ',' + string_value[i]
            else:
                new_value = new_value + string_value[i]
        return new_value
