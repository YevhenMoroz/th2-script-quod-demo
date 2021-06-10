import logging

from pathlib import Path
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.aggregated_rates_wrappers import RFQTileOrderSide, PlaceRFQRequest, ModifyRFQTileRequest, \
    ContextAction
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.order_book_wrappers import ExtractionDetail
from win_gui_modules.quote_wrappers import QuoteDetailsRequest
from win_gui_modules.utils import set_session_id, prepare_fe_2, get_base_request, call, get_opened_fe
from win_gui_modules.wrappers import set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def create_or_get_rfq(base_request, service):
    call(service.createRFQTile, base_request.build())


def send_rfq(base_request, service):
    call(service.sendRFQOrder, base_request.build())


def modify_rfq_tile(base_request, service, near_qty, cur1, cur2, near_date, far_date, client, venues):
    modify_request = ModifyRFQTileRequest(details=base_request)
    action = ContextAction.create_venue_filters(venues)
    modify_request.add_context_action(action)
    modify_request.set_settlement_date(bca.get_t_plus_date(near_date))
    modify_request.set_far_leg_settlement_date(bca.get_t_plus_date(far_date))
    modify_request.set_quantity(near_qty)
    modify_request.set_from_currency(cur1)
    modify_request.set_to_currency(cur2)
    modify_request.set_client(client)
    call(service.modifyRFQTile, modify_request.build())


def place_order_tob(base_request, service):
    rfq_request = PlaceRFQRequest(details=base_request)
    rfq_request.set_action(RFQTileOrderSide.BUY)
    call(service.placeRFQOrder, rfq_request.build())


def cancel_rfq(base_request, service):
    call(service.cancelRFQ, base_request.build())


def check_quote_request_b(base_request, service, case_id, status, quote_sts, venue, user):
    qrb = QuoteDetailsRequest(base=base_request)
    execution_id = bca.client_orderid(4)
    qrb.set_extraction_id(execution_id)
    qrb.set_filter(["Venue", venue])
    qrb_venue = ExtractionDetail("quoteRequestBook.venue", "Venue")
    qrb_status = ExtractionDetail("quoteRequestBook.status", "Status")
    qrb_quote_status = ExtractionDetail("quoteRequestBook.qoutestatus", "QuoteStatus")
    qrb_user = ExtractionDetail("quoteRequestBook.user", "User")
    qrb.add_extraction_details([qrb_venue, qrb_status, qrb_quote_status, qrb_user])
    response = call(service.getQuoteRequestBookDetails, qrb.request())

    verifier = Verifier(case_id)
    verifier.set_event_name("Check QuoteRequest book")
    verifier.compare_values('Venue', venue, response[qrb_venue.name])
    verifier.compare_values('Status', status, response[qrb_status.name])
    verifier.compare_values("QuoteStatus", quote_sts, response[qrb_quote_status.name])
    verifier.compare_values("User", user, response[qrb_user.name])
    verifier.verify()


def execute(report_id):
    ar_service = Stubs.win_act_aggregated_rates_service

    case_name = Path(__file__).name[:-3]
    quote_owner = Stubs.custom_config['qf_trading_fe_user_309']
    case_venue_hsbcr = "HSBCR"
    case_qty = 1000000
    case_near_date = 2
    case_far_date = 3
    case_currency_eur = "EUR"
    case_currency_usd = "USD"
    case_client = "ASPECT_CITI"
    venues_hsb = ["HSB"]
    quote_sts_new = 'New'
    quote_quote_sts_accepted = "Accepted"
    quote_quote_sts_terminated = "Terminated"

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)
    session_id = set_session_id()
    set_base(session_id, case_id)
    case_base_request = get_base_request(session_id, case_id)

    base_rfq_details = BaseTileDetails(base=case_base_request, window_index=0)

    try:
        if not Stubs.frontend_is_open:
            prepare_fe_2(case_id, session_id)
        else:
            get_opened_fe(case_id, session_id)
        # Step 1
        create_or_get_rfq(base_rfq_details, ar_service)

        modify_rfq_tile(base_rfq_details, ar_service, case_qty, case_currency_eur,
                        case_currency_usd, case_near_date, case_far_date, case_client, venues_hsb)
        # Step 2
        send_rfq(base_rfq_details, ar_service)

        check_quote_request_b(case_base_request, ar_service, case_id, quote_sts_new,
                              quote_quote_sts_accepted, case_venue_hsbcr, quote_owner)
        place_order_tob(base_rfq_details, ar_service)
        # Step 3
        check_quote_request_b(case_base_request, ar_service, case_id, quote_quote_sts_terminated,
                              quote_quote_sts_terminated, case_venue_hsbcr, quote_owner)

    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        try:
            # Close tile
            call(ar_service.closeRFQTile, base_rfq_details.build())
        except Exception:
            logging.error("Error execution", exc_info=True)
