import logging
import os
from datetime import datetime

import pyautogui
from th2_grpc_act_gui_quod import order_ticket_service

import quod_qa.wrapper.eq_fix_wrappers
from quod_qa.wrapper import eq_wrappers
from win_gui_modules.order_book_wrappers import OrdersDetails, ManualExecutingDetails, ModifyOrderDetails

from custom.basic_custom_actions import create_event, timestamps

from quod_qa.wrapper.fix_manager import FixManager
from quod_qa.wrapper.fix_message import FixMessage
from rule_management import RuleManager
from stubs import Stubs
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction, OrderInfo
from win_gui_modules.order_ticket import OrderTicketDetails
from win_gui_modules.utils import set_session_id, get_base_request, prepare_fe, call, get_opened_fe
from win_gui_modules.wrappers import set_base, verification, verify_ent, accept_order_request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-1039"
    seconds, nanos = timestamps()  # Store case start time
    # region Declarations
    act = Stubs.win_act_order_book
    common_act = Stubs.win_act
    qty = "900"
    qty2 = "901"
    price = "10"
    client = "CLIENT_FIX_CARE"
    lookup = "VETO"
    time = datetime.utcnow().isoformat()
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
    # endregion
    # region Create CO
    fix_message = quod_qa.wrapper.eq_fix_wrappers.create_order_via_fix(case_id, 3, 2, client, 2, qty, 0, price)
    fix_message.pop("response")
    # endregion
    # region Accept CO
    call(common_act.acceptOrder, accept_order_request(lookup, qty, price))
    # endregion
    # region Check values in OrderBook
    before_order_details_id = "order_details"
    order_details = OrdersDetails()
    order_details.set_default_params(base_request)
    order_details.set_extraction_id(before_order_details_id)
    order_status = ExtractionDetail("order_status", "Sts")
    order_qty = ExtractionDetail("order_qty", "Qty")
    order_pts = ExtractionDetail("order_pts", "PostTradeStatus")
    order_dfd = ExtractionDetail("order_dfd", "DoneForDay")
    order_es = ExtractionDetail("order_es", "ExecSts")
    order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[order_status,
                                                                                            order_qty,
                                                                                            order_pts,
                                                                                            order_dfd,
                                                                                            order_es,
                                                                                            ])
    order_details.add_single_order_info(OrderInfo.create(action=order_extraction_action))
    order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[order_status])
    order_details.add_single_order_info(OrderInfo.create(action=order_extraction_action))
    call(act.getOrdersDetails, order_details.request())
    call(common_act.verifyEntities, verification(before_order_details_id, "checking order",
                                                 [verify_ent("Order Status", order_status.name, "Open"),
                                                  verify_ent("Qty", order_qty.name, qty)
                                                  ]))
    # endregion
    # region manual execution order
    call(act.getOrdersDetails, order_details.request())
    manual_executing_details = ManualExecutingDetails(base_request)
    executions_details = manual_executing_details.add_executions_details()
    executions_details.set_quantity(qty)
    executions_details.set_price(price)
    executions_details.set_executing_firm("ExecutingFirm")
    executions_details.set_contra_firm("Contra_Firm")
    executions_details.set_last_capacity("Agency")
    call(act.manualExecution, manual_executing_details.build())
    # endregion
    # region Amend order
    fix_message = FixMessage(fix_message)
    param_list = {'OrderQty': qty2}
    quod_qa.wrapper.eq_fix_wrappers.amend_order_via_fix(case_id, fix_message, param_list, client + "_PARIS")
    eq_wrappers.accept_modify(lookup, qty, price)
    # endregion
    # region Check order after Amending
    order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[order_status
                                                                                            ])
    order_details.add_single_order_info(OrderInfo.create(action=order_extraction_action))

    call(act.getOrdersDetails, order_details.request())
    call(common_act.verifyEntities, verification(before_order_details_id, "checking order",
                                                 [verify_ent("Order Status", order_status.name, "Open"),
                                                  verify_ent("ExecStatus", order_status.name, "PartiallyFilled")
                                                  ]))
    # endregion
    # region manual execution order after amending
    manual_executing_details = ManualExecutingDetails(base_request)
    executions_details = manual_executing_details.add_executions_details()
    executions_details.set_quantity("1")
    executions_details.set_price(price)
    executions_details.set_executing_firm("ExecutingFirm")
    executions_details.set_contra_firm("Contra_Firm")
    executions_details.set_last_capacity("Agency")
    call(act.manualExecution, manual_executing_details.build())
    # endregion
    # region Complete
    order_details = OrdersDetails()
    order_details.set_default_params(base_request)
    complete_order_details = ModifyOrderDetails()
    complete_order_details.set_default_params(base_request)
    call(act.completeOrders, complete_order_details.build())
    # endregion
    # region Check order after Complete
    call(act.getOrdersDetails, order_details.request())
    call(common_act.verifyEntities, verification(before_order_details_id, "checking order",
                                                 [verify_ent("Order Status", order_status.name, "Open"),
                                                  verify_ent("PostTradeStatus", order_pts.name, "ReadyToBook"),
                                                  verify_ent("DoneForDay", order_dfd.name, "Yes"),
                                                  verify_ent("ExecSts", order_status.name, "Filled")
                                                  ]))
    # endregion
    # region Amend order after Complete
    order_amend = OrderTicketDetails()
    amend_order_details = ModifyOrderDetails()
    amend_order_details.set_default_params(base_request)
    amend_order_details.set_order_details(order_amend)
    call(act.amendOrder, amend_order_details.build())
    # endregion
    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
