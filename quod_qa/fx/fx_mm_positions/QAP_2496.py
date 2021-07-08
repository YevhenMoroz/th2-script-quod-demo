import logging
from pathlib import Path

from th2_grpc_act_gui_quod.common_pb2 import BaseTileData

from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.client_pricing_wrappers import ModifyRatesTileRequest, PlaceRatesTileOrderRequest, \
    PlaceRateTileTableOrderRequest, RatesTileTableOrdSide

from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.dealing_positions_wrappers import GetOrdersDetailsRequest, ExtractionPositionsFieldsDetails, \
    PositionsInfo, ExtractionPositionsAction
from win_gui_modules.order_ticket import FXOrderDetails
from win_gui_modules.order_ticket_wrappers import NewFxOrderDetails
from win_gui_modules.utils import prepare_fe_2, get_base_request, call, get_opened_fe
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
    mtm_pnl = ExtractionPositionsFieldsDetails("dealingpositions.mtmPnl", " MTM PnL (USD)")

    dealing_positions_details.add_single_positions_info(
        PositionsInfo.create(
            action=ExtractionPositionsAction.create_extraction_action(extraction_details=[position, quote_position,
                                                                                          mkt_px,
                                                                                          mtm_pnl])))

    response = call(del_act.getFxDealingPositionsDetails, dealing_positions_details.request())
    return response


def check_pnl(case_id, position, mtk_px, quote_pos, extracted_pnl):
    position = float(position.replace(",", ""))
    mtk_px = float(mtk_px)
    quote_pos = float(quote_pos.replace(",", ""))
    expected_pnl = (position * mtk_px + quote_pos) / mtk_px
    verifier = Verifier(case_id)
    verifier.set_event_name("Check MTM Pnl USD")
    verifier.compare_values("MTM Pnl USD", str(round(expected_pnl, 2)), extracted_pnl.replace(",", ""))
    verifier.verify()


def execute(report_id, session_id):
    cp_service = Stubs.win_act_cp_service
    pos_service = Stubs.act_fx_dealing_positions
    order_ticket_service = Stubs.win_act_order_ticket_fx

    case_name = Path(__file__).name[:-3]
    client_tier = "Argentum"
    instrument_spot = "USD/CAD-SPOT"
    client = "Silver"
    symbol = instrument_spot[:7]
    slippage = "2"
    qty_2m = "2000000"
    qty_6m = "6000000"
    qty_8m = "8000000"
    qty_3m = "3000000"

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)

    set_base(session_id, case_id)
    case_base_request = get_base_request(session_id, case_id)
    base_details = BaseTileDetails(base=case_base_request)
    base_tile_data = BaseTileData(base=case_base_request)
    try:
        # Step 1
        create_or_get_rates_tile(base_details, cp_service)
        modify_rates_tile(base_details, cp_service, instrument_spot, client_tier)
        place_order_buy(base_details, cp_service, qty_2m, slippage, client)
        place_order_buy(base_details, cp_service, qty_6m, slippage, client)
        # Step 2
        position_info = get_dealing_positions_details(pos_service, case_base_request, symbol, client)
        check_pnl(case_id, position_info["dealingpositions.position"], position_info["dealingpositions.mktPx"],
                  position_info["dealingpositions.quotePosition"], position_info["dealingpositions.mtmPnl"])
        # Step 3
        open_order_ticket_sell(base_tile_data, cp_service, 3)
        place_order(case_base_request, order_ticket_service, qty_8m, slippage, client)
        position_info_after_8m = get_dealing_positions_details(pos_service, case_base_request, symbol, client)
        # Step 4
        check_pnl(case_id, position_info_after_8m["dealingpositions.position"],
                  position_info_after_8m["dealingpositions.mktPx"],
                  position_info_after_8m["dealingpositions.quotePosition"],
                  position_info_after_8m["dealingpositions.mtmPnl"])
        # Step 5
        open_order_ticket_sell(base_tile_data, cp_service, 2)
        place_order(case_base_request, order_ticket_service, qty_3m, slippage, client)
        position_info_after_3m = get_dealing_positions_details(pos_service, case_base_request, symbol, client)
        check_pnl(case_id, position_info_after_3m["dealingpositions.position"],
                  position_info_after_3m["dealingpositions.mktPx"],
                  position_info_after_3m["dealingpositions.quotePosition"],
                  position_info_after_3m["dealingpositions.mtmPnl"])

    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        try:
            # Close tile
            call(cp_service.closeRatesTile, base_details.build())
        except Exception:
            logging.error("Error execution", exc_info=True)
