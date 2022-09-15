import logging
import os
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.win_gui_wrappers.base_bag_order_book import EnumBagCreationPolitic
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBagColumn, OrderBookColumns, SecondLevelTabs, \
    Status, ExecSts, OrdersTabColumnFromBag
from test_framework.win_gui_wrappers.oms.oms_bag_order_book import OMSBagOrderBook
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7124(TestCase):
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
        self.rule_manager = RuleManager(Simulators.equity)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        qty = '7124'
        qty_of_bag = str(int(int(qty) * 2))
        price_1 = '10'
        price_2 = '5'
        client = self.data_set.get_client_by_name('client_pt_1')
        venue_client_account = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        self.fix_message.set_default_dma_limit()
        self.fix_message.change_parameter('OrderQtyData', {'OrderQty': qty})
        self.fix_message.change_parameter('Account', client)
        self.fix_message.change_parameter('Instrument', self.data_set.get_fix_instrument_by_name('instrument_1'))
        self.fix_message.change_parameter('Price', price_1)
        exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.fix_message.change_parameter('ExDestination', exec_destination)
        self.fix_message.change_parameter("HandlInst", '3')
        orders_id = []
        name_of_bag = 'QAP_T7124'
        filter_bag_list = [OrderBagColumn.ord_bag_name.value, name_of_bag]
        filter_bag_dict = {OrderBagColumn.ord_bag_name.value: name_of_bag}

        # endregion

        # region step 1, step 2 and step 3
        self.fix_message.change_parameter("HandlInst", '3')
        for i in range(2):
            self.fix_manager.send_message_fix_standard(self.fix_message)
            self.client_inbox.accept_order()
            self.order_book.set_filter([OrderBookColumns.qty.value, qty])
            orders_id.append(self.order_book.extract_field(OrderBookColumns.order_id.value, 1))
        self.order_book.set_filter([OrderBookColumns.qty.value, qty])
        self.bag_order_book.create_bag_details([1, 2], name_of_bag=name_of_bag)
        self.bag_order_book.create_bag(EnumBagCreationPolitic.BAG_BY_AVG_PX_PRIORITY)
        values = self.bag_order_book.extract_order_bag_book_details('1', [OrderBagColumn.bag_status.value],
                                                                    filter_bag_list)
        expected_result = {OrderBagColumn.bag_status.value: ExecSts.new.value}
        self.bag_order_book.compare_values(values, expected_result, 'Comparing values after creating bag')
        # endregion

        # region step 4 and step 5 and step 6
        self.__creating_and_trading_DMA_orders(price_2, exec_destination, venue_client_account, qty, client,
                                               name_of_bag)
        self.__creating_and_trading_DMA_orders(price_1, exec_destination, venue_client_account, qty, client,
                                               name_of_bag)
        # endregion

        # region check values from step 4 and step 5 and step 6
        columns = [OrderBookColumns.exec_sts.value, OrdersTabColumnFromBag.limit_price.value]
        expected_result = {OrderBookColumns.exec_sts.value: ExecSts.filled.value,
                           OrdersTabColumnFromBag.limit_price.value: price_1}
        self.__check_value_of_dma_orders(expected_result, columns, price_1)

        expected_result = {OrderBookColumns.exec_sts.value: ExecSts.filled.value,
                           OrdersTabColumnFromBag.limit_price.value: price_2}
        self.__check_value_of_dma_orders(expected_result, columns, price_2)
        # endregion

        # region check execution from CO orders(step 6)
        self.__check_execution_price(filter_bag_list, orders_id, price_1)
        self.__check_execution_price(filter_bag_list, orders_id, price_2)
        # endregion

        # region complete Bag
        self.bag_order_book.complete_or_un_complete_bag(filter_dict=filter_bag_dict, is_complete=True)
        self.__check_execution_price(filter_bag_list, orders_id, price_1)
        self.__check_execution_price(filter_bag_list, orders_id, price_2)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def __check_value_of_dma_orders(self, expected_result, columns: list, price: str):
        result = self.bag_order_book.extract_from_order_bag_book_and_other_tab('1', sub_extraction_fields=columns,
                                                                               sub_filter=[
                                                                                   OrdersTabColumnFromBag.limit_price.value,
                                                                                   price],
                                                                               table_name=SecondLevelTabs.slicing_orders.value)
        self.bag_order_book.compare_values(expected_result, result,
                                           f"Comparing values of DMA order with limit price = {price}")

    @try_except(test_id=Path(__file__).name[:-3])
    def __creating_and_trading_DMA_orders(self, price, exec_destination, venue_client_account, qty,
                                          client, name_of_bag):
        new_order_single_rule = trade_rule = None
        try:
            new_order_single_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side,
                venue_client_account,
                exec_destination,
                float(price))
            trade_rule = self.rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                                            venue_client_account,
                                                                                            exec_destination,
                                                                                            float(price), int(qty), 0)
            order_details = self.order_ticket.set_order_details(client, limit=price, qty=qty)
            self.bag_order_book.set_create_order_details({OrderBagColumn.ord_bag_name.value: name_of_bag},
                                                         order_details.order_details)
        except Exception as e:
            logger.info(f'Your Exception is {e}')

        finally:
            time.sleep(3)
            self.rule_manager.remove_rule(trade_rule)
            self.rule_manager.remove_rule(new_order_single_rule)

    @try_except(test_id=Path(__file__).name[:-3])
    def __check_execution_price(self, filter_bag_list, orders_id, price):
        for order_id in orders_id:
            values = self.bag_order_book.extraction_from_sub_levels_and_others_tab('1',
                                                                                   [OrderBookColumns.exec_price.value],
                                                                                   {1: filter_bag_list,
                                                                                    2: [OrderBookColumns.order_id.value,
                                                                                        order_id],
                                                                                    3: [
                                                                                        OrderBookColumns.exec_price.value,
                                                                                        price]},
                                                                                   [SecondLevelTabs.orders_tab.value,
                                                                                    SecondLevelTabs.executions.value],
                                                                                   3)
            expected_result = {OrderBookColumns.exec_price.value: price}
            self.bag_order_book.compare_values(expected_result, values, f'Comparing values of execution '
                                                                        f'with {price} of {order_id}')
