import logging
import os
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBagColumn, OrderBookColumns, BagStatuses, \
    SecondLevelTabs, DoneForDays, PostTradeStatuses
from test_framework.win_gui_wrappers.oms.oms_bag_order_book import OMSBagOrderBook
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7642(TestCase):
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

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        qty = '1093'
        qty_of_wave = str(int(int(qty) * 2))
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
        name_of_bag = 'QAP_T7642'
        filter_list = [OrderBagColumn.ord_bag_name.value, name_of_bag]
        filter_dict = dict({OrderBagColumn.ord_bag_name.value: name_of_bag})
        # endregion

        # region precondition (creating bag)
        self.fix_message.change_parameter("HandlInst", '3')
        for i in range(2):
            self.fix_manager.send_message_fix_standard(self.fix_message)
            self.client_inbox.accept_order(lookup, qty, price)
            self.order_book.set_filter([OrderBookColumns.qty.value, qty])
            orders_id.append(self.order_book.extract_field(OrderBookColumns.order_id.value, 1))
        self.order_book.set_filter([OrderBookColumns.qty.value, qty])
        self.bag_order_book.create_bag_details([1, 2], name_of_bag=name_of_bag)
        self.bag_order_book.create_bag()
        fields = self.bag_order_book.extract_order_bag_book_details('1', [OrderBagColumn.ord_bag_name.value,
                                                                          OrderBagColumn.bag_status.value
                                                                          ],
                                                                    filter_list)
        self.bag_order_book.compare_values(
            {OrderBagColumn.ord_bag_name.value: name_of_bag, OrderBagColumn.bag_status.value: BagStatuses.new.value},
            fields, "Comparing bag after creating")
        # endregion

        # region step 1 and step 2 complete bag
        self.bag_order_book.complete_or_un_complete_bag(filter_dict, True)
        # endregion

        # region check orders after complete
        for order in orders_id:
            orders_filter = [OrderBookColumns.order_id.value, order]
            fields = self.bag_order_book.extract_from_order_bag_book_and_other_tab('1', sub_extraction_fields=[
                OrderBookColumns.post_trade_status.value,
                OrderBookColumns.done_for_day.value], sub_filter=orders_filter,
                                                                                   table_name=SecondLevelTabs.orders_tab.value)
            self.bag_order_book.compare_values({OrderBookColumns.done_for_day.value: DoneForDays.yes.value,
                                                OrderBookColumns.post_trade_status.value: PostTradeStatuses.ready_to_book_from_second_level_tab_of_bag.value},
                                               fields, f'Comparing values of {order}')
        # endregion
