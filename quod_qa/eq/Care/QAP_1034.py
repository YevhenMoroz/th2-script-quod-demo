import logging
import os
from copy import deepcopy
from datetime import datetime

from th2_grpc_act_gui_quod import order_ticket_service

import quod_qa.wrapper.eq_fix_wrappers
from quod_qa.wrapper import eq_wrappers
from quod_qa.wrapper.fix_verifier import FixVerifier
from win_gui_modules.order_book_wrappers import OrdersDetails, CancelOrderDetails

from custom.basic_custom_actions import create_event, timestamps
import time
from quod_qa.wrapper.fix_manager import FixManager
from quod_qa.wrapper.fix_message import FixMessage
from rule_management import RuleManager
from stubs import Stubs
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction, OrderInfo
from win_gui_modules.utils import set_session_id, get_base_request, prepare_fe, call, get_opened_fe
from win_gui_modules.wrappers import set_base, verification, verify_ent, accept_order_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-1034"
    seconds, nanos = timestamps()  # Store case start time

    # region Declarations
    act = Stubs.win_act_order_book
    common_act = Stubs.win_act
    qty = "900"
    newQty = "100"
    price = "10"
    newPrice = "1"
    time = datetime.utcnow().isoformat()
    lookup = "VETO"
    client = "CLIENT_FIX_CARE"
    # endregion
    # region Open FE
    case_id = create_event(case_name, report_id)
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']

    if not Stubs.frontend_is_open:
        prepare_fe(case_id, session_id, work_dir, username, password)
    else:
        get_opened_fe(case_id, session_id)
    # endregionA
    # region Create CO
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(
            quod_qa.wrapper.eq_fix_wrappers.get_buy_connectivity(),
            client + "_PARIS", "XPAR", 20)
        fix_message = quod_qa.wrapper.eq_fix_wrappers.create_order_via_fix(case_id, 3, 2, client, 2, qty, 0, price)
        fix_message.pop("response")
    except Exception:
        logger.error("Error execution", exc_info=True)
    finally:
        rule_manager.remove_rule(nos_rule)

    # endregion
    # region Accept CO
    eq_wrappers.accept_order(lookup, qty, price)
    # endregion
    # region Send OrderCancelReplaceRequest
    fix_message = FixMessage(fix_message)
    params = {'Price': newPrice, 'OrderQty': newQty}
    quod_qa.wrapper.eq_fix_wrappers.amend_order_via_fix(case_id, fix_message, params, client + "_PARIS")
    # endregion
    # region Accept CO
    eq_wrappers.accept_modify(lookup, qty, price)
    # endregion
    # region Check values in OrderBook
    eq_wrappers.verify_order_value(base_request, case_id, "Sts", "Open")
    eq_wrappers.verify_order_value(base_request, case_id, "Qty", newQty)
    eq_wrappers.verify_order_value(base_request, case_id, "Limit Price", newPrice)
    # endregion
    # region Cancelling order
    cl_order_id = eq_wrappers.get_cl_order_id(base_request)
    quod_qa.wrapper.eq_fix_wrappers.cancel_order_via_fix(case_id, cl_order_id, cl_order_id, client, 1)
    eq_wrappers.accept_cancel(lookup, qty, price)
    # endregion
    # region Check values after Cancel
    eq_wrappers.verify_order_value(base_request, case_id, "Sts", "Cancelled")
    # endregion

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
