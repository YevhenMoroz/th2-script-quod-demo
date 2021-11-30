import logging
import time

import test_framework.old_wrappers.eq_fix_wrappers
from custom.basic_custom_actions import create_event
from custom.verifier import Verifier
from test_framework.old_wrappers import eq_wrappers
from rule_management import RuleManager
from stubs import Stubs
from test_framework.old_wrappers.eq_wrappers import open_fe
from win_gui_modules.utils import get_base_request
from win_gui_modules.wrappers import set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-3910"
    # region Declarations
    qty = "900"
    price = "20"
    client = "CLIENT_FIX_CARE"
    lookup = "VETO"
    # endregion

    # region Open FE
    case_id = create_event(case_name, report_id)
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    open_fe(session_id, report_id, case_id, work_dir, username)
    # endregion
    # region create & trade DMA
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(
            test_framework.old_wrappers.eq_fix_wrappers.get_buy_connectivity(),
            client + '_PARIS', "XPAR", float(price))
        nos_rule2 = rule_manager.add_NewOrdSingleExecutionReportTrade(
            test_framework.old_wrappers.eq_fix_wrappers.get_buy_connectivity(),
            client + '_PARIS', 'XPAR',
            float(price), int(qty), 1)
        test_framework.old_wrappers.eq_fix_wrappers.create_order_via_fix(case_id, 1, 1, client, 2, qty, 0, price)
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        time.sleep(1)
        rule_manager.remove_rule(nos_rule)
        rule_manager.remove_rule(nos_rule2)
    exec_id = eq_wrappers.get_2nd_lvl_order_detail(base_request, "ExecID")
    # endregion

    # region create CO
    test_framework.old_wrappers.eq_fix_wrappers.create_order_via_fix(case_id, 3, 1, client, 1, qty, 0)
    eq_wrappers.accept_order(lookup, qty, price)
    co_order = eq_wrappers.get_order_id(base_request)
    # endregion
    # region Manual Match
    eq_wrappers.manual_match(base_request, str(int(qty)/2), ["OrderId", co_order], ["ExecID", exec_id])
    # endregion
    # region Verify
    eq_wrappers.verify_order_value(base_request, case_id, "UnmatchedQty", str(int(int(qty)/2)))
    eq_wrappers.verify_order_value(base_request, case_id, "ExecSts", "PartiallyFilled")
    # endregion
    # region Manual Match
    eq_wrappers.manual_match(base_request, str(int(qty) / 2), ["OrderId", co_order], ["ExecID", exec_id])
    # endregion
    # region Verify
    eq_wrappers.verify_order_value(base_request, case_id, "UnmatchedQty", "0")
    eq_wrappers.verify_order_value(base_request, case_id, "ExecSts", "Filled")
    verifier = Verifier(case_id)
    verifier.set_event_name("Checking Fees")
    verifier.compare_values("ExecType", "Trade", eq_wrappers.get_2nd_lvl_order_detail(base_request, "ExecType"))
    verifier.verify()
    # endregion
