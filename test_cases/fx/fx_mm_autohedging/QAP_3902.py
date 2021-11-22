from th2_grpc_act_gui_quod.common_pb2 import BaseTileData
from custom.verifier import Verifier, VerificationMethod
from stubs import Stubs
from custom import basic_custom_actions as bca
from win_gui_modules.aggregated_rates_wrappers import PlaceESPOrder, ESPTileOrderSide
from win_gui_modules.dealing_positions_wrappers import GetOrdersDetailsRequest, ExtractionPositionsFieldsDetails, \
    ExtractionPositionsAction, PositionsInfo
from win_gui_modules.order_book_wrappers import OrdersDetails, ExtractionDetail, OrderInfo, ExtractionAction, \
    CancelFXOrderDetails
from win_gui_modules.order_ticket import FXOrderDetails
from win_gui_modules.order_ticket_wrappers import NewFxOrderDetails
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
firm_account = 'QUOD3'
symbol = 'EUR/USD'
instrument_tier = 'EUR/USD-SPOT'
from_currency = 'EUR'
to_currency = 'USD'
case_tenor = 'Spot'
status_open = 'Open'
row = 2
SELL = RatesTileTableOrdSide.SELL
BUY = RatesTileTableOrdSide.BUY
case_qty = '5000000'
api = Stubs.api_service
column_positions = 'Position'
column_working = 'Working Position'
owner = Stubs.custom_config['qf_trading_fe_user']


def set_send_hedge_order(case_id):
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
                "timeInForce": 'GTC',
                "sendHedgeOrders": 'true',
                "exposureDuration": 120,
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


def get_dealing_positions_details(del_act, base_request, symbol, account, column):
    dealing_positions_details = GetOrdersDetailsRequest()
    dealing_positions_details.set_default_params(base_request)
    extraction_id = bca.client_orderid(4)
    dealing_positions_details.set_extraction_id(extraction_id)
    dealing_positions_details.set_filter(["Symbol", symbol, "Account", account])
    position = ExtractionPositionsFieldsDetails("dealingpositions.position", column)
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


def create_or_get_esp_tile(base_request, service):
    call(service.createRatesTile, base_request.build())


def modify_esp_tile(base_request, service, from_c, to_c, tenor, qty):
    from win_gui_modules.aggregated_rates_wrappers import ModifyRatesTileRequest
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.set_instrument(from_c, to_c, tenor)
    modify_request.set_quantity(qty)
    call(service.modifyRatesTile, modify_request.build())


def check_order_book_hedger(even_name, case_id, base_request, act_ob, qty):
    ob = OrdersDetails()
    extraction_id = bca.client_orderid(4)
    ob.set_extraction_id(extraction_id)
    ob.set_default_params(base_request)
    ob.set_filter(['Order ID', 'AO', "Orig", 'AutoHedger', 'Sts', 'Open'])
    order_tif = ExtractionDetail('orderBook.TIF', 'TIF')
    order_sts = ExtractionDetail('orderBook.Sts', 'Sts')
    order_qty = ExtractionDetail('orderBook.Qty', 'Qty')
    order_id = ExtractionDetail('orderBook.ID', 'Order ID')
    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[order_tif, order_sts, order_id,
                                                                                 order_qty])))
    response = call(act_ob.getOrdersDetails, ob.request())
    verifier = Verifier(case_id)
    verifier.set_event_name(even_name)
    verifier.compare_values('TIF', 'GoodTillCancel', response[order_tif.name])
    verifier.compare_values('Sts', 'Open', response[order_sts.name])
    verifier.compare_values('Qty, doesnt match placed algo', qty, response[order_qty.name].replace(",", ""),
                            VerificationMethod.NOT_EQUALS)
    verifier.verify()
    ord_id = response[order_id.name]
    return ord_id


