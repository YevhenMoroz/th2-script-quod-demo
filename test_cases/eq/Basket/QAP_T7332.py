import logging
import os
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.verifier import VerificationMethod
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import BasketBookColumns, OrderBookColumns, ClientInboxColumns
from test_framework.win_gui_wrappers.oms.oms_basket_order_book import OMSBasketOrderBook
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7332(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.basket_book = OMSBasketOrderBook(self.test_id, self.session_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        qty = '4670'
        price = '10'
        self.fix_message.set_default_care_limit()
        first_client = self.data_set.get_client_by_name('client_pt_1')
        self.fix_message.change_parameter('OrderQtyData', {'OrderQty': qty})
        self.fix_message.change_parameter('Account', first_client)
        self.fix_message.change_parameter('Instrument', self.data_set.get_fix_instrument_by_name('instrument_1'))
        self.fix_message.change_parameter('Price', price)
        exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.fix_message.change_parameter('ExDestination', exec_destination)
        lookup = self.data_set.get_lookup_by_name('lookup_1')
        orders_id = []
        basket_name = "QAP_T7332"
        second_client = self.data_set.get_client_by_name('client_pt_2')
        filter_dict = {ClientInboxColumns.qty.value: qty}
        filter_qty = [OrderBookColumns.qty.value, qty]
        basket_filter = {BasketBookColumns.basket_name.value: basket_name}
        # endregion

        # region create 3 CO order and basket(step 1, step 2)
        for i in range(3):
            if i < 2:
                self.fix_manager.send_message_fix_standard(self.fix_message)
            else:
                self.fix_message.change_parameter('Account', second_client)
                self.fix_manager.send_message_fix_standard(self.fix_message)
            self.client_inbox.accept_order(lookup, qty, price,
                                           filter=filter_dict)
            self.order_book.set_filter(filter_qty)

            orders_id.append(self.order_book.extract_field(OrderBookColumns.order_id.value, 1))
        self.order_book.extract_field(OrderBookColumns.order_id.value)
        self.order_book.set_filter(filter_qty)
        self.order_book.create_basket([2, 3], basket_name)
        basket_id = self.basket_book.get_basket_value(BasketBookColumns.id.value, basket_filter)
        # endregion

        # region add order in basket(step 3)
        filter_list = [OrderBookColumns.order_id.value, orders_id[0]]
        self.order_book.set_filter(filter_list)
        result = self.order_book.add_to_basket([1], basket_name, True)
        self.order_book.compare_values({'Footer Value': 'Error - [QUOD-11505]'},
                                       result, 'Comparing error message', VerificationMethod.CONTAINS)
        # endregion
