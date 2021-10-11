import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.aggregated_rates_wrappers import ModifyRFQTileRequest, ContextAction, ExtractRFQTileValues, \
    TableActionsRequest, TableAction, CellExtractionDetails
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.order_book_wrappers import ExtractionDetail
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


def check_value_in_tob(base_request, service, case_id):
    extract_value = ExtractRFQTileValues(details=base_request)
    extraction_id = bca.client_orderid(4)
    extract_value.set_extraction_id(extraction_id)
    extract_value.extract_best_bid("ar_rfq.extract_best_bid")
    response = call(service.extractRFQTileValues, extract_value.build())
    tob_len = len(response["ar_rfq.extract_best_bid"][2:])
    verifier = Verifier(case_id)
    verifier.set_event_name("Check digits in TOB")
    verifier.compare_values("Number of digits in TOB", "5", str(tob_len))
    verifier.verify()


def check_value_dist(base_request, service, case_id, venue):
    extract_value = ExtractRFQTileValues(details=base_request)
    extraction_id = bca.client_orderid(4)
    extract_value.set_extraction_id(extraction_id)
    table_actions_request = TableActionsRequest(details=base_request)
    extraction_id = bca.client_orderid(4)
    table_actions_request.set_extraction_id(extraction_id)
    extract_pts = TableAction.extract_cell_value(CellExtractionDetails("PTSSell", "Pts", venue[0], 0))
    extract_dist = TableAction.extract_cell_value(CellExtractionDetails("DistSell", "Dist", venue[0], 0))
    table_actions_request.add_actions([extract_pts, extract_dist])
    extract_value.extract_best_bid_small("ar_rfq.extract_best_bid_small")
    extract_table = call(service.processTableActions, table_actions_request.build())
    extract_bid = call(service.extractRFQTileValues, extract_value.build())
    extracted_bid = extract_bid["ar_rfq.extract_best_bid_small"]
    extracted_dist = extract_table["DistSell"]
    extracted_pts = extract_table["PTSSell"]
    distance = float(extracted_bid) - float(extracted_pts)
    verifier = Verifier(case_id)
    verifier.set_event_name("Check column Pts and Dist")
    verifier.compare_values("Dist", str(distance), extracted_dist)
    verifier.verify()


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


def check_column_spot(base_request, service, case_id, venue):
    table_actions_request = TableActionsRequest(details=base_request)
    extraction_id = bca.client_orderid(4)
    table_actions_request.set_extraction_id(extraction_id)
    extract_pts = TableAction.extract_cell_value(CellExtractionDetails("PTSSell", "Pts", venue[0], 0))
    table_actions_request.add_action(extract_pts)
    extract_table = call(service.processTableActions, table_actions_request.build())
    spot = extract_table["PTSSell"]
    if len(spot) > 0:
        displayed = "Yes"
    else:
        displayed = "No"
    verifier = Verifier(case_id)
    verifier.set_event_name("Check column Spot")
    verifier.compare_values("Spot is displayed", displayed, "Yes")
    verifier.verify()


def check_value_in_header(base_request, service, case_id, value):
    table_actions_request = TableActionsRequest(details=base_request)
    extraction_id = bca.client_orderid(4)
    table_actions_request.set_extraction_id(extraction_id)
    extract_header = TableAction.extract_headers(colIndexes=[3])
    table_actions_request.add_action(extract_header)
    response = call(service.processTableActions, table_actions_request.build())

    verifier = Verifier(case_id)
    verifier.set_event_name("Check value in header column")
    verifier.compare_values("Tenor value", value, response['Headers'].split(';')[0])
    verifier.verify()


def execute(report_id, session_id):
    ar_service = Stubs.win_act_aggregated_rates_service
    case_name = Path(__file__).name[:-3]
    case_client = "ASPECT_CITI"
    case_from_currency = "EUR"
    case_to_currency = "USD"
    case_tenor = "1M"
    case_venue = ["CITI"]
    case_filter_venue = "CITI"
    case_qty = 2000000
    quote_sts_new = 'New'
    quote_quote_sts_accepted = "Accepted"

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)
    
    set_base(session_id, case_id)
    case_base_request = get_base_request(session_id, case_id)
    base_rfq_details = BaseTileDetails(base=case_base_request)

    try:

        # Step 1
        create_or_get_rfq(base_rfq_details, ar_service)
        modify_rfq_tile(base_rfq_details, ar_service, case_qty, case_from_currency,
                        case_to_currency, case_tenor, case_client, case_venue)
        send_rfq(base_rfq_details, ar_service)
        check_quote_request_b(case_base_request, ar_service, case_id, quote_sts_new,
                              quote_quote_sts_accepted, case_filter_venue)
        # Step 2
        # TODO Add check countdown
        # Step 3
        check_value_in_tob(base_rfq_details, ar_service, case_id)
        # Step 4
        check_value_dist(base_rfq_details, ar_service, case_id, case_venue)
        # Step 5
        check_value_in_header(base_rfq_details, ar_service, case_id, case_tenor)
        # Step 6
        check_column_spot(base_rfq_details, ar_service, case_id, case_venue)

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
    finally:
        try:
            # Close tile
            call(ar_service.closeRFQTile, base_rfq_details.build())
        except Exception:
            logging.error("Error execution", exc_info=True)
