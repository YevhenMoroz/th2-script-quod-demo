import logging

from custom.basic_custom_actions import create_event
from test_cases.wrapper import eq_wrappers
from stubs import Stubs
from win_gui_modules.utils import get_base_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute(report_id, session_id):
    case_name = "QAP-5822"
    # Declarations
    qty = "100"
    price = "10"
    client = "MOClient"
    lookup = "VETO"
    lookup_symbol = "ORA.EUR-[PARIS]"
    case_id = create_event(case_name, report_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    # Open FE
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # Create CO
    eq_wrappers.create_order(base_request, qty, client, lookup, "Limit", price=price, instrument=lookup_symbol)
    eq_wrappers.verify_order_value(base_request, case_id, "Lookup", lookup_symbol)
