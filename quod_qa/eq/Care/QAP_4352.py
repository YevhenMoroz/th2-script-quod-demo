import logging

from custom.verifier import Verifier
from quod_qa.wrapper import eq_wrappers
from custom.basic_custom_actions import create_event
from stubs import Stubs
from win_gui_modules.utils import get_base_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute(report_id, session_id):
    case_name = "QAP-4352"
    # region Declarations
    qty = "40"
    price = "11"
    client = "CLIENT_FIX_CARE"
    case_id = create_event(case_name, report_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    # endregion

    # region Open FE
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # endregion
    # region Create CO
    eq_wrappers.create_order_via_fix(case_id, 3, 1, client, 2, qty, 0, price)
    eq_wrappers.accept_order('VETO', qty, price)
    order_id = eq_wrappers.get_order_id(base_request)
    # endregion

    # region suspend order
    eq_wrappers.suspend_order(base_request, False)
    # endregion
    eq_wrappers.split_order(base_request, qty, 'Limit', price)
    result = eq_wrappers.extract_error_order_ticket(base_request)
    verifier = Verifier(case_id)
    verifier.set_event_name("Check value")
    verifier.compare_values("Order ID from View",
                            "Error - [QUOD-11801] Validation by CS failed, Request not allowed:  The order is "
                            "suspended, OrdID=" + order_id,
                            result['ErrorMessage'],
                            )
    verifier.verify()
