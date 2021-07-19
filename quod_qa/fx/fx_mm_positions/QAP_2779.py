import logging
from datetime import datetime
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import ndf_spo_front_end, ndf_wk2_front_end, ndf_wk1_front_end
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
    place_request.sell()
    call(service.placeRatesTileOrder, place_request.build())


def get_dealing_positions_details_top_level(del_act, base_request, symbol, account):
    dealing_positions_details = GetOrdersDetailsRequest()
    dealing_positions_details.set_default_params(base_request)
    extraction_id = bca.client_orderid(4)
    dealing_positions_details.set_extraction_id(extraction_id)
    dealing_positions_details.set_filter(["Symbol", symbol, "Account", account])
    position = ExtractionPositionsFieldsDetails("dealingpositions.position", "Position")

    dealing_positions_details.add_single_positions_info(
        PositionsInfo.create(
            action=ExtractionPositionsAction.create_extraction_action(extraction_details=[position])))

    response = call(del_act.getFxDealingPositionsDetails, dealing_positions_details.request())
    return float(response["dealingpositions.position"].replace(",", ""))


def get_dealing_pos_child_lvl(del_act, base_request, symbol, account, date):
    dealing_positions_details = GetOrdersDetailsRequest()
    dealing_positions_details.set_default_params(base_request)
    extraction_id = bca.client_orderid(4)
    dealing_positions_details.set_extraction_id(extraction_id)
    dealing_positions_details.set_filter(["Symbol", symbol, "Account", account])
    position = ExtractionPositionsFieldsDetails("dealingpositions.position", "Position")
    sub_position = ExtractionPositionsFieldsDetails("sub_dealingpositions.position", "Position")
    sub_settle_date = ExtractionPositionsFieldsDetails("sub_positions.settldate", "Settle Date")
    lvl1_info = PositionsInfo.create(
        action=ExtractionPositionsAction.create_extraction_action(
            extraction_details=[sub_position, sub_settle_date]))
    lvl1_details = GetOrdersDetailsRequest.create(info=lvl1_info)
    lvl1_details.set_filter(["Settle Date", date])

    dealing_positions_details.add_single_positions_info(
        PositionsInfo.create(
            action=ExtractionPositionsAction.create_extraction_action(extraction_detail=position),
            positions_by_currency=lvl1_details))

    response = call(del_act.getFxDealingPositionsDetails, dealing_positions_details.request())
    return float(response["sub_dealingpositions.position"].replace(",", ""))


def check_position(case_id, pos_before, qty, pos_after):
    expected_pos = pos_before + float(qty)
    verifier = Verifier(case_id)
    verifier.set_event_name("Check position")
    verifier.compare_values("Quote position", str(expected_pos), str(pos_after))
    verifier.verify()


def check_top_lvl_calculation(case_id, child_list, top_lvl):
    expected_top_lvl = sum(child_list)
    verifier = Verifier(case_id)
    verifier.set_event_name("Check sum of child")
    verifier.compare_values("Top lvl pos", str(expected_top_lvl), str(top_lvl))
    verifier.verify()


def execute(report_id, session_id):
    cp_service = Stubs.win_act_cp_service
    pos_service = Stubs.act_fx_dealing_positions

    case_name = Path(__file__).name[:-3]

    client_tier = "Argentum"
    instrument_spot = "USD/CAD-SPOT"
    instrument_1w = "USD/CAD-1W"
    instrument_2w = "USD/CAD-2W"
    client = "Argentum1"
    symbol = instrument_spot[:7]
    slippage = "2"
    qty_2m = "2000000"
    qty_4m = "4000000"
    qty_5m = "5000000"
    date_spo = ndf_spo_front_end()
    date_spo = datetime.strptime(date_spo, '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
    date_wk1 = ndf_wk1_front_end()
    date_wk1 = datetime.strptime(date_wk1, '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
    date_wk2 = ndf_wk2_front_end()
    date_wk2 = datetime.strptime(date_wk2, '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
    child_list = []
    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)

    set_base(session_id, case_id)
    case_base_request = get_base_request(session_id, case_id)
    base_details = BaseTileDetails(base=case_base_request)

    try:
        # Step 1
        modify_rates_tile(base_details, cp_service, instrument_spot, client_tier)
        place_order_buy(base_details, cp_service, qty_5m, slippage, client)
        top_lvl_pos_after_5m = get_dealing_positions_details_top_level(pos_service, case_base_request, symbol, client)
        child_pos_after_5m = get_dealing_pos_child_lvl(pos_service, case_base_request, symbol, client, date_spo)
        check_position(case_id, 0, qty_5m, top_lvl_pos_after_5m)
        child_list.append(child_pos_after_5m)
        check_top_lvl_calculation(case_id, child_list, top_lvl_pos_after_5m)
        # Step 2
        modify_rates_tile(base_details, cp_service, instrument_1w, client_tier)
        place_order_buy(base_details, cp_service, qty_2m, slippage, client)
        top_lvl_pos_after_2m = get_dealing_positions_details_top_level(pos_service, case_base_request, symbol, client)
        child_pos_after_2m = get_dealing_pos_child_lvl(pos_service, case_base_request, symbol, client, date_wk1)
        check_position(case_id, top_lvl_pos_after_5m, qty_2m, top_lvl_pos_after_2m)
        child_list.append(child_pos_after_2m)
        check_top_lvl_calculation(case_id, child_list, top_lvl_pos_after_2m)
        # Step 3
        modify_rates_tile(base_details, cp_service, instrument_2w, client_tier)
        place_order_sell(base_details, cp_service, qty_4m, slippage, client)
        top_lvl_pos_after_4m = get_dealing_positions_details_top_level(pos_service, case_base_request, symbol, client)
        child_pos_after_4m = get_dealing_pos_child_lvl(pos_service, case_base_request, symbol, client, date_wk2)
        check_position(case_id, top_lvl_pos_after_2m, -float(qty_4m), top_lvl_pos_after_4m)
        child_list.append(child_pos_after_4m)
        check_top_lvl_calculation(case_id, child_list, top_lvl_pos_after_4m)

    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        try:
            # Close tile
            call(cp_service.closeRatesTile, base_details.build())
        except Exception:
            logging.error("Error execution", exc_info=True)
