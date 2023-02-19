import logging
from pathlib import Path

from th2_grpc_act_gui_quod.middle_office_pb2 import PanelForExtraction

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import timestamps
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, DoneForDays, \
    PostTradeStatuses, ExecSts, MiddleOfficeColumns
from test_framework.win_gui_wrappers.oms.oms_booking_window import OMSBookingWindow
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOffice
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

seconds, nanos = timestamps()  # Test case start time

@try_except(test_id=Path(__file__).name[:-3])
class QAP_T7129(TestCase):
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
        # region set up fee and commission via Rest Api(precondition)
        self.rest_api_manager.send_default_fee()
        self.rest_api_manager.set_modify_client_commission_message(client=self.client)
        # endregion
        # region create order via fix (precondition)
        orders_id = []
        self.fix_message.set_default_care_limit('instrument_3')
        self.fix_message.change_parameters(
            {'Side': '1', 'OrderQtyData': {'OrderQty': self.qty}, 'Account': self.client, 'Price': self.price,
             "Currency": self.data_set.get_currency_by_name("currency_3")})
        for index in range(2):
            response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
            orders_id.append(response[0].get_parameters()['OrderID'])
            filter_dict = {OrderBookColumns.order_id.value: orders_id[index]}
            self.client_inbox.accept_order(filter=filter_dict)
        # endregion

        # # region execute and complete CO orders (step 1)
        for order in orders_id:
            filter_dict = {OrderBookColumns.order_id.value: order}
            self.order_book.manual_execution(self.qty, self.price, filter_dict=filter_dict)
            self.order_book.complete_order(filter_list=[OrderBookColumns.order_id.value, order])
        # endregion

        # region check value (step 1)
        for order in orders_id:
            self.order_book.set_filter(filter_list=[OrderBookColumns.order_id.value, order])
            values = self.order_book.extract_fields_list(
                {OrderBookColumns.done_for_day.value: OrderBookColumns.done_for_day.value,
                 OrderBookColumns.post_trade_status.value: OrderBookColumns.post_trade_status.value,
                 OrderBookColumns.exec_sts.value: OrderBookColumns.exec_sts.value})
            self.order_book.compare_values({OrderBookColumns.done_for_day.value: DoneForDays.yes.value,
                                            OrderBookColumns.post_trade_status.value: PostTradeStatuses.ready_to_book.value,
                                            OrderBookColumns.exec_sts.value: ExecSts.filled.value}, values,
                                           'Comparing values after execute and complete')
        # endregion

        # region step 2 , step 3 and step 4
        checking_values = self.order_book.extracting_values_from_booking_ticket(
            [PanelForExtraction.MAIN_PANEL], filter_dict={OrderBookColumns.qty.value: self.qty}, count_of_rows=2)
        values = self.order_book.split_main_tab(checking_values)
        # check netAmount and netPrice
        gross_amount = int(self.qty) * 2 * int(self.price) / 100
        net_amount = gross_amount + 1 + 1
        net_price = net_amount / (int(self.qty) * 2)
        net_price = ' {0:1.4}'.format(net_price)
        net_amount = ' ' + str(net_amount)
        net_amount = net_amount[0:2] + ',' + net_amount[2:7]
        # endregion
        # check expected result from 3 step
        expected_result = dict()
        expected_result.update({'Net Amount': net_amount})
        expected_result.update({'Net Price': net_price})
        actually_result = dict()
        actually_result.update(values[len(values) - 2])
        actually_result.update(values[len(values) - 1])
        self.order_book.compare_values(expected_result, actually_result, 'Comparing NetPrice and Net Amount')
        # endregion

        # check expected result from step 4
        expected_result.clear()
        actually_result.clear()
        expected_result.update({'Total Comm': ' 1', 'Total Fees': ' 1'})
        actually_result.update(values[-4])
        actually_result.update(values[-3])
        self.order_book.compare_values(expected_result, actually_result, "Comparing values of Fee and Commission")
        # endregion

        # region step 5, step 6 and step 7
        net_gross_ind = self.data_set.get_net_gross_ind_type('net_ind')
        give_up_broker = self.data_set.get_give_up_broker('give_up_broker_1')
        self.middle_office.set_modify_ticket_details(net_gross_ind=net_gross_ind, give_up_broker=give_up_broker,
                                                     selected_row_count=2, extract_book=True,
                                                     net_price=str((int(self.price) / 100) * 2))
        result: dict = self.middle_office.book_order([OrderBookColumns.qty.value, self.qty])

        # region check expected result from 5 and 6 step
        expected_result.clear()
        actually_result.clear()
        net_amount_new = str(gross_amount * 2)
        net_amount_new = net_amount_new[0:1] + ',' + net_amount_new[1:7]
        expected_result.update({'book.Commission': 'Commissions are empty ', 'book.Fees': 'Fees are empty',
                                'book.netAmount': net_amount_new})
        actually_result.update({'book.Commission': result['book.Commission']})
        actually_result.update({'book.Fees': result['book.Fees']})
        actually_result.update({'book.netAmount': result['book.netAmount']})
        self.order_book.compare_values(expected_result, actually_result,
                                       'Comparing Fees and Commission after setting giveUpBroker ')
        # endregion

        # region check value for block
        self.booking_blotter.set_extraction_details([MiddleOfficeColumns.total_fees.value,
                                                     MiddleOfficeColumns.client_comm.value])
        result = self.booking_blotter.extract_from_booking_window()

        self.order_book.compare_values(
            {MiddleOfficeColumns.total_fees.value: '', MiddleOfficeColumns.client_comm.value: ''},
            result, 'Comparing values Fees and Commission in Booking Blotter')
        #endregion