def check_order_book_algo(even_name, case_id, base_request, act_ob, qty):
    ob = OrdersDetails()
    extraction_id = bca.client_orderid(4)
    ob.set_extraction_id(extraction_id)
    ob.set_default_params(base_request)
    ob.set_filter(['Order ID', 'AO', "Orig", 'TradingFE', 'Sts', 'Open', 'Owner', owner, 'Qty', qty])
    order_tif = ExtractionDetail('orderBook.TIF', 'TIF')
    order_sts = ExtractionDetail('orderBook.Sts', 'Sts')
    order_qty = ExtractionDetail('orderBook.Qty', 'Qty')
    order_id = ExtractionDetail('orderBook.ID', 'Order ID')
    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[order_tif, order_sts, order_id,
                                                                                 order_qty])))
    response = call(act_ob.getOrdersDetails, ob.request())
    verifier = Verifier(case_id)
    verifier.set_event_name(even_name)
    verifier.compare_values('TIF', 'GoodTillCancel', response[order_tif.name])
    verifier.compare_values('Sts', 'Open', response[order_sts.name])
    verifier.compare_values('Qty', qty, response[order_qty.name], VerificationMethod.NOT_EQUALS)
    verifier.verify()
    ord_id = response[order_id.name]
    ord_qty = response[order_qty.name].replace(",", "")
    return ord_id, ord_qty


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


def place_order_esp(base_request, service):
    esp_request = PlaceESPOrder(details=base_request)
    esp_request.set_action(ESPTileOrderSide.BUY)
    esp_request.top_of_book()
    call(service.placeESPOrder, esp_request.build())


def send_order(base_request, service):
    order_ticket = FXOrderDetails()
    order_ticket.set_place()
    order_ticket.set_client(firm_account)
    order_ticket.set_strategy('Hedging_Test')
    # order_ticket.set_child_strategy('Hedging_Test')
    order_ticket.set_price_pips('000')
    order_ticket.set_tif('GoodTillCancel')
    new_order_details = NewFxOrderDetails(base_request, order_ticket)
    call(service.placeFxOrder, new_order_details.build())


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    case_base_request = get_base_request(session_id, case_id)
    base_tile_data = BaseTileData(base=case_base_request)
    base_details = BaseTileDetails(base=case_base_request)
    ob_act = Stubs.win_act_order_book
    cp_service = Stubs.win_act_cp_service
    ar_service = Stubs.win_act_aggregated_rates_service
    pos_service = Stubs.act_fx_dealing_positions
    order_ticket_service = Stubs.win_act_order_ticket_fx
    try:
        # Step 1
        initial_pos = get_dealing_positions_details(pos_service, case_base_request, symbol, account, column_positions)
        initial_pos_working = get_dealing_positions_details(pos_service, case_base_request, symbol, account,
                                                            column_working)
        set_send_hedge_order(case_id)
        create_or_get_esp_tile(base_details, ar_service)
        modify_esp_tile(base_details, ar_service, from_currency, to_currency, case_tenor, case_qty)
        place_order_esp(base_details, ar_service)
        send_order(case_base_request, order_ticket_service)
        # Step 2
        order_id_algo, algo_qty = check_order_book_algo('Checking placed order', case_id, case_base_request, ob_act,
                                                        case_qty)
        affected_pos_working = get_dealing_positions_details(pos_service, case_base_request, symbol, account,
                                                             column_working)
        compare_position('Checking that work positions affected by algo order', case_id, affected_pos_working, algo_qty)
        call(cp_service.createRatesTile, base_details.build())
        modify_rates_tile(base_details, cp_service, instrument_tier, client_tier)
        open_ot_by_doubleclick_row(base_tile_data, cp_service, row, SELL)
        place_order(base_details, cp_service, client)
        order_id_ah = check_order_book_hedger('Checking placed AH order', case_id, case_base_request, ob_act, algo_qty)
        # Step 4
        open_ot_by_doubleclick_row(base_tile_data, cp_service, row, BUY)
        place_order(base_details, cp_service, client)
        cancel_order(ob_act, case_base_request, order_id_ah)
        cancel_order(ob_act, case_base_request, order_id_algo)
        affected_pos = get_dealing_positions_details(pos_service, case_base_request, symbol, account,
                                                     column_positions)
        affected_pos_working = get_dealing_positions_details(pos_service, case_base_request, symbol, account,
                                                             column_working)
        compare_position('Checking positions back to initial', case_id, initial_pos, affected_pos)
        compare_position('Checking working positions back to initial', case_id, initial_pos_working,
                         affected_pos_working)
    except Exception as e:
        logging.error('Error execution', exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
    finally:
        try:
            pass
            # Close tile
            call(ar_service.closeRatesTile, base_details.build())
            call(cp_service.closeRatesTile, base_details.build())
        except Exception:
            logging.error("Error execution", exc_info=True)
