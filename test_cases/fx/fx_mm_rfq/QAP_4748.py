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
                                                 ExtractionAction, OrderInfo)
from win_gui_modules.quote_wrappers import QuoteDetailsRequest
from win_gui_modules.utils import get_base_request, call
from win_gui_modules.wrappers import set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

user = Stubs.custom_config['qf_trading_fe_user']


def create_client_rfq_tile(cp_service, base_tile_data: BaseTileData):
    call(cp_service.createClientRFQTile, base_tile_data)


def modify_client_rfq_tile(cp_service, base_tile_data, qty):
    request = ModifyClientRFQTileRequest(data=base_tile_data)
    request.change_client_tier("Gold_Day")
    request.set_from_curr("GBP")
    request.set_to_curr("USD")
    request.change_near_tenor("Spot")
    request.change_near_leg_aty(qty)
    call(cp_service.modifyRFQTile, request.build())


def place_client_rfq_order(cp_service, base_tile_data):
    requests = ClientRFQTileOrderDetails(data=base_tile_data)
    # requests.set_action_buy()
    requests.set_action_sell()
    call(cp_service.placeClientRFQOrder, requests.build())


def send_client_rfq(cp_service, base_tile_data):
    call(cp_service.sendRFQOrder, base_tile_data)


def check_quote_request_b(base_request, service, case_id, qty,  status="New", venue="QUODFX", quote_status='Accepted'):
    qrb = QuoteDetailsRequest(base=base_request)
    qrb.set_filter(["Venue", venue, "User", user, 'Status', status, 'Qty', qty])
    qrb_venue = ExtractionDetail("quoteRequestBook.venue", "Venue")
    qrb_status = ExtractionDetail("quoteRequestBook.status", "Status")
    qrb_quote_status = ExtractionDetail("quoteRequestBook.qoutestatus", "QuoteStatus")
    qrb.add_extraction_details([qrb_venue, qrb_status, qrb_quote_status])
    response = call(service.getQuoteRequestBookDetails, qrb.request())
    verifier = Verifier(case_id)
    verifier.set_event_name("Check QuoteRequest book")
    verifier.compare_values('Venue', venue, response[qrb_venue.name])
    verifier.compare_values('Status', status, response[qrb_status.name])
    verifier.compare_values('QuoteStatus', quote_status, response[qrb_quote_status.name])
    verifier.verify()


def check_order_book(base_request, act_ob):
    ob = OrdersDetails()
    extraction_id = bca.client_orderid(4)
    ob.set_extraction_id(extraction_id)
    ob.set_default_params(base_request)
    ob.set_filter(['Venue', 'QUODFX', 'Owner', user])
    order_id = ExtractionDetail("orderBook.order_id", "Order ID")
    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[order_id])))
    response = call(act_ob.getOrdersDetails, ob.request())
    ord_id = response[order_id.name]
    return ord_id


def check_order_book_no_new_order(case_id, base_request, act_ob, ord_id):
    ob = OrdersDetails()
    extraction_id = bca.client_orderid(4)
    ob.set_extraction_id(extraction_id)
    ob.set_default_params(base_request)
    ob.set_filter(['Venue', 'QUODFX', 'Owner', user])
    order_id = ExtractionDetail("orderBook.order_id", "Order ID")
    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[order_id])))
    response = call(act_ob.getOrdersDetails, ob.request())
    verifier = Verifier(case_id)
    verifier.set_event_name('Checking that there is no new orders')
    verifier.compare_values('ID', ord_id, response[order_id.name])
    verifier.verify()


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)
    print(f'{case_name} started {datetime.now()}')

    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    base_tile_data = BaseTileData(base=base_request, )
    base_tile_details = BaseTileDetails(base=base_request)

    ar_service = Stubs.win_act_aggregated_rates_service
    ob_act = Stubs.win_act_order_book
    cp_service = Stubs.win_act_cp_service
    rand = random.Random()
    qty = str(rand.randint(1000000, 5000000))
    try:
        create_client_rfq_tile(cp_service, base_tile_data)
        modify_client_rfq_tile(cp_service, base_tile_data, qty)
        send_client_rfq(cp_service, base_tile_data)
        check_quote_request_b(base_request, ar_service, case_id, qty)
        ord_id = check_order_book(base_request, ob_act)
        place_client_rfq_order(cp_service, base_tile_data)
        check_order_book_no_new_order(case_id, base_request, ob_act, ord_id)
    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
    finally:
        try:
            # Close tile
            call(cp_service.closeClientRFQTile, base_tile_data)
        except Exception:
            logging.error("Error execution", exc_info=True)
