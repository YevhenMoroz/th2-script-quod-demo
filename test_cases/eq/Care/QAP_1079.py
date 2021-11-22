import logging

import test_framework.old_wrappers.eq_fix_wrappers
from test_cases.wrapper import eq_wrappers
from win_gui_modules.order_book_wrappers import OrdersDetails
from custom.basic_custom_actions import create_event, timestamps
from stubs import Stubs
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction, OrderInfo
from win_gui_modules.utils import get_base_request, call
from win_gui_modules.wrappers import verification, verify_ent

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id, session_id):
    case_name = "QAP-1079"
    seconds, nanos = timestamps()  # Store case start time
    # region Declarations
    act = Stubs.win_act_order_book
    common_act = Stubs.win_act
    qty = "900"
    price = "20"
    client = "CLIENT_FIX_CARE"
    lookup = "PROL"
    case_id = create_event(case_name, report_id)
    base_request = get_base_request(session_id, case_id)
    work_dir = Stubs.custom_config['qf_trading_fe_folder']
    username = Stubs.custom_config['qf_trading_fe_user']
    password = Stubs.custom_config['qf_trading_fe_password']
    # endregion
    # region Open FE
    eq_wrappers.open_fe(session_id, report_id, case_id, work_dir, username, password)
    # endregion
    # region Create CO
    test_framework.old_wrappers.eq_fix_wrappers.create_order_via_fix(case_id, 3, 1, client, 2, qty, 0, price)
    # endregion
    # region Accept CO
    eq_wrappers.accept_order(lookup, qty, price)
    # endregion

    # region Check values in OrderBook
    before_order_details_id = "before_order_details"
    order_details = OrdersDetails()
    order_details.set_default_params(base_request)
    order_details.set_extraction_id(before_order_details_id)

    order_status = ExtractionDetail("order_status", "Sts")
    order_qty = ExtractionDetail("order_qty", "Qty")
    order_price = ExtractionDetail("order_price", "Limit Price")
    order_es = ExtractionDetail("order_es", "ExecSts")
    order_leaves_qty = ExtractionDetail("order_leaves_qty", "LeavesQty")
    order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[order_status,
                                                                                            order_qty,
                                                                                            order_price,
                                                                                            order_es,
                                                                                            order_leaves_qty
                                                                                            ])
    order_details.add_single_order_info(OrderInfo.create(action=order_extraction_action))
    call(act.getOrdersDetails, order_details.request())
    call(common_act.verifyEntities, verification(before_order_details_id, "checking order",
                                                 [verify_ent("Order Status", order_status.name, "Open")
                                                  ]))
    # endregion
    # region partially fill
    eq_wrappers.manual_execution(base_request, str(int(int(qty) / 2)), price)
    # endregion

    # region Extract
    order_id = eq_wrappers.get_order_id(base_request)
    cl_order_id = eq_wrappers.get_cl_order_id(base_request)
    # endregion
    # Cancel order
    test_framework.old_wrappers.eq_fix_wrappers.cancel_order_via_fix(case_id, order_id, cl_order_id, client, 1)
    # region Accept Cancel message
    eq_wrappers.accept_cancel(lookup, qty, price)
    # endregion
    # Check order
    call(act.getOrdersDetails, order_details.request())
    call(common_act.verifyEntities, verification(before_order_details_id, "checking order",
                                                 [verify_ent("Order Status", order_status.name, "Cancelled"),
                                                  verify_ent('Order LeavesQty', order_leaves_qty.name, "0")]))
    # endregion
