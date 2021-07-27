import logging

from datetime import datetime
from custom.basic_custom_actions import create_event, timestamps
from stubs import Stubs
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction, OrderInfo, OrdersDetails
from win_gui_modules.utils import get_base_request, call
from win_gui_modules.wrappers import set_base, verification, verify_ent, direct_loc_request_correct
from th2_grpc_act_gui_quod.order_ticket_pb2 import DiscloseFlagEnum
from quod_qa.wrapper import eq_wrappers

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(session_id, report_id):
    case_name = "QAP_1719"

    seconds, nanos = timestamps()  # Store case start time

    # region Declarations
    order_book_service = Stubs.win_act_order_book
    common_act = Stubs.win_act
    qty = "100"
    client = "HAKKIM"
    lookup = "T55FD"
    order_type = "Limit"
    tif = "Day"
    price = "30"
    recipient = "RIN-DESK (CL)"
    # endregion

    # region Open FE
    case_id = create_event(case_name, report_id)
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)

    # region Create Care order via FE
    eq_wrappers.create_order(base_request, qty, client, lookup, order_type, tif, True, recipient, price, False,
                             DiscloseFlagEnum.DEFAULT_VALUE)
    # end region

    # region Check values in OrderBook
    before_order_details_id = "before_order_details"
    order_details = OrdersDetails()
    order_details.set_default_params(base_request)
    order_details.set_extraction_id(before_order_details_id)

    parent_order_status = ExtractionDetail("order_status", "Sts")

    order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[parent_order_status])

    order_details.add_single_order_info(OrderInfo.create(action=order_extraction_action))
    call(order_book_service.getOrdersDetails, order_details.request())
    call(common_act.verifyEntities, verification(before_order_details_id, "checking order",
                                                 [verify_ent("Parent Status", parent_order_status.name, "Sent")]))

    # endregion

    # region accept order
    eq_wrappers.accept_order(lookup, qty, price)
    # end region

    # region direct order
    call(order_book_service.orderBookDirectLoc, direct_loc_request_correct(qty, "100", "NSE"))
    # end region

    # region Check value in child order
    before_order_details_id = "before_order_details"
    order_details = OrdersDetails()
    order_details.set_default_params(base_request)
    order_details.set_extraction_id(before_order_details_id)

    child_order_status = ExtractionDetail("order_status", "Sts")
    child_qty = ExtractionDetail("child_qty", "Qty")
    child_order_type = ExtractionDetail("order_type", "OrdType")
    child_order_tif = ExtractionDetail("order_tif", "TIF")
    order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[child_order_status,
                                                                                            child_qty,
                                                                                            child_order_type,
                                                                                            child_order_tif])

    order_details.add_single_order_info(OrderInfo.create(action=order_extraction_action))
    call(order_book_service.getChildOrdersDetails, order_details.request())
    call(common_act.verifyEntities, verification(before_order_details_id, "checking Child order",
                                                 [verify_ent("Child Order Status", child_order_status.name, "Open"),
                                                  verify_ent("Child Order Qty", child_qty.name, qty),
                                                  verify_ent("Child Order Type", child_order_type.name, "Limit"),
                                                  verify_ent("Child Order TIF", child_order_tif.name, "AtTheClose")]))
    # end region

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
