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
    Status, ExecSts
from test_framework.win_gui_wrappers.oms.oms_bag_order_book import OMSBagOrderBook
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7853(TestCase):
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
        qty = '7853'
        qty_of_bag = str(int(int(qty) * 2))
        qty_for_verifying_bag = qty_of_bag[0:2] + ',' + qty_of_bag[2:5]
        price = '10'
        client = self.data_set.get_client_by_name('client_pt_1')
        venue_client_account = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        self.fix_message.set_default_dma_limit()
        self.fix_message.change_parameter('OrderQtyData', {'OrderQty': qty})
        self.fix_message.change_parameter('Account', client)
        self.fix_message.change_parameter('Instrument', self.data_set.get_fix_instrument_by_name('instrument_1'))
        self.fix_message.change_parameter('Price', price)
        exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.fix_message.change_parameter('ExDestination', exec_destination)
        self.fix_message.change_parameter("HandlInst", '3')
        rule_manager = RuleManager(Simulators.equity)
        orders_id = []
        name_of_bag = 'QAP_T7853'
        new_order_single_rule = trade_rule = None
        filter_bag_list = [OrderBagColumn.ord_bag_name.value, name_of_bag]

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
        values = self.bag_order_book.extract_order_bag_book_details('1', [OrderBagColumn.ord_bag_name.value,
                                                                          OrderBagColumn.order_bag_qty.value],
                                                                    filter_bag_list)
        expected_result = {OrderBagColumn.order_bag_qty.value: qty_for_verifying_bag,
                           OrderBagColumn.ord_bag_name.value: name_of_bag}
        self.bag_order_book.compare_values(values, expected_result, 'Comparing values after creating bag')
        # endregion

        # region step 4 and step 5 and step 6
        try:
            new_order_single_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side,
                venue_client_account,
                exec_destination,
                float(price))
            trade_rule = rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
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
            rule_manager.remove_rule(trade_rule)
            rule_manager.remove_rule(new_order_single_rule)
        # endregion

        # expected result step 4 and step 5 and step 6
        result = self.bag_order_book.extract_from_order_bag_book_and_other_tab('1', sub_extraction_fields=[
            OrderBookColumns.sts.value, OrderBookColumns.exec_sts.value],
                                                                               table_name=SecondLevelTabs.slicing_orders.value)
        expected_result = {OrderBookColumns.sts.value: ExecSts.terminated.value,
                           OrderBookColumns.exec_sts.value: ExecSts.filled.value}
        self.bag_order_book.compare_values(expected_result, result, "Comparing values")
        expected_result = {OrderBookColumns.exec_sts.value: ExecSts.partially_filled.value}
        for order in orders_id:
            self.__check_value_of_co_orders(expected_result, [OrderBookColumns.exec_sts.value], order)
        # endregion

        # region step 7 and step 8
        self.bag_order_book.dissociate_bag(filter_bag_list)
        self.order_book.manual_execution(qty=str(int(int(qty) / 2)), price=price,
                                         filter_dict={OrderBookColumns.order_id.value: orders_id[0]})
        # endregion

        # region expected result for step 7 and step 8
        values = self.bag_order_book.extract_order_bag_book_details('1', [OrderBagColumn.bag_status.value],
                                                                    filter_bag_list)
        expected_result = {OrderBagColumn.bag_status.value: Status.canceled.value}
        self.bag_order_book.compare_values(values, expected_result, 'Comparing values after dissociating bag')
        expected_result = {OrderBookColumns.exec_sts.value: ExecSts.filled.value}
        self.__check_value_of_co_orders(expected_result, [OrderBookColumns.exec_sts.value], orders_id[0])
        # endregion

    def __check_value_of_co_orders(self, expected_result, columns: list, order_id: str):
        result = self.bag_order_book.extract_from_order_bag_book_and_other_tab('1', sub_extraction_fields=columns,
                                                                               sub_filter=[
                                                                                   OrderBookColumns.order_id.value,
                                                                                   order_id],
                                                                               table_name=SecondLevelTabs.orders_tab.value)
        self.bag_order_book.compare_values(expected_result, result, f"Comparing values of {order_id}")