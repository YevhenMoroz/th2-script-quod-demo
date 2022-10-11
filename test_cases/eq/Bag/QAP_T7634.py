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
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBagColumn, OrderBookColumns, BagStatuses, \
    SecondLevelTabs, TimeInForce, WaveColumns, Status, OffsetTypes
from test_framework.win_gui_wrappers.oms.oms_bag_order_book import OMSBagOrderBook
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7634(TestCase):
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
        qty = '1101'
        qty_of_bag = str(int(int(qty) * 2))
        qty_for_verifying_bag = qty_of_bag[0] + ',' + qty_of_bag[1:4]
        price = '10'
        price_offset = '0.05'
        venue_client_account = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        self.fix_message.set_default_dma_limit()
        self.fix_message.change_parameter('OrderQtyData', {'OrderQty': qty})
        self.fix_message.change_parameter('Account', self.data_set.get_client_by_name('client_pt_1'))
        self.fix_message.change_parameter('Instrument', self.data_set.get_fix_instrument_by_name('instrument_1'))
        self.fix_message.change_parameter('Price', price)
        exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.fix_message.change_parameter('ExDestination', exec_destination)
        lookup = self.data_set.get_lookup_by_name('lookup_1')
        self.fix_message.change_parameter("HandlInst", '3')
        rule_manager = RuleManager(Simulators.equity)
        orders_id = []
        name_of_bag = 'QAP_T7634'
        offset_type = OffsetTypes.price.value

        # endregion

        # # region step Precondition
        self.fix_message.change_parameter("HandlInst", '3')
        for i in range(2):
            self.fix_manager.send_message_fix_standard(self.fix_message)
            self.client_inbox.accept_order(lookup, qty, price)
            self.order_book.set_filter([OrderBookColumns.qty.value, qty])
            orders_id.append(self.order_book.extract_field(OrderBookColumns.order_id.value, 1))
        self.order_book.set_filter([OrderBookColumns.qty.value, qty])
        self.bag_order_book.create_bag_details([1, 2], name_of_bag=name_of_bag)
        self.bag_order_book.create_bag()
        tif = TimeInForce.DAY.value
        values = self.bag_order_book.extract_order_bag_book_details('1', [OrderBagColumn.ord_bag_name.value,
                                                                          OrderBagColumn.order_bag_qty.value])
        expected_result = {OrderBagColumn.order_bag_qty.value: qty_for_verifying_bag,
                           OrderBagColumn.ord_bag_name.value: name_of_bag}
        self.bag_order_book.compare_values(values, expected_result, 'Comparing values after creating bag')
        expected_result.clear()
        # endregion

        # region wave bag order (step 1, step 2 and step 3)
        new_order_single = None
        try:
            new_order_single = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side,
                venue_client_account, exec_destination,
                float(price))
            self.bag_order_book.set_order_bag_wave_details(price=price, qty=str(int(qty) * 2), tif=tif,
                                                           price_type='None',
                                                           offset_type=offset_type,
                                                           price_offset=price_offset)
            self.bag_order_book.wave_bag()
        except Exception as e:
            logger.error(f'{e}')
        finally:
            time.sleep(3)
            rule_manager.remove_rule(new_order_single)

        filter_list = [OrderBagColumn.ord_bag_name.value, name_of_bag]
        values = self.bag_order_book.extract_from_order_bag_book_and_other_tab('1', sub_extraction_fields=[
            WaveColumns.status.value, WaveColumns.peg_offset_value.value, WaveColumns.peg_offset_type.value],
                                                                               filter=filter_list,
                                                                               table_name=SecondLevelTabs.order_bag_waves.value)
        expected_result[WaveColumns.status.value] = Status.new.value
        expected_result.update({WaveColumns.peg_offset_type.value: offset_type})
        expected_result.update({WaveColumns.peg_offset_value.value: price_offset})
        self.order_book.compare_values(expected_result, values, 'Comparing values after waving')
        # endregion
