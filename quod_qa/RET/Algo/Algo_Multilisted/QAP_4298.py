import logging
import os

from datetime import datetime

from custom.verifier import Verifier
from win_gui_modules.order_book_wrappers import OrdersDetails, \
    OrderInfo, ExtractionAction, ExtractionDetail, ModifyOrderDetails, CancelOrderDetails
from th2_grpc_act_gui_quod.act_ui_win_pb2 import VerificationDetails
from custom.basic_custom_actions import create_event, timestamps
from win_gui_modules.order_ticket_wrappers import NewOrderDetails
from custom import basic_custom_actions as bca
from stubs import Stubs
from win_gui_modules.order_ticket import OrderTicketDetails
from win_gui_modules.utils import get_base_request, call
from win_gui_modules.wrappers import set_base, check_value, \
    create_order_analysis_events_request, create_verification_request
from quod_qa.wrapper.ret_wrappers import close_order_book, decorator_try_except

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def get_order_id(request):
    order_details = OrdersDetails()
    order_details.set_default_params(request)
    order_details.set_extraction_id("orderID")
    order_id = ExtractionDetail("order_id", "Order ID")
    order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[order_id])
    order_details.add_single_order_info(OrderInfo.create(action=order_extraction_action))
    result = call(Stubs.win_act_order_book.getOrdersDetails, order_details.request())
    return result[order_id.name]


def create_order_multilisting(base_request, order_ticket_service, qty, client, order_type, price, tif, display_qty,
                              side,
                              lookup, allow_missing_prim=None, available_venue=None, post_mode=None):
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

    multilisting_strategy = order_ticket.add_multilisting_strategy("Quod Multilisting")
    multilisting_strategy.set_allow_missing_prim(allow_missing_prim)
    multilisting_strategy.set_available_venues(available_venue)
    multilisting_strategy.set_post_mode(post_mode)

    new_order_details = NewOrderDetails()
    new_order_details.set_lookup_instr(lookup)
    new_order_details.set_order_details(order_ticket)
    new_order_details.set_default_params(base_request)

    call(order_ticket_service.placeOrder, new_order_details.build())


def verifier(case_id, event_name, expected_value, actual_value):
    # region verifier
    verifier = Verifier(case_id)
    verifier.set_event_name("Check Value")
    verifier.compare_values(event_name, expected_value, actual_value)
    verifier.verify()


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


def extract_child_lvl3_order_details(base_request, column_name, order_book_service, parent_order_id, extraction_id):
    order_details = OrdersDetails()
    order_details.set_default_params(base_request)
    order_details.set_extraction_id(extraction_id)
    order_details.set_filter(['ParentOrdID', parent_order_id])

    value = ExtractionDetail(column_name, column_name)
    order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[value])
    order_details.add_single_order_info(OrderInfo.create(action=order_extraction_action))
    request = call(order_book_service.getChildOrdersDetails, order_details.request())
    return request


