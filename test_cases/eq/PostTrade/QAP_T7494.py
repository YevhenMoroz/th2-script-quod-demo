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
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns,BookingBlotterColumns, \
    AllocInstructionQties, SecondLevelTabs
from test_framework.win_gui_wrappers.oms.oms_booking_window import OMSBookingWindow
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7494(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.case_id = bca.create_event(os.path.basename(__file__), self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.case_id)
        self.order_book = OMSOrderBook(self.case_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.case_id, self.session_id)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.case_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.middle_office = OMSMiddleOffice(self.case_id, self.session_id)
        self.booking_blotter = OMSBookingWindow(self.case_id, self.session_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declaration
        qty = '200'
        price = '10'
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
        # endregion

        # region create order
        try:
            new_order_single_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side, account, exec_destination, float(price))
            trade_rule = rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side, account,
                                                                                       exec_destination, float(price),
                                                                                       int(qty), 0)
            self.fix_manager.send_message_fix_standard(self.fix_message)
        except Exception as ex:
            logger.exception(f'{ex} - your exception')

        finally:
            time.sleep(5)
            rule_manager.remove_rule(trade_rule)
            rule_manager.remove_rule(new_order_single_rule)

        # endregion

        # region verify value of fields after trade
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, self.fix_message.get_parameter('ClOrdID')])
        order_id = self.order_book.extract_field(OrderBookColumns.order_id.value)
        self.order_book.set_filter([OrderBookColumns.qty.value, qty])
        post_trade_status = self.order_book.extract_field(OrderBookColumns.post_trade_status.value)
        self.order_book.set_filter([OrderBookColumns.qty.value, qty])
        value_exec_sts = self.order_book.extract_field(OrderBookColumns.exec_sts.value)
        self.order_book.compare_values(
            {OrderBookColumns.post_trade_status.value: 'ReadyToBook', OrderBookColumns.done_for_day.value: 'Filled'},
            {OrderBookColumns.post_trade_status.value: post_trade_status,
             OrderBookColumns.done_for_day.value: value_exec_sts}, 'Comparing values after trade')
        # endregion

        # region step 1, step 2, step 3, step 4(split booking)
        commission_basis = self.data_set.get_commission_basis('comm_basis_1')
        fee_type = self.data_set.get_fee_type_from_booking_ticket('fee_type_in_booking_ticket_1')
        give_up_broker = self.data_set.get_give_up_broker('give_up_broker_1')
        net_gross_ind = self.data_set.get_net_gross_ind_type('net_ind')
        qty_of_split = str(int((int(qty) / 2)))
        self.order_book.set_filter([OrderBookColumns.order_id.value, self.fix_message.get_parameter('ClOrdID')])
        split_param_1 = self.order_book.create_split_booking_parameter(split_qty=qty_of_split,
                                                                       comm_basis=commission_basis, comm_rate='5',
                                                                       fee_type=fee_type, fee_rate='5',
                                                                       give_up_broker=give_up_broker,
                                                                       net_gross_ind=net_gross_ind)
        split_param_2 = self.order_book.create_split_booking_parameter(split_qty=qty_of_split)
        self.order_book.split_book([split_param_1, split_param_2], row_numbers=[1], error_expected=False)

        self.booking_blotter.set_extraction_details([BookingBlotterColumns.status.value,
                                                     BookingBlotterColumns.match_status.value,
                                                     BookingBlotterColumns.summary_status.value],
                                                    filter_dict={
                                                        BookingBlotterColumns.order_id.value: order_id})
        result = self.booking_blotter.extract_from_booking_window()
        self.booking_blotter.compare_values(
            {BookingBlotterColumns.status.value: self.data_set.get_middle_office_status('status_1'),
             BookingBlotterColumns.match_status.value: self.data_set.get_middle_office_match_status('match_status_1'),
             BookingBlotterColumns.summary_status.value: ''},
            result, 'Comparing values from booking blotter')
        self.booking_blotter.set_extraction_details([AllocInstructionQties.booking_qty.value,
                                                     AllocInstructionQties.give_up_broker.value],
                                                    filter_dict={
                                                        BookingBlotterColumns.order_id.value: order_id})
        result = self.booking_blotter.extract_from_second_level_tab(SecondLevelTabs.alloc_instruction_qties.value, 2)
        format_tuple = (AllocInstructionQties.booking_qty.value, qty_of_split, AllocInstructionQties.give_up_broker.value,give_up_broker)
        self.booking_blotter.compare_values({
            '1': '{%s=%s, %s=%s}' % format_tuple,
            '2': '{%s=%s, %s=%s}' % format_tuple},
                                            result, 'Comparing second level values(last step)')
        # endregion
