import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from stubs import Stubs
from win_gui_modules.aggregated_rates_wrappers import RFQTileOrderSide, PlaceRFQRequest, ModifyRFQTileRequest, \
    ContextAction
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.order_book_wrappers import OrdersDetails, OrderInfo, ExtractionDetail, ExtractionAction
from win_gui_modules.quote_wrappers import QuoteDetailsRequest
from win_gui_modules.utils import set_session_id, prepare_fe_2, get_base_request, call, get_opened_fe
from win_gui_modules.wrappers import set_base, verification, verify_ent

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def create_or_get_rfq(base_request, service):
    call(service.createRFQTile, base_request.build())


def send_rfq(base_request, service):
    call(service.sendRFQOrder, base_request.build())


def modify_rfq_tile(base_request, service, qty, cur1, cur2, tenor, client, venues):
    modify_request = ModifyRFQTileRequest(details=base_request)
    action = ContextAction.create_venue_filters(venues)
    modify_request.add_context_action(action)
    modify_request.set_quantity(qty)
    modify_request.set_from_currency(cur1)
    modify_request.set_to_currency(cur2)
    modify_request.set_near_tenor(tenor)
    modify_request.set_client(client)
    call(service.modifyRFQTile, modify_request.build())


def place_order_tob(base_request, service):
    rfq_request = PlaceRFQRequest(details=base_request)
    rfq_request.set_action(RFQTileOrderSide.BUY)
    call(service.placeRFQOrder, rfq_request.build())


def cancel_rfq(base_request, service):
    call(service.cancelRFQ, base_request.build())


def check_quote_request_b(ex_id, base_request, service, act, status, quote_sts, venue):
    qrb = QuoteDetailsRequest(base=base_request)
    qrb.set_extraction_id(ex_id)
    qrb.set_filter(["Venue", venue])
    qrb_venue = ExtractionDetail("quoteRequestBook.venue", "Venue")
    qrb_status = ExtractionDetail("quoteRequestBook.status", "Status")
    qrb_quote_status = ExtractionDetail("quoteRequestBook.qoutestatus", "QuoteStatus")
    qrb.add_extraction_details([qrb_venue, qrb_status, qrb_quote_status])
    call(service.getQuoteRequestBookDetails, qrb.request())
    call(act.verifyEntities, verification(ex_id, "checking QRB",
                                          [verify_ent("QRB Venue", qrb_venue.name, venue),
                                           verify_ent("QRB Status", qrb_status.name, status),
                                           verify_ent("QRB QuoteStatus", qrb_quote_status.name, quote_sts)]))


def check_quote_book(ex_id, base_request, service, act, owner, quote_id):
    qb = QuoteDetailsRequest(base=base_request)
    qb.set_extraction_id(ex_id)
    qb.set_filter(["Id", quote_id])
    qb_owner = ExtractionDetail("quoteBook.owner", "Owner")
    qb_quote_status = ExtractionDetail("quoteBook.quotestatus", "QuoteStatus")
    qb_id = ExtractionDetail("quoteBook.id", "Id")
    qb.add_extraction_details([qb_owner, qb_quote_status, qb_id])
    call(service.getQuoteBookDetails, qb.request())
    call(act.verifyEntities, verification(ex_id, "checking QB",
                                          [verify_ent("QB Owner", qb_owner.name, owner),
                                           verify_ent("QB QuoteStatus", qb_quote_status.name, "Terminated"),
                                           verify_ent("QB Id vs OB Id", qb_id.name, quote_id)]))


def check_order_book(ex_id, base_request, instr_type, act, act_ob):
    ob = OrdersDetails()
    ob.set_default_params(base_request)
    ob.set_extraction_id(ex_id)
    ob_instr_type = ExtractionDetail("orderBook.instrtype", "InstrType")
    ob_exec_sts = ExtractionDetail("orderBook.execsts", "ExecSts")
    ob_id = ExtractionDetail("orderBook.quoteid", "QuoteID")
    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[ob_instr_type,
                                                                                 ob_exec_sts,
                                                                                 ob_id])))
    data = call(act_ob.getOrdersDetails, ob.request())
    call(act.verifyEntities, verification(ex_id, "checking OB",
                                          [verify_ent("OB InstrType", ob_instr_type.name, instr_type),
                                           verify_ent("OB ExecSts", ob_exec_sts.name, "Filled")]))
    return data[ob_id.name]


def execute(report_id):
    common_act = Stubs.win_act
    ar_service = Stubs.win_act_aggregated_rates_service
    ob_act = Stubs.win_act_order_book

    case_name = Path(__file__).name[:-3]
    quote_owner = Stubs.custom_config['qf_trading_fe_user_309']
    case_instr_type = "Spot"
    case_sts_new = 'New'
    case_sts_terminated = 'Terminated'
    case_quote_sts_accepted = "Accepted"
    case_quote_sts_terminated = "Terminated"
    case_venue = "HSBCR"
    case_qty = 1000000
    case_near_tenor = "Spot"
    case_from_currency = "EUR"
    case_to_currency = "USD"
    case_client = "ASPECT_CITI"
    venues = ["HSB"]

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)
    session_id = set_session_id()
    set_base(session_id, case_id)
    case_base_request = get_base_request(session_id, case_id)

    base_rfq_details = BaseTileDetails(base=case_base_request)

    try:
        if not Stubs.frontend_is_open:
            prepare_fe_2(case_id, session_id)
        else:
            get_opened_fe(case_id, session_id)
        # Step 1
        create_or_get_rfq(base_rfq_details, ar_service)
        modify_rfq_tile(base_rfq_details, ar_service, case_qty, case_from_currency,
                        case_to_currency, case_near_tenor, case_client, venues)
        # Step 2
        send_rfq(base_rfq_details, ar_service)
        check_quote_request_b("QRB_0", case_base_request, ar_service, common_act,
                              case_sts_new, case_quote_sts_accepted, case_venue)
        # Step 3
        cancel_rfq(base_rfq_details, ar_service)
        check_quote_request_b("QRB_0", case_base_request, ar_service, common_act,
                              case_sts_terminated, case_quote_sts_terminated, case_venue)

        # Step 4
        send_rfq(base_rfq_details, ar_service)
        check_quote_request_b("QRB_0", case_base_request, ar_service, common_act,
                              case_sts_new, case_quote_sts_accepted, case_venue)
        place_order_tob(base_rfq_details, ar_service)
        ob_quote_id = check_order_book("OB_0", case_base_request, case_instr_type, common_act, ob_act)
        check_quote_book("QB_0", case_base_request, ar_service, common_act, quote_owner, ob_quote_id)

        # Close tile
        call(ar_service.closeRFQTile, base_rfq_details.build())

    except Exception:
        logging.error("Error execution", exc_info=True)
