import logging
import time
from pathlib import Path

from th2_grpc_act_gui_quod.act_ui_win_pb2 import VenueStatusesRequest
from th2_grpc_act_gui_quod.ar_operations_pb2 import ExtractOrderTicketValuesRequest, ExtractDirectVenueExecutionRequest
from th2_grpc_act_gui_quod.common_pb2 import BaseTileData

from custom.tenor_settlement_date import spo
from custom.verifier import Verifier, VerificationMethod
from quod_qa.fx.fx_wrapper.CaseParamsBuy import CaseParamsBuy
from quod_qa.fx.fx_wrapper.CaseParamsSellEsp import CaseParamsSellEsp
from quod_qa.fx.fx_wrapper.FixClientBuy import FixClientBuy
from quod_qa.fx.fx_wrapper.FixClientSellEsp import FixClientSellEsp
from stubs import Stubs
from custom import basic_custom_actions as bca

from win_gui_modules.dealing_positions_wrappers import GetOrdersDetailsRequest, ExtractionPositionsFieldsDetails, \
    ExtractionPositionsAction, PositionsInfo
from win_gui_modules.order_book_wrappers import OrdersDetails, ExtractionDetail, OrderInfo, ExtractionAction, \
    CancelFXOrderDetails, ModifyFXOrderDetails
from win_gui_modules.order_ticket import FXOrderDetails
from win_gui_modules.order_ticket_wrappers import NewFxOrderDetails
from win_gui_modules.wrappers import set_base
from win_gui_modules.client_pricing_wrappers import BaseTileDetails, ExtractRatesTileTableValuesRequest, \
    ModifyRatesTileRequest, PlaceRateTileTableOrderRequest, RatesTileTableOrdSide, PlaceRatesTileOrderRequest
from th2_grpc_act_rest_quod.act_rest_quod_pb2 import SubmitMessageRequest
from win_gui_modules.utils import set_session_id, get_base_request, call, close_fe, prepare_fe303
import logging
from datetime import datetime
from pathlib import Path


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
client = 'Osmium1'
client_tier = 'Osmium'
account = 'Osmium1_1'
symbol = 'EUR/USD'
instrument_tier = 'EUR/USD-SPOT'
status_open = 'Open'
row = 2
SELL = RatesTileTableOrdSide.SELL
BUY = RatesTileTableOrdSide.BUY
qty = '3000000'
new_qty = '4000000'


def modify_rates_tile(base_request, service, instrument, client):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.set_client_tier(client)
    modify_request.set_instrument(instrument)
    call(service.modifyRatesTile, modify_request.build())


def get_dealing_positions_details(del_act, base_request, symbol, account):
    dealing_positions_details = GetOrdersDetailsRequest()
    dealing_positions_details.set_default_params(base_request)
    extraction_id = bca.client_orderid(4)
    dealing_positions_details.set_extraction_id(extraction_id)
    dealing_positions_details.set_filter(["Symbol", symbol, "Account", account])
    position = ExtractionPositionsFieldsDetails("dealingpositions.position", 'Position')
    dealing_positions_details.add_single_positions_info(
        PositionsInfo.create(
            action=ExtractionPositionsAction.create_extraction_action(extraction_details=[position])))

    response = call(del_act.getFxDealingPositionsDetails, dealing_positions_details.request())
    return response["dealingpositions.position"].replace(",", "")


def compare_position(even_name, case_id, expected_pos, actual_pos):
    verifier = Verifier(case_id)
    verifier.set_event_name(even_name)
    verifier.compare_values("Quote position", str(expected_pos), str(actual_pos))
    verifier.verify()


def check_order_book_ao(even_name, case_id, base_request, act_ob, Qty, status_exp):
    ob = OrdersDetails()
    extraction_id = bca.client_orderid(4)
    ob.set_extraction_id(extraction_id)
    ob.set_default_params(base_request)
    ob.set_filter(["Order ID", 'AO', "Orig", 'AutoHedger', "Strategy", "test"])
    qty = ExtractionDetail("orderBook.qty", "Qty")
    status = ExtractionDetail("orderBook.sts", "Sts")
    order_id = ExtractionDetail("orderBook.order_id", "Order ID")

    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[qty, status, order_id])))
    response = call(act_ob.getOrdersDetails, ob.request())

    verifier = Verifier(case_id)
    verifier.set_event_name(even_name)
    verifier.compare_values('Qty', Qty, response[qty.name].replace(",", ""))
    verifier.compare_values('Sts', status_exp, response[status.name])

    verifier.verify()
    ord_id = response[order_id.name]

    return ord_id


