import logging
from pathlib import Path

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


def check_quote_book(base_request, service, case_id, owner, quote_sts, venue):
    qb = QuoteDetailsRequest(base=base_request)
    extraction_id = bca.client_orderid(4)
    qb.set_extraction_id(extraction_id)
    qb.set_filter(["Venue", venue])
    qb_owner = ExtractionDetail("quoteBook.owner", "Owner")
    qb_quote_status = ExtractionDetail("quoteBook.quotestatus", "QuoteStatus")
    qb_id = ExtractionDetail("quoteBook.id", "Id")
    qb.add_extraction_details([qb_owner, qb_quote_status, qb_id])
    response = call(service.getQuoteBookDetails, qb.request())

    verifier = Verifier(case_id)
    verifier.set_event_name("Check Quote book")
    verifier.compare_values('Owner', owner, response[qb_owner.name])
    verifier.compare_values('QuoteStatus', quote_sts, response[qb_quote_status.name])
    verifier.verify()


# TODO Change in webadmin->Venue->CITIR->SuportQuoteCancel


def execute(report_id, session_id):
    ar_service = Stubs.win_act_aggregated_rates_service

    case_name = Path(__file__).name[:-3]
    case_client = "ASPECT_CITI"
    case_from_currency = "EUR"
    case_to_currency = "USD"
    case_near_tenor = "Spot"
    case_venue = ["CITI", "JPM"]
    case_filter_venue = "CITI"
    case_filter_venue_1 = "JPM"
    case_qty = 10000000
    case_quote_owner = Stubs.custom_config['qf_trading_fe_user']
    quote_sts_new = 'New'
    quote_sts_terminated = "Terminated"
    quote_sts_accepted = "Accepted"

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
                              quote_sts_new, quote_sts_accepted, case_filter_venue_1)
        check_quote_request_b(case_base_request, ar_service, case_id,
                              quote_sts_new, quote_sts_accepted, case_filter_venue)

        check_quote_book(case_base_request, ar_service, case_id, case_quote_owner,
                         quote_sts_accepted, case_filter_venue_1)
        check_quote_book(case_base_request, ar_service, case_id, case_quote_owner,
                         quote_sts_accepted, case_filter_venue)

        # Step 2
        cancel_rfq(base_rfq_details, ar_service)
        check_quote_request_b(case_base_request, ar_service, case_id,
                              quote_sts_terminated, quote_sts_terminated, case_filter_venue_1)
        check_quote_request_b(case_base_request, ar_service, case_id,
                              quote_sts_terminated, quote_sts_terminated, case_filter_venue)

        check_quote_book(case_base_request, ar_service, case_id, case_quote_owner,
                         quote_sts_terminated, case_filter_venue_1)
        check_quote_book(case_base_request, ar_service, case_id, case_quote_owner,
                         quote_sts_terminated, case_filter_venue)

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
    finally:
        try:
            # Close tile
            call(ar_service.closeRFQTile, base_rfq_details.build())
        except Exception:
            logging.error("Error execution", exc_info=True)
