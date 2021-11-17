import logging
import time

from custom.basic_custom_actions import create_event
from quod_qa.wrapper import eq_wrappers, eq_fix_wrappers
from rule_management import RuleManager
from stubs import Stubs
from win_gui_modules.utils import get_base_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute(report_id, session_id):
    case_name = "QAP-5593"
    # region Declarations
    qty = "40"
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
    fix_message = eq_fix_wrappers.create_order_via_fix(case_id, 3, 1, client, 2, qty, 0, price)
    response = fix_message.pop("response")
    eq_wrappers.accept_order('VETO', qty, price)
    # endregion
    # region Execute CO
    eq_wrappers.manual_execution(base_request,qty,price,contra_firm=" ")
    # endregion
    print(eq_wrappers.extract_error_order_ticket(base_request))