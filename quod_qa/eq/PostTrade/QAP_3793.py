import logging
import time

from custom.basic_custom_actions import create_event
from quod_qa.wrapper import eq_fix_wrappers, eq_wrappers
from rule_management import RuleManager
from stubs import Stubs
from win_gui_modules.utils import get_base_request
from win_gui_modules.wrappers import set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-3793"
    qty = "115"
    client = "MOClient"
    price = 10
    side = 1
    tif = 1
    case_id = create_event(case_name, report_id)
    set_base(session_id, case_id)
    buy_connectivity = eq_fix_wrappers.get_buy_connectivity()
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingle_Market(buy_connectivity, client + "_PARIS", "XPAR", True, int(qty),
                                                        price)
        fix_message = eq_fix_wrappers.create_order_via_fix(case_id, 1, side, client, 1, qty, tif)
        response = fix_message.pop('response')
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        time.sleep(1)
        rule_manager.remove_rule(nos_rule)

    order_id = response.response_messages_list[0].fields['OrderID'].simple_value
    test_string = "Test string"
    base_request = get_base_request(session_id, case_id)
    open_fe(case_id, report_id, session_id)
    eq_wrappers.verify_order_value(base_request, case_id, "PostTradeStatus", "ReadyToBook",
                                   order_filter_list=["Order ID", order_id])
    eq_wrappers.verify_order_value(base_request, case_id, "ExecSts", "Filled",
                                   order_filter_list=["Order ID", order_id])
    eq_wrappers.book_order(base_request, client, str(price), bo_notes=test_string)
    eq_wrappers.verify_order_value(base_request, case_id, "PostTradeStatus", "Booked",
                                   order_filter_list=["Order ID", order_id])
    verify_bo_fields_list(["BOC1", "BOC2", "BOC3", "BOC4", "BOC5"], base_request, case_id)
    eq_wrappers.verify_block_value(base_request, case_id, "Back Office Notes", test_string,)
    eq_wrappers.verify_block_value(base_request, case_id, "Status", "ApprovalPending")
    eq_wrappers.verify_block_value(base_request, case_id, "Match Status", "Unmatched")
    eq_wrappers.amend_block(base_request, misc_arr=["1", "2", "3", "4", "5"])
    verify_bo_fields_list(["1", "2", "3", "4", "5"], base_request, case_id)
    eq_wrappers.approve_block(base_request)
    eq_wrappers.verify_block_value(base_request, case_id, "Status", "Accepted")
    eq_wrappers.verify_block_value(base_request, case_id, "Match Status", "Matched")
    verify_bo_fields_list(["1", "2", "3", "4", "5"], base_request, case_id)
    eq_wrappers.verify_block_value(base_request, case_id, "Back Office Notes", test_string)
    eq_wrappers.amend_block(base_request, misc_arr=["11", "22", "33", "44", "55"])
    verify_bo_fields_list(["11", "22", "33", "44", "55"], base_request, case_id)
    eq_wrappers.allocate_order(base_request,
                               arr_allocation_param=[{"Security Account": "MOClient_SA1", "Alloc Qty": qty}])
    verify_allocation_fields_list(["AccBO1", "AccBO2", "AccBO3", "AccBO4", "AccBO5"], base_request, case_id)


def open_fe(case_id, report_id, session_id):
    work_dir = Stubs.custom_config['qf_trading_fe_folder_1']
    username = Stubs.custom_config['qf_trading_fe_user_1']
    password = Stubs.custom_config['qf_trading_fe_password_1']
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)


def verify_bo_fields_list(values, base_request, case_id):
    for i in range(5):
        eq_wrappers.verify_block_value(base_request, case_id, "Bo Field " + str(i + 1), values[i])


def verify_allocation_fields_list(values, base_request, case_id):
    for i in range(5):
        eq_wrappers.verify_allocate_value(base_request, case_id, "Alloc BO Field " + str(i + 1), values[i])
