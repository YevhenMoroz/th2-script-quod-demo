import logging
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
    rfq_request.set_action(RFQTileOrderSide.SELL)
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
    verifier.compare_values('Venue', venue + "R", response[qrb_venue.name])
    verifier.compare_values('Status', status, response[qrb_status.name])
    verifier.compare_values("QuoteStatus", quote_sts, response[qrb_quote_status.name])
    verifier.verify()


def check_quote_book(ex_id, base_request, service, case_id, owner, quote_id):
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
    verifier.compare_values('QuoteStatus', 'Terminated', response[qb_quote_status.name])
    verifier.compare_values("QuoteID", quote_id, response[qb_id.name])
    verifier.verify()


def check_order_book(ex_id, base_request, instr_type, act_ob, case_id, qty, tenor):
    ob = OrdersDetails()
    ob.set_default_params(base_request)
    ob.set_extraction_id(ex_id)
    ob_instr_type = ExtractionDetail("orderBook.instrtype", "InstrType")
    ob_exec_sts = ExtractionDetail("orderBook.execsts", "ExecSts")
    ob_qty = ExtractionDetail("orderbook.qty", "Qty")
    ob_limit_price = ExtractionDetail("orderbook.lmtprice", "LmtPrice")
    ob_id = ExtractionDetail("orderBook.quoteid", "QuoteID")
    ob_tenor = ExtractionDetail("orderBook.nearlegtenor", "Tenor")

    sub_order_id_dt = ExtractionDetail("subOrder_lvl_1.id", "ExecID")
    sub_order_qty = ExtractionDetail("subOrder_lvl_1.id", "Qty")
    sub_order_price = ExtractionDetail("subOrder_lvl_1.execprice", "ExecPrice")
    lvl1_info = OrderInfo.create(action=ExtractionAction.create_extraction_action(extraction_details=[sub_order_id_dt,
                                                                                                      sub_order_qty,
                                                                                                      sub_order_price]))
    lvl1_details = OrdersDetails.create(info=lvl1_info)

    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[ob_instr_type,
                                                                                 ob_exec_sts,
                                                                                 ob_qty,
                                                                                 ob_id,
                                                                                 ob_tenor,
                                                                                 ob_limit_price]),
            sub_order_details=lvl1_details))

    response = call(act_ob.getOrdersDetails, ob.request())
    verifier = Verifier(case_id)
    verifier.set_event_name("Check Order book")
    verifier.compare_values('InstrType', instr_type, response[ob_instr_type.name])
    verifier.compare_values('Sts', 'Filled', response[ob_exec_sts.name])
    verifier.compare_values('Qty', str(qty), response[ob_qty.name].replace(",", ""))
    verifier.compare_values('Tenor', tenor, response[ob_tenor.name])
    verifier.compare_values('Exec Qty', response[sub_order_qty.name], response[ob_qty.name])
    verifier.compare_values('Exec Price', response[ob_limit_price.name], response[sub_order_price.name])
    verifier.verify()
    return response[ob_id.name]


def execute(report_id):
    ar_service = Stubs.win_act_aggregated_rates_service
    ob_act = Stubs.win_act_order_book

    case_name = "QAP-604"
    quote_owner = "ostronov"
    case_instr_type = "Spot"
    case_filter_venue = "HSBC"
    case_qty = 1000000
    case_near_tenor = "Spot"
    case_venue = ["CIT", "HSB"]
    case_from_currency = "EUR"
    case_to_currency = "USD"
    case_client = "MMCLIENT2"
    quote_sts_new = 'New'
    quote_quote_sts_accepted = "Accepted"

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)
    session_id = set_session_id()
    set_base(session_id, case_id)
    case_base_request = get_base_request(session_id, case_id)

    base_rfq_details = BaseTileDetails(base=case_base_request)

    if not Stubs.frontend_is_open:
        prepare_fe_2(case_id, session_id)
    else:
        get_opened_fe(case_id, session_id)
    try:
        # Step 1
        create_or_get_rfq(base_rfq_details, ar_service)
        modify_rfq_tile(base_rfq_details, ar_service, case_qty, case_from_currency,
                        case_to_currency, case_near_tenor, case_client, case_venue)
        send_rfq(base_rfq_details, ar_service)
        check_quote_request_b("QRB_0", case_base_request, ar_service, case_id,
                              quote_sts_new, quote_quote_sts_accepted, case_filter_venue)

        # Step 2
        place_order_tob(base_rfq_details, ar_service)
        ob_quote_id = check_order_book("OB_0", case_base_request, case_instr_type, ob_act, case_id,
                                       case_qty, case_near_tenor)
        check_quote_book("QB_0", case_base_request, ar_service, case_id, quote_owner, ob_quote_id)

        # Close tile
        call(ar_service.closeRFQTile, base_rfq_details.build())

    except Exception:
        logging.error("Error execution", exc_info=True)
