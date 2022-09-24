import logging
import os
import time
from pathlib import Path

from th2_grpc_act_gui_quod.middle_office_pb2 import PanelForExtraction

from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7186(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__), self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_api_manager = JavaApiManager(self.java_api, self.test_id)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.fix_env.sell_side, self.test_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.middle_office = OMSMiddleOffice(self.test_id, self.session_id)

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
        cl_ord_id = self.fix_message.get_parameter('ClOrdID')
        # endregion

        # region create order
        try:
            new_order_single_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew_FIXStandard(
                self.fix_env.buy_side, account, exec_destination, float(price))
            trade_rule = rule_manager.add_NewOrdSingleExecutionReportTrade_FIXStandard(self.fix_env.buy_side, account,
                                                                                       exec_destination, float(price),
                                                                                       int(qty), 0)
            response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
            order_id = response[0].get_parameters()['OrderID']
        except Exception as ex:
            logger.error(f"{ex}", exc_info=True, stack_info=True)

        finally:
            time.sleep(10)
            rule_manager.remove_rule(trade_rule)
            rule_manager.remove_rule(new_order_single_rule)
        filter_dict = {OrderBookColumns.order_id.value: order_id}
        # endregion

        # region verify value of fields after trade (precondition)
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id])
        post_trade_status = self.order_book.extract_field(OrderBookColumns.post_trade_status.value)
        self.order_book.set_filter([OrderBookColumns.cl_ord_id.value, cl_ord_id])
        value_done_for_day = self.order_book.extract_field(OrderBookColumns.done_for_day.value)
        self.order_book.compare_values(
            {OrderBookColumns.post_trade_status.value: 'ReadyToBook', OrderBookColumns.done_for_day.value: 'Yes'},
            {OrderBookColumns.post_trade_status.value: post_trade_status,
             OrderBookColumns.done_for_day.value: value_done_for_day}, 'Comparing values after trade'
        )
        # endregion

        # region book order(step 1)
        self.middle_office.only_opening_booking_ticket(filter_dict=filter_dict)
        # endregion

        # region step 2
        currency_recompute = " "+self.data_set.get_currency_by_name('currency_4')
        currency_of_order = " "+self.data_set.get_currency_by_name('currency_1')
        exchange_of_usd = 1.327
        settl_amount = str(exchange_of_usd * int(qty) * int(price))
        settl_amount_for_checking = " "+settl_amount[0] + ',' + settl_amount[1:4]
        details = self.middle_office.set_modify_ticket_details(settl_currency='USD', toggle_recompute=True)
        self.middle_office.only_set_details_to_booking_ticket(details=details)
        list_of_extraction_panel = [PanelForExtraction.SETTLEMENT, PanelForExtraction.MAIN_PANEL]
        list_of_values = ['Currency', 'Settl Amount']
        expected_result = {'Currency': currency_recompute, 'Settl Amount': settl_amount_for_checking}
        self.__comparing_values_after_extraction(list_of_extraction_panel=list_of_extraction_panel,
                                                 list_of_column=list_of_values,
                                                 expected_result=expected_result,
                                                 end_of_message="after turn on recompute"
                                                 )
        # endregion

        # region step 3
        details = self.middle_office.set_modify_ticket_details(toggle_recompute=True)
        self.middle_office.only_set_details_to_booking_ticket(details=details)
        # endregion

        # region checking of step 3
        expected_result = {'Currency': currency_of_order, 'Settl Amount': settl_amount_for_checking}
        self.__comparing_values_after_extraction(list_of_extraction_panel=list_of_extraction_panel,
                                                 list_of_column=list_of_values,
                                                 expected_result=expected_result,
                                                 end_of_message="after turn off recompute")
        # endregion

        # region close booking ticket with creating block (postcondition)
        self.middle_office.only_close_booking_ticket()
        # endregion

    def __comparing_values_after_extraction(self, expected_result, list_of_extraction_panel, list_of_column,
                                            end_of_message: str):
        result = self.middle_office.only_extract_value_from_booking_ticket(list_of_extraction_panel)
        result = self.order_book.split_main_tab(result)
        actually_result = dict()
        for column in list_of_column:
            for values in result:
                keys = values.keys()
                if column in keys:
                    actually_result.update(values)
        self.order_book.compare_values(expected_result, actually_result, f"Comparing values {end_of_message}")
        # endregion
