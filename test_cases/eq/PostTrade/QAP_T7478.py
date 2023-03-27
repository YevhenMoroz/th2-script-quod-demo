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
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, BookingBlotterColumns, \
    BookingOrderResult
from test_framework.win_gui_wrappers.oms.oms_booking_window import OMSBookingWindow
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7478(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.middle_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.booking_window = OMSBookingWindow(self.test_id, self.session_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        qty = '3440'
        price = '10'
        qty_of_booking = str((int(int(qty) * 2))).replace('8', ',', 1).replace('0', '8', 1).__add__('0')
        account = self.data_set.get_venue_client_names_by_name('client_pt_1_venue_1')
        self.fix_message.set_default_dma_limit()
        self.fix_message.change_parameter('OrderQtyData', {'OrderQty': qty})
        self.fix_message.change_parameter('Account', self.data_set.get_client_by_name('client_pt_1'))
        self.fix_message.change_parameter('Instrument', self.data_set.get_fix_instrument_by_name('instrument_1'))
        self.fix_message.change_parameter('Price', price)
        exec_destination = self.data_set.get_mic_by_name('mic_1')
        self.fix_message.change_parameter('ExDestination', exec_destination)
        rule_manager = RuleManager(Simulators.equity)
        trade_rule = None
        new_order_single_rule = None
        orders_id = []
        give_up_broker = self.data_set.get_give_up_broker('give_up_broker_1')
        # endregion

        # region create orders(precondition)
        try:
            new_order_single_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side, account, exec_destination, float(price))
            trade_rule = rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side, account,
                                                                                       exec_destination, float(price),
                                                                                       int(qty), 0)
            for i in range(2):
                self.fix_manager.send_message_fix_standard(self.fix_message)
                self.order_book.set_filter([OrderBookColumns.qty.value, qty])
                orders_id.append(self.order_book.extract_field(OrderBookColumns.order_id.value))
        except Exception as ex:
            logger.exception(f'{ex} - your exception')

        finally:
            time.sleep(10)
            rule_manager.remove_rule(trade_rule)
            rule_manager.remove_rule(new_order_single_rule)
        # endregion

        # region book orders (step 1, 2)
        self.middle_office.set_modify_ticket_details(give_up_broker=give_up_broker, selected_row_count=2)
        self.middle_office.book_order()
        # endregion

        # region extract value from booking blotter(step 3)
        self.booking_window.set_extraction_details([BookingBlotterColumns.qty.value,
                                                    BookingBlotterColumns.order_id.value,
                                                    BookingBlotterColumns.give_up_broker.value],
                                                   filter_dict={
                                                       BookingBlotterColumns.give_up_broker.value: give_up_broker})
        result = self.booking_window.extract_from_booking_window()
        self.booking_window.compare_values({BookingBlotterColumns.order_id.value:BookingOrderResult.multi.value,
                                            BookingBlotterColumns.give_up_broker.value:give_up_broker,
                                            BookingBlotterColumns.qty.value:qty_of_booking},
                                           result, 'Comparing values from booking blotter')
        # endregion
