import logging
from datetime import datetime, timedelta
from pathlib import Path

import psycopg2

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, PostTradeStatuses, Status
from test_framework.win_gui_wrappers.oms.oms_booking_window import OMSBookingWindow
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()


class QAP_T6958(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        # region Declarations
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.rest_api_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side
        self.qty = '7129'
        self.price = '10'
        self.client = self.data_set.get_client('client_pt_1')
        self.alloc_account = self.data_set.get_account_by_name('client_pt_1_acc_1')
        self.order_book = OMSOrderBook(self.test_id, self.session_id)
        self.middle_office = OMSMiddleOffice(self.test_id, self.session_id)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set)
        self.fix_verifier = FixVerifier(self.fix_env.drop_copy, self.test_id)
        self.execution_report = FixMessageExecutionReportOMS(self.data_set)
        self.booking_blotter = OMSBookingWindow(self.test_id, self.session_id)
        self.rest_api_manager = RestCommissionsSender(self.rest_api_connectivity, self.test_id, self.data_set)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region create order via fix (precondition)
        self.fix_message.set_default_care_limit('instrument_1')
        self.fix_message.change_parameters(
            {'Side': '1', 'OrderQtyData': {'OrderQty': self.qty}, 'Account': self.client, 'Price': self.price})
        self.fix_message.change_parameters(
            {'TimeInForce': '6', 'ExpireDate': (datetime.now() + timedelta(days=1)).strftime("%Y%m%d")})
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = response[0].get_parameters()['OrderID']
        self.order_book.extract_field("OrderID")
        filter_dict = {OrderBookColumns.order_id.value: order_id}
        filter_list = [OrderBookColumns.order_id.value, order_id]
        self.client_inbox.accept_order(filter=filter_dict)

        # endregion

        # region partially filled CO order
        comulative_qty = str(int(int(self.qty) / 2))
        self.order_book.manual_execution(comulative_qty, self.price)
        # endregion

        # region check daycumqty
        self.order_book.set_filter(filter_list)
        actual_day_cum_qty = self.order_book.extract_fields_list(
            {OrderBookColumns.day_cum_qty.value: OrderBookColumns.day_cum_qty.value})
        self.order_book.compare_values({OrderBookColumns.day_cum_qty.value: comulative_qty}, actual_day_cum_qty,
                                       "Comparing day cum Qty")
        # endregion

        # region send procedure
        connection = None
        cursor = None
        try:
            connection = psycopg2.connect(user="quod317prd",
                                          password="quod317prd",
                                          host="10.0.22.69",
                                          port="5432",
                                          database="quoddb")
            cursor = connection.cursor()
            cursor.execute("select eod_expireOrders(null,'N');")
            connection.commit()
        except Exception as error:
            print("Error while connecting to PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")
        # endregion

        # region check order after perform of procedure
        self.order_book.set_filter(filter_list)
        actual_day_cum_qty = self.order_book.extract_fields_list(
            {OrderBookColumns.day_cum_qty.value: OrderBookColumns.day_cum_qty.value})
        self.order_book.compare_values({OrderBookColumns.day_cum_qty.value: comulative_qty}, actual_day_cum_qty,
                                       "Comparing actual result")
        # endregion

        # region check expected result from step 3
        self.order_book.refresh_order(filter_list)
        self.order_book.set_filter(filter_list)
        values = self.order_book.extract_fields_list({OrderBookColumns.sts.value: OrderBookColumns.sts.value,
                                                      OrderBookColumns.free_notes.value: OrderBookColumns.free_notes.value,
                                                      OrderBookColumns.post_trade_status.value: OrderBookColumns.post_trade_status.value})
        self.order_book.compare_values({
            OrderBookColumns.sts.value: Status.expired.value,
            OrderBookColumns.free_notes.value: "Order terminated by Quod eod_ExpireOrders procedure",
            OrderBookColumns.post_trade_status.value: PostTradeStatuses.ready_to_book.value
        }, values, 'Comparing values from step 3')
        # endregion
