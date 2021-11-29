import logging
import time
from copy import deepcopy
from datetime import datetime

import test_framework.old_wrappers.eq_fix_wrappers
from test_cases.wrapper import eq_wrappers
from win_gui_modules.order_book_wrappers import OrdersDetails
from custom.basic_custom_actions import create_event, timestamps

from test_framework.old_wrappers.fix_manager import FixManager
from test_framework.old_wrappers.fix_message import FixMessage
from rule_management import RuleManager
from stubs import Stubs
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction, OrderInfo
from win_gui_modules.utils import set_session_id, get_base_request, prepare_fe, call, get_opened_fe
from win_gui_modules.wrappers import set_base, verification, verify_ent, accept_order_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-1021"
    seconds, nanos = timestamps()  # Store case start time
    # region Declarations
    qty = "900"
    qty2 = "400"
    price = "20"
    price2 = "50"
    client = "CLIENT_FIX_CARE"
    lookup = "XPAR"
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
    # region Create CO
    fix_message = test_framework.old_wrappers.eq_fix_wrappers.create_order_via_fix(case_id, 3, 1, client, 2, qty, 0, price)
    # endregion
    # region Check values in OrderBook
    eq_wrappers.verify_order_value(base_request, case_id, "Sts", "Sent")
    eq_wrappers.verify_order_value(base_request, case_id, "Qty", qty)
    eq_wrappers.verify_order_value(base_request, case_id, "Limit Price", price)

    # endregion
    # region Accept CO
    eq_wrappers.accept_order(lookup, qty, price)
    # endregion
    # region Check values in OrderBook after Accept
    eq_wrappers.verify_order_value(base_request, case_id, "Sts", "Open")
    # endregion
    # region Amend order
    request = fix_message.pop('response')
    fix_message1 = FixMessage(fix_message)
    param_list = {'OrderQty': qty2, 'Price': price2}
    test_framework.old_wrappers.eq_fix_wrappers.amend_order_via_fix(case_id, fix_message1, param_list, client + "_PARIS")
    eq_wrappers.accept_modify(lookup, price2, qty2)
    # endregion
    # region Cancel order
    rule_manager = RuleManager()
    cl_order_id = request.response_messages_list[0].fields['ClOrdID'].simple_value
    try:
        rule = rule_manager.add_OrderCancelRequest(test_framework.old_wrappers.eq_fix_wrappers.get_sell_connectivity(), client + "_PARIS",
                                                   "XPAR", True)
        test_framework.old_wrappers.eq_fix_wrappers.cancel_order_via_fix(case_id, cl_order_id, cl_order_id, client, 2)
    finally:
        time.sleep(1)
        rule_manager.remove_rule(rule)
    eq_wrappers.accept_cancel(lookup, qty, price)
    # endregion
    # region Check values after Cancel
    eq_wrappers.verify_order_value(base_request, case_id, "Sts", "Cancelled")
    eq_wrappers.verify_order_value(base_request, case_id, "Qty", qty2)
    eq_wrappers.verify_order_value(base_request, case_id, "Limit Price", price2)
    # endregion
