import logging
import time

from datetime import datetime

from win_gui_modules.order_book_wrappers import OrdersDetails

from custom.basic_custom_actions import create_event, timestamps
from win_gui_modules.order_ticket_wrappers import NewOrderDetails

from stubs import Stubs
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction, OrderInfo
from win_gui_modules.order_ticket import OrderTicketDetails
from win_gui_modules.utils import get_base_request, call
from win_gui_modules.wrappers import set_base, verification, verify_ent

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(session_id, report_id):
    case_name = "QAP_4317"

    seconds, nanos = timestamps()  # Store case start time

    # region Declarations
    order_ticket_service = Stubs.win_act_order_ticket
    order_book_service = Stubs.win_act_order_book
    common_act = Stubs.win_act
    qty = "1,000"
    price = "1"
    order_type = "Limit"
    tif = "Day"
    client = "HAKKIM"
    lookup = "T55FD"
    # end region

    # region Open FE
    case_id = create_event(case_name, report_id)
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)

    # region Create Algo(TWAP) order via FE according with step 1
    order_ticket = OrderTicketDetails()
    order_ticket.set_quantity(qty)
    order_ticket.set_client(client)
    order_ticket.set_order_type(order_type)
    order_ticket.set_tif(tif)
    order_ticket.set_limit(price)
    order_ticket.buy()

    twap_strategy = order_ticket.add_twap_strategy("Quod TWAP")
    twap_strategy.set_start_date("Now")
    twap_strategy.set_end_date("Now", "0.5")
    twap_strategy.set_aggressivity("Passive")
    twap_strategy.set_waves("4")

    new_order_details = NewOrderDetails()
    new_order_details.set_lookup_instr(lookup)
    new_order_details.set_order_details(order_ticket)
    new_order_details.set_default_params(base_request)

    call(order_ticket_service.placeOrder, new_order_details.build())
    # end region

    # region extract and verify Parent details
    extraction_id = "before_order_details"
    order_details = OrdersDetails()
    order_details.set_default_params(base_request)
    order_details.set_extraction_id(extraction_id)

    parent_qty = ExtractionDetail("order_qty", "Qty")

    order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[parent_qty])

    order_details.add_single_order_info(OrderInfo.create(action=order_extraction_action))

    # parent request
    call(order_book_service.getOrdersDetails, order_details.request())

    call(common_act.verifyEntities, verification(extraction_id, "checking order",
                                                 [verify_ent("Parent Qty", parent_qty.name, qty)]))
    # end region extraction and verify

    # region extraction Child order details(step 2)
    child_order_info_extraction = "getOrderInfoChild"
    child_main_order_details = OrdersDetails()
    child_main_order_details.set_default_params(base_request)
    child_main_order_details.set_extraction_id(child_order_info_extraction)

    child1_id = ExtractionDetail("subOrder_lvl_1.id", "Order ID")
    child1_order_qty = ExtractionDetail("subOrder_lvl_1.Qty", "Qty")
    sub_lvl1_1_ext_action = ExtractionAction.create_extraction_action(extraction_details=[child1_id, child1_order_qty])
    sub_lv1_1_info = OrderInfo.create(actions=[sub_lvl1_1_ext_action])

    child2_id = ExtractionDetail("subOrder_lvl_2.id", "Order ID")
    child2_order_qty = ExtractionDetail("subOrder_lvl_2.Qty", "Qty")
    sub_lvl1_2_ext_action = ExtractionAction.create_extraction_action(extraction_details=[child2_id, child2_order_qty])
    sub_lv1_2_info = OrderInfo.create(actions=[sub_lvl1_2_ext_action])

    child3_id = ExtractionDetail("subOrder_lvl_3.id", "Order ID")
    child3_order_qty = ExtractionDetail("subOrder_lvl_3.Qty", "Qty")
    sub_lvl1_3_ext_action = ExtractionAction.create_extraction_action(extraction_details=[child3_id, child3_order_qty])
    sub_lv1_3_info = OrderInfo.create(actions=[sub_lvl1_3_ext_action])

    child4_id = ExtractionDetail("subOrder_lvl_4.id", "Order ID")
    child4_order_qty = ExtractionDetail("subOrder_lvl_4.Qty", "Qty")
    sub_lvl1_4_ext_action = ExtractionAction.create_extraction_action(extraction_details=[child4_id, child4_order_qty])
    sub_lv1_4_info = OrderInfo.create(actions=[sub_lvl1_4_ext_action])

    time.sleep(240)
    sub_order_details = OrdersDetails.create(order_info_list=[sub_lv1_1_info,
                                                              sub_lv1_2_info,
                                                              sub_lv1_3_info,
                                                              sub_lv1_4_info])
    child_main_order_details.add_single_order_info(OrderInfo.create(sub_order_details=sub_order_details))

    # child request
    call(Stubs.win_act_order_book.getOrdersDetails, child_main_order_details.request())
    # end region extraction

    # region verify Child details(step 2)
    call(common_act.verifyEntities, verification(child_order_info_extraction, "checking Child order",
                                                 [verify_ent("Child Order Qty - 4", child1_order_qty.name, "250"),
                                                  verify_ent("Child Order Qty - 3", child2_order_qty.name, "250"),
                                                  verify_ent("Child Order Qty - 2", child3_order_qty.name, "250"),
                                                  verify_ent("Child Order Qty - 1", child4_order_qty.name, "250")]))
    # end region(step 2)

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
