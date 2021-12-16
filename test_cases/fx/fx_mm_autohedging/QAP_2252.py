import time
from th2_grpc_act_gui_quod.common_pb2 import BaseTileData
from custom.verifier import Verifier
from stubs import Stubs
from custom import basic_custom_actions as bca
from test_cases.fx.fx_mm_autohedging.QAP_2250 import send_rfq_and_filled_order_sell, send_rfq_and_filled_order_buy
from win_gui_modules.dealing_positions_wrappers import GetOrdersDetailsRequest, ExtractionPositionsFieldsDetails, \
    ExtractionPositionsAction, PositionsInfo
from win_gui_modules.order_book_wrappers import OrdersDetails, ExtractionDetail, OrderInfo, ExtractionAction, \
    CancelFXOrderDetails
from win_gui_modules.client_pricing_wrappers import BaseTileDetails, \
    ModifyRatesTileRequest, PlaceRateTileTableOrderRequest, RatesTileTableOrdSide, PlaceRatesTileOrderRequest
from th2_grpc_act_rest_quod.act_rest_quod_pb2 import SubmitMessageRequest
from win_gui_modules.utils import get_base_request, call
import logging
from pathlib import Path


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
client = 'Osmium1'
client_tier = 'Osmium'
account = 'QUOD3_1'
symbol = 'EUR/USD'
instrument_tier = 'EUR/USD-SPOT'
status_open = 'Open'
row = 2
SELL = RatesTileTableOrdSide.SELL
BUY = RatesTileTableOrdSide.BUY
qty = '2000000'
api = Stubs.api_service
ttl_default = 120
ttl_null = None
ttl_test = 300

def set_send_hedge_order(case_id, ttl):
    modify_params = {
        "autoHedgerName": "OsmiumAH",
        "hedgeAccountGroupID": "QUOD3",
        "autoHedgerID": 1400008,
        "alive": "true",
        "hedgedAccountGroup": [
            {
                "accountGroupID": "Osmium1"
            }
        ],
        "autoHedgerInstrSymbol": [
            {
                "instrSymbol": "EUR/USD",
                "longUpperQty": 2000000,
                "longLowerQty": 0,
                "maintainHedgePositions": "true",
                "crossCurrPairHedgingPolicy": "DIR",
                "useSameLongShortQty": "true",
                "hedgingStrategy": "POS",
                "algoPolicyID": 400018,
                "shortLowerQty": 0,
                "shortUpperQty": 0,
                "timeInForce": "DAY",
                "sendHedgeOrders": 'true',
                "exposureDuration": ttl,
                "hedgeOrderDestination": "EXT"
            }

        ]
    }
    api.sendMessage(
        request=SubmitMessageRequest(message=bca.wrap_message(modify_params, 'ModifyAutoHedger', 'rest_wa314luna'),
                                     parent_event_id=case_id))


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


def check_order_book_ao(even_name, case_id, base_request, act_ob):
    ob = OrdersDetails()
    extraction_id = bca.client_orderid(4)
    ob.set_extraction_id(extraction_id)
    ob.set_default_params(base_request)
    ob.set_filter(["Order ID", 'AO', "Orig", 'AutoHedger', 'Sts', 'Open'])
    order_id = ExtractionDetail("orderBook.order_id", "Order ID")
    order_TIF = ExtractionDetail('orderBook.TIF', 'TIF')
    order_sts = ExtractionDetail('orderBook.Sts', 'Sts')
    order_owner = ExtractionDetail('orderBook.Orig', 'Orig')
    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[order_id, order_TIF, order_sts,
                                                                                 order_owner])))
    response = call(act_ob.getOrdersDetails, ob.request())
    verifier = Verifier(case_id)
    verifier.set_event_name(even_name)
    verifier.compare_values('TIF', 'Day', response[order_TIF.name])
    verifier.compare_values('Sts', 'Open', response[order_sts.name])
    verifier.compare_values("Orig", 'AutoHedger', response[order_owner.name])
    verifier.verify()
    ord_id = response[order_id.name]
    return ord_id


