import logging
import os
import time
from pathlib import Path

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from stubs import Stubs
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.win_gui_wrappers.fe_trading_constant import SecondLevelTabs, Status, \
    OrderBagColumn, WaveColumns, OrderBookColumns
from test_framework.win_gui_wrappers.oms.oms_bag_order_book import OMSBagOrderBook
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7520(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.test_id)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.bag_order_book = OMSBagOrderBook(self.test_id, self.session_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.rule_manager = RuleManager(Simulators.equity)
        self.act_java_api = Stubs.act_java_api
        self.order_book = OMSOrderBook(self.test_id, self.session_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        qty = '3297'
        price = '10'
        qty_of_wave = str(int(qty) * 2)
        qty_of_wave_verifying = qty_of_wave[0] + ',' + qty_of_wave[1:4]
        client_name = self.data_set.get_client_by_name('client_pt_1')
        self.fix_message.set_default_dma_limit()
        cl_ord_id = self.fix_message.get_parameter('ClOrdID')
        self.fix_message.change_parameter('OrderQtyData', {'OrderQty': qty})
        self.fix_message.change_parameter('Account', client_name)
        client_for_rule = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        self.fix_message.change_parameter('Instrument', self.data_set.get_fix_instrument_by_name('instrument_1'))
        self.fix_message.change_parameter('Price', price)
        exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.fix_message.change_parameter('ExDestination', exec_destination)
        lookup = self.data_set.get_lookup_by_name('lookup_1')
        self.fix_message.change_parameter("HandlInst", '3')
        name_of_bag = 'QAP_T7520'
        inbox_filter = {'ClientName': client_name}
        new_order_single_rule = None
        strategy = self.data_set.get_strategy('internal_twap')
        scenario = self.data_set.get_scenario('twap_strategy')
        filter_list = [OrderBagColumn.ord_bag_name.value, name_of_bag]
        orders_id = []
        # endregion

        # region create 2 CO order
        for i in range(2):
            self.fix_manager.send_message_fix_standard(self.fix_message)
            self.client_inbox.accept_order(lookup, qty, price,
                                           filter=inbox_filter)
            self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id])
            orders_id.append(self.order_book.extract_field(OrderBookColumns.order_id.value, 1))
        # endregion

        # region create Bag (step 1-7)
        self.bag_order_book.create_bag_details([1, 2], name_of_bag=name_of_bag, price=price)
        self.bag_order_book.create_bag()
        # endregion

        # region wave bag order (step 8-9)
        try:
            new_order_single_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side,
                client_for_rule,
                exec_destination,
                float(price))
            result = self.bag_order_book.extract_values_from_wave_ticket(tif=False, error_message=False,
                                                                         qty_to_release=True)
            self.bag_order_book.compare_values({'QTY_TO_RELEASE': qty_of_wave_verifying}, result, "Comparing value")
            self.bag_order_book.set_twap_strategy(scenario=scenario, strategy=strategy)
            self.bag_order_book.set_order_bag_wave_details(price=price)
            self.bag_order_book.wave_bag()
        except Exception as e:
            logger.error(f'Your Exception is {e}')

        finally:
            time.sleep(3)
            self.rule_manager.remove_rule(new_order_single_rule)
        # endregion

        # check status of wave
        self.__check_wave_status(filter_list, tab_name=SecondLevelTabs.order_bag_waves.value,
                                 status=Status.new.value)
        # endregion

        # checking values of child order
        self.__check_child_order_after_waving(order_ids=orders_id,
                                              expected_result={OrderBookColumns.nin.value: client_for_rule,
                                                               OrderBookColumns.exec_pcy.value: self.data_set.get_exec_policy(
                                                                   'synthetic')})
        # endregion

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

    @try_except(test_id=Path(__file__).name[:-3])
    def __check_child_order_after_waving(self, order_ids: list, expected_result):
        for order in order_ids:
            values = self.order_book.extract_2lvl_fields(SecondLevelTabs.child_tab.value,
                                                         [OrderBookColumns.exec_pcy.value, OrderBookColumns.nin.value],
                                                         [1], {OrderBookColumns.order_id.value: order})[0]
            self.order_book.compare_values(expected_result, values, f"Comparing values for order {order}")
