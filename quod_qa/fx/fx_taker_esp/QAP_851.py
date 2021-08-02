import logging
from pathlib import Path

from th2_grpc_act_gui_quod.common_pb2 import BaseTileData

from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.aggregated_rates_wrappers import ModifyRatesTileRequest, ContextActionRatesTile, ActionsRatesTile
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.order_ticket import ExtractFxOrderTicketValuesRequest, FXOrderDetails
from win_gui_modules.order_ticket_wrappers import NewFxOrderDetails
from win_gui_modules.utils import call, get_base_request
from win_gui_modules.wrappers import set_base


def create_or_get_rates_tile(base_request, service):
    call(service.createRatesTile, base_request.build())


def modify_rates_tile(base_request, service, from_c, to_c, tenor):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.set_instrument(from_c, to_c, tenor)
    call(service.modifyRatesTile, modify_request.build())


def open_direct_venue(base_request, service, venue):
    modify_request = ModifyRatesTileRequest(details=base_request)
    venue_filter = ContextActionRatesTile.create_venue_filter(venue)
    add_dve_action = ContextActionRatesTile.open_direct_venue_panel()
    modify_request.add_context_actions([venue_filter, add_dve_action])
    call(service.modifyRatesTile, modify_request.build())


def click_on_venue(base_request, service, venue):
    modify_request = ModifyRatesTileRequest(details=base_request)
    click_to_venue = ActionsRatesTile.click_to_ask_esp_order(venue)
    modify_request.add_action(click_to_venue)
    call(service.modifyRatesTile, modify_request.build())


def check_algo_disabled(base_request, service, case_id):
    request = ExtractFxOrderTicketValuesRequest(base_request)
    request.get_is_algo_checked()
    response = call(service.extractFxOrderTicketValues, request.build())
    verifier = Verifier(case_id)
    verifier.set_event_name("Check Algo disabled")
    verifier.compare_values("Unchecked", "", response["fx_order_ticket.is_algo_checked"])
    verifier.verify()


def close_order_ticket(base_request, service):
    order_ticket = FXOrderDetails()
    order_ticket.set_close(True)

    new_order_details = NewFxOrderDetails(base_request, order_ticket)
    call(service.placeFxOrder, new_order_details.build())


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)

    set_base(session_id, case_id)
    ar_service = Stubs.win_act_aggregated_rates_service
    order_ticket_service = Stubs.win_act_order_ticket_fx

    case_base_request = get_base_request(session_id, case_id)
    base_esp_details = BaseTileDetails(base=case_base_request)
    base_tile_data = BaseTileData(base=case_base_request)

    from_curr = "EUR"
    to_curr = "USD"
    tenor = "Spot"
    venue = "CIT"

    try:
        # Step 1
        create_or_get_rates_tile(base_esp_details, ar_service)
        modify_rates_tile(base_esp_details, ar_service, from_curr, to_curr, tenor)
        open_direct_venue(base_esp_details, ar_service, venue)
        click_on_venue(base_esp_details, ar_service, venue)
        check_algo_disabled(base_tile_data, order_ticket_service, case_id)

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
