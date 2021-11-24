import logging

import test_framework.old_wrappers.eq_fix_wrappers
from test_cases.wrapper import eq_wrappers
from custom.basic_custom_actions import create_event, timestamps
from stubs import Stubs
from win_gui_modules.utils import set_session_id, get_base_request
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id):
    case_name = "QAP-3991"
    case_id = create_event(case_name, report_id)
    # region Declarations
    qty = "900"
    price = "40"
    dummy_client = "DUMMY_CLIENT"
    client = "CLIENTYMOROZ"
    account = "YM_client_SA1"
    lookup = "VETO"
    route = "Route via FIXBUYTH2"

    act = Stubs.win_act_order_book
    common_act = Stubs.win_act
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    session_id = set_session_id()
    base_request = get_base_request(session_id, case_id)
    recipient = 'Desk of SalesDealers 1 (CL)'
    # endregion
    # region Open FE
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # endregion
    # region create DMA
    responce= test_framework.old_wrappers.eq_fix_wrappers.create_order_via_fix(case_id, 1, 1, dummy_client, 2, qty, 0, price)
    # endregion
    # region verify values
    eq_wrappers.verify_order_value(base_request, case_id, "Sts", "Held")
    eq_wrappers.verify_order_value(base_request, case_id, "Client ID", "DUMMY")
    # endregion verify values
    # region GroupModify
    eq_wrappers.group_modify(base_request,client,account,route,"Free notes")
    # endregion
    # region verify values
    eq_wrappers.verify_order_value(base_request, case_id, "Sts", "Open")
    eq_wrappers.verify_order_value(base_request, case_id, "Client ID", client)
    eq_wrappers.verify_order_value(base_request, case_id, "Account ID", account)
    eq_wrappers.verify_order_value(base_request, case_id, "Routes", "ESBUYTH2")
    # endregion verify values
