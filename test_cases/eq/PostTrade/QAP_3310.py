import test_framework.old_wrappers.eq_fix_wrappers
from custom.verifier import Verifier
from test_framework.old_wrappers import eq_wrappers
from rule_management import RuleManager
from stubs import Stubs
from custom.basic_custom_actions import create_event
from test_framework.old_wrappers.eq_wrappers import open_fe
from win_gui_modules.utils import get_base_request
import logging
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute(report_id, session_id):
    case_name = "QAP-3310"
    case_id = create_event(case_name, report_id)
    # region Declarations
    qty = "900"
    price = "40"
    client = "MOClient"
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    base_request = get_base_request(session_id, case_id)
    # endregion
    # region Open FE
    open_fe(session_id, report_id, case_id, work_dir, username)
    # # endregion
    # region Create CO
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(
            test_framework.old_wrappers.eq_fix_wrappers.get_buy_connectivity(),
            client + '_PARIS', "XPAR", int(price))
        nos_rule2 = rule_manager.add_NewOrdSingleExecutionReportTrade(
            test_framework.old_wrappers.eq_fix_wrappers.get_buy_connectivity(),
            client + '_PARIS', 'XPAR',
            int(price), int(qty), 1)
        fix_message = test_framework.old_wrappers.eq_fix_wrappers.create_order_via_fix(case_id, 1, 1, client, 2, qty, 0, price)
        response = fix_message.pop('response')
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        time.sleep(1)
        rule_manager.remove_rule(nos_rule)
        rule_manager.remove_rule(nos_rule2)
    # endregion
    # region verify order
    eq_wrappers.verify_order_value(base_request, case_id, 'ExecSts', 'Filled', False)
    eq_wrappers.verify_order_value(base_request, case_id, 'PostTradeStatus', 'ReadyToBook', False)
    #  endregion
    #  region Book
    book_ticket = eq_wrappers.book_order(base_request, client, price, settlement_type='Regular', fees_type="ExchFees",
                                         fees_basis="Absolute", fees_rate="100")
    # endregion
    # region Verify
    verifier = Verifier(case_id)
    verifier.set_event_name("Checking realtime parameters")
    verifier.compare_values("Total Fees", "100", book_ticket["book.totalFees"])
    verifier.verify()
    eq_wrappers.verify_block_value(base_request, case_id, "Total Fees", "100")
    # endregion

    # region Amend block
    book_ticket = eq_wrappers.amend_block(base_request, remove_fees=True)
    # endregion
    # region Verify
    verifier = Verifier(case_id)
    verifier.set_event_name("Checking realtime parameters")
    verifier.compare_values("Total Fees", "0", book_ticket["book.totalFees"])
    verifier.verify()
    eq_wrappers.verify_block_value(base_request, case_id, "Total Fees", "0")
    # endregion
