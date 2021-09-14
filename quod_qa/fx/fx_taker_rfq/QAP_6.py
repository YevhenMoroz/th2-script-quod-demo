import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.aggregated_rates_wrappers import ModifyRFQTileRequest, \
    ContextAction
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.order_book_wrappers import ExtractionDetail
from win_gui_modules.quote_wrappers import QuoteDetailsRequest
from win_gui_modules.utils import set_session_id, prepare_fe_2, get_base_request, call, get_opened_fe
from win_gui_modules.wrappers import set_base


def create_or_get_rfq(base_request, service):
    call(service.createRFQTile, base_request.build())


def send_rfq(base_request, service):
    call(service.sendRFQOrder, base_request.build())


def cancel_rfq(base_request, service):
    call(service.cancelRFQ, base_request.build())


def modify_rfq_tile(base_request, service, near_qty, cur1, cur2, near_tenor, client, venues):
    modify_request = ModifyRFQTileRequest(details=base_request)
    action = ContextAction.create_venue_filters(venues)
    modify_request.add_context_action(action)
    modify_request.set_near_tenor(near_tenor)
    modify_request.set_quantity(near_qty)
    modify_request.set_from_currency(cur1)
    modify_request.set_to_currency(cur2)
    modify_request.set_client(client)
    call(service.modifyRFQTile, modify_request.build())


def check_quote_request_b(ex_id, base_request, service, case_id, status, quote_sts, venue):
    qrb = QuoteDetailsRequest(base=base_request)
    qrb.set_extraction_id(ex_id)
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


def execute(report_id, session_id):
    ar_service = Stubs.win_act_aggregated_rates_service

    case_name = Path(__file__).name[:-3]
    case_client = "ASPECT_CITI"
    case_eur_currency = "EUR"
    case_usd_currency = "USD"
    case_ndf_currency = "PHP"
    case_near_tenor = "Spot"
    case_far_tenor = "1W"
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
    modify_request = ModifyRFQTileRequest(base_rfq_details)

    try:
        
        # Step 1
        create_or_get_rfq(base_rfq_details, ar_service)

        # Step 2
        modify_rfq_tile(base_rfq_details, ar_service, case_qty, case_eur_currency, case_usd_currency, case_near_tenor,
                        case_client, case_venue)
        send_rfq(base_rfq_details, ar_service)
        check_quote_request_b("QR_0", case_base_request, ar_service, case_id, quote_sts_new,
                              quote_quote_sts_accepted, case_filter_venue)

        # Step 3
        modify_request.set_from_currency(case_usd_currency)
        modify_request.set_to_currency(case_ndf_currency)
        call(ar_service.modifyRFQTile, modify_request.build())
        send_rfq(base_rfq_details, ar_service)
        check_quote_request_b("QR_1", case_base_request, ar_service, case_id, quote_sts_new,
                              quote_quote_sts_accepted, case_filter_venue)

        # Step 4
        modify_request.set_from_currency(case_eur_currency)
        modify_request.set_to_currency(case_usd_currency)
        modify_request.set_far_leg_tenor(case_far_tenor)
        call(ar_service.modifyRFQTile, modify_request.build())
        send_rfq(base_rfq_details, ar_service)
        check_quote_request_b("QR_2", case_base_request, ar_service, case_id, quote_sts_new,
                              quote_quote_sts_accepted, case_filter_venue)

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
    finally:
        try:
            # Close tile
            call(ar_service.closeRFQTile, base_rfq_details.build())
        except Exception:
            logging.error("Error execution", exc_info=True)