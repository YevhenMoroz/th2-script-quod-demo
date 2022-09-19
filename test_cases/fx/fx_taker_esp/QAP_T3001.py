import logging
from pathlib import Path

from th2_grpc_act_gui_quod.common_pb2 import BaseTileData

from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.aggregated_rates_wrappers import ModifyRatesTileRequest, PlaceESPOrder, ESPTileOrderSide, \
    ExtractRatesTileDataRequest
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.order_ticket import FXOrderDetails, ExtractFxOrderTicketValuesRequest
from win_gui_modules.order_ticket_wrappers import NewFxOrderDetails
from win_gui_modules.utils import call, set_session_id, get_base_request, prepare_fe_2, get_opened_fe
from win_gui_modules.wrappers import set_base


def create_or_get_rates_tile(base_request, service):
    call(service.createRatesTile, base_request.build())


def modify_order_ticket(base_request, service, qty):
    order_ticket = FXOrderDetails()
    order_ticket.set_qty(qty)
    new_order_details = NewFxOrderDetails(base_request, order_ticket)
    call(service.placeFxOrder, new_order_details.build())


def close_order_ticket(base_request, service):
    order_ticket = FXOrderDetails()
    order_ticket.set_close()
    new_order_details = NewFxOrderDetails(base_request, order_ticket)
    call(service.placeFxOrder, new_order_details.build())


def place_order(base_request, service):
    rfq_request = PlaceESPOrder(details=base_request)
    rfq_request.set_action(ESPTileOrderSide.BUY)
    rfq_request.top_of_book()
    call(service.placeESPOrder, rfq_request.build())


def modify_rates_tile(base_request, service, qty):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.set_quantity(qty)
    call(service.modifyRatesTile, modify_request.build())


def check_qty_in_tile(base_request, service, case_id, qty):
    extraction_value = ExtractRatesTileDataRequest(details=base_request)
    extraction_id = bca.client_orderid(4)
    extraction_value.set_extraction_id(extraction_id)
    extraction_value.extract_quantity("ratestile.qty")
    response = call(service.extractRatesTileValues, extraction_value.build())
    extracted_qty = response["ratestile.qty"].replace(',', '')[:-3]

    verifier = Verifier(case_id)
    verifier.set_event_name("Check qty it tile")
    verifier.compare_values("Qty", qty, extracted_qty)
    verifier.verify()


def check_qty_in_ord_t(base_request, service, case_id, qty):
    extract_value = ExtractFxOrderTicketValuesRequest(base_request)
    extract_value.get_quantity("orderTicket.qty")
    response = call(service.extractFxOrderTicketValues, extract_value.build())
    extracted_qty = response["orderTicket.qty"].replace(',', '')

    verifier = Verifier(case_id)
    verifier.set_event_name("Check qty in order ticket")
    verifier.compare_values("Qty", qty, extracted_qty)
    verifier.verify()


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    order_ticket_service = Stubs.win_act_order_ticket_fx
    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)
    
    set_base(session_id, case_id)
    ar_service = Stubs.win_act_aggregated_rates_service

    case_base_request = get_base_request(session_id, case_id)
    base_esp_details = BaseTileDetails(base=case_base_request)
    base_data = BaseTileData(base=case_base_request)

    try:
        # Step 1
        create_or_get_rates_tile(base_esp_details, ar_service)
        # Step 2
        modify_rates_tile(base_esp_details, ar_service, "1m")
        check_qty_in_tile(base_esp_details, ar_service, case_id, "1000000.00")
        # Step 3
        modify_rates_tile(base_esp_details, ar_service, "1k")
        check_qty_in_tile(base_esp_details, ar_service, case_id, "1000.00")
        # Step 4
        modify_rates_tile(base_esp_details, ar_service, "1b")
        check_qty_in_tile(base_esp_details, ar_service, case_id, "1000000000.00")
        # Step 5
        modify_rates_tile(base_esp_details, ar_service, "1kk")
        check_qty_in_tile(base_esp_details, ar_service, case_id, "1000.00")
        # Step 6
        place_order(base_esp_details, ar_service)
        modify_order_ticket(case_base_request, order_ticket_service, "1m")
        check_qty_in_ord_t(base_data, order_ticket_service, case_id, "1000000.00")
        modify_order_ticket(case_base_request, order_ticket_service, "1k")
        check_qty_in_ord_t(base_data, order_ticket_service, case_id, "1000.00")
        modify_order_ticket(case_base_request, order_ticket_service, "1kk")
        check_qty_in_ord_t(base_data, order_ticket_service, case_id, "1000.00")
        close_order_ticket(case_base_request, order_ticket_service)

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
    finally:
        try:
            # Close tile
            call(ar_service.closeRatesTile, base_esp_details.build())
        except Exception:
            logging.error("Error execution", exc_info=True)
