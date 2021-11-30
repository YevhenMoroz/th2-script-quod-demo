import logging
import time

import test_framework.old_wrappers.eq_fix_wrappers
from custom.basic_custom_actions import create_event
from custom.verifier import Verifier
from rule_management import RuleManager
from stubs import Stubs
from test_framework.old_wrappers import eq_wrappers
from test_framework.old_wrappers.eq_wrappers import open_fe
from win_gui_modules.utils import get_base_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute(report_id, session_id):
    case_name = "QAP-2850"
    case_id = create_event(case_name, report_id)
    # region Declarations
    qty = "800"
    price = "3"
    client = "SBK"

    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
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
            client +'_PARIS', "XPAR", float(price))
        nos_rule2 = rule_manager.add_NewOrdSingleExecutionReportTrade(
            test_framework.old_wrappers.eq_fix_wrappers.get_buy_connectivity(),
            client +'_PARIS', 'XPAR', float(price),
            800, 0)
        time.sleep(1)
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        fix_message = test_framework.old_wrappers.eq_fix_wrappers.create_order_via_fix(case_id, 2, 1, client, 2, qty, 1, price)
        response = fix_message.pop('response')
        rule_manager.remove_rule(nos_rule)
        rule_manager.remove_rule(nos_rule2)
    # endregion
    #
    # region verify order
    eq_wrappers.verify_order_value(base_request, case_id, 'ExecSts', 'Filled', False)
    eq_wrappers.verify_order_value(base_request, case_id, 'PostTradeStatus', 'ReadyToBook', False)
    # # endregion
    # # region Book
    response = eq_wrappers.check_error_in_book(base_request)
    verifier = Verifier(case_id)
    verifier.set_event_name("Check value")
    verifier.compare_values('Check value', "Error - [QUOD-11699] Invalid AccountGroupID: SBK", response['errorMessage'])
    verifier.verify()
