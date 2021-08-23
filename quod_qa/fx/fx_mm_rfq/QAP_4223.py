import base64
import logging
import random
from datetime import datetime
from pathlib import Path
from th2_grpc_act_gui_quod.common_pb2 import BaseTileData
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.client_pricing_wrappers import (ModifyClientRFQTileRequest, ClientRFQTileOrderDetails)
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.order_book_wrappers import (OrdersDetails, ExtractionDetail,
                                                 ExtractionAction, OrderInfo, FXOrdersDetails, FXOrderInfo)
from win_gui_modules.quote_wrappers import QuoteDetailsRequest
from win_gui_modules.utils import get_base_request, call
from win_gui_modules.wrappers import set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

qty = str(random.randint(1000000, 5000000))
near_tenor='Spot'
far_tenor='2W'
from_curr='GBP'
to_curr='USD'
client_tier='Iridium1'
client='Iridium1'

def create_client_rfq_tile(cp_service, base_tile_data: BaseTileData):
    call(cp_service.createClientRFQTile, base_tile_data)


def close_client_rfq_tile(cp_service, base_tile_data: BaseTileData):
    call(cp_service.closeClientRFQTile, base_tile_data)


def modify_client_rfq_tile(cp_service, base_tile_data):
    request = ModifyClientRFQTileRequest(data=base_tile_data)
    request.change_client_tier(client_tier)
    request.set_from_curr(from_curr)
    request.set_to_curr(to_curr)
    request.change_near_tenor(near_tenor)
    request.change_far_tenor(far_tenor)
    request.change_near_leg_aty(qty)
    request.change_far_leg_aty(qty)
    request.change_client(client)
    call(cp_service.modifyRFQTile, request.build())


def place_client_rfq_order(cp_service, base_tile_data):
    requests = ClientRFQTileOrderDetails(data=base_tile_data)
    requests.set_action_sell()
    call(cp_service.placeClientRFQOrder, requests.build())


def send_client_rfq(cp_service, base_tile_data):
    call(cp_service.sendRFQOrder, base_tile_data)


def check_quote_request_b(base_request, service, case_id, price,):
    qrb = QuoteDetailsRequest(base=base_request)
    qrb.set_filter(['Qty', qty])
    qrb_price = ExtractionDetail('quoteRequestBook.BidPx', 'Bid Px')
    qrb.add_child_extraction_detail(qrb_price)
    response = call(service.getQuoteRequestBookDetails, qrb.request())
    verifier = Verifier(case_id)
    verifier.set_event_name("Check QuoteRequest book")
    verifier.compare_values('Quote request book bid px', price, response[qrb_price.name])
    verifier.verify()


def check_order_book(base_request, act_ob, case_id):
    ob = OrdersDetails()
    execution_id = bca.client_orderid(4)
    ob.set_default_params(base_request)
    ob.set_extraction_id(execution_id)
    ob.set_filter(['Qty', qty])
    order_id = ExtractionDetail("orderBook.OrdId", 'Order ID')
    exec_id = ExtractionDetail("executions.id", "ExecID")
    exec_price = ExtractionDetail("executions.price", "ExecPrice")

    exec_info = OrderInfo.create(action=ExtractionAction.create_extraction_action(extraction_details=[exec_id,
                                                                                                      exec_price]))
    exec_details = OrdersDetails.create(info=exec_info)

    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[order_id]),
            sub_order_details=exec_details))
    response = call(act_ob.getOrdersDetails, ob.request())
    verifier = Verifier(case_id)
    verifier.set_event_name("Check Order book")
    verifier.verify()
    id_order = response[order_id.name]
    id_exec = response[exec_id.name]
    price = response[exec_price.name]
    return [id_exec, price]


def check_trades_book(base_request, ob_act, case_id, exec_id, price):
    execution_details = OrdersDetails()
    extraction_id = bca.client_orderid(4)
    execution_details.set_default_params(base_request)
    execution_details.set_extraction_id(extraction_id)
    execution_details.set_filter(["ExecID", exec_id])
    trades_price = ExtractionDetail("tradeBook.price", "ExecPrice")
    execution_details.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[trades_price])))
    response = call(ob_act.getTradeBookDetails, execution_details.request())

    verifier = Verifier(case_id)
    verifier.set_event_name("Check Trade Book")
    verifier.compare_values("Price", price, response[trades_price.name])
    verifier.verify()


def check_quote_book(base_request, service, case_id, price):
    qb = QuoteDetailsRequest(base=base_request)
    ex_id = bca.client_orderid(4)
    qb.set_extraction_id(ex_id)
    qb.set_filter(["OrdQty", qty])
    qb.set_row_number(1)
    qb_offer_px = ExtractionDetail("quoteBook.OfferPx", "Bid Px")
    qb_exec_price = ExtractionDetail('executions.ExecPrice', 'ExecPrice')
    qb.add_extraction_detail(qb_offer_px)
    qb.add_child_extraction_detail(qb_exec_price)
    response = call(service.getQuoteBookDetails, qb.request())
    verifier = Verifier(case_id)
    verifier.set_event_name("Check Quote book")
    verifier.compare_values("Bid Px", price, response[qb_offer_px.name])
    verifier.compare_values("Exec price", price, response[qb_exec_price.name])
    verifier.verify()




def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)
    print(f'{case_name} started {datetime.now()}')

    set_base(session_id, case_id)
    case_base_request = get_base_request(session_id, case_id)
    base_tile_data = BaseTileData(base=case_base_request)
    base_tile_details = BaseTileDetails(base=case_base_request)

    ar_service = Stubs.win_act_aggregated_rates_service
    ob_fx_act = Stubs.win_act_order_book_fx
    ob_act = Stubs.win_act_order_book
    cp_service = Stubs.win_act_cp_service
    try:
        create_client_rfq_tile(cp_service, base_tile_data)
        modify_client_rfq_tile(cp_service, base_tile_data)
        send_client_rfq(cp_service, base_tile_data)
        place_client_rfq_order(cp_service, base_tile_data)
        order_info = check_order_book(case_base_request, ob_act, case_id)
        check_quote_book(case_base_request, ar_service, case_id, order_info[1])
        check_trades_book(case_base_request, ob_act, case_id, order_info[0], order_info[1])
        check_quote_request_b(case_base_request, ar_service, case_id, order_info[1])
    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
    finally:
        try:
            # Close tile
            call(cp_service.closeClientRFQTile, base_tile_data)
        except Exception:
            logging.error("Error execution", exc_info=True)
