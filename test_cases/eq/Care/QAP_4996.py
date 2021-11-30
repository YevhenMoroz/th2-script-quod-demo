import logging
from datetime import datetime

from custom.verifier import Verifier
from test_framework.old_wrappers import eq_wrappers
from custom.basic_custom_actions import create_event, timestamps
from stubs import Stubs
from test_framework.win_gui_wrappers.base_main_window import open_fe
from win_gui_modules.utils import get_base_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute(report_id, session_id):
    case_name = "QAP-4996"
    # region Declarations
    seconds, nanos = timestamps()  # Store case start time
    qty = "40"
    price = "11"
    price_amend = '50'
    client = "CLIENT_FIX_CARE"
    new_qty = '100'
    case_id = create_event(case_name, report_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    # endregion

    # region Open FE
    open_fe(session_id, report_id, case_id, work_dir, username)
    # endregion

    # region Create CO
    eq_wrappers.create_order_via_fix(case_id, 3, 1, client, 2, qty, 0, price)
    eq_wrappers.accept_order('VETO', qty, price)
    order_id = eq_wrappers.get_order_id(base_request)
    # endregion

    # region suspend order
    eq_wrappers.suspend_order(base_request, False)
    # endregion

    # region amend CO order
    eq_wrappers.amend_order(base_request, qty=new_qty, price=price_amend)
    eq_wrappers.verify_order_value(base_request, case_id, 'Qty', new_qty, False)
    eq_wrappers.verify_order_value(base_request, case_id, 'Limit Price', price_amend, False)
    eq_wrappers.verify_order_value(base_request, case_id, 'Suspended', 'Yes', False)

    # endregion

    # region release order
    eq_wrappers.release_order(base_request)
    eq_wrappers.verify_order_value(base_request, case_id, 'Suspended', 'No', False)
    # endregion

    # region manual execute
    eq_wrappers.manual_execution(base_request, str(int(int(qty) / 4)), price_amend)
    eq_wrappers.verify_order_value(base_request, case_id, 'ExecSts', 'PartiallyFilled', False)
    # endregion

    # region suspend again
    eq_wrappers.suspend_order(base_request, False)
    eq_wrappers.verify_order_value(base_request, case_id, 'Suspended', 'Yes', False)
    # endregion

    # region extract error
    eq_wrappers.split_order(base_request, str(int(int(qty) / 4)), 'Limit', price_amend)
    result = eq_wrappers.extract_error_order_ticket(base_request)
    verifier = Verifier(case_id)
    verifier.set_event_name("Check value")
    verifier.compare_values("Order ID from View",
                            "Error - [QUOD-11801] Validation by CS failed, Request not allowed:  The order is "
                            "suspended, OrdID=" + order_id,
                            result['ErrorMessage'],
                            )
    verifier.verify()
    # endregion
    # region cancel order
    eq_wrappers.cancel_order(base_request)
    eq_wrappers.verify_order_value(base_request, case_id, 'Suspended', 'Yes', False)
    eq_wrappers.verify_order_value(base_request, case_id, 'Sts', 'Cancelled', False)
    # endregion

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")