import logging

from custom.basic_custom_actions import create_event
from quod_qa.wrapper import eq_wrappers, eq_fix_wrappers
from stubs import Stubs
from win_gui_modules.utils import get_base_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute(report_id, session_id):
    case_name = "QAP-5726"
    # Declarations
    qty = "100"
    price = "10"
    client1 = "CLIENT_COMM_1"
    client2 = "MOClient"
    alloc_acc = "CLIENT_COMM_1_SA4"
    case_id = create_event(case_name, report_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    # Open FE
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # Create CO
    eq_fix_wrappers.create_order_via_fix(case_id, 3, 1, client1, 2, qty, 0, price)
    eq_wrappers.accept_order('VETO', qty, price)
    eq_wrappers.manual_execution(base_request, qty, price)
    eq_wrappers.complete_order(base_request)
    eq_wrappers.book_order(base_request, client1, price)
    eq_wrappers.approve_block(base_request)
    param = [{"Security Account": alloc_acc, "Alloc Qty": qty}]
    eq_wrappers.allocate_order(base_request, param)
    eq_wrappers.unallocate_order(base_request)
    eq_wrappers.unbook_order(base_request)
    eq_wrappers.book_order(base_request,client2, price)
    eq_wrappers.verify_block_value(base_request,case_id, "Client ID",client2)
