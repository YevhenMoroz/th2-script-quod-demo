import logging
from time import sleep
from custom.basic_custom_actions import create_event
from test_framework.old_wrappers import eq_wrappers
from rule_management import RuleManager
from stubs import Stubs
from test_framework.old_wrappers.eq_wrappers import open_fe
from win_gui_modules.utils import get_base_request
from win_gui_modules.wrappers import set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


# need to modify
def execute(report_id, session_id):
    case_name = "QAP-2548"
    # region Declarations
    act = Stubs.win_act_order_book
    common_act = Stubs.win_act
    qty = "800"
    price = '30'
    client = 'CLIENT4'
    lookup = 'VETO'
    account = 'CLIENT4_SA1'
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

    # region Create order via FIX
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(eq_wrappers.get_buy_connectivity(),
                                                                             client + "_PARIS", 'XPAR', float(price))
        eq_wrappers.create_order(base_request, qty, client, lookup, 'Limit', 'Day', False, None, price,
                                 account=account)
    finally:
        sleep(3)
        rule_manager.remove_rule(nos_rule)
    # endregion

    # region verify
    eq_wrappers.verify_order_value(base_request, case_id, 'Capacity', 'Agency', False)
    # endregion

    # region amend order
    try:
        amend_rule = rule_manager.add_OrderCancelReplaceRequest(eq_wrappers.get_buy_connectivity(), client + "_PARIS",
                                                                'XPAR', True)
        eq_wrappers.amend_order(base_request, qty='800', price=None, account=None, capacity='Principal')
    finally:
        sleep(3)
        rule_manager.remove_rule(amend_rule)
    # endregion
    eq_wrappers.verify_order_value(base_request, case_id, 'Capacity', 'Principal', False)
    eq_wrappers.verify_order_value(base_request, case_id, 'Client ID', client, False)
    eq_wrappers.verify_order_value(base_request, case_id, 'Account ID', account, False)
