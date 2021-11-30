import logging

from custom.basic_custom_actions import create_event
from test_framework.old_wrappers.eq_wrappers import open_fe
from test_framework.win_gui_wrappers.base_window import BaseWindow
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket
from stubs import Stubs

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-1718"
    case_id = create_event(case_name, report_id)
    # region Declarations
    qty = "900"
    price = "30"
    client = "CLIENT_FEES_1"
    route = 'ChiX direct access'
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    # base_request = get_base_request(session_id, case_id)
    base_window = BaseWindow(case_id, session_id)
    open_fe(session_id, report_id, work_dir, username, password)
    # # create CO order
    oms_order_book = OMSOrderBook(case_id, session_id)
    oms_order_inbox = OMSClientInbox(case_id, session_id)
    oms_order_ticket = OMSOrderTicket(case_id, session_id)
    oms_order_ticket.set_order_details(client=client, limit=price, qty=qty, order_type='Limit',
                                       tif='Day', is_sell_side=False, instrument='VETO', desk='Desk of Order Book')
    oms_order_ticket.oms_create_order(lookup='VETO')
    oms_order_inbox.accept_order('VETO', qty, price)
    # # oms_order_book.scroll_order_book(1)
    # # endregion
    #
    # # region manual Execute CO order
    oms_order_book.direct_moc_order_correct(qty, route)
    # endregion
    # region Extract value from Booking Ticket
    order_id = oms_order_book.extract_field('Order ID')
    result_of_extraction = oms_order_book.extract_2lvl_fields('Child Orders', {'ID': 'Order ID', 'Qty': 'Qty'}, [1])
    print(result_of_extraction)
    expected_result = {'Order ID': order_id, 'Qty': qty}
    oms_order_book.compare_values(expected_result, result_of_extraction[0], event_name='Check values')

    # endregion
