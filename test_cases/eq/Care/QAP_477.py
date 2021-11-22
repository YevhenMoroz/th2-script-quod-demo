import logging
import time

import test_cases.wrapper.eq_fix_wrappers
from test_cases.wrapper import eq_wrappers
from custom.basic_custom_actions import create_event, timestamps
from rule_management import RuleManager
from stubs import Stubs
from win_gui_modules.order_book_wrappers import OrdersDetails, ExtractionDetail, ExtractionAction, OrderInfo
from win_gui_modules.utils import set_session_id, get_base_request, close_fe, call
from win_gui_modules.wrappers import set_base, verification, verify_ent

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id,session_id):
    case_name = "QAP-477"
    seconds, nanos = timestamps()
    case_id = create_event(case_name, report_id)
    # region Declarations
    act = Stubs.win_act_order_book
    common_act = Stubs.win_act
    qty = "900"
    price = "20"
    client = "CLIENT_FIX_CARE"
    lookup = "VETO"
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    base_request = get_base_request(session_id, case_id)
    # endregion
    # region Open FE
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # endregion
    # region create CO
    fix_message = test_cases.wrapper.eq_fix_wrappers.create_order_via_fix(case_id, 3, 1, client, 2, qty, 0, price)
    eq_wrappers.accept_order(lookup,qty,price)
    # endregions

    # region Check values in OrderBook
    eq_wrappers.verify_order_value(base_request,case_id,"Sts","Open")
    # endregion
    # region DirectLOC split
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(
            test_cases.wrapper.eq_fix_wrappers.get_buy_connectivity(),
            client + '_PARIS', "XPAR", float(price))
        eq_wrappers.direct_loc_order('50', 'Route via FIXBUYTH2 - component used by TH2 simulator and autotests')
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        time.sleep(1)
        rule_manager.remove_rule(nos_rule)
    # endregion
    # check Child Order status
    eq_wrappers.verify_order_value(base_request, case_id, 'Qty', str(int(int(qty)/2)), True)
    eq_wrappers.verify_order_value(base_request, case_id, 'ExecPcy', 'DMA', True)
    # endregion
