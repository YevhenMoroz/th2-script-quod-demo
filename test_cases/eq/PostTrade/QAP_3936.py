import test_framework.old_wrappers.eq_fix_wrappers
from custom.verifier import Verifier
from test_cases.wrapper import eq_wrappers
from test_framework.old_wrappers.fix_verifier import FixVerifier
from stubs import Stubs
from custom.basic_custom_actions import create_event
from win_gui_modules.utils import get_base_request
import logging
import time
from rule_management import RuleManager

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute(report_id, session_id):
    case_name = "QAP-3936"
    case_id = create_event(case_name, report_id)
    # region Declarations
    qty = "800"
    price = "10.12345678"
    client = "CLIENT_PRECISION"
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    base_request = get_base_request(session_id, case_id)
    # endregion
    # region Open FE
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # endregion
    # region Create Care
    fix_message = test_framework.old_wrappers.eq_fix_wrappers.create_order_via_fix(case_id, 3, 1, client, 2, qty, 1, price)
    # endregion

    # region accept order
    eq_wrappers.accept_order('VETO', qty, price)
    # endregion

    # region Manual Execution
    eq_wrappers.manual_execution(base_request, qty, price)
    # endregion
    eq_wrappers.complete_order(base_request)
    eq_wrappers.verify_order_value(base_request, case_id, 'PostTradeStatus', 'ReadyToBook')
    eq_wrappers.verify_order_value(base_request, case_id, 'Limit Price', price)
    # region book order
    eq_wrappers.book_order(base_request, client, price)
    # endregion
    eq_wrappers.verify_block_value(base_request, case_id, 'AvgPx', '10.12345678')
