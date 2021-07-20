import logging
import time

from custom.basic_custom_actions import create_event, timestamps
from quod_qa.wrapper import eq_wrappers
from quod_qa.wrapper.fix_verifier import FixVerifier
from rule_management import RuleManager
from stubs import Stubs
from win_gui_modules.utils import set_session_id, get_base_request
from win_gui_modules.wrappers import set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-3910"

    # region Declarations
    qty = "900"
    price = "20"
    client = "CLIENT_FIX_CARE"
    lookup = "VETO"
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
    '''
    eq_wrappers.create_order_via_fix(case_id, 3, 2, client, 1, int(qty), 0)
    eq_wrappers.accept_order(lookup, qty, price)
    co_order = eq_wrappers.get_order_id(base_request)
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(eq_wrappers.get_buy_connectivity(),
                                                                             client + '_PARIS', "XPAR", float(price))
        nos_rule2 = rule_manager.add_NewOrdSingleExecutionReportTrade(eq_wrappers.get_buy_connectivity(),
                                                                      client + '_PARIS', 'XPAR',
                                                                      float(price), int(qty), 1)
        eq_wrappers.create_order_via_fix(case_id, 1, 1, client, 2, qty, 0, price)
        dma_order = eq_wrappers.get_order_id(base_request)
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        time.sleep(1)
        rule_manager.remove_rule(nos_rule)
        rule_manager.remove_rule(nos_rule2)
    '''
    # eq_wrappers.manual_match(base_request,str(int(int(qty)/2)))
    eq_wrappers.is_menu_item_present(base_request, "Splitvc", 1, "Spliteww", {"Order ID": "CO1210715134510139001"})
