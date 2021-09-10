import logging
from datetime import datetime

from custom.basic_custom_actions import create_event, timestamps
from custom.verifier import Verifier
from quod_qa.wrapper import eq_wrappers
from stubs import Stubs
from win_gui_modules.utils import get_base_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute(report_id, session_id):
    case_name = "QAP-4994"
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
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # endregion

    # region Create CO
    eq_wrappers.create_order_via_fix(case_id, 3, 1, client, 2, qty, 0, price)
    eq_wrappers.accept_order('VETO', qty, price)
    order_id = eq_wrappers.get_order_id(base_request)
    cl_ord_id = eq_wrappers.get_cl_order_id(base_request)
    # endregion

    # region suspend order
    eq_wrappers.suspend_order(base_request, False)
    # endregion

    # region cancel CO order via FIX
    eq_wrappers.cancel_order_via_fix(case_id, cl_ord_id, cl_ord_id, client, 1)
    eq_wrappers.accept_cancel('VETO', qty, price)
    eq_wrappers.verify_order_value(base_request, case_id, 'Sts', 'Cancelled', False)
    # endregion
    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
