import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.client_pricing_wrappers import ModifyRatesTileRequest, PlaceRatesTileOrderRequest

from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.dealing_positions_wrappers import GetOrdersDetailsRequest, ExtractionPositionsFieldsDetails, \
    PositionsInfo, ExtractionPositionsAction
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


def place_order_sell(base_request, service, qty, slippage, client):
    place_request = PlaceRatesTileOrderRequest(details=base_request)
    place_request.set_quantity(qty)
    place_request.set_slippage(slippage)
    place_request.set_client(client)
    place_request.set_order_price_pips("115")
    place_request.sell()
    call(service.placeRatesTileOrder, place_request.build())


def get_dealing_positions_details(del_act, base_request, symbol, account):
    dealing_positions_details = GetOrdersDetailsRequest()
    dealing_positions_details.set_default_params(base_request)
    extraction_id = bca.client_orderid(4)
    dealing_positions_details.set_extraction_id(extraction_id)
    dealing_positions_details.set_filter(["Symbol", symbol, "Account", account])
    position = ExtractionPositionsFieldsDetails("dealingpositions.position", "Position")
    quote_position = ExtractionPositionsFieldsDetails("dealingpositions.quotePosition", "Quote Position")
    daily_mtm_quote_pos = ExtractionPositionsFieldsDetails("dealingpositions.dailyMTMQuotePos",
                                                           "Daily MTM Quote Position")
    avg_px = ExtractionPositionsFieldsDetails("dealingpositions.avgPx", "Avg Px")
    daily_avg_px = ExtractionPositionsFieldsDetails("dealingpositions.dailyAvgPx", "Daily MTM Avg Px")

    dealing_positions_details.add_single_positions_info(
        PositionsInfo.create(
            action=ExtractionPositionsAction.create_extraction_action(extraction_details=[position, quote_position,
                                                                                          daily_mtm_quote_pos,
                                                                                          daily_avg_px,
                                                                                          avg_px])))

    response = call(del_act.getFxDealingPositionsDetails, dealing_positions_details.request())
    return response


def check_avg_price(case_id, quote_pos, position, avg_price):
    expected_avg_price = float(quote_pos.replace(",", "")) / float(position.replace(",", ""))
    verifier = Verifier(case_id)
    verifier.set_event_name("Check AVG price")
    verifier.compare_values("AVG Price", str(abs(round(expected_avg_price, 8))), avg_price)
    verifier.verify()


def check_daily_avg_price(case_id, daily_mtm_pos, position, mtm_avg_price):
    expected_mtm_avg_price = float(daily_mtm_pos.replace(",", "")) / float(position.replace(",", ""))
    verifier = Verifier(case_id)
    verifier.set_event_name("Check daily AVG price")
    verifier.compare_values("AVG Price", str(abs(round(expected_mtm_avg_price, 8))), mtm_avg_price)
    verifier.verify()


def check_avg_price_empty(case_id, avg_price):
    verifier = Verifier(case_id)
    verifier.set_event_name("Check AVG price is empty")
    verifier.compare_values("Avg price", "", avg_price)
    verifier.verify()


def execute(report_id, session_id):
    cp_service = Stubs.win_act_cp_service
    pos_service = Stubs.act_fx_dealing_positions

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

    try:
        if not Stubs.frontend_is_open:
            prepare_fe_2(case_id, session_id)
        else:
            get_opened_fe(case_id, session_id)
        # Step 1

        create_or_get_rates_tile(base_details, cp_service)
        modify_rates_tile(base_details, cp_service, instrument_spot, client_tier)
        place_order_buy(base_details, cp_service, qty_2m, slippage, client)
        place_order_buy(base_details, cp_service, qty_6m, slippage, client)
        # Step 2
        position_info = get_dealing_positions_details(pos_service, case_base_request, symbol, client)
        check_avg_price(case_id, position_info["dealingpositions.quotePosition"],
                        position_info["dealingpositions.position"],
                        position_info["dealingpositions.avgPx"])
        # Step 3
        check_daily_avg_price(case_id, position_info["dealingpositions.dailyMTMQuotePos"],
                              position_info["dealingpositions.position"],
                              position_info["dealingpositions.dailyAvgPx"])
        # Step 4
        place_order_sell(base_details, cp_service, qty_8m, slippage, client)
        position_info_after_8m = get_dealing_positions_details(pos_service, case_base_request, symbol, client)
        # Step 5
        check_avg_price_empty(case_id, position_info_after_8m["dealingpositions.avgPx"])
        # Step 6
        place_order_sell(base_details, cp_service, qty_3m, slippage, client)
        position_info_after_3m = get_dealing_positions_details(pos_service, case_base_request, symbol, client)
        check_daily_avg_price(case_id, position_info_after_3m["dealingpositions.dailyMTMQuotePos"],
                              position_info_after_3m["dealingpositions.position"],
                              position_info_after_3m["dealingpositions.dailyAvgPx"])
        # Step 7
        check_avg_price(case_id, position_info_after_3m["dealingpositions.quotePosition"],
                        position_info_after_3m["dealingpositions.position"],
                        position_info_after_3m["dealingpositions.avgPx"])



    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        try:
            # Close tile
            call(cp_service.closeRatesTile, base_details.build())
        except Exception:
            logging.error("Error execution", exc_info=True)
