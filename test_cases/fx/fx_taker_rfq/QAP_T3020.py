import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.verifier import Verifier, VerificationMethod
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


def modify_rfq_tile_swap(base_request, service, near_qty, cur1, cur2, near_date, far_date, client, venues):
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


def place_order_venue(base_request, service, venue):
    rfq_request = PlaceRFQRequest(details=base_request)
    rfq_request.set_venue(venue[:-1])
    rfq_request.set_action(RFQTileOrderSide.SELL)
    call(service.placeRFQOrder, rfq_request.build())


def cancel_rfq(base_request, service):
    call(service.cancelRFQ, base_request.build())


def check_quote_request_b(base_request, service, case_id, status, quote_sts, venue):
    qrb = QuoteDetailsRequest(base=base_request)
    execution_id = bca.client_orderid(4)
    qrb.set_extraction_id(execution_id)
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


def check_quote_book(base_request, service, case_id, owner, quote_id):
    qb = QuoteDetailsRequest(base=base_request)
    execution_id = bca.client_orderid(4)
    qb.set_extraction_id(execution_id)
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


def check_order_book(base_request, instr_type, act_ob, case_id, qty):
    ob = OrdersDetails()
    execution_id = bca.client_orderid(4)
    ob.set_default_params(base_request)
    ob.set_extraction_id(execution_id)
    ob_instr_type = ExtractionDetail("orderBook.instrtype", "InstrType")
    ob_exec_sts = ExtractionDetail("orderBook.execsts", "ExecSts")
    ob_id = ExtractionDetail("orderBook.quoteid", "QuoteID")

    exec_id = ExtractionDetail("executions.id", "ExecID")
    exec_near_px = ExtractionDetail("executions.near_px", "NearPx")
    exec_far_px = ExtractionDetail("executions.far_px", "FarPx")
    exec_near_qty = ExtractionDetail("executions.near_qty", "NearQty")
    exec_far_qty = ExtractionDetail("executions.far_qty", "FarQty")
    exec_near_fwd_pts = ExtractionDetail("executions.near_fwd_pts", "NearFwdPts")
    exec_far_fwd_pts = ExtractionDetail("executions.far_fwd_pts", "FarFwdPts")
    exec_info = OrderInfo.create(action=ExtractionAction.create_extraction_action(extraction_details=[exec_id,
                                                                                                      exec_near_px,
                                                                                                      exec_far_px,
                                                                                                      exec_near_fwd_pts,
                                                                                                      exec_far_fwd_pts,
                                                                                                      exec_near_qty,
                                                                                                      exec_far_qty]))
    exec_details = OrdersDetails.create(info=exec_info)

    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[ob_instr_type,
                                                                                 ob_exec_sts,
                                                                                 ob_id]),
            sub_order_details=exec_details))
    response = call(act_ob.getOrdersDetails, ob.request())
    verifier = Verifier(case_id)
    verifier.set_event_name("Check Order book")
    verifier.compare_values('InstrType', instr_type, response[ob_instr_type.name])
    verifier.compare_values('Sts', 'Filled', response[ob_exec_sts.name])
    verifier.compare_values('Near PX', '1', response[exec_near_px.name], VerificationMethod.CONTAINS)
    verifier.compare_values('Far PX', '1', response[exec_far_px.name], VerificationMethod.CONTAINS)
    verifier.compare_values('Near FwdPts', '0', response[exec_near_fwd_pts.name], VerificationMethod.CONTAINS)
    verifier.compare_values('Far FwdPts', '0', response[exec_far_fwd_pts.name], VerificationMethod.CONTAINS)
    verifier.compare_values('Near Qty', str(qty), response[exec_near_qty.name].replace(",", ""))
    verifier.compare_values('Far Qty', str(qty), response[exec_far_qty.name].replace(",", ""))
    verifier.verify()
    return response[ob_id.name]


def execute(report_id, session_id):
    ar_service = Stubs.win_act_aggregated_rates_service
    ob_act = Stubs.win_act_order_book

    case_name = Path(__file__).name[:-3]
    case_client = "ASPECT_CITI"
    case_from_currency = "EUR"
    case_to_currency = "USD"
    case_near_date = 5
    case_far_date = 10
    case_venue = ["CITI"]
    case_filter_venue = "CITI"
    case_qty = 10000000
    quote_sts_new = 'New'
    quote_quote_sts_accepted = "Accepted"
    case_instr_type = 'FXSwap'
    quote_owner = Stubs.custom_config['qf_trading_fe_user']

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)

    set_base(session_id, case_id)
    case_base_request = get_base_request(session_id, case_id)
    base_rfq_details = BaseTileDetails(base=case_base_request)

    try:
        # Step 1
        create_or_get_rfq(base_rfq_details, ar_service)
        modify_rfq_tile_swap(base_rfq_details, ar_service, case_qty, case_from_currency, case_to_currency,
                             case_near_date, case_far_date, case_client, case_venue)
        send_rfq(base_rfq_details, ar_service)
        check_quote_request_b(case_base_request, ar_service, case_id,
                              quote_sts_new, quote_quote_sts_accepted, case_filter_venue)
        # Step 2
        place_order_venue(base_rfq_details, ar_service, case_filter_venue)
        # Step 3
        quote_id = check_order_book(case_base_request, case_instr_type, ob_act, case_id,
                                    case_qty)
        check_quote_book(case_base_request, ar_service, case_id, quote_owner, quote_id)

        # Close tile
        call(ar_service.closeRFQTile, base_rfq_details.build())

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
