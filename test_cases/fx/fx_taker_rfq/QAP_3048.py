import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from test_cases.fx.fx_wrapper.common_tools import random_qty
from stubs import Stubs
from win_gui_modules.aggregated_rates_wrappers import ModifyRFQTileRequest, ContextAction, PlaceRFQRequest, \
    RFQTileOrderSide
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.order_book_wrappers import OrdersDetails, ExtractionDetail, OrderInfo, ExtractionAction, \
    FXOrdersDetails, FXOrderInfo
from win_gui_modules.quote_wrappers import QuoteDetailsRequest
from win_gui_modules.utils import call, get_base_request
from win_gui_modules.wrappers import set_base


def create_or_get_rfq(base_request, service):
    call(service.createRFQTile, base_request.build())


def send_rfq(base_request, service):
    call(service.sendRFQOrder, base_request.build())


def place_order_tob(base_request, service):
    rfq_request = PlaceRFQRequest(details=base_request)
    rfq_request.set_action(RFQTileOrderSide.BUY)
    call(service.placeRFQOrder, rfq_request.build())


def modify_rfq_tile(base_request, service, qty, cur1, cur2, tenor, client, venue):
    modify_request = ModifyRFQTileRequest(details=base_request)
    modify_request.set_quantity_as_string(qty)
    modify_request.set_from_currency(cur1)
    modify_request.set_to_currency(cur2)
    modify_request.set_near_tenor(tenor)
    modify_request.set_client(client)
    action = ContextAction.create_venue_filter(venue)
    modify_request.add_context_action(action)
    call(service.modifyRFQTile, modify_request.build())


def check_quote_request_b(base_request, service, case_id, qty, tenor, near_tenor, far_tenor):
    qrb = QuoteDetailsRequest(base=base_request)
    extraction_id = bca.client_orderid(4)
    qrb.set_extraction_id(extraction_id)
    qrb.set_filter(["Qty", qty])
    qr_tenor = ExtractionDetail("quoteRequestBook.tenor", "Tenor")
    qr_near_tenor = ExtractionDetail("quoteRequestBook.nearLegTenor", "Near Leg Tenor")
    qr_far_tenor = ExtractionDetail("quoteRequestBook.farLegTenor", "Far Leg Tenor")
    qrb.add_extraction_details([qr_tenor, qr_near_tenor, qr_far_tenor])
    response = call(service.getQuoteRequestBookDetails, qrb.request())

    verifier = Verifier(case_id)
    verifier.set_event_name("Check QuoteRequest book")
    verifier.compare_values("Tenor", tenor, response[qr_tenor.name])
    verifier.compare_values("Near Leg Tenor", near_tenor, response[qr_near_tenor.name])
    verifier.compare_values("Tenor", far_tenor, response[qr_far_tenor.name])
    verifier.verify()


def check_trades_book(base_request, ob_act, case_id, qty, tenor, near_tenor, far_tenor):
    execution_details = OrdersDetails()
    extraction_id = bca.client_orderid(4)
    execution_details.set_default_params(base_request)
    execution_details.set_extraction_id(extraction_id)
    execution_details.set_filter(["Qty", qty])
    trades_tenor = ExtractionDetail("tradeBook.tenor", "Tenor")
    trades_near_tenor = ExtractionDetail("tradeBook.nearLegTenor", "Near Leg Tenor")
    trades_far_tenor = ExtractionDetail("tradeBook.farLegTenor", "Far Leg Tenor")
    execution_details.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(
                extraction_details=[trades_tenor, trades_near_tenor, trades_far_tenor])))
    response = call(ob_act.getTradeBookDetails, execution_details.request())

    verifier = Verifier(case_id)
    verifier.set_event_name("Check Trade Book")
    verifier.compare_values("Tenor", tenor, response[trades_tenor.name])
    verifier.compare_values("Near Leg Tenor", near_tenor, response[trades_near_tenor.name])
    verifier.compare_values("Tenor", far_tenor, response[trades_far_tenor.name])
    verifier.verify()


def check_my_orders(base_request, ob_act, case_id, qty, tenor, near_tenor, far_tenor):
    main_order_details = OrdersDetails()
    main_order_details.set_default_params(base_request)
    extraction_id = bca.client_orderid(4)
    main_order_details.set_extraction_id(extraction_id)
    main_order_details.set_filter(["Qty", qty])
    my_order_tenor = ExtractionDetail("myOrders.tenor", "Tenor")
    my_order_near_tenor = ExtractionDetail("myOrders.nearLegTenor", "Near Leg Tenor")
    my_order_far_tenor = ExtractionDetail("myOrders.farLegTenor", "Far Leg Tenor")
    main_order_details.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(
                extraction_details=[my_order_tenor, my_order_near_tenor, my_order_far_tenor])))
    response = call(ob_act.getMyOrdersDetails, main_order_details.request())

    verifier = Verifier(case_id)
    verifier.set_event_name("Check My Order book")
    verifier.compare_values("Tenor", tenor, response[my_order_tenor.name])
    verifier.compare_values("Near Leg Tenor", near_tenor, response[my_order_near_tenor.name])
    verifier.compare_values("Tenor", far_tenor, response[my_order_far_tenor.name])
    verifier.verify()


