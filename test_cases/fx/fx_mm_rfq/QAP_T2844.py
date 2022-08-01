import logging
import time
from datetime import datetime
from pathlib import Path
from th2_grpc_act_rest_quod.act_rest_quod_pb2 import SubmitMessageRequest
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import spo
from custom.verifier import Verifier
from test_cases.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from test_cases.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq
from stubs import Stubs
from win_gui_modules.order_book_wrappers import FXOrdersDetails, ExtractionDetail, FXOrderInfo, ExtractionAction
from win_gui_modules.utils import call, get_base_request
from win_gui_modules.wrappers import set_base

timestamp = str(datetime.now().timestamp())
timestamp = timestamp.split(".", 1)
timestamp = timestamp[0]


def set_price_slippage(service, case_id, status, pip):
    modify_params = {
        "instrSymbol": "EUR/GBP",
        "quoteTTL": 120,
        "clientTierID": 2400009,
        "alive": "true",
        "clientTierInstrSymbolQty": [
            {
                "upperQty": 1000000,
                "indiceUpperQty": 1,
                "publishPrices": "true"
            },
            {
                "upperQty": 5000000,
                "indiceUpperQty": 2,
                "publishPrices": "true"
            }
        ],
        "clientTierInstrSymbolTenor": [
            {
                "tenor": "SPO",
                "minSpread": "0",
                "maxSpread": "300.5",
                "marginPriceType": "PIP",
                "lastUpdateTime": timestamp,
                "MDQuoteType": "TRD",
                "activeQuote": "true",
                "priceSlippageRange": pip,
                "validatePriceSlippage": status,
                "clientTierInstrSymbolTenorQty": [
                    {
                        "MDQuoteType": "TRD",
                        "activeQuote": "true",
                        "indiceUpperQty": 1
                    },
                    {
                        "MDQuoteType": "TRD",
                        "activeQuote": "true",
                        "indiceUpperQty": 2
                    }
                ]
            },
            {
                "tenor": "WK1",
                "minSpread": "0",
                "maxSpread": "250",
                "marginPriceType": "PIP",
                "lastUpdateTime": timestamp,
                "MDQuoteType": "TRD",
                "activeQuote": "true",
                "priceSlippageRange": 1,
                "validatePriceSlippage": "true",
                "clientTierInstrSymbolTenorQty": [
                    {
                        "MDQuoteType": "TRD",
                        "activeQuote": "true",
                        "indiceUpperQty": 2
                    },
                    {
                        "MDQuoteType": "TRD",
                        "activeQuote": "true",
                        "indiceUpperQty": 1
                    }
                ]
            }
        ],
        "clientTierInstrSymbolVenue": [
            {
                "venueID": "HSBC"
            }
        ],
        "clientTierInstrSymbolActGrp": [
            {
                "accountGroupID": "Iridium1"
            }
        ],
        "clientTierInstrSymbolFwdVenue": [
            {
                "venueID": "HSBC"
            }
        ]
    }
    service.sendMessage(
        request=SubmitMessageRequest(
            message=bca.wrap_message(modify_params, 'ModifyClientTierInstrSymbol', 'rest_wa314luna'),
            parent_event_id=case_id))


def check_order_book(base_request, act_ob, case_id, qty, status, notes):
    ob = FXOrdersDetails()
    extraction_id = bca.client_orderid(4)
    ob.set_default_params(base_request)
    ob.set_extraction_id(extraction_id)
    ob.set_filter(["Qty", qty])
    ob_sts = ExtractionDetail("orderBook.sts", "Sts")
    ob_notes = ExtractionDetail("orderBook.notes", "FreeNotes")
    ob.add_single_order_info(
        FXOrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[ob_sts,
                                                                                 ob_notes])))

    response = call(act_ob.getOrdersDetails, ob.request())
    verifier = Verifier(case_id)
    verifier.set_event_name("Check Order book")
    verifier.compare_values("Sts", status, response[ob_sts.name])
    verifier.compare_values("FreeNotes", notes, response[ob_notes.name])
    verifier.verify()


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)

    set_base(session_id, case_id)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    api_service = Stubs.api_service
    ob_service = Stubs.win_act_order_book_fx
    case_base_request = get_base_request(session_id, case_id)

    client_tier = "Iridium1"
    account = "Iridium1_1"
    symbol = "EUR/GBP"
    security_type_spo = "FXSPOT"
    settle_date = spo()
    settle_type = "0"
    currency = "EUR"
    settle_currency = "GBP"
    side = "1"
    qty = "1000000"

    try:
        # Step 1
        set_price_slippage(api_service, case_id, "true", 2)
        # Step 2
        time.sleep(3)
        params = CaseParamsSellRfq(client_tier, case_id, orderqty=qty, symbol=symbol,
                                   securitytype=security_type_spo, settldate=settle_date, settltype=settle_type,
                                   currency=currency, side=side, securityid=symbol, settlcurrency=settle_currency,
                                   account=account)
        rfq = FixClientSellRfq(params)
        rfq.send_request_for_quote()
        rfq.verify_quote_pending()
        price = rfq.extract_filed("OfferPx")
        range_above = str(round(float(price) + 0.0002, 5))
        range_bellow = str(round(float(price) - 0.0002, 5))
        price_above = str(round(float(price) + 0.001, 5))
        rfq.send_new_order_single(price_above)
        text = f"order price is not ranging in [{range_bellow}, {range_above}]"
        rfq.verify_order_rejected(text=text)
        check_order_book(case_base_request, ob_service, case_id, qty, "Rejected", text)
        # Step 3
        rfq.send_new_order_single(price)
        rfq.verify_order_pending().verify_order_filled()
        check_order_book(case_base_request, ob_service, case_id, qty, "Terminated", "")
        # Step 4
        set_price_slippage(api_service, case_id, "false", 2)
        time.sleep(3)
        # Step 5
        new_params = CaseParamsSellRfq(client_tier, case_id, orderqty=qty, symbol=symbol,
                                       securitytype=security_type_spo, settldate=settle_date, settltype=settle_type,
                                       currency=currency, side=side, securityid=symbol, settlcurrency=settle_currency,
                                       account=account)
        new_rfq = FixClientSellRfq(new_params)
        new_rfq.send_request_for_quote()
        new_rfq.verify_quote_pending()
        new_price = new_rfq.extract_filed("OfferPx")
        new_price_bellow = str(round(float(new_price) - 0.0001, 5))

        new_rfq.send_new_order_single(new_price_bellow)
        text = f"order price ({new_price_bellow}) lower than offer ({new_price})"
        new_rfq.verify_order_rejected(text=text)
        check_order_book(case_base_request, ob_service, case_id, qty, "Rejected", text)

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
