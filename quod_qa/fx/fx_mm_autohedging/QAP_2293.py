import random
import time
from custom.tenor_settlement_date import spo
from custom.verifier import Verifier, VerificationMethod
from quod_qa.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from quod_qa.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq
from stubs import Stubs
from custom import basic_custom_actions as bca
from win_gui_modules.dealing_positions_wrappers import GetOrdersDetailsRequest, ExtractionPositionsFieldsDetails, \
    ExtractionPositionsAction, PositionsInfo
from win_gui_modules.order_book_wrappers import OrdersDetails, ExtractionDetail, OrderInfo, ExtractionAction
from th2_grpc_act_rest_quod.act_rest_quod_pb2 import SubmitMessageRequest
from win_gui_modules.utils import get_base_request, call
import logging
from pathlib import Path


api = Stubs.api_service
tif_default = 'DAY'
tif_test = 'FOK'
test_id = 400018
test_fake_id = 400024
status_eliminated = "Eliminated"


# FIX params
client = 'Osmium1'
client_tier = 'Osmium'
account_client = "Osmium1_1"
account_quod = "QUOD3_1"
symbol = "EUR/USD"
security_type_spo = "FXSPOT"
settle_date_spo = spo()
settle_type_spo = "0"
currency = "EUR"
settle_currency = "USD"
side = "1"
qty = str(random.randint(3000000, 4000000))


def set_send_hedge_order(case_id, strategy, tif):
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
                "algoPolicyID": strategy,
                "shortLowerQty": 0,
                "shortUpperQty": 0,
                "timeInForce": tif,
                "sendHedgeOrders": 'true',
                "exposureDuration": '120',
                "hedgeOrderDestination": "EXT"
            }

        ]
    }
    api.sendMessage(
        request=SubmitMessageRequest(message=bca.wrap_message(modify_params, 'ModifyAutoHedger', 'rest_wa314luna'),
                                     parent_event_id=case_id))


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


def check_order_book(case_id, base_request, act_ob, o_id, ord_number):
    ob = OrdersDetails()
    extraction_id = bca.client_orderid(4)
    ob.set_default_params(base_request)
    ob.set_extraction_id(extraction_id)
    ob.set_filter(["Order ID", 'AO'])
    ob.set_filter(["Orig", 'AutoHedger'])
    ob.set_filter(["Qty", qty])
    ob_id = ExtractionDetail("orderBook.id", "Order ID")
    ob_sts = ExtractionDetail("orderBook.sts", "Sts")
    ob_qty = ExtractionDetail("orderBook.qty", "Qty")
    order_info = OrderInfo.create(
        action=ExtractionAction.create_extraction_action(
            extraction_details=[ob_sts, ob_qty, ob_id]))
    order_info.set_number(ord_number)
    ob.add_single_order_info(order_info)

    response = call(act_ob.getOrdersDetails, ob.request())

    verifier = Verifier(case_id)
    verifier.set_event_name(f'Checking eliminated AH orders (#{ord_number})')
    verifier.compare_values("Sts", status_eliminated, response[ob_sts.name])
    verifier.compare_values("Qty", qty, response[ob_qty.name].repalce(',', ''))
    verifier.compare_values("Checking that it is not previous order", response[ob_id.name], o_id,
                            VerificationMethod.NOT_EQUALS)
    verifier.verify()
    return response[ob_id.name]


def check_order_number(case_id, number_of_orders):
    verifier = Verifier(case_id)
    verifier.set_event_name(f"Checking that next 5 orders were Eliminated")
    verifier.compare_values("Number of orders", '5', str(number_of_orders))
    verifier.verify()


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    case_base_request = get_base_request(session_id, case_id)
    ob_act = Stubs.win_act_order_book
    pos_service = Stubs.act_fx_dealing_positions
    try:
        # Step 1
        set_send_hedge_order(case_id, test_fake_id, tif_test)

        params_spot = CaseParamsSellRfq(client, case_id, orderqty=qty, symbol=symbol,
                                        securitytype=security_type_spo, settldate=settle_date_spo,
                                        settltype=settle_type_spo, securityid=symbol, settlcurrency=settle_currency,
                                        currency=currency, side=side,
                                        account=account_client)
        rfq = FixClientSellRfq(params_spot)
        rfq.send_request_for_quote()
        rfq.verify_quote_pending()
        price = rfq.extract_filed("OfferPx")
        rfq.send_new_order_single(price=price). \
            verify_order_pending(). \
            verify_order_filled()

        # Step 2
        actual_pos_client = get_dealing_positions_details(pos_service, case_base_request, symbol, account_client)
        compare_position('Checking positions Client Osmium1_1', case_id, qty, actual_pos_client)
        actual_pos_quod = get_dealing_positions_details(pos_service, case_base_request, symbol, account_quod)
        compare_position('Checking positions Quod QUOD3_1', case_id, f'-{qty}', actual_pos_quod)
        time.sleep(20)

        # Step 3-6
        row = 1
        order_id = ''
        while row < 6:
            order_id = check_order_book(case_id, case_base_request, ob_act, order_id, row)
            row += 1
        check_order_number(case_id, row-1)
    except Exception as e:
        logging.error('Error execution', exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
    finally:
        try:
            set_send_hedge_order(case_id, test_id, tif_default)

            params_spot = CaseParamsSellRfq(client, case_id, orderqty=qty, symbol=symbol,
                                            securitytype=security_type_spo, settldate=settle_date_spo,
                                            settltype=settle_type_spo, securityid=symbol, settlcurrency=settle_currency,
                                            currency=currency, side='2',
                                            account=account_client)
            rfq = FixClientSellRfq(params_spot)
            rfq.send_request_for_quote()
            rfq.verify_quote_pending()
            price = rfq.extract_filed("BidPx")
            rfq.send_new_order_single(price=price). \
                verify_order_pending(). \
                verify_order_filled()

            actual_pos_client = get_dealing_positions_details(pos_service, case_base_request, symbol, account_client)
            compare_position('Checking positions Client Osmium1_1', case_id, '0', actual_pos_client)
            actual_pos_quod = get_dealing_positions_details(pos_service, case_base_request, symbol, account_quod)
            compare_position('Checking positions Quod QUOD3_1', case_id, '0', actual_pos_quod)
        except:
            logging.error('Error execution', exc_info=True)
            bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
