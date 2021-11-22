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


def place_order_sell(base_request, service, qty, slippage, client):
    place_request = PlaceRatesTileOrderRequest(details=base_request)
    place_request.set_quantity(qty)
    place_request.set_slippage(slippage)
    place_request.set_client(client)
    place_request.sell()
    call(service.placeRatesTileOrder, place_request.build())


def execute(report_id, session_id):
    cp_service = Stubs.win_act_cp_service

    case_name = Path(__file__).name[:-3]
    client_tier = "Argentum"
    instrument_spot = "USD/CAD-SPOT"
    instrument_1w = "USD/CAD-1W"
    instrument_2w = "USD/CAD-2W"
    client = "Silver"
    slippage = "2"
    qty_1m = "1000000"

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)

    set_base(session_id, case_id)
    case_base_request = get_base_request(session_id, case_id)
    base_details = BaseTileDetails(base=case_base_request)
    try:
        # Step 1
        create_or_get_rates_tile(base_details, cp_service)
        modify_rates_tile(base_details, cp_service, instrument_spot, client_tier)
        place_order_buy(base_details, cp_service, qty_1m, slippage, client)
        place_order_sell(base_details, cp_service, qty_1m, slippage, client)

        modify_rates_tile(base_details, cp_service, instrument_1w, client_tier)
        place_order_buy(base_details, cp_service, qty_1m, slippage, client)
        place_order_sell(base_details, cp_service, qty_1m, slippage, client)

        modify_rates_tile(base_details, cp_service, instrument_2w, client_tier)
        place_order_buy(base_details, cp_service, qty_1m, slippage, client)
        place_order_sell(base_details, cp_service, qty_1m, slippage, client)

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
    finally:
        try:
            # Close tile
            call(cp_service.closeRatesTile, base_details.build())
        except Exception:
            logging.error("Error execution", exc_info=True)