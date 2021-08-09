import time
import datetime

from custom.verifier import Verifier
from quod_qa.wrapper import eq_wrappers
from quod_qa.wrapper.fix_verifier import FixVerifier
from rule_management import RuleManager
from stubs import Stubs
from custom.basic_custom_actions import create_event
from win_gui_modules.utils import set_session_id, get_base_request
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute(report_id, session_id):
    case_name = "QAP-3491"
    case_id = create_event(case_name, report_id)
    # region Declarations
    qty = "900"
    price = "50"
    client = "MOClient"
    account = "MOClient_SA1"
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    base_request = get_base_request(session_id, case_id)
    # endregion
    # region Open FE
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # endregion
    # region Create CO
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(eq_wrappers.get_buy_connectivity(),
                                                                             client + '_PARIS', "XPAR", float(price))
        nos_rule2 = rule_manager.add_NewOrdSingleExecutionReportTrade(eq_wrappers.get_buy_connectivity(),
                                                                      client + '_PARIS', 'XPAR',
                                                                      float(price), int(qty), 1)
        fix_message = eq_wrappers.create_order_via_fix(case_id, 1, 1, client, 2, qty, 0, price)
        response = fix_message.pop('response')
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        time.sleep(1)
        rule_manager.remove_rule(nos_rule)
        rule_manager.remove_rule(nos_rule2)
    # endregion
    # region Book
    eq_wrappers.book_order(base_request, client, price, remove_fees=True, remove_commission=True)
    # endregion
    # region Verify
    eq_wrappers.verify_block_value(base_request, case_id, "Status", "ApprovalPending")
    eq_wrappers.verify_block_value(base_request, case_id, "Match Status", "Unmatched")

    # endregion
    # region Amend Book
    bool_reply = eq_wrappers.amend_block(base_request, comm_basis="Absolute", comm_rate="-1", fees_basis="Absolute",
                                         fees_rate="-1",
                                         fee_type="Tax")
    # endregion
    # region Verify
    verifier = Verifier(case_id)
    verifier.set_event_name("Checking realtime parameters")
    verifier.compare_values("totalComm", "-1", bool_reply["book.totalComm"])
    verifier.compare_values("totalFees", "-1", bool_reply["book.totalFees"])
    verifier.verify()
    # endregion
    # region Approve
    eq_wrappers.approve_block(base_request)
    # endregion
    # region Verify
    eq_wrappers.verify_block_value(base_request, case_id, "Status", "Accepted")
    eq_wrappers.verify_block_value(base_request, case_id, "Match Status", "Matched")
    # endregion
    # region Allocate
    arr_allocation_param = [{"Security Account": account, "Alloc Qty": qty}]
    eq_wrappers.allocate_order(base_request, arr_allocation_param)
    # endregion
    # region Verify
    eq_wrappers.verify_block_value(base_request, case_id, "Summary Status", "MatchedAgreed")
    eq_wrappers.verify_allocate_value(base_request, case_id, "Total Fees", "-1")
    eq_wrappers.verify_allocate_value(base_request, case_id, "Client Comm", "-1")
    # endregion
