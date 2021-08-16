import logging
from pathlib import Path

from custom import basic_custom_actions as bca
from custom.verifier import Verifier, VerificationMethod
from stubs import Stubs
from win_gui_modules.aggregated_rates_wrappers import ModifyRatesTileRequest, ContextActionRatesTile, ActionsRatesTile, \
    PlaceESPOrder, ESPTileOrderSide
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.order_book_wrappers import OrdersDetails, ExtractionDetail, OrderInfo, ExtractionAction
from win_gui_modules.order_ticket import FXOrderDetails
from win_gui_modules.order_ticket_wrappers import NewFxOrderDetails
from win_gui_modules.utils import call, get_base_request
from win_gui_modules.wrappers import set_base


def create_or_get_rates_tile(base_request, service):
    call(service.createRatesTile, base_request.build())


def modify_order_ticket(base_request, service, qty, tif, client):
    order_ticket = FXOrderDetails()
    order_ticket.set_qty(qty)
    order_ticket.set_tif(tif)
    order_ticket.set_client(client)
    order_ticket.set_place()
    new_order_details = NewFxOrderDetails(base_request, order_ticket)
    call(service.placeFxOrder, new_order_details.build())


def place_order(base_request, service):
    esp_request = PlaceESPOrder(details=base_request)
    esp_request.top_of_book()
    esp_request.set_action(ESPTileOrderSide.BUY)
    call(service.placeESPOrder, esp_request.build())


def modify_rates_tile(base_request, service, from_c, to_c, tenor):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.set_instrument(from_c, to_c, tenor)
    call(service.modifyRatesTile, modify_request.build())


def filter_venue(base_request, service, venues):
    modify_request = ModifyRatesTileRequest(details=base_request)
    venue_filter = ContextActionRatesTile.create_venue_filters(venues)
    modify_request.add_context_action(venue_filter)
    call(service.modifyRatesTile, modify_request.build())


def check_order_book_2_child(base_request, act_ob, case_id, tif, owner, qty):
    ob = OrdersDetails()
    execution_id = bca.client_orderid(4)
    ob.set_default_params(base_request)
    ob.set_extraction_id(execution_id)
    ob.set_filter(["Owner", owner, "Qty", qty])
    child_1_tif = ExtractionDetail("child_1.tif", "TIF")
    child_1_ext_action = ExtractionAction.create_extraction_action(
        extraction_detail=child_1_tif)
    child_1_info = OrderInfo.create(action=child_1_ext_action)
    child_2_tif = ExtractionDetail("child_2.tif", "TIF")
    child_2_ext_action = ExtractionAction.create_extraction_action(
        extraction_detail=child_2_tif)
    child_2_info = OrderInfo.create(action=child_2_ext_action)

    child_orders_details = OrdersDetails.create(order_info_list=[child_1_info, child_2_info])

    ob_tif = ExtractionDetail("orderBook.tif", "TIF")
    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[ob_tif]),
            sub_order_details=child_orders_details))
    response = call(act_ob.getOrdersDetails, ob.request())
    verifier = Verifier(case_id)
    verifier.set_event_name("Check Order book")
    verifier.compare_values("Main order TIF", tif, response[ob_tif.name])
    verifier.compare_values("Check that child orders have different TIF", response[child_1_tif.name],
                            response[child_2_tif.name], VerificationMethod.NOT_EQUALS)

    verifier.verify()


def check_order_book_1_child(base_request, act_ob, case_id, tif, owner, qty):
    ob = OrdersDetails()
    execution_id = bca.client_orderid(4)
    ob.set_default_params(base_request)
    ob.set_extraction_id(execution_id)
    ob.set_filter(["Owner", owner, "Qty", qty])
    child_1_tif = ExtractionDetail("child_1.tif", "TIF")
    child_1_ext_action = ExtractionAction.create_extraction_action(
        extraction_detail=child_1_tif)
    child_1_info = OrderInfo.create(action=child_1_ext_action)

    child_orders_details = OrdersDetails.create(order_info_list=[child_1_info])

    ob_tif = ExtractionDetail("orderBook.tif", "TIF")
    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[ob_tif]),
            sub_order_details=child_orders_details))
    response = call(act_ob.getOrdersDetails, ob.request())
    verifier = Verifier(case_id)
    verifier.set_event_name("Check Order book")
    verifier.compare_values("Main order TIF", tif, response[ob_tif.name])
    verifier.compare_values("Check child order TIF", tif, response[child_1_tif.name])

    verifier.verify()


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]

    order_ticket_service = Stubs.win_act_order_ticket_fx
    ob_act = Stubs.win_act_order_book

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)

    set_base(session_id, case_id)
    ar_service = Stubs.win_act_aggregated_rates_service

    case_base_request = get_base_request(session_id, case_id)
    base_esp_details = BaseTileDetails(base=case_base_request)

    owner = Stubs.custom_config['qf_trading_fe_user']
    from_curr = "EUR"
    to_curr = "USD"
    tenor = "Spot"
    venue = ["CIT", "MS"]
    tif_fok = "FillOrKill"
    tif_iok = "ImmediateOrCancel"
    qty = "8000000"
    client = "ASPECT_CITI"
    try:
        # Step 1
        create_or_get_rates_tile(base_esp_details, ar_service)
        modify_rates_tile(base_esp_details, ar_service, from_curr, to_curr, tenor)
        filter_venue(base_esp_details, ar_service, venue)
        # Step 2
        place_order(base_esp_details, ar_service)
        modify_order_ticket(case_base_request, order_ticket_service, qty, tif_iok, client)
        check_order_book_2_child(case_base_request, ob_act, case_id, tif_iok, owner, qty)
        # Step 3
        place_order(base_esp_details, ar_service)
        modify_order_ticket(case_base_request, order_ticket_service, qty, tif_fok, client)
        check_order_book_1_child(case_base_request, ob_act, case_id, tif_fok, owner, qty)

    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        try:
            # Close tile
            call(ar_service.closeRatesTile, base_esp_details.build())

        except Exception:
            logging.error("Error execution", exc_info=True)
