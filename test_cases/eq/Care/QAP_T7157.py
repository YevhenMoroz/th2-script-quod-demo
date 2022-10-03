import logging
import os
from pathlib import Path

from custom import basic_custom_actions as bca
from stubs import Stubs
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.win_gui_wrappers.fe_trading_constant import OrderType, TimeInForce, OrderBookColumns
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


class QAP_T7157(TestCase):
    def __init__(self, report_id, session_id, data_set, environment):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(os.path.basename(__file__)[:-3], self.report_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Declarations
        qty = "900"
        price = "30"
        client = self.data_set.get_client_by_name('client_pt_1')
        account = self.data_set.get_account_by_name('client_pt_1_acc_1')
        account_new = self.data_set.get_account_by_name('client_pt_1_acc_2')
        venue_client_account_first = self.data_set.get_venue_client_account('client_pt_1_acc_1_venue_client_account')
        venue_client_account_second = self.data_set.get_venue_client_account('client_pt_1_acc_2_venue_client_account')
        lookup = self.data_set.get_lookup_by_name('lookup_1')
        order_type = OrderType.limit.value
        time_in_force = TimeInForce.DAY.value
        user = Stubs.custom_config['qf_trading_fe_user']
        venue_client_column_name = OrderBookColumns.venue_client_account.value
        account_id_column_name = OrderBookColumns.account_id.value
        # create CO order
        oms_order_book = OMSOrderBook(self.test_id, self.session_id)
        oms_order_inbox = OMSClientInbox(self.test_id, self.session_id)
        oms_order_ticket = OMSOrderTicket(self.test_id, self.session_id)
        oms_order_ticket.set_order_details(client=client, limit=price, qty=qty, tif='Day', recipient=user,
                                           partial_desk=False, account=account)
        oms_order_ticket.create_order(self.data_set.get_lookup_by_name('lookup_1'))
        oms_order_inbox.accept_order(lookup, qty, price)
        # region extract Venue Client Account
        venue_client_account = oms_order_book.extract_field(venue_client_column_name)
        extracted_account = oms_order_book.extract_field(account_id_column_name)
        # endregion

        # region verify velues
        expected_result = {account_id_column_name: account,
                           venue_client_column_name: venue_client_account_first}
        actually_result = {account_id_column_name: extracted_account, venue_client_column_name: venue_client_account}
        oms_order_book.compare_values(expected_result, actually_result, event_name='Check values 1')
        # endregion

        # region amend order
        oms_order_ticket.set_order_details(account=account_new)
        oms_order_ticket.amend_order()
        #endregion

        # region extract Venue Client Account
        venue_client_new_account = oms_order_book.extract_field('Venue Client Account')
        extracted_account = oms_order_book.extract_field(account_id_column_name)
        expected_result = {account_id_column_name: account_new,
                           venue_client_column_name: venue_client_account_second}
        actually_result = {account_id_column_name: extracted_account,
                           venue_client_column_name: venue_client_new_account}
        oms_order_book.compare_values(expected_result, actually_result, event_name='Check values 2')
        # endregion
