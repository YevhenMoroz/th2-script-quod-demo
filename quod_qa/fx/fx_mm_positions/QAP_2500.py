import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import spo, spo_ndf
from custom.verifier import Verifier
from quod_qa.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from quod_qa.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq
from stubs import Stubs
from win_gui_modules.client_pricing_wrappers import ModifyRatesTileRequest, PlaceRatesTileOrderRequest, \
    PlaceRateTileTableOrderRequest, RatesTileTableOrdSide

from win_gui_modules.dealing_positions_wrappers import GetOrdersDetailsRequest, ExtractionPositionsFieldsDetails, \
    PositionsInfo, ExtractionPositionsAction
from win_gui_modules.order_ticket import FXOrderDetails
from win_gui_modules.order_ticket_wrappers import NewFxOrderDetails
from win_gui_modules.utils import get_base_request, call
from win_gui_modules.wrappers import set_base


def create_or_get_rates_tile(base_request, service):
    call(service.createRatesTile, base_request.build())


def modify_rates_tile(base_request, service, instrument, client):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.set_instrument(instrument)
    modify_request.set_client_tier(client)
    call(service.modifyRatesTile, modify_request.build())


def place_order_buy(base_request, service, qty, slippage, client):
    place_request = PlaceRatesTileOrderRequest(details=base_request)
    place_request.set_quantity(qty)
    place_request.set_slippage(slippage)
    place_request.set_client(client)
    place_request.buy()
    call(service.placeRatesTileOrder, place_request.build())


def open_order_ticket_sell(btd, service, row):
    request = PlaceRateTileTableOrderRequest(btd, row, RatesTileTableOrdSide.SELL)
    call(service.placeRateTileTableOrder, request.build())


def place_order(base_request, service, qty, slippage, client):
    order_ticket = FXOrderDetails()
    order_ticket.set_qty(qty)
    order_ticket.set_client(client)
    order_ticket.set_slippage(slippage)
    order_ticket.set_place()
    new_order_details = NewFxOrderDetails(base_request, order_ticket)
    call(service.placeFxOrder, new_order_details.build())


def get_dealing_positions_details(del_act, base_request, symbol, account):
    dealing_positions_details = GetOrdersDetailsRequest()
    dealing_positions_details.set_default_params(base_request)
    extraction_id = bca.client_orderid(4)
    dealing_positions_details.set_extraction_id(extraction_id)
    dealing_positions_details.set_filter(["Symbol", symbol, "Account", account])
    position = ExtractionPositionsFieldsDetails("dealingpositions.position", "Position")
    quote_position = ExtractionPositionsFieldsDetails("dealingpositions.quotePosition", "Quote Position")
    mkt_px = ExtractionPositionsFieldsDetails("dealingpositions.mktPx", "Mkt Px")
    mtm_pnl = ExtractionPositionsFieldsDetails("dealingpositions.mtmPnl", "MTM PnL")
    mtm_pnl_usd = ExtractionPositionsFieldsDetails("dealingpositions.mtmPnlUsd", " MTM PnL (USD)")

    dealing_positions_details.add_single_positions_info(
        PositionsInfo.create(
            action=ExtractionPositionsAction.create_extraction_action(extraction_details=[position, quote_position,
                                                                                          mkt_px, mtm_pnl,
                                                                                          mtm_pnl_usd])))

    response = call(del_act.getFxDealingPositionsDetails, dealing_positions_details.request())
    return response


def check_pnl(case_id, position, mtk_px, quote_pos, extracted_pnl):
    position = float(position.replace(",", ""))
    mtk_px = float(mtk_px)
    quote_pos = float(quote_pos.replace(",", ""))
    expected_pnl = position * mtk_px + quote_pos
    verifier = Verifier(case_id)
    verifier.set_event_name("Check MTM Pnl")
    verifier.compare_values("MTM Pnl", str(round(expected_pnl, 2)), extracted_pnl.replace(",", ""))
    verifier.verify()


