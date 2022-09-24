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
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBagColumn, OrderBookColumns, ExecSts, BagStatuses, \
    SecondLevelTabs, WaveColumns
from test_framework.win_gui_wrappers.oms.oms_bag_order_book import OMSBagOrderBook
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7640(TestCase):
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
        self.rule_manager = RuleManager(Simulators.equity)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        qty = '1095'
        price = '10'
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
        new_order_single_rule = None
        orders_id = []
        name_of_bag = 'QAP_T7640'
        # endregion
        # region create 2 CO order
        self.fix_message.change_parameter("HandlInst", '3')
        for i in range(2):
            self.fix_manager.send_message_fix_standard(self.fix_message)
            self.client_inbox.accept_order(lookup, qty, price, )
            self.order_book.set_filter([OrderBookColumns.qty.value, qty])
            orders_id.append(self.order_book.extract_field(OrderBookColumns.order_id.value, 1))
        # endregion

        # region create Bag and extract values from it (precondition)
        self.bag_order_book.create_bag_details([1, 2], name_of_bag=name_of_bag)
        self.bag_order_book.create_bag()
        order_bag_id = self.__extracting_and_comparing_value_for_bag_order([OrderBagColumn.ord_bag_name.value,
                                                                            OrderBagColumn.id.value,
                                                                            OrderBagColumn.bag_status.value
                                                                            ], [name_of_bag, BagStatuses.new.value],
                                                                           True, 'creating')
        # endregion

        # region step 1 and step 2(wave) and comparing value after that
        try:
            new_order_single_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side,
                client_for_rule, exec_destination,
                float(price))
            self.bag_order_book.set_order_bag_wave_details(price, qty)
            self.bag_order_book.wave_bag()
        except Exception as e:
            logger.error(f'{e}')
        finally:
            self.rule_manager.remove_rule(new_order_single_rule)
        fields = self.bag_order_book.extract_from_order_bag_book_and_other_tab('1',
                                                                               extraction_fields=[
                                                                                   OrderBagColumn.id.value],
                                                                               sub_extraction_fields=['Status'])
        self.bag_order_book.compare_values(
            {{WaveColumns.status.value}: 'BagStatuses.new.value'},
            {{WaveColumns.status.value}:
                 fields[{WaveColumns.status.value}]}, 'Comparing Status of Wave')
        for order_id in orders_id:
            self.order_book.set_filter([OrderBookColumns.order_id.value, order_id])
            sts_field = OrderBookColumns.sts.value
            self.order_book.compare_values({sts_field: ExecSts.open.value}, {
                sts_field: self.order_book.extract_field(sts_field)
            }, f'Compare Sts for order{order_id}')
        # endregion

        # region dissociate order  and check value after it(step 3, step 4)
        filter_list = [OrderBagColumn.id.value, order_bag_id]
        self.bag_order_book.dissociate_bag(filter_list)
        self.__extracting_and_comparing_value_for_bag_order([OrderBagColumn.bag_status.value],
                                                            [BagStatuses.terminated.value], False, action='dissociate')

        for order_id in orders_id:
            field = self.order_book.extract_2lvl_fields(SecondLevelTabs.child_tab.value, [OrderBookColumns.sts.value],
                                                        [1],
                                                        {OrderBookColumns.order_id.value: order_id})
            self.bag_order_book.compare_values({OrderBookColumns.sts.value: ExecSts.open.value}, field[0],
                                               f'Comparing child for {order_id}')
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
