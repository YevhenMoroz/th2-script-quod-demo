import logging
import os
from copy import deepcopy
from datetime import datetime

import pyautogui
from th2_grpc_act_gui_quod import order_ticket_service

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
    case_name = "QAP-1045"
    seconds, nanos = timestamps()  # Store case start time

    # region Declarations
    act = Stubs.win_act_order_book
    common_act = Stubs.win_act
    qty = "900"
    newQty = "100"
    price = "10"
    newPrice = "1"
    timeStart = datetime.utcnow().isoformat()
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
    # region Create order via FIX
    fix_message = eq_wrappers.create_order_via_fix(case_id, 3, 1, client, 2, qty, 0, price)
    fix_message.pop("response")
    # endregion

    # region Check values in OrderBook
    before_order_details_id = "before_order_details"
    order_details = OrdersDetails()
    order_details.set_default_params(base_request)
    order_details.set_extraction_id(before_order_details_id)
    order_status = ExtractionDetail("order_status", "Sts")
    order_price = ExtractionDetail("order_price", "Limit Price")
    order_qty = ExtractionDetail("order_qty", "Qty")
    order_id = ExtractionDetail("order_id", "Order ID")
    client_order_id = ExtractionDetail("client_order_id", "ClOrdID")
    order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[client_order_id,
                                                                                            order_status,
                                                                                            order_price,
                                                                                            order_qty,
                                                                                            order_id
                                                                                            ])
    order_details.add_single_order_info(OrderInfo.create(action=order_extraction_action))

    request = call(act.getOrdersDetails, order_details.request())
    call(common_act.verifyEntities, verification(before_order_details_id, "checking order",
                                                 [verify_ent("Order Status", order_status.name, "Sent"),
                                                  verify_ent("Qty", order_qty.name, qty),
                                                  verify_ent("LmtPrice", order_price.name, price)]))
    # endregion

    # region Accept CO
    call(common_act.acceptOrder, accept_order_request(lookup, qty, price))
    # endregion
    # region Send OrderCancelReplaceRequest with new price
    fix_message=FixMessage(fix_message)
    param={'Price': newPrice}
    eq_wrappers.amend_order_via_fix(case_id,fix_message,param,client+"_PARIS")
    eq_wrappers.accept_modify(lookup,qty,price)
    # endregion
    # region Send OrderCancelReplaceRequest with new qty
    param = {'OrderQty': newQty, 'Price': newPrice}
    eq_wrappers.amend_order_via_fix(case_id, fix_message, param, client + "_PARIS")
    eq_wrappers.accept_modify(lookup, qty, price)
    # endregion
    # region Cancel order
    cl_order_id=eq_wrappers.get_cl_order_id(base_request)
    eq_wrappers.cancel_order_via_fix(case_id,cl_order_id,cl_order_id,client,1)
    eq_wrappers.accept_cancel(lookup,qty,price)
    # endregion
    # region Check values in OrderBook after Cancel
    eq_wrappers.verify_order_value(base_request,case_id,"Sts","Cancelled")
    eq_wrappers.verify_order_value(base_request, case_id, "Qty", newQty)
    eq_wrappers.verify_order_value(base_request, case_id, "Limit Price", newPrice)
    # endregion

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
