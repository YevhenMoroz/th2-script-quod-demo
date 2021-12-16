from th2_grpc_act_gui_quod.common_pb2 import BaseTileData

from custom.tenor_settlement_date import spo
from custom.verifier import Verifier, VerificationMethod
from stubs import Stubs
from custom import basic_custom_actions as bca
from test_cases.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from test_cases.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq
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
account = 'Osmium1_1'
symbol = 'EUR/USD'
side_b = "1"
side_s = "2"
instrument_tier = 'EUR/USD-SPOT'
security_type_spo = "FXSPOT"
settle_date_spo = spo()
settle_type_spo = "0"
currency = "EUR"
settle_currency = "USD"
ord_qty='3000000'

status_open = 'Open'
row = 2
SELL = RatesTileTableOrdSide.SELL
BUY = RatesTileTableOrdSide.BUY
qty = '2000000'
test_id = 400018
test_fake_id = 400024
test_name = 'test'
test_fake_name = 'test_fake'
api = Stubs.api_service


def set_send_hedge_order(case_id, strategy_id):
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
                "algoPolicyID": int(strategy_id),
                "shortLowerQty": 0,
                "shortUpperQty": 0,
                "timeInForce": "DAY",
                "sendHedgeOrders": 'true',
                "exposureDuration": 120,
                "hedgeOrderDestination": "EXT"
            }
        ]
    }
    api.sendMessage(
        request=SubmitMessageRequest(message=bca.message_to_grpc('ModifyAutoHedger', modify_params, 'rest_wa314luna'),
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


def check_order_book_ao(even_name, case_id, base_request, act_ob, strategy_name):
    ob = OrdersDetails()
    extraction_id = bca.client_orderid(4)
    ob.set_extraction_id(extraction_id)
    ob.set_default_params(base_request)
    ob.set_filter(["Order ID", 'AO', "Orig", 'AutoHedger', 'Sts', 'Open'])
    order_id = ExtractionDetail("orderBook.order_id", "Order ID")
    order_strategy = ExtractionDetail('orderBook.AlgoStrategy', 'Strategy')
    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[order_id, order_strategy])))
    response = call(act_ob.getOrdersDetails, ob.request())
    verifier = Verifier(case_id)
    verifier.set_event_name(even_name)
    verifier.compare_values('Strategy', strategy_name, response[order_strategy.name])
    verifier.verify()
    ord_id = response[order_id.name]
    return ord_id


def check_order_book_after_strategy_change(case_id, case_base_request, act_ob, ord_id, strategy_name):
    ob = OrdersDetails()
    extraction_id = bca.client_orderid(4)
    ob.set_extraction_id(extraction_id)
    ob.set_default_params(case_base_request)
    ob.set_filter(["Order ID", 'AO', "Orig", 'AutoHedger', 'Sts', 'Open'])
    order_id = ExtractionDetail("orderBook.order_id", "Order ID")
    order_strategy = ExtractionDetail('orderBook.AlgoStrategy', 'Strategy')
    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[order_id, order_strategy])))
    response = call(act_ob.getOrdersDetails, ob.request())
    verifier = Verifier(case_id)
    verifier.set_event_name('Checking order strategy changed')
    verifier.compare_values('ID', ord_id, response[order_id.name], VerificationMethod.NOT_EQUALS)
    verifier.compare_values('Strategy Name', strategy_name, response[order_strategy.name])
    verifier.verify()
    return response[order_id.name]


def check_order_book_no_new_order(case_id, base_request, act_ob, ord_id):
    ob = OrdersDetails()
    extraction_id = bca.client_orderid(4)
    ob.set_extraction_id(extraction_id)
    ob.set_default_params(base_request)
    ob.set_filter(["Order ID", 'AO', "Orig", 'AutoHedger'])
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


def open_ot_by_doubleclick_row(btd, cp_service, _row, _side):
    request = PlaceRateTileTableOrderRequest(btd, _row, _side)
    call(cp_service.placeRateTileTableOrder, request.build())


def place_order(base_request, service, _client):
    place_request = PlaceRatesTileOrderRequest(details=base_request)
    place_request.set_client(client)
    call(service.placeRatesTileOrder, place_request.build())


def send_rfq_and_filled_order_buy(case_id, qty):
    params_spot = CaseParamsSellRfq(client, case_id, orderqty=qty, symbol=symbol,
                                    securitytype=security_type_spo, settldate=settle_date_spo,
                                    settltype=settle_type_spo, securityid=symbol, settlcurrency=settle_currency,
                                    currency=currency, side=side_b,
                                    account=account)
    rfq = FixClientSellRfq(params_spot)
    rfq.send_request_for_quote()
    rfq.verify_quote_pending()
    price = rfq.extract_filed("OfferPx")
    rfq.send_new_order_single(price)
    rfq.verify_order_pending().verify_order_filled()


def send_rfq_and_filled_order_sell(case_id, qty):
    params_spot = CaseParamsSellRfq(client, case_id, orderqty=qty, symbol=symbol,
                                    securitytype=security_type_spo, settldate=settle_date_spo,
                                    settltype=settle_type_spo, securityid=symbol, settlcurrency=settle_currency,
                                    currency=currency, side=side_s,
                                    account=account)
    rfq = FixClientSellRfq(params_spot)
    rfq.send_request_for_quote()
    rfq.verify_quote_pending()
    price = rfq.extract_filed("BidPx")
    rfq.send_new_order_single(price)
    rfq.verify_order_pending().verify_order_filled()


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
        set_send_hedge_order(case_id, test_fake_id)

        # call(cp_service.createRatesTile, base_details.build())
        # modify_rates_tile(base_details, cp_service, instrument_tier, client_tier)
        # open_ot_by_doubleclick_row(base_tile_data, cp_service, row, SELL)
        # place_order(base_details, cp_service, client)
        send_rfq_and_filled_order_sell(case_id, ord_qty)

        # Step 2
        ord_id = check_order_book_ao('Checking placed order', case_id, case_base_request, ob_act, test_fake_name)
        set_send_hedge_order(case_id, test_id)
        cancel_order(ob_act, case_base_request, ord_id)
        # Step 3
        ord_id = check_order_book_after_strategy_change(case_id, case_base_request, ob_act, ord_id, test_name)
        # open_ot_by_doubleclick_row(base_tile_data, cp_service, row, BUY)
        # place_order(base_details, cp_service, client)
        # cancel_order(ob_act, case_base_request, ord_id)
        send_rfq_and_filled_order_buy(case_id, ord_qty)

        # Step 4
        check_order_book_no_new_order(case_id, case_base_request, ob_act, ord_id)
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
            set_send_hedge_order(case_id, test_id)
        except Exception:
            logging.error("Error execution", exc_info=True)
