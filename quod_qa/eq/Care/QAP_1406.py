import logging

from custom.basic_custom_actions import create_event
from quod_qa.wrapper import eq_wrappers
from stubs import Stubs
from win_gui_modules.utils import get_base_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-1406"
    case_id = create_event(case_name, report_id)
    # region Declarations
    qty = "900"
    price = "40"
    dummy_client = "DUMMY_CLIENT"
    client = "CLIENT_FIX_CARE"
    route = "Route via FIXBUYTH2"
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    base_request = get_base_request(session_id, case_id)
    # endregion
    # region Open FE
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # endregion
    # region create CO
    responce=eq_wrappers.create_order_via_fix(case_id, 2, 1, dummy_client, 2, qty, 0, price)
    # endregion
    # region verify values
    eq_wrappers.verify_order_value(base_request, case_id, "Sts", "Held")
    eq_wrappers.verify_order_value(base_request, case_id, "Client ID", "DUMMY")
    # endregion verify values
    # region GroupModify
    eq_wrappers.group_modify(base_request,client,routes=route)
    # endregion
    # region verify values
    eq_wrappers.verify_order_value(base_request, case_id, "Sts", "Open")
    eq_wrappers.verify_order_value(base_request, case_id, "Client ID", client)
    eq_wrappers.verify_order_value(base_request, case_id, "Routes", route)
    # endregion verify values
