from custom.verifier import Verifier
from quod_qa.wrapper import eq_wrappers, eq_fix_wrappers
from quod_qa.wrapper.fix_verifier import FixVerifier
from stubs import Stubs
from custom.basic_custom_actions import create_event
from win_gui_modules.utils import set_session_id, get_base_request
import logging
from rule_management import RuleManager

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute(report_id):
    case_name = "QAP-3304"
    case_id = create_event(case_name, report_id)
    # region Declarations
    qty = "800"
    price = "40"
    client = "CLIENT_VSKULINEC"

    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    session_id = set_session_id()
    base_request = get_base_request(session_id, case_id)
    # endregion
    # region Open FE
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # endregion
    # region Create CO
    fix_message = eq_fix_wrappers.create_order_via_fix(case_id, 3, 1, client, 2, qty, 1, price)
    response = fix_message.pop('response')
    # endregion
    eq_wrappers.accept_order("VETO", qty, price)
    eq_wrappers.manual_execution(base_request, qty, price)
    eq_wrappers.complete_order(base_request)
    # region Book
    eq_wrappers.book_order(base_request, client, price)
    # region verify
    eq_wrappers.verify_order_value(base_request, case_id, 'PostTradeStatus', 'Booked')
    eq_wrappers.verify_block_value(base_request, case_id, 'Status', 'Approval Pending')
    eq_wrappers.verify_block_value(base_request, case_id, 'Match Status', 'Unmatched')
    eq_wrappers.verify_order_value(base_request, case_id, 'Summary Status', '')

    eq_wrappers.unbook_order(base_request)
    eq_wrappers.verify_block_value(base_request, case_id, 'PostTradeStatus', 'ReadyToBook')
    eq_wrappers.verify_block_value(base_request, case_id, 'Status', 'Canceled')
    eq_wrappers.verify_block_value(base_request, case_id, 'Match Status', 'Unmatched')
    eq_wrappers.verify_order_value(base_request, case_id, 'Summary Status', '')
