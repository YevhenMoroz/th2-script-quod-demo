import logging
import time
from pathlib import Path
from th2_grpc_hand import rhbatch_pb2
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.aggregated_rates_wrappers import ModifyRFQTileRequest, ContextAction, \
    TableActionsRequest, TableAction
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.order_book_wrappers import ExtractionDetail
from win_gui_modules.utils import set_session_id, prepare_fe_2, get_base_request, call, get_opened_fe, close_fe
from win_gui_modules.wrappers import set_base


def create_or_get_rfq(base_request, service):
    call(service.createRFQTile, base_request.build())


def modify_rfq_tile(base_request, service, from_curr, to_curr, venues):
    modify_request = ModifyRFQTileRequest(details=base_request)
    action = ContextAction.create_venue_filters(venues)
    modify_request.add_context_action(action)
    modify_request.set_from_currency(from_curr)
    modify_request.set_to_currency(to_curr)
    call(service.modifyRFQTile, modify_request.build())


def check_venue(base_request, service, case_id, hsb, cit, ms):
    table_actions_request = TableActionsRequest(details=base_request)
    check1 = TableAction.create_check_table_venue(ExtractionDetail("aggrRfqTile.hsbVenue", hsb))
    check2 = TableAction.create_check_table_venue(ExtractionDetail("aggrRfqTile.citVenue", cit))
    check3 = TableAction.create_check_table_venue(ExtractionDetail("aggrRfqTile.msVenue", ms))
    table_actions_request.set_extraction_id("extrId")
    table_actions_request.add_actions([check1, check2, check3])
    response = call(service.processTableActions, table_actions_request.build())

    verifier = Verifier(case_id)
    verifier.set_event_name("Check Venues")
    verifier.compare_values("Venue CIT", "found", response["aggrRfqTile.citVenue"])
    verifier.compare_values("Venue MS", "not found", response["aggrRfqTile.msVenue"])
    verifier.compare_values("Venue HSB", "found", response["aggrRfqTile.hsbVenue"])
    verifier.verify()


def execute(report_id):
    ar_service = Stubs.win_act_aggregated_rates_service

    case_name = Path(__file__).name[:-3]
    case_venues_filter = ["HSB", "CIT"]
    case_from_curr = "EUR"
    case_to_curr = "USD"
    venue_cit = "CIT"
    venue_hsb = "HSB"
    venue_ms = "MS"

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)
    session_id = set_session_id()
    session_id2 = Stubs.win_act.register(
        rhbatch_pb2.RhTargetServer(target=Stubs.custom_config['target_server_win'])).sessionID
    set_base(session_id, case_id)
    case_base_request = get_base_request(session_id, case_id)
    case_base_request_2 = get_base_request(session_id2, case_id)

    base_rfq_details = BaseTileDetails(base=case_base_request)
    base_rfq_details_2 = BaseTileDetails(base=case_base_request_2)

    if not Stubs.frontend_is_open:
        prepare_fe_2(case_id, session_id)
    else:
        get_opened_fe(case_id, session_id)
    try:
        # Step 1
        create_or_get_rfq(base_rfq_details, ar_service)
        modify_rfq_tile(base_rfq_details, ar_service, case_from_curr, case_to_curr, case_venues_filter)
        check_venue(base_rfq_details, ar_service, case_id, venue_hsb, venue_cit, venue_ms)
        close_fe(case_id, session_id)
        time.sleep(5)
        prepare_fe_2(case_id, session_id2)
        create_or_get_rfq(base_rfq_details_2, ar_service)
        check_venue(base_rfq_details_2, ar_service, case_id, venue_hsb, venue_cit, venue_ms)

        # Close tile
        call(ar_service.closeRFQTile, base_rfq_details.build())

    except Exception:
        logging.error("Error execution", exc_info=True)
