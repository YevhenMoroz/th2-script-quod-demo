import logging
import time

from custom.basic_custom_actions import create_event
from test_cases.wrapper import eq_wrappers
from rule_management import RuleManager
from stubs import Stubs
from win_gui_modules.utils import get_base_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute(report_id, session_id):
    case_name = "QAP-4991"
    # region Declarations
    qty = "100"
    price = "11"
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
    fix_message = eq_wrappers.create_order_via_fix(case_id, 3, 1, client, 2, qty, 0, price)
    eq_wrappers.accept_order('VETO', qty, price)
    # order_id = eq_wrappers.get_order_id(base_request)
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(eq_wrappers.get_buy_connectivity(),
                                                                             client + "_PARIS", 'XPAR', float(price))
        trade_rule = rule_manager.add_NewOrdSingleExecutionReportTrade(eq_wrappers.get_buy_connectivity(),
                                                                       client + "_PARIS", 'XPAR', float(price),
                                                                       traded_qty=int(qty), delay=65000)
        eq_wrappers.split_order(base_request, qty, 'Limit', price)
        # order_id_child = eq_wrappers.get_2nd_lvl_detail(base_request, 'Order ID')

        # endregion
        # region check values of order
        eq_wrappers.suspend_order(base_request, False)
        eq_wrappers.verify_order_value(base_request, case_id, 'Sts', 'Open', True)
        eq_wrappers.verify_order_value(base_request, case_id, 'Suspended', 'Yes', False)
        # endregion
        eq_wrappers.verify_order_value(base_request, case_id, 'ExecSts', 'Filled', True)
    finally:
        rule_manager.remove_rule(nos_rule)
        rule_manager.remove_rule(trade_rule)
