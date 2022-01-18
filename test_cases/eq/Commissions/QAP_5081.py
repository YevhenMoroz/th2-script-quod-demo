import logging

from th2_grpc_act_gui_quod.middle_office_pb2 import PanelForExtraction

from custom.basic_custom_actions import create_event

from test_framework.old_wrappers.eq_wrappers import open_fe
from test_framework.win_gui_wrappers.base_window import BaseWindow
from test_framework.win_gui_wrappers.oms.oms_client_inbox import OMSClientInbox
from test_framework.win_gui_wrappers.oms.oms_middle_office import OMSMiddleOfficeBook
from stubs import Stubs
from test_framework.win_gui_wrappers.oms.oms_order_book import OMSOrderBook
from test_framework.win_gui_wrappers.oms.oms_order_ticket import OMSOrderTicket
from win_gui_modules.utils import get_base_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-5081"
    case_id = create_event(case_name, report_id)
    # region Declarations
    qty = "900"
    price = "30"
    client = "CLIENT_COMM_1"
    client_new = 'CLIENT_COMM_2'
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    open_fe(session_id, report_id, work_dir, username, password)
    # create CO order
    oms_order_book = OMSOrderBook(case_id, session_id)
    oms_order_inbox = OMSClientInbox(case_id, session_id)
    oms_order_ticket = OMSOrderTicket(case_id, session_id)
    oms_order_middle_office = OMSMiddleOfficeBook(case_id, session_id)
    oms_order_ticket.set_order_details(client=client, limit=price, qty=qty, order_type='Limit',
                                       tif='Day', is_sell_side=False, instrument='ISI3', recipient='Desk of Order Book')
    oms_order_ticket.create_order(lookup='ISI3')
    oms_order_inbox.accept_order('ISI3', qty, price)
    oms_order_book.scroll_order_book(1)
    # endregion
    oms_order_ticket.set_order_details(client=client_new)
    oms_order_ticket.amend_order()
    # region manual Execute CO order
    oms_order_book.manual_execution(qty=qty, price=price)
    order_id = oms_order_book.extract_field('Order ID')
    oms_order_book.complete_order()
    # endregion

    # region book order
    oms_order_middle_office.book_order()
    # endregion
    filter_for_extracting = {'Order ID': order_id}
    # region Extract value from Amend  Ticket of block
    result_of_extraction = oms_order_middle_office.extracting_values_from_amend_ticket([PanelForExtraction.COMMISSION],
                                                                                       filter_for_extracting)
    print(result_of_extraction)
    result = BaseWindow.split_2lvl_values(result_of_extraction)
    print(result)
    expected_result = {'Basis': 'PerUnit', 'Rate': '0', 'Amount': '0', 'Currency': 'EUR',
                       'Category': 'Other'}
    oms_order_book.compare_values(expected_result, result[0], event_name='Check values')

    # endregion
