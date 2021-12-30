import logging
from pathlib import Path

from th2_grpc_act_gui_quod.common_pb2 import BaseTileData

from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from stubs import Stubs
from test_framework.win_gui_wrappers.forex.client_rates_tile import ClientRatesTile
from win_gui_modules.client_pricing_wrappers import PlaceRateTileTableOrderRequest, RatesTileTableOrdSide
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.order_book_wrappers import CancelOrderDetails, OrdersDetails, ExtractionDetail, ExtractionAction, \
    OrderInfo
from win_gui_modules.order_ticket import FXOrderDetails
from win_gui_modules.order_ticket_wrappers import NewFxOrderDetails
from win_gui_modules.utils import get_base_request, call
from win_gui_modules.wrappers import set_base


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

    def open_order_ticket_sell(btd, service, row):
        request = PlaceRateTileTableOrderRequest(btd, row, RatesTileTableOrdSide.SELL)
        call(service.placeRateTileTableOrder, request.build())

    def place_order(base_request, service, qty):
        order_ticket = FXOrderDetails()
        order_ticket.set_qty(qty)
        order_ticket.set_client(client)
        order_ticket.set_slippage(slippage)
        order_ticket.set_close()
        new_order_details = NewFxOrderDetails(base_request, order_ticket, isMM=True)
        call(service.placeFxOrder, new_order_details.build())

    def close_ticket(base_request, service):
        order_ticket = FXOrderDetails()
        order_ticket.set_close()
        new_order_details = NewFxOrderDetails(base_request, order_ticket, isMM=True)
        call(service.placeFxOrder, new_order_details.build())

    def place_order(base_request, service, qty):
        order_ticket = FXOrderDetails()
        order_ticket.set_qty(qty)
        new_order_details = NewFxOrderDetails(base_request, order_ticket, isMM=True)
        call(service.placeFxOrder, new_order_details.build())

    try:
        # rates_tile = ClientRatesTile(case_id, session_id)
        # rates_tile.modify_client_tile("EUR/USD-SPOT", "Iridium1")
        # rates_tile.place_order(client="Iridium1")
        open_order_ticket_sell(base_tile_data, cp_service, 1)
        place_order(case_base_request, order_ticket_service, qty_3m)
        close_ticket(case_base_request, order_ticket_service)
    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
