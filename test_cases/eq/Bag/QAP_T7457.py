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
    ExecSts, Side
from test_framework.win_gui_wrappers.oms.oms_bag_order_book import OMSBagOrderBook
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7457(TestCase):
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
        self.order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        self.rule_manager = RuleManager(Simulators.equity)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        qty = '3668'
        qty_for_verifying = qty[0] + ',' + qty[1:4]
        price = '10'
        client_name = self.data_set.get_client_by_name('client_pt_1')
        self.fix_message.set_default_dma_limit()
        self.fix_message.change_parameter('OrderQtyData', {'OrderQty': qty})
        self.fix_message.change_parameter('Account', client_name)
        client_for_rule = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        self.fix_message.change_parameter('Instrument', self.data_set.get_fix_instrument_by_name('instrument_1'))
        self.fix_message.change_parameter('Price', price)
        exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.fix_message.change_parameter('ExDestination', exec_destination)
        lookup = self.data_set.get_lookup_by_name('lookup_1')
        self.fix_message.change_parameter("HandlInst", '3')
        name_of_bag = 'QAP_T7457'
        inbox_filter = {'ClientName': client_name}
        new_order_single_rule = None
        # endregion

        # region create 2 CO order
        for i in range(2):
            self.fix_manager.send_message_fix_standard(self.fix_message)
            self.client_inbox.accept_order(lookup, qty, price,
                                           filter=inbox_filter)
            self.order_book.set_filter([OrderBookColumns.qty.value, qty])
        # endregion

        # region create Bag
        self.bag_order_book.create_bag_details([1, 2], name_of_bag=name_of_bag, price=price)
        self.bag_order_book.create_bag(EnumBagCreationPolitic.BAG_BY_AVG_PX_PRIORITY)

        # endregion

        # region partially fill bag order via wave
        try:
            new_order_single_rule = self.rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side,
                client_for_rule,
                exec_destination,
                float(price))
            order_details = self.order_ticket.set_order_details(client_name, limit=price, qty=qty)
            self.bag_order_book.set_create_order_details({OrderBagColumn.ord_bag_name.value: name_of_bag},
                                                         order_details.order_details)
        except Exception as e:
            logger.info(f'Your Exception is {e}')

        finally:
            time.sleep(3)
            self.rule_manager.remove_rule(new_order_single_rule)
        # endregion

        fields = self.bag_order_book.extract_from_order_bag_book_and_other_tab('1', [OrderBagColumn.ord_bag_name.value],
                                                                               sub_extraction_fields=[
                                                                                   OrderBookColumns.sts.value,
                                                                                   OrderBookColumns.side.value,
                                                                                   OrderBookColumns.qty.value],
                                                                               table_name=SecondLevelTabs.slicing_orders.value)
        self.order_book.compare_values(
            {OrderBookColumns.sts.value: ExecSts.open.value, OrderBagColumn.ord_bag_name.value: name_of_bag,
             OrderBookColumns.side.value: Side.buy.value, OrderBookColumns.qty.value: qty_for_verifying}, fields,
            'Comparing values')
