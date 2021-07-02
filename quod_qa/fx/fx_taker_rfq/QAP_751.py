import logging
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


def create_or_get_rfq(base_request, service):
    call(service.createRFQTile, base_request.build())


def send_rfq(base_request, service):
    call(service.sendRFQOrder, base_request.build())


def modify_rfq_tile_swap(base_request, service, near_qty, cur1, cur2, near_tenor, far_tenor, client, venues):
    modify_request = ModifyRFQTileRequest(details=base_request)
    action = ContextAction.create_venue_filters(venues)
    modify_request.add_context_action(action)
    modify_request.set_near_tenor(near_tenor)
    modify_request.set_far_leg_tenor(far_tenor)
    modify_request.set_quantity(near_qty)
    modify_request.set_from_currency(cur1)
    modify_request.set_to_currency(cur2)
    modify_request.set_client(client)
    call(service.modifyRFQTile, modify_request.build())


def place_order_tob(base_request, service):
    rfq_request = PlaceRFQRequest(details=base_request)
    rfq_request.set_action(RFQTileOrderSide.BUY)
    call(service.placeRFQOrder, rfq_request.build())


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


def check_order_book(base_request, instr_type, act_ob, case_id):
    ob = OrdersDetails()
    execution_id = bca.client_orderid(4)
    ob.set_default_params(base_request)
    ob.set_extraction_id(execution_id)
    ob_instr_type = ExtractionDetail("orderBook.instrtype", "InstrType")
    ob_exec_sts = ExtractionDetail("orderBook.execsts", "ExecSts")
    ob_id = ExtractionDetail("orderBook.quoteid", "QuoteID")
    exec_id = ExtractionDetail("executions.id", "ExecID")
    near_tenor = ExtractionDetail("executions.nearTenor", "NearTenor")
    near_qty = ExtractionDetail("executions.nearQty", "NearQty")
    near_fwd_pts = ExtractionDetail("executions.nearFwdPts", "NearFwdPts")
    near_px = ExtractionDetail("executions.nearPx", "NearPx")
    near_settle_date = ExtractionDetail("executions.farSettleDate", "NearSettlDate")
    far_tenor = ExtractionDetail("executions.farTenor", "FarTenor")
    far_qty = ExtractionDetail("executions.farQty", "FarQty")
    far_fwd_pts = ExtractionDetail("executions.farFwdPts", "FarFwdPts")
    far_px = ExtractionDetail("executions.farPx", "FarPx")
    far_settle_date = ExtractionDetail("executions.farSettleDate", "FarSettlDate")
    last_spot_rate = ExtractionDetail("executions.lastSpotRate", "LastSpotRate")

    exec_info = OrderInfo.create(
        action=ExtractionAction.create_extraction_action(
            extraction_details=[exec_id, near_tenor, near_qty, last_spot_rate,
                                near_fwd_pts, near_px, near_settle_date,
                                far_tenor, far_qty, far_fwd_pts,
                                far_px, far_settle_date]))
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
    verifier.verify()
    return response


def check_trades_book(base_request, ob_act, exec_id):
    execution_details = OrdersDetails()
    extraction_id = bca.client_orderid(4)
    execution_details.set_default_params(base_request)
    execution_details.set_extraction_id(extraction_id)
    execution_details.set_filter(["ExecID", exec_id])
    near_tenor = ExtractionDetail("executions.nearTenor", "Near Leg Tenor")
    near_qty = ExtractionDetail("executions.nearQty", "NearQty")
    near_fwd_pts = ExtractionDetail("executions.nearFwdPts", "NearFwdPts")
    near_px = ExtractionDetail("executions.nearPx", "NearPx")
    near_settle_date = ExtractionDetail("executions.farSettleDate", "Near Leg Settle Date")
    far_tenor = ExtractionDetail("executions.farTenor", "Far Leg Tenor")
    far_qty = ExtractionDetail("executions.farQty", "FarQty")
    far_fwd_pts = ExtractionDetail("executions.farFwdPts", "FarFwdPts")
    far_px = ExtractionDetail("executions.farPx", "FarPx")
    far_settle_date = ExtractionDetail("executions.farSettleDate", "Far Leg Settle Date")
    last_spot_rate = ExtractionDetail("executions.lastSpotRate", "LastSpotRate")
    execution_details.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[near_tenor, near_qty,
                                                                                 near_fwd_pts, near_px,
                                                                                 near_settle_date, last_spot_rate,
                                                                                 far_tenor, far_qty, far_fwd_pts,
                                                                                 far_px, far_settle_date])))
    response = call(ob_act.getTradeBookDetails, execution_details.request())
    return response


def compare_values(case_id, order_book, trade_book):
    verifier = Verifier(case_id)
    verifier.set_event_name("Check value")
    for key in trade_book:
        verifier.compare_values(key, order_book[key], trade_book[key])
    verifier.verify()


def execute(report_id, session_id):
    ar_service = Stubs.win_act_aggregated_rates_service
    ob_act = Stubs.win_act_order_book

    case_name = Path(__file__).name[:-3]
    case_client = "ASPECT_CITI"
    case_from_currency = "EUR"
    case_to_currency = "USD"
    case_tenor = "Spot"
    case_far_tenor = "1W"
    case_venue = ["HSBC"]
    case_filter_venue = "HSBC"
    case_qty = 10000000
    quote_sts_new = 'New'
    quote_quote_sts_accepted = "Accepted"
    case_instr_type = "FXSwap"
    quote_owner = Stubs.custom_config['qf_trading_fe_user_309']

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)

    set_base(session_id, case_id)
    case_base_request = get_base_request(session_id, case_id)
    base_rfq_details = BaseTileDetails(base=case_base_request)

    try:
        # Step 1
        create_or_get_rfq(base_rfq_details, ar_service)
        modify_rfq_tile_swap(base_rfq_details, ar_service, case_qty, case_from_currency, case_to_currency,
                             case_tenor, case_far_tenor, case_client, case_venue)
        send_rfq(base_rfq_details, ar_service)
        check_quote_request_b(case_base_request, ar_service, case_id, quote_sts_new,
                              quote_quote_sts_accepted, case_filter_venue)

        place_order_tob(base_rfq_details, ar_service)
        # 2
        order_info = check_order_book(case_base_request, case_instr_type, ob_act, case_id)
        check_quote_book(case_base_request, ar_service, case_id, quote_owner, order_info["orderBook.quoteid"])
        # Step 3
        trades_info = check_trades_book(case_base_request, ob_act, order_info["executions.id"])
        compare_values(case_id, order_info, trades_info)
        # Close Tile
        call(ar_service.closeRFQTile, base_rfq_details.build())

    except Exception:
        logging.error("Error execution", exc_info=True)
