import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.aggregated_rates_wrappers import RFQTileOrderSide, PlaceRFQRequest, ModifyRFQTileRequest, \
    ContextAction
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.order_book_wrappers import OrdersDetails, OrderInfo, ExtractionDetail, ExtractionAction
from win_gui_modules.quote_wrappers import QuoteDetailsRequest
from win_gui_modules.utils import set_session_id, prepare_fe_2, get_base_request, call, get_opened_fe
from win_gui_modules.wrappers import set_base


def create_or_get_rfq(base_request, service):
    call(service.createRFQTile, base_request.build())


def send_rfq(base_request, service):
    call(service.sendRFQOrder, base_request.build())


def modify_rfq_tile(base_request, service, qty, cur1, cur2, near_tenor, client, venues):
    modify_request = ModifyRFQTileRequest(details=base_request)
    action = ContextAction.create_venue_filters(venues)
    modify_request.add_context_action(action)
    modify_request.set_quantity(qty)
    modify_request.set_from_currency(cur1)
    modify_request.set_to_currency(cur2)
    modify_request.set_near_tenor(near_tenor)
    modify_request.set_client(client)
    call(service.modifyRFQTile, modify_request.build())


def place_order_tob(base_request, service, side):
    rfq_request = PlaceRFQRequest(details=base_request)
    if side == "Sell":
        rfq_request.set_action(RFQTileOrderSide.SELL)
    elif side == "Buy":
        rfq_request.set_action(RFQTileOrderSide.BUY)
    call(service.placeRFQOrder, rfq_request.build())


def cancel_rfq(base_request, service):
    call(service.cancelRFQ, base_request.build())


def check_quote_request_b(base_request, service, case_id, status, quote_sts, venue):
    qrb = QuoteDetailsRequest(base=base_request)
    extraction_id = bca.client_orderid(4)
    qrb.set_extraction_id(extraction_id)
    qrb.set_filter(["Venue", venue])
    qrb_venue = ExtractionDetail("quoteRequestBook.venue", "Venue")
    qrb_status = ExtractionDetail("quoteRequestBook.status", "Status")
    qrb_quote_status = ExtractionDetail("quoteRequestBook.qoutestatus", "QuoteStatus")
    qrb.add_extraction_details([qrb_venue, qrb_status, qrb_quote_status])
    response = call(service.getQuoteRequestBookDetails, qrb.request())

    verifier = Verifier(case_id)
    verifier.set_event_name("Check QuoteRequest book")
    verifier.compare_values('Venue', venue + "R", response[qrb_venue.name])
    verifier.compare_values('Status', status, response[qrb_status.name])
    verifier.compare_values("QuoteStatus", quote_sts, response[qrb_quote_status.name])
    verifier.verify()


def click_checkboxes(base_request, service, side):
    modify_request = ModifyRFQTileRequest(details=base_request)
    if side == "Left":
        modify_request.click_checkbox_left()
    if side == "Right":
        modify_request.click_checkbox_right()
    call(service.modifyRFQTile, modify_request.build())


def check_order_book(base_request, act_ob):
    ob = OrdersDetails()
    extraction_id = bca.client_orderid(4)
    ob.set_default_params(base_request)
    ob.set_extraction_id(extraction_id)
    ob_id = ExtractionDetail("orderBook.quoteid", "Order ID")
    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[ob_id])))
    response = call(act_ob.getOrdersDetails, ob.request())
    return response[ob_id.name]


def compare_order(base_request, act_ob, case_id, order_id):
    ob = OrdersDetails()
    extraction_id = bca.client_orderid(4)
    ob.set_default_params(base_request)
    ob.set_extraction_id(extraction_id)
    ob_id = ExtractionDetail("orderBook.quoteid", "Order ID")
    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[ob_id])))
    response = call(act_ob.getOrdersDetails, ob.request())

    verifier = Verifier(case_id)
    verifier.set_event_name("Compare Order ID")
    verifier.compare_values("ID", order_id, response[ob_id.name])
    verifier.verify()


def execute(report_id, session_id):
    ar_service = Stubs.win_act_aggregated_rates_service
    ob_act = Stubs.win_act_order_book

    case_name = Path(__file__).name[:-3]
    case_client = "ASPECT_CITI"
    case_from_currency = "EUR"
    case_to_currency = "USD"
    case_near_tenor = "Spot"
    case_venue = ["CITI"]
    case_filter_venue = "CITI"
    case_qty = 2000000
    quote_sts_new = 'New'
    quote_quote_sts_accepted = "Accepted"
    case_left_checkbox = "Left"
    case_right_checkbox = "Right"
    case_side_sell = "Sell"
    case_side_buy = "Buy"

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)

    set_base(session_id, case_id)
    case_base_request = get_base_request(session_id, case_id)
    base_rfq_details = BaseTileDetails(base=case_base_request)

    try:
        # Step 1
        create_or_get_rfq(base_rfq_details, ar_service)
        modify_rfq_tile(base_rfq_details, ar_service, case_qty, case_from_currency, case_to_currency,
                        case_near_tenor, case_client, case_venue)
        send_rfq(base_rfq_details, ar_service)
        check_quote_request_b(case_base_request, ar_service, case_id,
                              quote_sts_new, quote_quote_sts_accepted, case_filter_venue)
        order_id = check_order_book(case_base_request, ob_act)
        # Step 2
        click_checkboxes(base_rfq_details, ar_service, case_left_checkbox)
        place_order_tob(base_rfq_details, ar_service, case_side_sell)
        compare_order(case_base_request, ob_act, case_id, order_id)
        # Step 3
        click_checkboxes(base_rfq_details, ar_service, case_right_checkbox)
        place_order_tob(base_rfq_details, ar_service, case_side_buy)
        compare_order(case_base_request, ob_act, case_id, order_id)

        # Close tile
        call(ar_service.closeRFQTile, base_rfq_details.build())

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
