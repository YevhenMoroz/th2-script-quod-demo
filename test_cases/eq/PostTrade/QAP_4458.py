import test_framework.old_wrappers.eq_fix_wrappers
from test_framework.old_wrappers import eq_wrappers
from stubs import Stubs
from custom.basic_custom_actions import create_event
from test_framework.old_wrappers.eq_wrappers import open_fe
from win_gui_modules.utils import set_session_id, get_base_request
import logging
import time
from rule_management import RuleManager

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute(report_id):
    case_name = "QAP-4458"
    case_id = create_event(case_name, report_id)
    # region Declarations
    qty = "800"
    price = "3"
    client = "MOClient"
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    session_id = set_session_id()
    base_request = get_base_request(session_id, case_id)
    # endregion
    # region Open FE
    open_fe(session_id, report_id, case_id, work_dir, username)
    # # endregion
    # # region Create CO
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(
            test_framework.old_wrappers.eq_fix_wrappers.get_buy_connectivity(),
            client + '_PARIS', "XPAR", float(price))
        nos_rule2 = rule_manager.add_NewOrdSingleExecutionReportTrade(
            test_framework.old_wrappers.eq_fix_wrappers.get_buy_connectivity(),
            client + '_PARIS', 'XPAR', float(price),
            int(qty), 1)
        fix_message = test_framework.old_wrappers.eq_fix_wrappers.create_order_via_fix(case_id, 2, 1, client, 2, qty, 0, price)
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        time.sleep(1)
        rule_manager.remove_rule(nos_rule)
        rule_manager.remove_rule(nos_rule2)

    # endregion
    # # region check order at order book
    eq_wrappers.verify_order_value(base_request, case_id, 'ExecSts', 'Filled', False)
    eq_wrappers.verify_order_value(base_request, case_id, 'PostTradeStatus', 'ReadyToBook', False)
    # endregion

    # region book
    eq_wrappers.book_order(base_request, client, price)
    # endregion

    eq_wrappers.verify_order_value(base_request, case_id, 'PostTradeStatus', 'Booked', False)
    eq_wrappers.verify_block_value(base_request, case_id, 'Status', 'ApprovalPending')
    eq_wrappers.verify_block_value(base_request, case_id, 'Match Status', 'Unmatched')

    # region approve block
    eq_wrappers.approve_block(base_request)
    # endregion

    eq_wrappers.verify_block_value(base_request, case_id, 'Status', 'Accepted')
    eq_wrappers.verify_block_value(base_request, case_id, 'Match Status', 'Matched')

    # region amend the block without any changes
    eq_wrappers.amend_block(base_request)
    # endregion

    eq_wrappers.verify_block_value(base_request, case_id, 'Qty', '800')
    eq_wrappers.verify_block_value(base_request, case_id, 'AvgPx', '3')