@decorator_try_except(test_id=os.path.basename(__file__))
def execute(session_id, report_id):
    case_name = "QAP_4298"

    seconds, nanos = timestamps()  # Store case start time

    # region Declarations
    order_ticket_service = Stubs.win_act_order_ticket
    order_book_service = Stubs.win_act_order_book
    common_act = Stubs.win_act
    qty = "1300"
    display_qty = "1000"
    price = "1"
    order_type = "Limit"
    tif = "Day"
    client = "HAKKIM"
    lookup = "SBIN"
    side = 'Sell'
    allow_missing_prim = True
    available_venue = True
    post_mode = 'Single'
    parent_order_details_id = 'ParentOrderDetails'
    child_order_details_id_lvl2 = "ChildOrderDetailsLvl2"
    child_order_details_id_lvl3 = "ChildOrderDetailsLvl3"
    # end region

    # region Open FE
    case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    # end region

    # region Create Algo(TWAP) order via FE according with step 1,2,3,4
    create_order_multilisting(base_request, order_ticket_service, qty, client, order_type, price, tif, display_qty,
                              side, lookup, allow_missing_prim, available_venue, post_mode)
    # end region

    # region Extract  parent order details according with step 4
    parent_status = extract_parent_order_details(base_request, 'Sts', parent_order_details_id)
    parent_id = get_order_id(base_request)
    # end region

    # region Verify parent order details according with step 4
    verifier(case_id, 'Parent Status', 'Open', parent_status['Sts'])
    # end region

    # region Extract child lvl2 order details according with step 4
    child_lvl2_id = extract_child_lvl2_order_details(base_request, 'Order ID', child_order_details_id_lvl2)

    child_lvl2_status = extract_child_lvl2_order_details(base_request, 'Sts', child_order_details_id_lvl2)

    child_lvl2_qty = extract_child_lvl2_order_details(base_request, 'Qty', child_order_details_id_lvl2)

    child_lvl2_display_qty = extract_child_lvl2_order_details(base_request, 'DisplQty', child_order_details_id_lvl2)
    # end region

    # region Verify child lvl2 order details according with step 4
    verifier(case_id, 'Child Status lvl2', 'Open', child_lvl2_status['Sts'])
    verifier(case_id, 'Child Qty lvl2', '1,300', child_lvl2_qty['Qty'])
    verifier(case_id, 'Child Display Qty lvl2', '1,000', child_lvl2_display_qty['DisplQty'])
    # end region

    # region Extract child lvl3 order details according with step 4
    child_lvl3_status = extract_child_lvl3_order_details(base_request, 'Sts', order_book_service,
                                                         child_lvl2_id['Order ID'], child_order_details_id_lvl2)
    # end region

    # region Verify child lvl3 order details according with step 4
    verifier(case_id, 'Child status lvl3', 'Open', child_lvl3_status['Sts'])
    # end region

    # region Amend according with step 5
    order_amend = OrderTicketDetails()
    order_amend.set_display_qty("1100")
    amend_order_details = ModifyOrderDetails()
    amend_order_details.set_default_params(base_request)
    amend_order_details.set_order_details(order_amend)

    call(order_book_service.amendOrder, amend_order_details.build())
    # end region

    close_order_book(base_request, Stubs.win_act_order_book)

    # region Extract parent order status after amend according with step 5
    parent_display_qty_after_amend = extract_parent_order_details(base_request, 'DisplQty', parent_order_details_id)
    # end region

    # region Verify parent order status
    verifier(case_id, 'Parent Display Qty after amend', '1,100', parent_display_qty_after_amend['DisplQty'])
    # end region

    # region extract Child OrderDetails after Amend according with step 5
    child_order_info_extraction = child_order_details_id_lvl2
    child_main_order_details = OrdersDetails()
    child_main_order_details.set_default_params(base_request)
    child_main_order_details.set_extraction_id(child_order_info_extraction)

    child2_new_id = ExtractionDetail('New Order_Id', 'Order ID')
    child2_new_order_display_qty = ExtractionDetail('Display Qty', "DisplQty")
    sub_lvl1_2_ext_action = ExtractionAction.create_extraction_action(extraction_details=[child2_new_id,
                                                                                          child2_new_order_display_qty])
    sub_lv1_2_info = OrderInfo.create(actions=[sub_lvl1_2_ext_action])

    child1_old_order_status = ExtractionDetail('Order Status', "Sts")
    sub_lvl1_3_ext_action = ExtractionAction.create_extraction_action(extraction_details=[child1_old_order_status])
    sub_lvl1_3_info = OrderInfo.create(actions=[sub_lvl1_3_ext_action])

    sub_orders_details = OrdersDetails.create(order_info_list=[sub_lv1_2_info, sub_lvl1_3_info])
    child_main_order_details.add_single_order_info(OrderInfo.create(sub_order_details=sub_orders_details))

    request = call(Stubs.win_act_order_book.getOrdersDetails, child_main_order_details.request())
    # end region

    # region Verify new child lvl2 order details according with step 5
    verifier(case_id, 'New Order - Child Display Qty lvl2', '1,100', request['Display Qty'])
    # end region

    # region Verify old child lvl2 order details according with step 5
    verifier(case_id, 'Old Order after amend - Child Status lvl2', 'Cancelled', request['Order Status'])
    # end region

    # region Extract new value in Child order lvl 3 according with step 5
    child_lvl3_qty = extract_child_lvl3_order_details(base_request, 'Qty', order_book_service,
                                                      request['New Order_Id'], child_order_details_id_lvl3)
    # end region

    # region Verify new value in Child order lvl 3 according with step 5
    verifier(case_id, 'New Order - Child lvl3 Qty', '1,100', child_lvl3_qty['Qty'])
    # end region

    # region Extract old value in Child order lvl 3 according with step 5
    child_lvl3_sts = extract_child_lvl3_order_details(base_request, 'Sts', order_book_service, child_lvl2_id['Order ID'],
                                                      child_order_details_id_lvl3)
    # end region

    # region Verify old value in Child order lvl 3 according with step 5
    verifier(case_id, 'Old Order after amend - Child lvl3 Status', 'Cancelled', child_lvl3_sts['Sts'])
    # end region

    # region Cancel parent order according with step 6
    cancel_order_details = CancelOrderDetails()
    cancel_order_details.set_default_params(base_request)
    cancel_order_details.set_filter(["Order ID", parent_id])
    cancel_order_details.set_comment("Order cancelled by script")

    call(order_book_service.cancelOrder, cancel_order_details.build())
    # end region

    # region extract OrderAnalysisEvents according with step 7
    extraction_id = "OrderAnalysisEvents"
    call(common_act.getOrderAnalysisEvents,
         create_order_analysis_events_request(extraction_id, {"Order ID": parent_id}))

    analysis_event_verifier = create_verification_request("Checking order events", extraction_id, extraction_id)

    check_value(analysis_event_verifier, "Event 1 Description contains", "event1.desc",
                "New User's Synthetic Order Received (Sell 1,300 @ 1)",
                VerificationDetails.VerificationMethod.CONTAINS)

    check_value(analysis_event_verifier, "Event 2 Description contains", "event2.desc",
                "Passive order acknowledgement received on National Stock Exchange (1,300 @ INR 1)",
                VerificationDetails.VerificationMethod.CONTAINS)

    check_value(analysis_event_verifier, "Event 3 Description contains", "event3.desc",
                "User's Modification Received on the Synthetic Order",
                VerificationDetails.VerificationMethod.CONTAINS)

    check_value(analysis_event_verifier, "Event 4 Description contains", "event4.desc",
                "Cancel request acknowledgement received on National Stock Exchange (1,300 @ INR 1)",
                VerificationDetails.VerificationMethod.CONTAINS)

    check_value(analysis_event_verifier, "Event 5 Description contains", "event5.desc",
                "Passive order acknowledgement received on National Stock Exchange (1,300 @ INR 1)",
                VerificationDetails.VerificationMethod.CONTAINS)

    check_value(analysis_event_verifier, "Event 6 Description contains", "event6.desc",
                "User's Cancellation Received on the Synthetic Order",
                VerificationDetails.VerificationMethod.CONTAINS)

    check_value(analysis_event_verifier, "Event 7 Description contains", "event7.desc",
                "Cancel request acknowledgement received on National Stock Exchange (1,300 @ INR 1)",
                VerificationDetails.VerificationMethod.CONTAINS)

    check_value(analysis_event_verifier, "Events Count", "events.count", "7")
    call(common_act.verifyEntities, analysis_event_verifier)
    # end region

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
