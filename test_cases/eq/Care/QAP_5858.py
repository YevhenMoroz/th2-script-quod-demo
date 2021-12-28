import logging

from custom.basic_custom_actions import create_event
from test_framework.old_wrappers.eq_wrappers import open_fe
from test_framework.win_gui_wrappers.base_window import BaseWindow
from stubs import Stubs
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-5858"
    case_id = create_event(case_name, report_id)
    # region Declarations
    qty = "900"
    price = "30"
    client = "MOClient"
    account = 'MOClient_SA1'
    account_new = 'MOClient_SA2'
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    base_window = BaseWindow(case_id, session_id)
    open_fe(session_id, report_id, work_dir, username, password)
    # create CO order
    oms_order_book = OMSOrderBook(case_id, session_id)
    oms_order_inbox = OMSClientInbox(case_id, session_id)
    oms_order_ticket = OMSOrderTicket(case_id, session_id)
    oms_order_ticket.set_order_details(client=client, limit=price, qty=qty, order_type='Limit',
                                       tif='Day', is_sell_side=False, instrument='VETO', account='MOClient_SA1',
                                       desk='Desk of Order Book')

    oms_order_ticket.oms_create_order(lookup='VETO')
    oms_order_inbox.accept_order('VETO', qty, price)
    oms_order_book.scroll_order_book(1)
    # region extract Venue Client Account
    venue_client_account = oms_order_book.extract_field('Venue Client Account')
    # endregion

    # region verify velues
    expected_result = {'Account ID': 'MOClient_SA1', 'Venue Client Account': 'MOCLIENT_SA1'}
    actually_result = {'Account ID': account, 'Venue Client Account': venue_client_account}
    oms_order_book.compare_values(expected_result, actually_result, event_name='Check values')
    # endregion

    # region amend order
    oms_order_ticket.set_order_details(account=account_new)
    oms_order_ticket.amend_order()

    # region extract Venue Client Account
    venue_client_new_account = oms_order_book.extract_field('Venue Client Account')
    expected_result = {'Account ID': 'MOClient_SA2', 'Venue Client Account': 'MOCLIENT_SA2'}
    actually_result = {'Account ID': account_new, 'Venue Client Account': venue_client_new_account}
    oms_order_book.compare_values(expected_result, actually_result, event_name='Check values')
    # endregion