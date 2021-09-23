import os

from custom.verifier import Verifier
from win_gui_modules.order_book_wrappers import OrdersDetails,\
    OrderInfo, ExtractionAction, ExtractionDetail, CancelOrderDetails
from custom.basic_custom_actions import create_event, timestamps
from win_gui_modules.order_ticket_wrappers import NewOrderDetails
from stubs import Stubs
from win_gui_modules.order_ticket import OrderTicketDetails
from win_gui_modules.utils import get_base_request, call
from win_gui_modules.wrappers import set_base
from custom import basic_custom_actions as bca

def get_order_id(request):
    order_details = OrdersDetails()
    order_details.set_default_params(request)
    order_details.set_extraction_id("orderID")
    order_id = ExtractionDetail("order_id", "Order ID")
    order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[order_id])
    order_details.add_single_order_info(OrderInfo.create(action=order_extraction_action))
    result = call(Stubs.win_act_order_book.getOrdersDetails, order_details.request())
    return result[order_id.name]


def create_order_iceberg(base_request, qty, client, order_type, price, tif, side, display_qty, lookup):

    order_ticket = OrderTicketDetails()
    order_ticket.set_quantity(qty)
    order_ticket.set_client(client)
    order_ticket.set_order_type(order_type)
    if order_type == 'Limit':
        order_ticket.set_limit(price)
    order_ticket.set_tif(tif)

    order_ticket.set_display_qty(display_qty)
    if side == 'Buy':
        order_ticket.buy()
    elif side == 'Sell':
        order_ticket.sell()

    new_order_details = NewOrderDetails()
    new_order_details.set_lookup_instr(lookup)
    new_order_details.set_order_details(order_ticket)
    new_order_details.set_default_params(base_request)

    order_ticket_service = Stubs.win_act_order_ticket
    call(order_ticket_service.placeOrder, new_order_details.build())


def extract_parent_order_details(base_request, column_name, extraction_id):
    order_details = OrdersDetails()
    order_details.set_default_params(base_request)
    order_details.set_extraction_id(extraction_id)
    value = ExtractionDetail(column_name, column_name)
    order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[value])
    order_details.add_single_order_info(OrderInfo.create(action=order_extraction_action))

    result = call(Stubs.win_act_order_book.getOrdersDetails, order_details.request())
    return result


def extract_child_lvl2_order_details(base_request, column_name, extraction_id):
    child_main_order_details = OrdersDetails()
    child_main_order_details.set_default_params(base_request)
    child_main_order_details.set_extraction_id(extraction_id)

    value = ExtractionDetail(column_name, column_name)
    sub_lvl1_1_ext_action = ExtractionAction.create_extraction_action(extraction_details=[value])

    sub_lv1_1_info = OrderInfo.create(actions=[sub_lvl1_1_ext_action])
    sub_order_details_level1 = OrdersDetails.create(order_info_list=[sub_lv1_1_info])
    child_main_order_details.add_single_order_info(OrderInfo.create(sub_order_details=sub_order_details_level1))

    request = call(Stubs.win_act_order_book.getOrdersDetails, child_main_order_details.request())
    return request


def cancel_order(base_request, parent_id, order_book_service):
    cancel_order_details = CancelOrderDetails()
    cancel_order_details.set_default_params(base_request)
    cancel_order_details.set_filter(["Order ID", parent_id])
    cancel_order_details.set_comment("Order cancelled by script")

    call(order_book_service.cancelOrder, cancel_order_details.build())


def verifier(case_id, event_name, expected_value, actual_value):
    # region verifier
    verifier = Verifier(case_id)
    verifier.set_event_name("Check Value")
    verifier.compare_values(event_name, expected_value, actual_value)
    verifier.verify()


def execute(session_id, report_id):
    case_name = "QAP_4289"

    # region Declarations
    qty = "1,000"
    client = "HAKKIM"
    price = "20"
    order_type = "Limit"
    tif = "Day"
    side = "Buy"
    display_qty = "50"
    lookup = "T55FD"
    parent_order_details_id = 'ParentOrderDetails'
    child_order_details_id_lvl2 = "ChildOrderDetailsLvl2"
    # endregion

    order_book_service = Stubs.win_act_order_book
    case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)

    # region Step 1
    create_order_iceberg(base_request, qty, client, order_type, price, tif, side, display_qty, lookup)


    parent_id = get_order_id(base_request)

    parent_status = extract_parent_order_details(base_request, 'Sts', parent_order_details_id)
    verifier(case_id, 'Parent Status', 'Open', parent_status['Sts'])

    parent_display_qty = extract_parent_order_details(base_request, 'DisplQty', child_order_details_id_lvl2)
    verifier(case_id, 'Parent Display Qty', '50', parent_display_qty['DisplQty'])
    # end Step 1

    # region Step 2
    child_lvl2_qty = extract_child_lvl2_order_details(base_request, 'Qty', child_order_details_id_lvl2)
    verifier(case_id, 'Child lvl2 Qty', '50', child_lvl2_qty['Qty'])

    child_lvl2_price = extract_child_lvl2_order_details(base_request, 'Limit Price', child_order_details_id_lvl2)
    verifier(case_id, 'Child lvl2 Price', '20', child_lvl2_price['Limit Price'])

    child_lvl2_tif = extract_child_lvl2_order_details(base_request, 'TIF', child_order_details_id_lvl2)
    verifier(case_id, 'Child lvl2 TIF', 'Day', child_lvl2_tif['TIF'])

    child_lvl2_display_qty = extract_child_lvl2_order_details(base_request, 'DisplQty', child_order_details_id_lvl2)
    verifier(case_id, 'Child Display Qty', '', child_lvl2_display_qty['DisplQty'])
    # end Step 2

    # region Step 3
    cancel_order(base_request, parent_id, order_book_service)
    # end Step 3


