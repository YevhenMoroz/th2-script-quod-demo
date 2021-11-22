import logging
from datetime import datetime

import test_framework.old_wrappers.eq_fix_wrappers
from test_cases.wrapper import eq_wrappers
from custom.basic_custom_actions import create_event, timestamps
from stubs import Stubs
from win_gui_modules.utils import get_base_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-3294"
    seconds, nanos = timestamps()  # Store case start time
    # region Declarations
    qty = "900"
    price = "20"
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
    test_framework.old_wrappers.eq_fix_wrappers.create_order_via_fix(case_id, 3, 2, client, 2, qty, 0, price)
    # endregion
    # region Check value
    eq_wrappers.verify_order_value(base_request, case_id, "Sts", "Open")
    # region Execute
    eq_wrappers.manual_execution(base_request, qty, price)
    # endregion
    # region Check value
    eq_wrappers.verify_order_value(base_request, case_id, "ExecSts", "Filled")
    eq_wrappers.verify_order_value(base_request, case_id, "Sts", "Open")
    # endregion
    # region Complete
    eq_wrappers.complete_order(base_request)
    # endregion
    # region Check value
    eq_wrappers.verify_order_value(base_request, case_id, "DoneForDay", "ReadyToBook")
    eq_wrappers.verify_order_value(base_request, case_id, "PostTradeStatus", "Yes")
    # endregion
    # region Un-Complete
    eq_wrappers.un_complete_order(base_request)
    # end region
    # region Check value
    eq_wrappers.verify_order_value(base_request, case_id, "DoneForDay", "")
    eq_wrappers.verify_order_value(base_request, case_id, "PostTradeStatus", "")
    # endregion
    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")