import logging
import os
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.ors_messages.ModifyBagOrderRequest import ModifyBagOrderRequest
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBagColumn, OrderBookColumns, SecondLevelTabs, \
    ExecSts, WaveColumns
from test_framework.win_gui_wrappers.oms.oms_bag_order_book import OMSBagOrderBook
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_trades_book import OMSTradesBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7413(TestCase):
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
        self.trade_book = OMSTradesBook(self.test_id, self.session_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        qty = '200'
        price = '10'
        wave_price = '2'
        account = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        self.fix_message.set_default_dma_limit()
        self.fix_message.change_parameter('OrderQtyData', {'OrderQty': qty})
        self.fix_message.change_parameter('Account', self.data_set.get_client_by_name('client_pt_1'))
        self.fix_message.change_parameter('Instrument', self.data_set.get_fix_instrument_by_name('instrument_1'))
        self.fix_message.change_parameter('Price', price)
        exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.fix_message.change_parameter('ExDestination', exec_destination)
        lookup = self.data_set.get_lookup_by_name('lookup_1')
        self.fix_message.change_parameter("HandlInst", '3')
        qty_of_bag = str(int(qty) * 2)
        tif = self.data_set.get_time_in_force("time_in_force_1")
        orders_id = []
        name_of_bag = 'QAP_T7413'
        # endregion

        # region step 1
        for i in range(2):
            self.fix_manager.send_message_fix_standard(self.fix_message)
            self.client_inbox.accept_order(lookup, qty, price,
                                           filter={'ClientName': self.data_set.get_client_by_name('client_pt_1')})
            self.order_book.set_filter([OrderBookColumns.qty.value, qty])
            orders_id.append(self.order_book.extract_field(OrderBookColumns.order_id.value, 1))
        # endregion

        # region step 2
        self.bag_order_book.create_bag_details([1, 2], name_of_bag=name_of_bag, price='5')
        self.bag_order_book.create_bag()
        fields = self.bag_order_book.extract_order_bag_book_details('1', [OrderBagColumn.order_bag_qty.value,
                                                                          OrderBagColumn.ord_bag_name.value,
                                                                          OrderBagColumn.id.value,
                                                                          OrderBagColumn.unmatched_qty.value,
                                                                          OrderBagColumn.leaves_qty.value
                                                                          ])
        expected_values_first = {OrderBagColumn.order_bag_qty.value: qty_of_bag,
                                 OrderBagColumn.ord_bag_name.value: name_of_bag,
                                 OrderBagColumn.unmatched_qty.value: qty_of_bag,
                                 OrderBagColumn.leaves_qty.value: qty_of_bag,
                                 }
        self.bag_order_book.compare_values(expected_values_first,
                                           fields, 'Compare values from bag_book after creation')

        # endregion

        # region create wave and execute it (step 3, step 4)
        rule_manager = RuleManager(sim=Simulators.equity)
        new_order_single = trade_rule = None
        try:
            new_order_single = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side,
                account, exec_destination,
                float(wave_price))
            trade_rule = rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side,
                                                                                       account, exec_destination,
                                                                                       float(wave_price), int(qty),
                                                                                       delay=0)
            self.bag_order_book.set_order_bag_wave_details(price=wave_price, qty=str(int(qty) * 2), tif=tif)
            self.bag_order_book.wave_bag()
        except Exception as e:
            logger.error(f'{e}')
        finally:
            rule_manager.remove_rule(new_order_single)
            rule_manager.remove_rule(trade_rule)

        '''
        verifying value of orders after trade
        '''
        filter = [OrderBagColumn.ord_bag_name.value, name_of_bag]
        for index in range(len(orders_id)):
            sub_filter = [OrderBookColumns.order_id.value, orders_id[index]]
            actual_result_order = self.bag_order_book.extract_from_order_bag_book_and_other_tab('1',
                                                                                                sub_extraction_fields=[
                                                                                                    OrderBookColumns.exec_sts.value,
                                                                                                    OrderBookColumns.sts.value],
                                                                                                sub_filter=sub_filter,
                                                                                                filter=filter,
                                                                                                table_name=SecondLevelTabs.orders_tab.value
                                                                                                )
            expected_result = {OrderBookColumns.exec_sts.value: ExecSts.filled.value,
                               OrderBookColumns.sts.value: ExecSts.open.value}
            self.bag_order_book.compare_values(expected_result, actual_result_order, 'Comparing values')

        '''
        verifying value of wave after trade
        '''
        actual_result_order = self.bag_order_book.extract_from_order_bag_book_and_other_tab('1',
                                                                                            sub_extraction_fields=[
                                                                                                WaveColumns.status.value],
                                                                                            filter=filter,
                                                                                            table_name=SecondLevelTabs.order_bag_waves.value
                                                                                            )
        expected_result = {WaveColumns.status.value: ExecSts.terminated.value}
        self.bag_order_book.compare_values(expected_result, actual_result_order, 'Comparing values')

        # region step 5
        for index in range(len(orders_id)):
            filter_dict = {OrderBookColumns.order_id.value: orders_id[index]}
            actually_result = self.order_book.extract_2lvl_fields(SecondLevelTabs.executions.value,
                                                                  [OrderBookColumns.disclosed_exec.value,
                                                                   OrderBookColumns.exec_price.value],
                                                                  [1], filter_dict)[0]
            self.order_book.compare_values(
                {OrderBookColumns.disclosed_exec.value: 'Y', OrderBookColumns.exec_price.value: wave_price},
                actually_result,
                f"Comparing values of execution for {orders_id[index]}")
        # endregion
