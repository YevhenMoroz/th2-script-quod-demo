import test_framework.old_wrappers.eq_fix_wrappers

from stubs import Stubs
from custom.basic_custom_actions import create_event
from test_framework.old_wrappers import eq_wrappers
from test_framework.win_gui_wrappers.base_main_window import open_fe
from win_gui_modules.utils import set_session_id, get_base_request
import logging
import time
from rule_management import RuleManager

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute(report_id, session_id):
    case_name = "QAP-4349"
    case_id = create_event(case_name, report_id)
    # region Declarations
    qty = "800"
    price = "3"
    client = "MOClient5"
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    base_request = get_base_request(session_id, case_id)
    # endregion
    # region Open FE
    open_fe(session_id, report_id, case_id, work_dir, username)
    # endregion
    # region Create DMA
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(
            test_framework.old_wrappers.eq_fix_wrappers.get_buy_connectivity(),
                                                                             'MOClient5_EUREX', "XEUR", float(price))
        nos_rule2 = rule_manager.add_NewOrdSingleExecutionReportTrade(
            test_framework.old_wrappers.eq_fix_wrappers.get_buy_connectivity(),
                                                                             'MOClient5_EUREX', "XEUR", float(price),
            int(qty), 1)
        fix_message = test_framework.old_wrappers.eq_fix_wrappers.create_order_via_fix(case_id, 2, 1, client, 2, qty, 1, price)
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        time.sleep(5)
        rule_manager.remove_rule(nos_rule)
        rule_manager.remove_rule(nos_rule2)
    # endregion

    # region book order
    eq_wrappers.book_order(base_request, client, price, remove_commission=True, remove_fees=True)
    eq_wrappers.verify_block_value(base_request, case_id, "Total Fees", '')
    eq_wrappers.verify_block_value(base_request, case_id, 'Client Comm', '')