def check_order_book_after_ttl_expire(case_id, case_base_request, act_ob, ord_id):
    ob = OrdersDetails()
    extraction_id = bca.client_orderid(4)
    ob.set_extraction_id(extraction_id)
    ob.set_default_params(case_base_request)
    ob.set_filter(["Order ID", ord_id])
    order_id = ExtractionDetail("orderBook.order_id", "Order ID")
    order_sts = ExtractionDetail('orderBook.Sts', 'Sts')
    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[order_id, order_sts])))
    response = call(act_ob.getOrdersDetails, ob.request())
    verifier = Verifier(case_id)
    verifier.set_event_name('Checking order after ttl expire')
    verifier.compare_values('ID', ord_id, response[order_id.name])
    verifier.compare_values('Order Sts', 'Cancelled', response[order_sts.name])
    verifier.verify()


def check_order_book_new_ttl_applied(case_id, base_request, act_ob, ord_id):
    ob = OrdersDetails()
    extraction_id = bca.client_orderid(4)
    ob.set_extraction_id(extraction_id)
    ob.set_default_params(base_request)
    ob.set_filter(["Order ID", ord_id])
    order_id = ExtractionDetail("orderBook.order_id", "Order ID")
    order_sts = ExtractionDetail('orderBook.Sts', 'Sts')
    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[order_id, order_sts])))
    response = call(act_ob.getOrdersDetails, ob.request())
    verifier = Verifier(case_id)
    verifier.set_event_name('Checking order with new ttl')
    verifier.compare_values('ID', ord_id, response[order_id.name])
    verifier.compare_values('Order Sts', 'Open', response[order_sts.name])
    verifier.verify()


def cancel_order(ob_act, base_request, ord_id):
    cancel_order_request = CancelFXOrderDetails(base_request)
    cancel_order_request.set_filter(['Order ID', ord_id])
    call(ob_act.cancelOrder, cancel_order_request.build())


def open_ot_by_doubleclick_row(btd, cp_service, _row, _side):
    request = PlaceRateTileTableOrderRequest(btd, _row, _side)
    call(cp_service.placeRateTileTableOrder, request.build())


def place_order(base_request, service, _client):
    place_request = PlaceRatesTileOrderRequest(details=base_request)
    place_request.set_client(_client)
    call(service.placeRatesTileOrder, place_request.build())


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    case_base_request = get_base_request(session_id, case_id)
    base_tile_data = BaseTileData(base=case_base_request)
    base_details = BaseTileDetails(base=case_base_request)
    ob_act = Stubs.win_act_order_book
    cp_service = Stubs.win_act_cp_service
    pos_service = Stubs.act_fx_dealing_positions
    try:
        # Step 1
        expecting_pos = get_dealing_positions_details(pos_service, case_base_request, symbol, account)
        set_send_hedge_order(case_id, ttl_null)
        time.sleep(3)
        # call(cp_service.createRatesTile, base_details.build())
        # modify_rates_tile(base_details, cp_service, instrument_tier, client_tier)
        # open_ot_by_doubleclick_row(base_tile_data, cp_service, row, SELL)
        # place_order(base_details, cp_service, client)
        send_rfq_and_filled_order_sell(case_id, '3000000')

        # Step 2
        ord_id = check_order_book_ao('Checking placed order', case_id, case_base_request, ob_act)
        time.sleep(40)
        check_order_book_after_ttl_expire(case_id, case_base_request, ob_act, ord_id)
        # Step 3
        set_send_hedge_order(case_id, ttl_test)
        time.sleep(3)
        ord_id = check_order_book_ao('Extracting order ID for cancelling', case_id, case_base_request, ob_act)
        cancel_order(ob_act, case_base_request, ord_id)
        ord_id = check_order_book_ao('Extracting order ID with new TTL', case_id, case_base_request, ob_act)
        time.sleep(60)
        # Step 4
        check_order_book_new_ttl_applied(case_id, case_base_request, ob_act, ord_id)
        # open_ot_by_doubleclick_row(base_tile_data, cp_service, row, BUY)
        # place_order(base_details, cp_service, client)
        send_rfq_and_filled_order_buy(case_id, '3000000')
        cancel_order(ob_act, case_base_request, ord_id)
        # Step 5
        actual_pos = get_dealing_positions_details(pos_service, case_base_request, symbol, account)
        compare_position('Checking positions', case_id, expecting_pos, actual_pos)
    except Exception as e:
        logging.error('Error execution', exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
    finally:
        try:
            # Close tile
            call(cp_service.closeRatesTile, base_details.build())
            # Set default parameters
            set_send_hedge_order(case_id, ttl_default)
        except Exception:
            logging.error("Error execution", exc_info=True)
