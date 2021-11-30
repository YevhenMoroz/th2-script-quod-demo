import logging

from custom.basic_custom_actions import create_event
from test_framework.old_wrappers import eq_wrappers
from stubs import Stubs
from test_framework.old_wrappers.eq_wrappers import open_fe
from win_gui_modules.utils import get_base_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute(report_id, session_id):
    case_name = "QAP-5712"
    # Declarations
    qty = "100"
    price = "10"
    client = "CLIENT_COMM_1"
    case_id = create_event(case_name, report_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    # Open FE
    open_fe(session_id, report_id, case_id, work_dir, username)
    # Create CO
    eq_fix_wrappers.create_order_via_fix(case_id, 3, 1, client, 2, qty, 0, price)
    eq_wrappers.accept_order('VETO', qty, price)
    eq_wrappers.manual_execution(base_request, qty, price)
    eq_wrappers.complete_order(base_request)
    eq_wrappers.book_order(base_request, client, price, comm_basis="Absolute", comm_rate="40", remove_commission=True)
    eq_wrappers.verify_block_value(base_request, case_id, 'Client Comm', '40')
