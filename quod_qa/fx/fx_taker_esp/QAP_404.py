import logging
from pathlib import Path

from th2_grpc_act_gui_quod.common_pb2 import BaseTileData

from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.aggregated_rates_wrappers import ExtractRatesTileDataRequest
from win_gui_modules.aggregated_rates_wrappers import ModifyRatesTileRequest, PlaceESPOrder, ESPTileOrderSide
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.order_ticket import FXOrderDetails, ExtractFxOrderTicketValuesRequest
from win_gui_modules.order_ticket_wrappers import NewFxOrderDetails
from win_gui_modules.utils import call, set_session_id, get_base_request, prepare_fe_2, get_opened_fe
from win_gui_modules.wrappers import set_base


def create_or_get_rates_tile(base_request, service):
    call(service.createRatesTile, base_request.build())


def modify_rates_tile(base_request, service, from_c, to_c, tenor):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.set_instrument(from_c, to_c, tenor)
    call(service.modifyRatesTile, modify_request.build())


def check_digit_price_on_esp(base_request, service, case_id):
    extraction_value = ExtractRatesTileDataRequest(details=base_request)
    extraction_id = bca.client_orderid(4)
    extraction_value.set_extraction_id(extraction_id)
    extraction_value.extract_best_bid_large("ratesTile.bidLarge")
    extraction_value.extract_best_bid_small("ratesTile.bidSmall")
    response = call(service.extractRatesTileValues, extraction_value.build())
    bid_large = response["ratesTile.bidLarge"].replace(".", "")
    bid_small = response["ratesTile.bidSmall"]

    verifier = Verifier(case_id)
    verifier.set_event_name("Check number of digits")
    verifier.compare_values("Large part", "3", str(len(bid_large)))
    verifier.compare_values("Small part", "3", str(len(bid_small)))
    verifier.verify()


def check_digit_price_in_ord_ticket(base_request, service, case_id):
    extract_value = ExtractFxOrderTicketValuesRequest(base_request)
    extract_value.get_price_large("orderTicket.largePrice")
    extract_value.get_price_pips("orderTicket.pipsPrice")
    response = call(service.extractFxOrderTicketValues, extract_value.build())
    large_price = response["orderTicket.largePrice"].replace(".", "")
    pips_price = response["orderTicket.pipsPrice"]

    verifier = Verifier(case_id)
    verifier.set_event_name("Check number of digits")
    verifier.compare_values("Large part", "3", str(len(large_price)))
    verifier.compare_values("Small part", "3", str(len(pips_price)))
    verifier.verify()


def place_order(base_request, service):
    esp_request = PlaceESPOrder(details=base_request)
    esp_request.set_action(ESPTileOrderSide.BUY)
    esp_request.top_of_book()
    call(service.placeESPOrder, esp_request.build())


def close_order_ticket(base_request, service):
    order_ticket = FXOrderDetails()
    order_ticket.set_close()
    new_order_details = NewFxOrderDetails(base_request, order_ticket)
    call(service.placeFxOrder, new_order_details.build())


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]

    order_ticket_service = Stubs.win_act_order_ticket_fx
    ar_service = Stubs.win_act_aggregated_rates_service

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)
    
    set_base(session_id, case_id)

    case_base_request = get_base_request(session_id, case_id)
    base_esp_details = BaseTileDetails(base=case_base_request)
    base_tile_data = BaseTileData(base=case_base_request)

    from_curr = "EUR"
    to_curr = "JPY"
    tenor = "Spot"

    try:
        if not Stubs.frontend_is_open:
            prepare_fe_2(case_id, session_id)
        else:
            get_opened_fe(case_id, session_id)
        # Step 1
        create_or_get_rates_tile(base_esp_details, ar_service)
        modify_rates_tile(base_esp_details, ar_service, from_curr, to_curr, tenor)
        check_digit_price_on_esp(base_esp_details, ar_service, case_id)
        # Step 2
        place_order(base_esp_details, ar_service)
        check_digit_price_in_ord_ticket(base_tile_data, order_ticket_service, case_id)
        close_order_ticket(case_base_request, order_ticket_service)

    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        try:
            # Close tile
            call(ar_service.closeRatesTile, base_esp_details.build())
        except Exception:
            logging.error("Error execution", exc_info=True)
