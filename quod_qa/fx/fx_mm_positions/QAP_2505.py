import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.client_pricing_wrappers import ModifyRatesTileRequest, PlaceRatesTileOrderRequest

from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.dealing_positions_wrappers import GetOrdersDetailsRequest, ExtractionPositionsFieldsDetails, \
    PositionsInfo, ExtractionPositionsAction
from win_gui_modules.order_book_wrappers import OrdersDetails, ExtractionDetail, OrderInfo, ExtractionAction

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


def check_order_book(base_request, act_ob):
    ob = OrdersDetails()
    extraction_id = bca.client_orderid(4)
    ob.set_default_params(base_request)
    ob.set_extraction_id(extraction_id)
    sub_order_qty = ExtractionDetail("subOrder_lvl_1.id", "Qty")
    sub_order_price = ExtractionDetail("subOrder_lvl_1.execprice", "ExecPrice")
    lvl1_info = OrderInfo.create(
        action=ExtractionAction.create_extraction_action(extraction_details=[sub_order_qty,
                                                                             sub_order_price]))
    lvl1_details = OrdersDetails.create(info=lvl1_info)
    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(), sub_order_details=lvl1_details))
    response = call(act_ob.getOrdersDetails, ob.request())
    return float(response[sub_order_price.name])


def get_dealing_positions_details(del_act, base_request, symbol, account):
    dealing_positions_details = GetOrdersDetailsRequest()
    dealing_positions_details.set_default_params(base_request)
    extraction_id = bca.client_orderid(4)
    dealing_positions_details.set_extraction_id(extraction_id)
    dealing_positions_details.set_filter(["Symbol", symbol, "Account", account])
    position = ExtractionPositionsFieldsDetails("dealingpositions.position", "Quote Position")
    dealing_positions_details.add_single_positions_info(
        PositionsInfo.create(
            action=ExtractionPositionsAction.create_extraction_action(extraction_details=[position])))

    response = call(del_act.getFxDealingPositionsDetails, dealing_positions_details.request())
    return float(response["dealingpositions.position"].replace(",", ""))


def compare_position(case_id, pos_before, position, pos_after):
    expected_pos = pos_before + position

    verifier = Verifier(case_id)
    verifier.set_event_name("Compare position")
    verifier.compare_values("Quote position", str(round(expected_pos, 2)), str(pos_after))

    verifier.verify()


def execute(report_id, session_id):
    cp_service = Stubs.win_act_cp_service
    ob_act = Stubs.win_act_order_book
    pos_service = Stubs.act_fx_dealing_positions

    case_name = Path(__file__).name[:-3]
    client_tier = "Argentum"
    instrument = "USD/CAD-SPOT"
    client = "Silver1"
    symbol = instrument[:7]
    slippage = "2"
    qty_6m = "6000000"
    qty_2m = "2000000"
    qty_8m = "8000000"
    qty_3m = "3000000"

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)

    set_base(session_id, case_id)
    case_base_request = get_base_request(session_id, case_id)
    base_details = BaseTileDetails(base=case_base_request)

    try:
        # Step 1
        pos_before = get_dealing_positions_details(pos_service, case_base_request, symbol, client)
        create_or_get_rates_tile(base_details, cp_service)
        modify_rates_tile(base_details, cp_service, instrument, client_tier)
        place_order_buy(base_details, cp_service, qty_6m, slippage, client)
        pos_after_6m = get_dealing_positions_details(pos_service, case_base_request, symbol, client)
        price = check_order_book(case_base_request, ob_act)
        position = price * -abs(float(qty_6m))
        compare_position(case_id, pos_before, position, pos_after_6m)
        # Step 2
        place_order_buy(base_details, cp_service, qty_2m, slippage, client)
        pos_after_2m = get_dealing_positions_details(pos_service, case_base_request, symbol, client)
        price = check_order_book(case_base_request, ob_act)
        position = price * -abs(float(qty_2m))
        compare_position(case_id, pos_after_6m, position, pos_after_2m)
        # Step 3
        place_order_sell(base_details, cp_service, qty_8m, slippage, client)
        pos_after_8m = get_dealing_positions_details(pos_service, case_base_request, symbol, client)
        price = check_order_book(case_base_request, ob_act)
        position = price * abs(float(qty_8m))
        compare_position(case_id, pos_after_2m, position, pos_after_8m)
        # Step 4
        place_order_sell(base_details, cp_service, qty_3m, slippage, client)
        pos_after_3m = get_dealing_positions_details(pos_service, case_base_request, symbol, client)
        price = check_order_book(case_base_request, ob_act)
        position = price * abs(float(qty_3m))
        compare_position(case_id, pos_after_8m, position, pos_after_3m)

    except Exception:
        logging.error("Error execution", exc_info=True)
    finally:
        try:
            # Close tile
            call(cp_service.closeRatesTile, base_details.build())
        except Exception:
            logging.error("Error execution", exc_info=True)
