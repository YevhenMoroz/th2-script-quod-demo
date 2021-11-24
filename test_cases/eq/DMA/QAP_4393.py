import logging
from datetime import datetime, date, timedelta

import test_framework.old_wrappers.eq_fix_wrappers

from custom.basic_custom_actions import create_event, timestamps

from rule_management import RuleManager
from test_cases.wrapper import eq_wrappers
from stubs import Stubs
from win_gui_modules.utils import get_base_request
from win_gui_modules.wrappers import set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


# need to modify
def execute(report_id, session_id):
    case_name = "QAP-4393"
    seconds, nanos = timestamps()  # Store case start time
    # region Declarations
    act = Stubs.win_act_order_book
    common_act = Stubs.win_act
    qty = "800"
    price = 30
    client = 'CLIENT4'
    expireDate = date.today() + timedelta(2)
    time = datetime.utcnow().isoformat()
    # endregion

    # region Open FE
    case_id = create_event(case_name, report_id)
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # endregion

    # region Create order via FIX
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(
            test_framework.old_wrappers.eq_fix_wrappers.get_buy_connectivity(),
            client + "_PARIS", 'XPAR', float(price))
        fix_message = test_framework.old_wrappers.eq_fix_wrappers.create_order_via_fix(case_id, 2, 1, client, 2, qty, 0, price, )
    finally:
        rule_manager.remove_rule(nos_rule)
    # endregion
    eq_wrappers.verify_order_value(base_request, case_id, 'Symbol', 'VETO', False)
