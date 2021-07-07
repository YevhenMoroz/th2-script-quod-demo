import logging
import time
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.aggregated_rates_wrappers import RFQTileOrderSide, PlaceRFQRequest, ModifyRFQTileRequest, \
    ContextAction
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.order_book_wrappers import OrdersDetails, OrderInfo, ExtractionDetail, ExtractionAction
from win_gui_modules.quote_wrappers import QuoteDetailsRequest
from win_gui_modules.utils import set_session_id, prepare_fe_2, get_base_request, call, get_opened_fe
from win_gui_modules.wrappers import set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def create_or_get_rfq(base_request, service):
    call(service.createRFQTile, base_request.build())


def send_rfq(base_request, service):
    call(service.sendRFQOrder, base_request.build())


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


def place_order_tob(base_request, service):
    rfq_request = PlaceRFQRequest(details=base_request)
    rfq_request.set_action(RFQTileOrderSide.BUY)
    call(service.placeRFQOrder, rfq_request.build())


def cancel_rfq(base_request, service):
    call(service.cancelRFQ, base_request.build())


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
    verifier.compare_values('Venue', venue, response[qrb_venue.name])
    verifier.compare_values('Status', status, response[qrb_status.name])
    verifier.compare_values("QuoteStatus", quote_sts, response[qrb_quote_status.name])
    verifier.verify()


def check_quote_book(ex_id, base_request, service, case_id, owner, quote_id, status):
    qb = QuoteDetailsRequest(base=base_request)
    qb.set_extraction_id(ex_id)
    qb.set_filter(["Id", quote_id])
    qb_owner = ExtractionDetail("quoteBook.owner", "Owner")
    qb_quote_status = ExtractionDetail("quoteBook.quotestatus", "QuoteStatus")
    qb_id = ExtractionDetail("quoteBook.id", "Id")
    qb.add_extraction_details([qb_owner, qb_quote_status, qb_id])
    response = call(service.getQuoteBookDetails, qb.request())

    verifier = Verifier(case_id)
    verifier.set_event_name("Check Quote book")
    verifier.compare_values('Owner', owner, response[qb_owner.name])
    verifier.compare_values('QuoteStatus', status, response[qb_quote_status.name])
    verifier.compare_values("QuoteID", quote_id, response[qb_id.name])
    verifier.verify()


def check_order_book(ex_id, base_request, instr_type, act_ob, case_id, qty, venue):
    ob = OrdersDetails()
    ob.set_default_params(base_request)
    ob.set_extraction_id(ex_id)
    ob.set_filter(["Venue", venue])
    ob_instr_type = ExtractionDetail("orderBook.instrtype", "InstrType")
    ob_exec_sts = ExtractionDetail("orderBook.execsts", "ExecSts")
    ob_quote_id = ExtractionDetail("orderBook.quoteid", "QuoteID")
    ob_qty = ExtractionDetail("orderBook.qty", "Qty")
    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[ob_instr_type,
                                                                                 ob_exec_sts,
                                                                                 ob_quote_id,
                                                                                 ob_qty])))
    response = call(act_ob.getOrdersDetails, ob.request())
    verifier = Verifier(case_id)
    verifier.set_event_name("Check Order book")
    verifier.compare_values('InstrType', instr_type, response[ob_instr_type.name])
    verifier.compare_values('Sts', 'Filled', response[ob_exec_sts.name])
    verifier.compare_values("Qty", str(qty), response[ob_qty.name].replace(',', ''))
    verifier.verify()
    return response[ob_quote_id.name]


