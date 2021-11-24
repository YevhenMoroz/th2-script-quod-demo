import logging

import test_framework.old_wrappers.eq_fix_wrappers
from custom.basic_custom_actions import create_event
from custom.verifier import Verifier
from test_cases.wrapper import eq_wrappers
from stubs import Stubs
from win_gui_modules.utils import get_base_request
from win_gui_modules.wrappers import set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-3503"
    # region Declarations
    qty = "900"
    price = "10"
    client = "CLIENT_COUNTERPART"
    case_id = create_event(case_name, report_id)
    set_base(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    base_request = get_base_request(session_id, case_id)
    # endregion
    # region Open FE
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # # endregion
    # region Create order via FIX
    test_framework.old_wrappers.eq_fix_wrappers.create_order_via_fix(case_id, 3, 1, client, 2, qty, 0, price)
    eq_wrappers.accept_order('VETO', qty, price)
    # endregion
    # region ManualExec
    eq_wrappers.manual_execution(base_request,qty,price,"ExecutingFirm", "ContraFirm")
    # endregion
    # region Verify
    verifier = Verifier(case_id)
    verifier.set_event_name("Checking Counterparts")
    verifier.compare_values("Contra Firm", "ContraFirm", eq_wrappers.get_2nd_lvl_order_detail(base_request, "Contra Firm"))
    verifier.compare_values("Executing Firm", "ExecutingFirm", eq_wrappers.get_2nd_lvl_order_detail(base_request,
                                                                                              "Executing Firm"))
    verifier.verify()
    # endregion
