import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.oms.FixMessageExecutionReportOMS import FixMessageExecutionReportOMS
from test_framework.fix_wrappers.oms.FixMessageNewOrderSingleOMS import FixMessageNewOrderSingleOMS
from test_framework.rest_api_wrappers.oms.rest_commissions_sender import RestCommissionsSender
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, ExecSts
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@try_except(test_id=Path(__file__).name[:-3])
class QAP_T6992(TestCase):

    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.wa_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.ss_connectivity = self.fix_env.sell_side
        self.client = self.data_set.get_client_by_name("client_com_1")
        self.mic = self.data_set.get_mic_by_name("mic_2")
        self.cur = self.data_set.get_currency_by_name('currency_3')
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_message = FixMessageNewOrderSingleOMS(self.data_set).set_default_care_limit("instrument_3")
        self.fix_message.change_parameters(
            {"Account": self.client,
             "ExDestination": self.mic,
             "Currency": self.cur})
        self.qty = self.fix_message.get_parameter('OrderQtyData')['OrderQty']
        self.venue = self.data_set.get_venue_by_name("venue_2")
        self.price = self.fix_message.get_parameter('Price')
        self.rest_commission_sender = RestCommissionsSender(self.wa_connectivity, self.test_id, self.data_set)
        self.fix_manager = FixManager(self.ss_connectivity, self.test_id)
        self.exec_report = FixMessageExecutionReportOMS(self.data_set)
        self.comm_profile = self.data_set.get_comm_profile_by_name("perc_amt")
        self.client_inbox = OMSClientInbox(self.test_id, self.session_id)
        self.order_book = OMSOrderBook(self.test_id, self.session_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        self.rest_commission_sender.clear_commissions()
        self.rest_commission_sender.set_modify_client_commission_message(
            comm_profile=self.comm_profile).change_message_params(
            {'venueID': self.venue}).send_post_request()
        # endregion
        # region send order
        response = self.fix_manager.send_message_and_receive_response_fix_standard(self.fix_message)
        order_id = response[0].get_parameter("OrderID")
        filter_dict = {OrderBookColumns.order_id.value: order_id}
        self.client_inbox.accept_order(filter=filter_dict)
        manual_day_cum_qty = str(int(int(self.qty) * int(self.price)))
        manual_day_cum_qty = manual_day_cum_qty[0]+','+manual_day_cum_qty[1:]
        # endregion
        # region manual execute order
        self.order_book.manual_execution(filter_dict=filter_dict)
        # endregion
        # region check ManualDayCumAmt and ManualDayCumQty
        self.order_book.set_filter([OrderBookColumns.order_id.value, order_id])
        actual_values = self.order_book.extract_fields_list(
            {OrderBookColumns.exec_sts.value: OrderBookColumns.exec_sts.value,
             OrderBookColumns.manual_day_cum_amt.value: OrderBookColumns.manual_day_cum_amt.value,
             OrderBookColumns.manual_day_cum_qty.value: OrderBookColumns.manual_day_cum_qty.value})
        self.order_book.compare_values(
            {OrderBookColumns.exec_sts.value: ExecSts.filled.value,
             OrderBookColumns.manual_day_cum_amt.value: manual_day_cum_qty,
             OrderBookColumns.manual_day_cum_qty.value: self.qty}, actual_values,
            'Comparing expected and actual values')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rest_commission_sender.clear_commissions()
