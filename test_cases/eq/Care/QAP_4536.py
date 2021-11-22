import logging
import time

import test_cases.wrapper.eq_fix_wrappers
from custom.basic_custom_actions import create_event
from test_cases.wrapper import eq_wrappers, eq_fix_wrappers
from rule_management import RuleManager
from stubs import Stubs
from win_gui_modules.utils import get_base_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-4536"
    # region Declarations
    qty = "900"
    price = "40"
    client = "MOClient"
    lookup = 'VETO'
    case_id = create_event(case_name, report_id)
    base_request = get_base_request(session_id, case_id)
    buy_connectivity = eq_fix_wrappers.get_buy_connectivity()
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    # endregion
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(buy_connectivity, client + "_PARIS",
                                                                             "XPAR", int(price))
        test_cases.wrapper.eq_fix_wrappers.create_order_via_fix(case_id, 3, 1, client, 2, qty, 0, price)
        eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
        eq_wrappers.accept_order(lookup, qty, price)
        eq_wrappers.split_order(base_request, qty, "Limit", price)
        cancel_rule = rule_manager.add_OrderCancelRequest(buy_connectivity, client + "_PARIS", "XPAR", True)
        eq_wrappers.cancel_child_orders(base_request)
        eq_wrappers.manual_execution(base_request, qty, price)
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        time.sleep(2)
        rule_manager.remove_rule(nos_rule)
        rule_manager.remove_rule(cancel_rule)

    eq_wrappers.complete_order(base_request)
    eq_wrappers.verify_order_value(base_request, case_id, "PostTradeStatus", "ReadyToBook")
    eq_wrappers.verify_order_value(base_request, case_id, "DoneForDay", "Yes")
