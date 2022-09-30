import logging
import os
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import MenuItemFromOrderBook, OrderBookColumns
from test_framework.win_gui_wrappers.oms.oms_bag_order_book import OMSBagOrderBook
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7652(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.bag_order_book = OMSBagOrderBook(self.test_id, self.session_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.fix_message.set_default_dma_limit()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # Declaration region
        qty = '999'
        price = '10'
        self.fix_message.change_parameter('Account', self.data_set.get_client_by_name('client_pt_1'))
        self.fix_message.change_parameter('Instrument', self.data_set.get_fix_instrument_by_name('instrument_1'))
        self.fix_message.change_parameter('Price', price)
        self.fix_message.change_parameter('OrderQtyData', {'OrderQty': qty})
        lookup = self.data_set.get_lookup_by_name('lookup_1')
        exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.fix_message.change_parameter('ExDestination', exec_destination)
        self.fix_message.change_parameter("HandlInst", '3')
        # endregion

        # region create 3 CO order
        for i in range(3):
            if i >= 2:
                self.fix_message.change_parameter('Side', '2')
                self.fix_manager.send_message_fix_standard(self.fix_message)
                self.client_inbox.accept_order(lookup, qty, price)
            else:
                self.fix_manager.send_message_fix_standard(self.fix_message)
                self.client_inbox.accept_order(lookup, qty, price)
        # endregion

        # region create verify, that bag order book can`t created with order
        self.__verifying_presenting_item_at_menu(MenuItemFromOrderBook.split_bag_by_qty_priority.value, [1, 2, 3],
                                                 {OrderBookColumns.qty.value: qty})
        self.__verifying_presenting_item_at_menu(MenuItemFromOrderBook.split_bag_by_avg_px_priority.value, [1, 2, 3],
                                                 {OrderBookColumns.qty.value: qty})
        self.__verifying_presenting_item_at_menu(MenuItemFromOrderBook.group_into_a_bag_for_grouping.value, [1, 2, 3],
                                                 {OrderBookColumns.qty.value: qty})
        self.__verifying_presenting_item_at_menu(MenuItemFromOrderBook.bag_by_avg_px_priority.value, [1, 2, 3],
                                                 {OrderBookColumns.qty.value: qty})
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def __verifying_presenting_item_at_menu(self, item_of_menu, list_of_orders: list, filter: dict):
        result_1 = self.order_book.is_menu_item_present(item_of_menu,
                                                        list_of_orders, filter)
        self.order_book.compare_values({'Is item present at menu': 'false'}, {'Is item present at menu': result_1},
                                       f'Verifying, that {item_of_menu} '
                                       f'doesn`t present at menu item')
