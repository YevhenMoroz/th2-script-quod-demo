import logging

from custom.basic_custom_actions import create_event, timestamps
from quod_qa.wrapper import eq_fix_wrappers, eq_wrappers
from stubs import Stubs
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction, OrderInfo
from win_gui_modules.order_book_wrappers import OrdersDetails
from win_gui_modules.utils import get_base_request, call
from win_gui_modules.wrappers import set_base, verification, verify_ent

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
    new_qty = "100"
    price = "10"
    new_price = "1"
    lookup = "VETO"
    client = "CLIENT1"
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
    # region Create order via FIX
    fix_params = eq_fix_wrappers.create_order_via_fix(case_id, "3", 2, client, "2", qty, "0", price)
    response = fix_params.pop('response')
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

    call(act.getOrdersDetails, order_details.request())
    call(common_act.verifyEntities, verification(before_order_details_id, "checking order",
                                                 [verify_ent("Order Status", order_status.name, "Sent"),
                                                  verify_ent("Qty", order_qty.name, qty),
                                                  verify_ent("LmtPrice", order_price.name, price)]))
    # endregion
    # region Accept CO
    eq_wrappers.accept_order(lookup, qty, price)
    # endregion
    # region Send OrderCancelReplaceRequest with new price
    params = {'Price': new_price}
    eq_fix_wrappers.amend_order_via_fix(case_id, fix_params, params)
    eq_wrappers.accept_modify(lookup, qty, new_price)
    # endregion
    # region Send OrderCancelReplaceRequest with new qty
    params = {'OrderQty': new_qty, 'Price': new_price}
    eq_fix_wrappers.amend_order_via_fix(case_id, fix_params, params)
    eq_wrappers.accept_modify(lookup, new_qty, new_price)
    # endregion
    # region Cancel order
    client_order_id = response.response_messages_list[0].fields['ClOrdID'].simple_value
    eq_fix_wrappers.cancel_order_via_fix(case_id, client_order_id, client_order_id, client, "2")
    eq_wrappers.accept_cancel(lookup, new_qty, new_price)
    # endregion
    # region Check values in OrderBook after Cancel
    order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[order_status])
    order_details.add_single_order_info(OrderInfo.create(action=order_extraction_action))

    call(act.getOrdersDetails, order_details.request())
    call(common_act.verifyEntities, verification(before_order_details_id, "checking order",
                                                 [verify_ent("Order Status", order_status.name, "Cancelled"),
                                                  verify_ent("Qty", order_qty.name, new_qty),
                                                  verify_ent("LmtPrice", order_price.name, new_price)]))
    # endregion
