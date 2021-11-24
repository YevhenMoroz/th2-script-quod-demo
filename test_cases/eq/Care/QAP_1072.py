import logging
from datetime import datetime

import test_framework.old_wrappers.eq_fix_wrappers
from custom.basic_custom_actions import create_event
from test_cases.wrapper import eq_wrappers
from stubs import Stubs
from win_gui_modules.utils import get_base_request
from win_gui_modules.wrappers import set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-1072"
    # region Declarations
    qty = "900"
    price = "10"
    new_price = "1"
    datetime.utcnow().isoformat()
    lookup = "VETO"
    client = "CLIENT_FIX_CARE"
    # endregion
    # region Open FE

    case_id = create_event(case_name, report_id)
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # endregion
    # region Create CO
    fix_message = test_framework.old_wrappers.eq_fix_wrappers.create_order_via_fix(case_id, 3, 2, client, 2, qty, 0, price)
    eq_wrappers.accept_order(lookup, qty, price)
    # endregion
    # region ManualExecute
    eq_wrappers.manual_execution(base_request, str(int((int(qty) / 2))), price)
    fix_message.pop('response')
    # endregion
    # regionAmend fix order
    param_list = {'Price': new_price}
    test_framework.old_wrappers.eq_fix_wrappers.amend_order_via_fix(case_id, fix_message, param_list)
    # endregion
    # region accept amend
    eq_wrappers.accept_modify(lookup, qty, price)
    # endregion
    eq_wrappers.verify_order_value(base_request, case_id, "Limit Price", new_price)
