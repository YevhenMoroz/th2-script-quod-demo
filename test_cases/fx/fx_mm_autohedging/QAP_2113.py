import locale
from random import randint
from decimal import Decimal

from th2_grpc_act_gui_quod.common_pb2 import BaseTileData
from custom.tenor_settlement_date import spo
from custom.verifier import Verifier, VerificationMethod
from stubs import Stubs
from custom import basic_custom_actions as bca
from test_cases.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from test_cases.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq
from test_framework.win_gui_wrappers.data_set import OrderBookColumns, ExecSts
from test_framework.win_gui_wrappers.forex.fx_order_book import FXOrderBook
from win_gui_modules.dealing_positions_wrappers import GetOrdersDetailsRequest, ExtractionPositionsFieldsDetails, \
    ExtractionPositionsAction, PositionsInfo
from win_gui_modules.order_book_wrappers import OrdersDetails, ExtractionDetail, OrderInfo, ExtractionAction, \
    CancelFXOrderDetails, ModifyFXOrderDetails
from win_gui_modules.order_ticket import FXOrderDetails
from win_gui_modules.client_pricing_wrappers import BaseTileDetails,\
    ModifyRatesTileRequest, PlaceRateTileTableOrderRequest, RatesTileTableOrdSide, PlaceRatesTileOrderRequest
from win_gui_modules.utils import get_base_request, call
import logging
from pathlib import Path


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
client = 'Osmium1'
client_tier = "Osmium"
account = 'Osmium1_1'
account_quod = 'QUOD3_1'
symbol = 'EUR/USD'
side_b = "1"
side_s = "2"
instrument_tier = 'EUR/USD-SPOT'
security_type_spo = "FXSPOT"
settle_date_spo = spo()
settle_type_spo = "0"
currency = "EUR"
settle_currency = "USD"
locale.setlocale(locale.LC_ALL, 'en_us')
ord_qty = randint(2000000, 4000000)
new_qty = randint(int(ord_qty), int(ord_qty)+1000000)
ord_qty_ob = '{0:n}'.format(Decimal(ord_qty))
new_qty_ob = '{0:n}'.format(Decimal(new_qty))
api = Stubs.api_service
ttl_test = 500
ttl_default = 120
verification_equal = VerificationMethod.EQUALS
verification_not_equal = VerificationMethod.NOT_EQUALS

status_true = 'true'
status_false = 'false'


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


def amend_order(base_request, service, _qty):
    place_request = PlaceRatesTileOrderRequest(details=base_request)
    place_request.set_quantity(str(_qty))
    call(service.placeRatesTileOrder, place_request.build())


def execute(report_id, session_id):
    ob_names = OrderBookColumns
    sts_names = ExecSts
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    case_base_request = get_base_request(session_id, case_id)
    base_details = BaseTileDetails(base=case_base_request)
    cp_service = Stubs.win_act_cp_service
    pos_service = Stubs.act_fx_dealing_positions
    try:
        expecting_pos = get_dealing_positions_details(pos_service, case_base_request, symbol, account)
        send_rfq_and_filled_order_sell(case_id, ord_qty)
        order_info = FXOrderBook(case_id, session_id).set_filter([ob_names.order_id.value, 'AO',
                                                                  ob_names.orig.value, 'AutoHedger']). \
            extract_fields_list({ob_names.order_id.value: '', ob_names.qty.value: ''})
        FXOrderBook(case_id, session_id).check_order_fields_list({
            ob_names.order_id.value: order_info[ob_names.order_id.value],
            ob_names.orig.value: 'AutoHedger',
            ob_names.qty.value: order_info[ob_names.qty.value],
            ob_names.sts.value: sts_names.open.value},
            event_name='Checking that AH triggered')
        #TODO Add order amending

        amend_order(base_details, cp_service, new_qty)

        order_info = FXOrderBook(case_id, session_id).set_filter([ob_names.order_id.value, 'AO',
                                                                  ob_names.orig.value, 'AutoHedger']). \
            extract_fields_list({ob_names.order_id.value: '', ob_names.qty.value: ''})
        FXOrderBook(case_id, session_id).check_order_fields_list({
            ob_names.order_id.value: order_info[ob_names.order_id.value],
            ob_names.orig.value: 'AutoHedger',
            ob_names.qty.value: new_qty_ob,
            ob_names.sts.value: sts_names.open.value},
            event_name='Checking that hedged order qty changed')
        FXOrderBook(case_id, session_id).set_filter([ob_names.order_id.value, order_info[ob_names.order_id.value]]).\
            cancel_order()
        FXOrderBook(case_id, session_id).check_order_fields_list({
            ob_names.order_id.value: order_info[ob_names.order_id.value],
            ob_names.orig.value: 'AutoHedger',
            ob_names.qty.value: ord_qty_ob,
            ob_names.sts.value: sts_names.open.value},
            event_name='Checking that new hedged order created with qty from Position Book')
        send_rfq_and_filled_order_buy(case_id, ord_qty)
        FXOrderBook(case_id, session_id).set_filter([ob_names.order_id.value, order_info[ob_names.order_id.value]]). \
            cancel_order()
        actual_pos = get_dealing_positions_details(pos_service, case_base_request, symbol, account)
        compare_position('Checking positions', case_id, expecting_pos, actual_pos)
    except Exception as e:
        logging.error('Error execution', exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