def execute(report_id, session_id):
    ar_service = Stubs.win_act_aggregated_rates_service
    ob_act = Stubs.win_act_order_book

    case_name = Path(__file__).name[:-3]
    quote_owner = Stubs.custom_config['qf_trading_fe_user_309']
    case_instr_type_ndf = "NDF"
    case_instr_type_fwd = "FXForward"
    case_venue_hsbcr = "HSBCR"
    case_venue_citir = "CITIR"
    case_qty = 1000000
    case_tenor_1m = "1M"
    case_tenor_2m = "2M"
    case_currency_usd = "USD"
    case_currency_php = "PHP"
    case_currency_cad = "CAD"
    case_client = "ASPECT_CITI"
    venues_hsb = ["HSBC"]
    venues_cit = ["CIT"]
    quote_sts_new = 'New'
    quote_sts_terminated = 'Terminated'
    quote_quote_sts_accepted = "Accepted"

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)

    set_base(session_id, case_id)
    case_base_request = get_base_request(session_id, case_id)

    base_rfq_details_0 = BaseTileDetails(base=case_base_request, window_index=0)
    base_rfq_details_1 = BaseTileDetails(base=case_base_request, window_index=1)

    try:
        # Step 1
        create_or_get_rfq(base_rfq_details_0, ar_service)
        create_or_get_rfq(base_rfq_details_1, ar_service)

        modify_rfq_tile(base_rfq_details_0, ar_service, case_qty, case_currency_usd,
                        case_currency_php, case_tenor_1m, case_client, venues_hsb)
        modify_rfq_tile(base_rfq_details_1, ar_service, case_qty, case_currency_usd,
                        case_currency_cad, case_tenor_2m, case_client, venues_cit)
        # Step 2
        send_rfq(base_rfq_details_0, ar_service)
        send_rfq(base_rfq_details_1, ar_service)

        check_quote_request_b("QRB_0", case_base_request, ar_service, case_id,
                              quote_sts_new, quote_quote_sts_accepted, case_venue_hsbcr)
        check_quote_request_b("QRB_1", case_base_request, ar_service, case_id,
                              quote_sts_new, quote_quote_sts_accepted, case_venue_citir)
        # Step 3
        place_order_tob(base_rfq_details_0, ar_service)
        place_order_tob(base_rfq_details_1, ar_service)

        quote_hsbcr = check_order_book("OB_0", case_base_request, case_instr_type_ndf, ob_act, case_id,
                                       case_qty, case_venue_hsbcr)
        quote_citir = check_order_book("OB_1", case_base_request, case_instr_type_fwd, ob_act, case_id,
                                       case_qty, case_venue_citir)

        check_quote_book("QB_0", case_base_request, ar_service, case_id, quote_owner,
                         quote_hsbcr, quote_sts_terminated)
        check_quote_book("QB_1", case_base_request, ar_service, case_id, quote_owner,
                         quote_citir, quote_sts_terminated)

        time.sleep(10)
        # Step 4
        send_rfq(base_rfq_details_0, ar_service)
        send_rfq(base_rfq_details_1, ar_service)

        check_quote_request_b("QRB_2", case_base_request, ar_service, case_id,
                              quote_sts_new, quote_quote_sts_accepted, case_venue_hsbcr)
        check_quote_request_b("QRB_3", case_base_request, ar_service, case_id,
                              quote_sts_new, quote_quote_sts_accepted, case_venue_citir)
        # Step 5
        place_order_tob(base_rfq_details_0, ar_service)
        place_order_tob(base_rfq_details_1, ar_service)

        quote_hsbcr = check_order_book("OB_2", case_base_request, case_instr_type_ndf, ob_act, case_id,
                                       case_qty, case_venue_hsbcr)
        quote_citir = check_order_book("OB_3", case_base_request, case_instr_type_fwd, ob_act, case_id,
                                       case_qty, case_venue_citir)

        check_quote_book("QB_2", case_base_request, ar_service, case_id, quote_owner,
                         quote_hsbcr, quote_sts_terminated)
        check_quote_book("QB_3", case_base_request, ar_service, case_id, quote_owner,
                         quote_citir, quote_sts_terminated)
        time.sleep(10)

        # Step 6
        send_rfq(base_rfq_details_0, ar_service)
        send_rfq(base_rfq_details_1, ar_service)

        check_quote_request_b("QRB_4", case_base_request, ar_service, case_id,
                              quote_sts_new, quote_quote_sts_accepted, case_venue_hsbcr)
        check_quote_request_b("QRB_5", case_base_request, ar_service, case_id,
                              quote_sts_new, quote_quote_sts_accepted, case_venue_citir)
        # Step 7

        # Step 8
        place_order_tob(base_rfq_details_1, ar_service)
        quote_citir = check_order_book("OB_4", case_base_request, case_instr_type_ndf, ob_act, case_id,
                                       case_qty, case_venue_citir)
        check_quote_book("QB_4", case_base_request, ar_service, case_id, quote_owner,
                         quote_citir, quote_sts_terminated)
        call(ar_service.closeRFQTile, base_rfq_details_0.build())
        call(ar_service.closeRFQTile, base_rfq_details_1.build())

    except Exception:
        logging.error("Error execution", exc_info=True)
