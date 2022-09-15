import logging
import os
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import Simulators, RuleManager
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBagColumn, OrderBookColumns, WaveColumns, \
    BagStatuses, SecondLevelTabs, Status, OrdersTabColumnFromBag
from test_framework.win_gui_wrappers.oms.oms_bag_order_book import OMSBagOrderBook
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7641(TestCase):
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
        self.rule_manager = RuleManager(Simulators.equity)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        qty = '1094'
        qty_of_verifying = qty[0] + ',' + qty[1:4]
        qty_of_wave = str(int(int(qty) * 2))
        price = '10'
        qty_of_wave_verifying = qty_of_wave[0] + ',' + qty_of_wave[1:4]
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
        new_order_single_rule = cancel_rule = None
        orders_id = []
        name_of_bag = 'QAP_T7641'
        filter_list = [OrderBagColumn.ord_bag_name.value, name_of_bag]
        # endregion

        # region precondition
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

        # region step 1 and step 2
        try:
            new_order_single_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side,
                client_for_rule, exec_destination,
                float(price))
            self.bag_order_book.set_order_bag_wave_details(tif=self.data_set.get_time_in_force('time_in_force_1'),
                                                           price=price, qty=qty_of_wave)
            self.bag_order_book.wave_bag()
        except Exception as e:
            logger.error(f'{e}')
        finally:
            time.sleep(5)
            self.rule_manager.remove_rule(new_order_single_rule)

        self.__check_unmatched_qty_of_orders_and_bag(filter_list, orders_id, '0', '0')
        self.__check_wave_status(filter_list, tab_name=SecondLevelTabs.order_bag_waves.value,
                                 status=Status.new.value)
        # endregion

        # region step 3
        try:
            cancel_rule = self.rule_manager.add_OrderCancelRequest(
                self.fix_env.buy_side,
                client_for_rule, exec_destination, True)
            self.bag_order_book.set_order_bag_wave_details(wave_filter=filter_list)
            self.bag_order_book.cancel_wave()
        except Exception as e:
            logger.error(f'{e}')
        finally:
            time.sleep(5)
            self.rule_manager.remove_rule(cancel_rule)
        # endregion

        # region check unmatched_qty after cancel
        self.__check_unmatched_qty_of_orders_and_bag(filter_list, orders_id, qty_of_wave_verifying, qty_of_verifying)
        self.__check_wave_status(filter_list, tab_name=SecondLevelTabs.order_bag_waves.value,
                                 status=Status.cancelled.value)
        # endregion

        # region check child_orders
        for order in orders_id:
            order_filter = {OrderBookColumns.order_id.value: order}
            values_of_sts = self.order_book.extract_2lvl_fields(SecondLevelTabs.child_tab.value,
                                                                [OrderBookColumns.sts.value], [1], order_filter)[0]
            self.order_book.compare_values({OrderBookColumns.sts.value: Status.canceled.value}, values_of_sts,
                                           f'Comparing status child order for {order}')

        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def __check_unmatched_qty_of_orders_and_bag(self, filter_list, orders_id, expected_unmatched_qty_of_bag,
                                                expected_unmatched_qty_of_order):
        fields = self.bag_order_book.extract_order_bag_book_details('1', [OrderBagColumn.unmatched_qty.value,
                                                                          ],
                                                                    filter_list)
        self.bag_order_book.compare_values(
            {OrderBagColumn.unmatched_qty.value: expected_unmatched_qty_of_bag},
            fields, "Comparing unmatched qty of  bag after creating")

        for index in range(len(orders_id)):
            filter_of_order = [OrderBookColumns.order_id.value, orders_id[index]]
            fields = self.bag_order_book.extract_from_order_bag_book_and_other_tab('1',
                                                                                   sub_extraction_fields=[
                                                                                       OrdersTabColumnFromBag.unmatched_qty.value],
                                                                                   sub_filter=filter_of_order,
                                                                                   filter=filter_list,
                                                                                   table_name=SecondLevelTabs.orders_tab.value)
            self.bag_order_book.compare_values(
                {OrdersTabColumnFromBag.unmatched_qty.value: expected_unmatched_qty_of_order},
                fields, f'Comparing of unmatched qty of {orders_id[index]} after wave')

    @try_except(test_id=Path(__file__).name[:-3])
    def __check_wave_status(self, filter_list, status: str, tab_name: str):
        fields = self.bag_order_book.extract_from_order_bag_book_and_other_tab('1',
                                                                               sub_extraction_fields=[
                                                                                   WaveColumns.status.value],
                                                                               filter=filter_list, table_name=tab_name)
        self.bag_order_book.compare_values(
            {WaveColumns.status.value: status},
            {WaveColumns.status.value:
                 fields[WaveColumns.status.value]}, 'Comparing Status of Wave')
