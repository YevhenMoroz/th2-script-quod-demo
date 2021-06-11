import time

from quod_qa.wrapper import eq_wrappers
from quod_qa.wrapper.fix_verifier import FixVerifier
from rule_management import RuleManager
from stubs import Stubs
from custom.basic_custom_actions import create_event
from win_gui_modules.utils import set_session_id, get_base_request
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute(report_id):
    case_name = "QAP-3337"
    case_id = create_event(case_name, report_id)
    # region Declarations
    qty = "900"
    price = "40"
    client = "CLIENT_YMOROZ"
    account = "YM_client_SA1"
    account2 = "YM_client_SA2"
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    session_id = set_session_id()
    base_request = get_base_request(session_id, case_id)
    recipient = "ymoroz (HeadOfSaleDealer)"
    # endregion

    # region Open FE
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # endregion

    # region Create CO
    # endregion
    eq_wrappers.manual_execution(base_request,qty,price)
    eq_wrappers.complete_order(base_request)
    # region Book
    eq_wrappers.book_order(base_request, client, price,comm_rate="10",comm_basis="Absolute")
    # endregion
    '''
    # region Verify
    eq_wrappers.verify_block_value(base_request, case_id, "Status", "ApprovalPending")
    eq_wrappers.verify_block_value(base_request, case_id, "Match Status", "Unmatched")
    # endregion
    # region Approve
    eq_wrappers.approve_block(base_request)
    # endregion
    # region Verify
    eq_wrappers.verify_block_value(base_request, case_id, "Status", "Accepted")
    eq_wrappers.verify_block_value(base_request, case_id, "Match Status", "Matched")
    # endregion
    # region Allocate
    arr_allocation_param = [{"Security Account": account, "Alloc Qty": str(450)},
                            {"Security Account": account2, "Alloc Qty": str(450)}]
    eq_wrappers.allocate_order(base_request, arr_allocation_param)
    # endregion

    # region Verify
    eq_wrappers.verify_allocate_value(base_request, case_id, account, "Status", "Matched")
    eq_wrappers.verify_allocate_value(base_request, case_id, account, "Match Status", "Affirmed")
    eq_wrappers.verify_allocate_value(base_request, case_id, account2, "Status", "Matched")
    eq_wrappers.verify_allocate_value(base_request, case_id, account2, "Match Status", "Affirmed")
    # endregion
    '''