def check_order_book(base_request, ob_act, case_id, qty, tenor, near_tenor, far_tenor):
    ob_details = FXOrdersDetails()
    ob_details.set_default_params(base_request)
    extraction_id = bca.client_orderid(4)
    ob_details.set_extraction_id(extraction_id)
    ob_details.set_filter(["Qty", qty])
    order_tenor = ExtractionDetail("myOrders.tenor", "Tenor")
    order_near_tenor = ExtractionDetail("myOrders.nearLegTenor", "Near Leg Tenor")
    order_far_tenor = ExtractionDetail("myOrders.farLegTenor", "Far Leg Tenor")
    ob_details.add_single_order_info(
        FXOrderInfo.create(
            action=ExtractionAction.create_extraction_action(
                extraction_details=[order_tenor, order_near_tenor, order_far_tenor])))
    response = call(ob_act.getOrdersDetails, ob_details.request())

    verifier = Verifier(case_id)
    verifier.set_event_name("Check Order book")
    verifier.compare_values("Tenor", tenor, response[order_tenor.name])
    verifier.compare_values("Near Leg Tenor", near_tenor, response[order_near_tenor.name])
    verifier.compare_values("Tenor", far_tenor, response[order_far_tenor.name])
    verifier.verify()


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)

    set_base(session_id, case_id)
    case_base_request = get_base_request(session_id, case_id)
    base_rfq_details = BaseTileDetails(base=case_base_request)

    ob_act = Stubs.win_act_order_book
    ob_fx_act = Stubs.win_act_order_book_fx
    ar_service = Stubs.win_act_aggregated_rates_service
    modify_request = ModifyRFQTileRequest(details=base_rfq_details)

    from_curr = "EUR"
    to_curr = "USD"
    qty_1 = str(random_qty(1, 2, 7))
    try:
        # Step 1
        create_or_get_rfq(base_rfq_details, ar_service)
        modify_rfq_tile(base_rfq_details, ar_service, qty_1, from_curr, to_curr,
                        "Spot", "ASPECT_CITI", "CITI")
        send_rfq(base_rfq_details, ar_service)
        place_order_tob(base_rfq_details, ar_service)
        # Step 2
        check_order_book(case_base_request, ob_fx_act, case_id, qty_1, "Spot", "", "")
        # check_my_orders(case_base_request, ob_act, case_id, qty_1, "Spot", "", "")
        check_trades_book(case_base_request, ob_act, case_id, qty_1, "Spot", "", "")
        check_quote_request_b(case_base_request, ar_service, case_id, qty_1, "Spot", "", "")
        # Step 3
        modify_request.set_near_tenor("1W")
        call(ar_service.modifyRFQTile, modify_request.build())
        send_rfq(base_rfq_details, ar_service)
        place_order_tob(base_rfq_details, ar_service)
        check_order_book(case_base_request, ob_fx_act, case_id, qty_1, "1W", "", "")
        # check_my_orders(case_base_request, ob_act, case_id, qty_1, "1W", "", "")
        check_trades_book(case_base_request, ob_act, case_id, qty_1, "1W", "", "")
        check_quote_request_b(case_base_request, ar_service, case_id, qty_1, "1W", "", "")
        # Step 4
        modify_request.set_near_tenor("Spot")
        modify_request.set_far_leg_tenor("1W")
        call(ar_service.modifyRFQTile, modify_request.build())
        send_rfq(base_rfq_details, ar_service)
        place_order_tob(base_rfq_details, ar_service)
        check_order_book(case_base_request, ob_fx_act, case_id, qty_1, "Spot", "Spot", "1W")
        # check_my_orders(case_base_request, ob_act, case_id, qty_1, "Spot", "Spot", "1W")
        check_trades_book(case_base_request, ob_act, case_id, qty_1, "Spot", "Spot", "1W")
        check_quote_request_b(case_base_request, ar_service, case_id, qty_1, "Spot", "Spot", "1W")
        # Step 5
        modify_request.set_near_tenor("TOM")
        modify_request.set_far_leg_tenor("2W")
        call(ar_service.modifyRFQTile, modify_request.build())
        send_rfq(base_rfq_details, ar_service)
        place_order_tob(base_rfq_details, ar_service)
        check_order_book(case_base_request, ob_fx_act, case_id, qty_1, "TOM,", "TOM", "2W")
        # check_my_orders(case_base_request, ob_act, case_id, qty_1, "TOM,", "TOM", "2W")
        check_trades_book(case_base_request, ob_act, case_id, qty_1, "TOM", "TOM", "2W")
        check_quote_request_b(case_base_request, ar_service, case_id, qty_1, "TOM", "TOM", "2W")

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
    finally:
        try:
            # Close tile
            call(ar_service.closeRFQTile, base_rfq_details.build())
        except Exception:
            logging.error("Error execution", exc_info=True)
