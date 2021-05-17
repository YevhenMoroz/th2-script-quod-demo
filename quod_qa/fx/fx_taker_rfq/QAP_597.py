import logging
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.aggregated_rates_wrappers import ModifyRFQTileRequest, ContextAction
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
    verifier.compare_values('Venue', "HSBCR", response[qrb_venue.name])
    verifier.compare_values('Status', status, response[qrb_status.name])
    verifier.compare_values("QuoteStatus", quote_sts, response[qrb_quote_status.name])
    verifier.verify()


def check_quote_book(ex_id, base_request, service, case_id, owner, quote_sts):
    qb = QuoteDetailsRequest(base=base_request)
    qb.set_extraction_id(ex_id)
    qb_owner = ExtractionDetail("quoteBook.owner", "Owner")
    qb_quote_status = ExtractionDetail("quoteBook.quotestatus", "QuoteStatus")
    qb.add_extraction_details([qb_owner, qb_quote_status])
    response = call(service.getQuoteBookDetails, qb.request())

    verifier = Verifier(case_id)
    verifier.set_event_name("Check Quote book")
    verifier.compare_values('Owner', owner, response[qb_owner.name])
    verifier.compare_values('QuoteStatus', quote_sts, response[qb_quote_status.name])
    verifier.verify()


def cancel_rfq(base_request, service):
    call(service.cancelRFQ, base_request.build())


def execute(report_id):

    case_name = "QAP-597"
    quote_owner = "ostronov"
    case_venue = "HSB"
    case_qty = 1000000
    case_near_tenor = "Spot"
    case_from_currency = "EUR"
    case_to_currency = "USD"
    case_client = "MMCLIENT2"
    venue_list = ["CIT", "HSB"]
    quote_sts_new = 'New'
    quote_quote_sts_accepted = "Accepted"
    quote_quote_sts_terminated = "Terminated"

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)
    session_id = set_session_id()
    set_base(session_id, case_id)
    case_base_request = get_base_request(session_id, case_id)
    ar_service = Stubs.win_act_aggregated_rates_service
    base_rfq_details = BaseTileDetails(base=case_base_request)

    if not Stubs.frontend_is_open:
        prepare_fe_2(case_id, session_id)
    else:
        get_opened_fe(case_id, session_id)

    try:
        # Step 1
        create_or_get_rfq(base_rfq_details, ar_service)
        modify_rfq_tile(base_rfq_details, ar_service, case_qty, case_from_currency,
                        case_to_currency, case_near_tenor, case_client, venue_list)
        # Step 2
        send_rfq(base_rfq_details, ar_service)
        check_quote_request_b("QRB_0", case_base_request, ar_service, case_id,
                              quote_sts_new, quote_quote_sts_accepted, case_venue)

        check_quote_book("QB_0", case_base_request, ar_service, case_id, quote_owner, quote_quote_sts_accepted)
        # Step 3

        check_quote_request_b("QRB_0", case_base_request, ar_service, case_id,
                              quote_quote_sts_terminated, quote_quote_sts_terminated, case_venue)

        check_quote_book("QB_0", case_base_request, ar_service, case_id, quote_owner, quote_quote_sts_terminated)

        # Close tile
        call(ar_service.closeRFQTile, base_rfq_details.build())
    except Exception:
        logging.error("Error execution", exc_info=True)

