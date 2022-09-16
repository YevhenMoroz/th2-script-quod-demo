import logging
import os
import sys
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.win_gui_wrappers.base_bag_order_book import EnumBagCreationPolitic
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBagColumn, OrderBookColumns, ClientInboxColumns, \
    WaveColumns, SecondLevelTabs, Status
from test_framework.win_gui_wrappers.oms.oms_bag_order_book import OMSBagOrderBook
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7637(TestCase):
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
        self.rule_manager = RuleManager(Simulators.equity)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        qty = '1098'
        price = '10'
        self.fix_message.set_default_dma_limit()
        venue_client_account = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        self.fix_message.change_parameter('OrderQtyData', {'OrderQty': qty})
        self.fix_message.change_parameter('Account', self.data_set.get_client_by_name('client_pt_1'))
        self.fix_message.change_parameter('Instrument', self.data_set.get_fix_instrument_by_name('instrument_1'))
        self.fix_message.change_parameter('Price', price)
        exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.fix_message.change_parameter('ExDestination', exec_destination)
        lookup = self.data_set.get_lookup_by_name('lookup_1')
        self.fix_message.change_parameter("HandlInst", '3')
        qty_of_bag = str(int(qty) * 2)
        qty_of_bag_for_verifying = qty_of_bag[0] + ',' + qty_of_bag[1:4]
        orders_id = []
        name_of_bag = 'QAP_T7637'
        filter_list = [OrderBagColumn.ord_bag_name.value, name_of_bag]
        new_order_single_rule = modification_rule = None
        sub_extraction_fields = [WaveColumns.status.value, WaveColumns.price.value]
        table_name = SecondLevelTabs.order_bag_waves.value
        ord_type = self.data_set.get_order_type('limit')
        # endregion

        # region create 2 CO order(precondition)
        for i in range(2):
            self.fix_manager.send_message_fix_standard(self.fix_message)
            self.client_inbox.accept_order(lookup, qty, price,
                                           filter={
                                               ClientInboxColumns.client_name.value: self.data_set.get_client_by_name(
                                                   'client_pt_1')})
            self.order_book.set_filter([OrderBookColumns.qty.value, qty])
            orders_id.append(self.order_book.extract_field(OrderBookColumns.order_id.value, 1))
        # endregion

        # region create OrderBag (precondition)
        self.bag_order_book.create_bag_details([1, 2], name_of_bag, price)
        self.bag_order_book.create_bag(politic_of_creation=EnumBagCreationPolitic.SPLIT_BY_AVG_PX)
        # endregion

        # region verify bag after creation (precondition)
        fields = self.bag_order_book.extract_order_bag_book_details('1', [OrderBagColumn.order_bag_qty.value,
                                                                          OrderBagColumn.ord_bag_name.value,
                                                                          OrderBagColumn.id.value,
                                                                          OrderBagColumn.unmatched_qty.value,
                                                                          OrderBagColumn.leaves_qty.value
                                                                          ], filter=filter_list)
        expected_values = {OrderBagColumn.order_bag_qty.value: qty_of_bag_for_verifying,
                           OrderBagColumn.ord_bag_name.value: name_of_bag,
                           OrderBagColumn.unmatched_qty.value: qty_of_bag_for_verifying,
                           OrderBagColumn.leaves_qty.value: qty_of_bag_for_verifying,
                           }
        self.bag_order_book.compare_values(expected_values,
                                           fields, 'Compare values from bag_book before modification')
        expected_values.clear()
        # endregion

        # region wave bag step 1 and step 2
        price_of_wave_1 = str(int(int(price) / int(price)))
        try:
            new_order_single_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side, venue_client_account, exec_destination, float(price_of_wave_1))
            self.bag_order_book.set_order_bag_wave_details(price=price_of_wave_1, qty=qty_of_bag)
            self.bag_order_book.wave_bag()
        except Exception as e:
            logger.error(f'{e}')

        finally:
            self.rule_manager.remove_rule(new_order_single_rule)
        # endregion

        # region check wave status
        values = self.__extract_values_from_second_level_tab(filter_list, extraction_fields=sub_extraction_fields,
                                                             table_name=table_name)
        expected_values[WaveColumns.status.value] = Status.new.value
        expected_values.update({WaveColumns.price.value: price_of_wave_1})
        self.order_book.compare_values(expected_values, values, 'Comparing values after waving')
        # endregion

        # region modification wave 2 time (step 4)
        price_of_wave_2 = str(int(int(price) / 2))
        try:
            modification_rule = self.rule_manager.add_OrderCancelReplaceRequest_FIXStandard(
                self.fix_env.buy_side, venue_client_account, exec_destination, True)
            self.bag_order_book.set_order_bag_wave_details(price=price_of_wave_2, sub_lvl_number=1)
            self.bag_order_book.modify_wave_bag()
        except Exception:
            info = sys.exc_info()
            print(info)

        finally:
            self.rule_manager.remove_rule(modification_rule)
        # endregion

        # region check wave after modification (step 5)
        values = self.__extract_values_from_second_level_tab(filter_list, extraction_fields=sub_extraction_fields, table_name=table_name)
        expected_values[WaveColumns.price.value] = price_of_wave_2
        self.order_book.compare_values(expected_values, values, 'Comparing values after waving')
        # endregion

        # region check child orders(step 5)
        for index in range(len(orders_id)):
            values = self.order_book.extract_2lvl_fields(SecondLevelTabs.child_tab.value,
                                                         [OrderBookColumns.limit_price.value,
                                                          OrderBookColumns.ord_type.value],
                                                         [1],
                                                         {OrderBookColumns.order_id.value: orders_id[index]})[0]
            self.order_book.compare_values(
                {OrderBookColumns.limit_price.value: price_of_wave_2, OrderBookColumns.ord_type.value: ord_type},
                values,
                f'Comparing values of {orders_id[index]} order')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def __extract_values_from_second_level_tab(self, filter_list, table_name, extraction_fields):
        values = self.bag_order_book.extract_from_order_bag_book_and_other_tab('1',
                                                                               sub_extraction_fields=extraction_fields,
                                                                               filter=filter_list,
                                                                               table_name=table_name)
        return values
