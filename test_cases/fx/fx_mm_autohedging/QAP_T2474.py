from random import randint

from custom.tenor_settlement_date import spo
from custom.verifier import Verifier, VerificationMethod
from stubs import Stubs
from custom import basic_custom_actions as bca
from test_cases.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from test_cases.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq
from test_framework.win_gui_wrappers.fe_trading_constant import OrderBookColumns, ExecSts
from test_framework.win_gui_wrappers.forex.fx_order_book import FXOrderBook
from win_gui_modules.dealing_positions_wrappers import GetOrdersDetailsRequest, ExtractionPositionsFieldsDetails, \
    ExtractionPositionsAction, PositionsInfo
from th2_grpc_act_rest_quod.act_rest_quod_pb2 import SubmitMessageRequest
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

ord_qty = str(randint(2000000, 4000000))
qty_1 = '4000000'
qty_2 = '2000000'
api = Stubs.api_service
ttl_test = 500
ttl_default = 120
verification_equal = VerificationMethod.EQUALS
verification_not_equal = VerificationMethod.NOT_EQUALS


def set_send_hedge_order(case_id, qty, ttl):
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
                "longUpperQty": qty,
                "longLowerQty": 0,
                "maintainHedgePositions": 'true',
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


def compare_position(even_name, case_id,
                     expected_pos_acc1, actual_pos_acc1,
                     expected_pos_acc2, actual_pos_acc2,
                     acc1_name, acc2_name,
                     acc1_verify_method, acc2_verify_method):
    verifier = Verifier(case_id)
    verifier.set_event_name(even_name)
    verifier.compare_values(f"Quote position {acc1_name}", str(expected_pos_acc1),
                            str(actual_pos_acc1), acc1_verify_method)
    verifier.compare_values(f"Quote position {acc2_name}", str(expected_pos_acc2),
                            str(actual_pos_acc2), acc2_verify_method)
    verifier.verify()


def execute(report_id, session_id):
    ob_names = OrderBookColumns
    sts_names = ExecSts
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    case_base_request = get_base_request(session_id, case_id)
    pos_service = Stubs.act_fx_dealing_positions
    try:
        # Step 1
        set_send_hedge_order(case_id, qty_1, ttl_test)
        initial_pos_quod = get_dealing_positions_details(pos_service, case_base_request, symbol, account_quod)
        initial_pos_osmium = get_dealing_positions_details(pos_service, case_base_request, symbol, account)

        send_rfq_and_filled_order_buy(case_id, ord_qty)

        order_id = FXOrderBook(case_id, session_id)
        order_id.extract_field(ob_names.order_id.value)
        FXOrderBook(case_id, session_id).check_order_fields_list({
            ob_names.order_id.value: '',
            ob_names.orig.value: 'AutoHedger'},
            event_name='Checking that AH was`n triggered',
            verification_method=verification_not_equal)

        extracted_pos_quod = get_dealing_positions_details(pos_service, case_base_request, symbol, account_quod)
        extracted_pos_osmium = get_dealing_positions_details(pos_service, case_base_request, symbol, account)

        compare_position(
            'Checking positions', case_id,
            f'-{ord_qty}', extracted_pos_quod,
            ord_qty, extracted_pos_osmium,
            account_quod, account,
            verification_equal, verification_equal
        )

        set_send_hedge_order(case_id, qty_2, ttl_test)

        temp = FXOrderBook(case_id, session_id)
        order_info = temp.set_filter([ob_names.order_id.value, 'AO', ob_names.orig.value, 'AutoHedger']). \
            extract_fields_list({ob_names.order_id.value: '', ob_names.qty.value: ''})

        FXOrderBook(case_id, session_id).set_filter([ob_names.order_id.value, 'AO',
                                                     ob_names.orig.value, 'AutoHedger']). \
            check_order_fields_list({ob_names.order_id.value: order_info['Order ID'],
                                     ob_names.orig.value: 'AutoHedger',
                                     ob_names.qty.value: order_info['Qty']},
                                    event_name='Checking that AH triggered after settings changed')

        send_rfq_and_filled_order_sell(case_id, ord_qty)

        FXOrderBook(case_id, session_id).cancel_order(filter_list=[ob_names.order_id.value, order_info['Order ID']])

        FXOrderBook(case_id, session_id).set_filter([ob_names.order_id.value, 'AO',
                                                     ob_names.orig.value, 'AutoHedger']). \
            check_order_fields_list({ob_names.order_id.value: order_info['Order ID'],
                                     ob_names.sts.value: sts_names.cancelled.value},
                                    event_name='Checking that after cancel there is no new AH orders')

        extracted_pos_quod = get_dealing_positions_details(pos_service, case_base_request, symbol, account_quod)
        extracted_pos_osmium = get_dealing_positions_details(pos_service, case_base_request, symbol, account)
        compare_position(
            'Checking positions', case_id,
            initial_pos_quod, extracted_pos_quod,
            initial_pos_osmium, extracted_pos_osmium,
            account_quod, account,
            verification_equal, verification_equal
        )


    except Exception as e:
        logging.error('Error execution', exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
        send_rfq_and_filled_order_sell(case_id, ord_qty)
    finally:
        try:
            # Set default parameters
            set_send_hedge_order(case_id, qty_2, ttl_default)
        except Exception:
            logging.error("Error execution", exc_info=True)
