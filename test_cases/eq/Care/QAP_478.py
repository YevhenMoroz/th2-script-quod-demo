import logging
import time
from datetime import datetime
import test_framework.old_wrappers.eq_fix_wrappers
from custom.basic_custom_actions import create_event, timestamps
from rule_management import RuleManager
from stubs import Stubs
from test_framework.old_wrappers import eq_wrappers
from test_framework.win_gui_wrappers.base_main_window import open_fe
from win_gui_modules.utils import get_base_request
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-478"
    seconds, nanos = timestamps()
    case_id = create_event(case_name, report_id)
    # region Declarations
    qty = "900"
    price = "10"
    client = "CLIENT_FIX_CARE"
    lookup = "VETO"
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    base_request = get_base_request(session_id, case_id)
    # endregion
    # region Open FE
    open_fe(session_id, report_id, case_id, work_dir, username)
    # endregion
    # region create CO
    test_framework.old_wrappers.eq_fix_wrappers.create_order_via_fix(case_id, 3, 1, client, 1, qty, 0)
    # endregions
    # region AcceptOrder
    eq_wrappers.accept_order(lookup, qty, "")
    # endregion
    # region Check values in OrderBook
    eq_wrappers.verify_order_value(base_request, case_id, "Sts", "Open")
    # endregion
    # region DirectMOC split
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingle_Market(eq_fix_wrappers.get_buy_connectivity(),
            client + '_PARIS', "XPAR", False, 0, 0)
        eq_wrappers.direct_moc_order('50', 'Route via FIXBUYTH2 - component used by TH2 simulator and autotests')
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        time.sleep(2)
        rule_manager.remove_rule(nos_rule)
    # endregion
    # region Check sub Order status
    eq_wrappers.verify_order_value(base_request, case_id, 'Qty', str(int(int(qty) / 2)), True)
    eq_wrappers.verify_order_value(base_request, case_id, 'ExecPcy', 'DMA', True)
    # endregion
    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")