def check_pnl_usd(case_id, position, mtk_px, quote_pos, extracted_pnl_usd):
    position = float(position.replace(",", ""))
    mtk_px = float(mtk_px)
    quote_pos = float(quote_pos.replace(",", ""))
    expected_pnl_usd = (position * mtk_px + quote_pos) / mtk_px
    verifier = Verifier(case_id)
    verifier.set_event_name("Check MTM Pnl")
    verifier.compare_values("MTM Pnl USD", str(round(expected_pnl_usd, 2)), extracted_pnl_usd.replace(",", ""))
    verifier.verify()


def execute(report_id, session_id):
    pos_service = Stubs.act_fx_dealing_positions

    # Preconditions
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    client = "Silver1"
    account = "Silver1_1"
    settle_type = "0"
    symbol = "USD/CAD"
    currency = "USD"
    settle_currency = "CAD"
    security_type = "FXSPOT"
    side_b = "1"
    side_s = "2"
    settle_date = spo_ndf()

    case_name = Path(__file__).name[:-3]
    qty_6m = "6000000"
    qty_8m = "8000000"
    qty_3m = "3000000"

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)

    set_base(session_id, case_id)
    case_base_request = get_base_request(session_id, case_id)
    try:
        # Step 1
        rfq = FixClientSellRfq(
            CaseParamsSellRfq(client, case_id, side=side_b, orderqty=qty_6m, symbol=symbol, securitytype=security_type,
                              settldate=settle_date, securityid=symbol, settlcurrency=settle_currency,
                              settltype=settle_type, currency=currency, account=account)). \
            send_request_for_quote(). \
            verify_quote_pending()
        price = rfq.extruct_filed("BidPx")
        rfq.send_new_order_single(price). \
            verify_order_pending(). \
            verify_order_filled()
        # Step 2
        position_info = get_dealing_positions_details(pos_service, case_base_request, symbol, client)
        check_pnl(case_id, position_info["dealingpositions.position"], position_info["dealingpositions.mktPx"],
                  position_info["dealingpositions.quotePosition"], position_info["dealingpositions.mtmPnl"])
        check_pnl_usd(case_id, position_info["dealingpositions.position"], position_info["dealingpositions.mktPx"],
                      position_info["dealingpositions.quotePosition"], position_info["dealingpositions.mtmPnlUsd"])
        # Step 3
        # rfq = FixClientSellRfq(
        #     CaseParamsSellRfq(client, case_id, side=side_s, orderqty=qty_8m, symbol=symbol, securitytype=security_type,
        #                       settldate=settle_date,
        #                       settltype=settle_type, currency=currency, account=account)). \
        #     send_request_for_quote(). \
        #     verify_quote_pending()
        # price = rfq.extruct_filed("OfferPx")
        # rfq.send_new_order_single(price). \
        #     verify_order_pending(). \
        #     verify_order_filled()
        # # Step 4
        # position_info_after_8m = get_dealing_positions_details(pos_service, case_base_request, symbol, client)
        # check_pnl_usd(case_id, position_info_after_8m["dealingpositions.position"],
        #               position_info_after_8m["dealingpositions.mktPx"],
        #               position_info_after_8m["dealingpositions.quotePosition"],
        #               position_info_after_8m["dealingpositions.mtmPnlUsd"])
        # # Step 5
        # rfq = FixClientSellRfq(
        #     CaseParamsSellRfq(client, case_id, side=side_s, orderqty=qty_3m, symbol=symbol, securitytype=security_type,
        #                       settldate=settle_date,
        #                       settltype=settle_type, currency=currency, account=account)). \
        #     send_request_for_quote(). \
        #     verify_quote_pending()
        # price = rfq.extruct_filed("OfferPx")
        # rfq.send_new_order_single(price). \
        #     verify_order_pending(). \
        #     verify_order_filled()
        # position_info_after_3m = get_dealing_positions_details(pos_service, case_base_request, symbol, client)
        # check_pnl_usd(case_id, position_info_after_3m["dealingpositions.position"],
        #               position_info_after_3m["dealingpositions.mktPx"],
        #               position_info_after_3m["dealingpositions.quotePosition"],
        #               position_info_after_3m["dealingpositions.mtmPnlUsd"])

    except Exception:
        logging.error("Error execution", exc_info=True)
