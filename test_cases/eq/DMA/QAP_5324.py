import logging
import time

from custom.basic_custom_actions import create_event
from test_framework.old_wrappers import eq_wrappers, eq_fix_wrappers
from rule_management import RuleManager
from stubs import Stubs
from test_framework.old_wrappers.eq_wrappers import open_fe
from win_gui_modules.utils import get_base_request
from win_gui_modules.wrappers import set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-5324"
    qty = "200"
    client = "CLIENT_VSKULINEC_PARIS"
    price = 400
    side = 1
    tif = 0
    case_id = create_event(case_name, report_id)
    set_base(session_id, case_id)
    buy_connectivity = eq_fix_wrappers.get_buy_connectivity()

    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(buy_connectivity, client, "XPAR", price)
        fix_message = eq_fix_wrappers.create_order_via_fix(case_id, 1, side, client, 2, qty, tif, price=price)
        fix_message.pop('response')
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        time.sleep(1)
        rule_manager.remove_rule(nos_rule)

    base_request = get_base_request(session_id, case_id)
    open_fe(case_id, report_id, session_id)
    eq_wrappers.verify_order_value(base_request, case_id, "NIN", client)
    eq_wrappers.verify_order_value(base_request, case_id, "Sts", "Open")


def open_fe(case_id, report_id, session_id):
    work_dir = Stubs.custom_config['qf_trading_fe_folder_1']
    username = Stubs.custom_config['qf_trading_fe_user_1']
    password = Stubs.custom_config['qf_trading_fe_password_1']
    open_fe(session_id, report_id, case_id, work_dir, username)
