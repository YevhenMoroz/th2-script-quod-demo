import logging
from datetime import datetime

import test_cases.wrapper.eq_fix_wrappers
from custom.basic_custom_actions import create_event, timestamps
from test_cases.wrapper import eq_wrappers
from stubs import Stubs
from win_gui_modules.utils import get_base_request
from win_gui_modules.wrappers import set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-3325"

    seconds, nanos = timestamps()  # Store case start time

    # region Declarations
    qty = "900"
    price = "40"
    time = datetime.utcnow().isoformat()
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
    # endregionA
    # region Create CO
    fix_message = test_cases.wrapper.eq_fix_wrappers.create_order_via_fix(case_id, 3, 1, client, 2, qty, 0, price)
    response = fix_message.pop('response')
    # Amend fix order
    eq_wrappers.amend_order(base_request, client)
    # endregion
    eq_wrappers.verify_order_value(base_request, case_id, 'Client ID', client)
