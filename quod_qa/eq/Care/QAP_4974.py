import logging
import time

import quod_qa.wrapper.eq_fix_wrappers
from custom.basic_custom_actions import create_event
from custom.verifier import Verifier
from quod_qa.wrapper import eq_wrappers
from rule_management import RuleManager
from stubs import Stubs
from win_gui_modules.utils import get_base_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def execute(report_id, session_id):
    case_name = "QAP-4974"
    case_id = create_event(case_name, report_id)
    # region Declarations
    qty = "900"
    price = "10"
    client = "CLIENT_YMOROZ"
    lookup = "VETO"
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    base_request = get_base_request(session_id, case_id)
    # endregion
    # region Open FE
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # endregion
    # region Create Order
    quod_qa.wrapper.eq_fix_wrappers.create_order_via_fix(case_id, 3, 1, client, 2, qty, 0, price)
    eq_wrappers.accept_order(lookup, qty, price)
    # endregion
    # region Split
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(
            quod_qa.wrapper.eq_fix_wrappers.get_buy_connectivity(),
            client + '_PARIS', "XPAR", float(price))
        eq_wrappers.split_order(base_request, str(int(qty) + 1), price)
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        time.sleep(1)
        rule_manager.remove_rule(nos_rule)

    # endregion
    # region Verify
    child_sts = eq_wrappers.get_2nd_lvl_order_detail(base_request, "Sts")
    child_qty = eq_wrappers.get_2nd_lvl_order_detail(base_request, "Qty")
    verifier = Verifier(case_id)
    verifier.set_event_name("Checking Child")
    verifier.compare_values("Sts", "Open", child_sts)
    verifier.compare_values("Qty", qty, child_qty)
    split_item = eq_wrappers.is_menu_item_present(base_request, "Split")
    verifier.compare_values("Split item", "false", split_item['isMenuItemPresent'])
    split_limit_item = eq_wrappers.is_menu_item_present(base_request, "Split Limit")
    verifier.compare_values("Split Limit item", "false", split_limit_item['isMenuItemPresent'])
    verifier.verify()
    # endregion