def check_order_book_after_amend(case_id, case_base_request, act_ob, Qty, status_exp, ord_id):
    ob = OrdersDetails()
    extraction_id = bca.client_orderid(4)
    ob.set_extraction_id(extraction_id)
    ob.set_default_params(case_base_request)
    ob.set_filter(["Order ID", ord_id])
    qty = ExtractionDetail("orderBook.qty", "Qty")
    status = ExtractionDetail("orderBook.sts", "Sts")
    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[qty, status])))
    response = call(act_ob.getOrdersDetails, ob.request())
    verifier = Verifier(case_id)
    verifier.set_event_name('Checking order after amend')
    verifier.compare_values('Qty', Qty, response[qty.name].replace(",", ""))
    verifier.compare_values('Sts', status_exp, response[status.name])
    verifier.verify()


def check_order_book_no_new_order(case_id, base_request, act_ob, ord_id):
    ob = OrdersDetails()
    extraction_id = bca.client_orderid(4)
    ob.set_extraction_id(extraction_id)
    ob.set_default_params(base_request)
    ob.set_filter(["Order ID", 'AO', "Orig", 'AutoHedger', "Strategy", "test"])
    status = ExtractionDetail("orderBook.sts", "Sts")
    order_id = ExtractionDetail("orderBook.order_id", "Order ID")
    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[status, order_id])))
    response = call(act_ob.getOrdersDetails, ob.request())
    verifier = Verifier(case_id)
    verifier.set_event_name('Checking that there is no new orders')
    verifier.compare_values('Sts', 'Cancelled', response[status.name])
    verifier.compare_values('ID', ord_id, response[order_id.name])
    verifier.verify()


def cancel_order(ob_act, base_request, ord_id):
    cancel_order_request = CancelFXOrderDetails(base_request)
    cancel_order_request.set_filter(['Order ID', ord_id])
    call(ob_act.cancelOrder, cancel_order_request.build())


def open_order_ticket_via_double_click(ob_act, base_request, ord_id):
    order_details = FXOrderDetails()
    modify_ot_order_request = ModifyFXOrderDetails(base_request)
    modify_ot_order_request.set_order_details(order_details)
    modify_ot_order_request.set_filter(['Qty', qty])
    modify_ot_order_request.set_filter(['Order ID', ord_id])
    call(ob_act.openOrderTicketByDoubleClick, modify_ot_order_request.build())


def amend_order(base_request, service, _qty):
    place_request = PlaceRatesTileOrderRequest(details=base_request)
    place_request.set_quantity(_qty)
    call(service.placeRatesTileOrder, place_request.build())


def open_ot_by_doubleclick_row(btd, cp_service, _row, _side):
    request = PlaceRateTileTableOrderRequest(btd, _row, _side)
    call(cp_service.placeRateTileTableOrder, request.build())


def place_order(base_request, service, _client):
    place_request = PlaceRatesTileOrderRequest(details=base_request)
    place_request.set_client(client)
    # place_request.buy()
    call(service.placeRatesTileOrder, place_request.build())


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    case_base_request = get_base_request(session_id, case_id)
    base_tile_data = BaseTileData(base=case_base_request)
    base_details = BaseTileDetails(base=case_base_request)
    api = Stubs.api_service
    ob_act = Stubs.win_act_order_book
    cp_service = Stubs.win_act_cp_service
    ob_fx_act = Stubs.win_act_order_book_fx
    order_ticket_service = Stubs.win_act_order_ticket_fx
    pos_service = Stubs.act_fx_dealing_positions
    try:
        # Step 1
        expecting_pos = get_dealing_positions_details(pos_service, case_base_request, symbol, account)
        call(cp_service.createRatesTile, base_details.build())
        modify_rates_tile(base_details, cp_service, instrument_tier, client_tier)
        open_ot_by_doubleclick_row(base_tile_data, cp_service, row, SELL)
        place_order(base_details, cp_service, client)
        # Step 2
        ord_id = check_order_book_ao('Checking placed order', case_id, case_base_request, ob_act, qty, status_open)
        open_order_ticket_via_double_click(ob_fx_act, case_base_request, ord_id)
        amend_order(base_details, cp_service, new_qty)
        # Step 3
        check_order_book_after_amend(case_id, case_base_request, ob_act, new_qty, status_open, ord_id)
        cancel_order(ob_act, case_base_request, ord_id)
        ord_id = check_order_book_ao('Checking new AH order', case_id, case_base_request, ob_act, qty, status_open)
        # Step 4
        open_ot_by_doubleclick_row(base_tile_data, cp_service, row, BUY)
        place_order(base_details, cp_service, client)
        # Step 5
        cancel_order(ob_act, case_base_request, ord_id)
        check_order_book_no_new_order(case_id, case_base_request, ob_act, ord_id)
        # Step 6
        actual_pos = get_dealing_positions_details(pos_service, case_base_request, symbol, account)
        compare_position('Checking positions', case_id, expecting_pos, actual_pos)
    except Exception as e:
        logging.error('Error execution', exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
    finally:
        try:
            # Close tile
            call(cp_service.closeRatesTile, base_details.build())
        except Exception:
            logging.error("Error execution", exc_info=True)
