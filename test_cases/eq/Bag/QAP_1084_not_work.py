import logging
import os
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBagColumn
from test_framework.win_gui_wrappers.oms.oms_bag_order_book import OMSBagOrderBook
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket
from test_framework.win_gui_wrappers.oms.oms_trades_book import OMSTradesBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_1084(TestCase):
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.case_id = bca.create_event(os.path.basename(__file__), self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.order_book = OMSOrderBook(self.case_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.case_id, self.session_id)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.case_id)
        self.trade_book = OMSTradesBook(self.case_id, self.session_id)
        self.order_ticket = OMSOrderTicket(self.case_id, self.session_id)
        self.bag_order_book = OMSBagOrderBook(self.case_id, self.session_id)
        self.qty = '100'
        self.price = '10'
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.fix_message.set_default_dma_limit()
        self.fix_message.change_parameter('OrderQtyData', {'OrderQty': self.qty})
        self.java_api_manager = JavaApiManager(self.java_api, self.case_id)
        self.fix_message.change_parameter('Account', self.data_set.get_client_by_name('client_pt_1'))
        self.fix_message.change_parameter('Instrument', self.data_set.get_fix_instrument_by_name('instrument_1'))
        self.fix_message.change_parameter('Price', self.price)
        self.client_for_rule = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        self.exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.fix_message.change_parameter('ExDestination', self.exec_destination)
        self.lookup = self.data_set.get_lookup_by_name('lookup_1')
        self.fix_message.change_parameter("HandlInst", '3')

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region create 3 CO order
        self.fix_message.change_parameter("HandlInst", '3')
        for i in range(3):
            self.fix_manager.send_message_fix_standard(self.fix_message)
            self.client_inbox.accept_order(self.lookup, self.qty, self.price)
            # endregion

        # region create Bag
        self.bag_order_book.create_bag_details([1, 2, 3], name_of_bag='Bag_1')
        self.bag_order_book.create_bag()
        fields = self.bag_order_book.extract_order_bag_book_details('1', [OrderBagColumn.order_bag_qty.value,
                                                                          OrderBagColumn.ord_bag_name.value],
                                                                    sub_extraction_fields=['Venue', 'Order ID'])
        print(fields)
        # endregion
