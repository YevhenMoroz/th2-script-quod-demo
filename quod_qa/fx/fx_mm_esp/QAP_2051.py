import logging
import time
from datetime import datetime
from pathlib import Path
from th2_grpc_act_rest_quod.act_rest_quod_pb2 import SubmitMessageRequest
from th2_grpc_common.common_pb2 import ConnectionID
from th2_grpc_sim_fix_quod.sim_pb2 import RequestMDRefID

from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import spo
from custom.verifier import Verifier
from quod_qa.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from quod_qa.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq
from stubs import Stubs
from win_gui_modules.client_pricing_wrappers import ExtractRatesTileTableValuesRequest, ModifyRatesTileRequest
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.order_book_wrappers import ExtractionDetail
from win_gui_modules.utils import call, get_base_request
from win_gui_modules.wrappers import set_base

timestamp = str(datetime.now().timestamp())
timestamp = timestamp.split(".", 1)
timestamp = timestamp[0]


def set_spread_and_margin(service, case_id, min_spread, max_spread, bid_margin, offer_margin):
    modify_params = {
        "instrSymbol": "GBP/USD",
        "quoteTTL": 120,
        "clientTierID": 2200009,
        "alive": "true",
        "clientTierInstrSymbolQty": [
            {
                "upperQty": 1000000,
                "indiceUpperQty": 1,
                "publishPrices": "true"
            }
        ],
        "clientTierInstrSymbolTenor": [
            {
                "tenor": "SPO",
                "minSpread": min_spread,
                "maxSpread": max_spread,
                "marginPriceType": "PIP",
                "lastUpdateTime": timestamp,
                "MDQuoteType": "TRD",
                "activeQuote": "true",
                "priceSlippageRange": 0,
                "validatePriceSlippage": "false",
                "clientTierInstrSymbolTenorQty": [
                    {
                        "MDQuoteType": "TRD",
                        "activeQuote": "true",
                        "indiceUpperQty": 1,
                        "defaultBidMargin": bid_margin,
                        "defaultOfferMargin": offer_margin,
                    }
                ]
            },
            {
                "tenor": "WK1",
                "minSpread": "0.1",
                "maxSpread": "0.2",
                "marginPriceType": "PIP",
                "lastUpdateTime": timestamp,
                "MDQuoteType": "TRD",
                "activeQuote": "true",
                "priceSlippageRange": 0,
                "validatePriceSlippage": "false",
                "clientTierInstrSymbolTenorQty": [
                    {
                        "MDQuoteType": "TRD",
                        "activeQuote": "true",
                        "indiceUpperQty": 1,
                        "defaultBidMargin": 1,
                        "defaultOfferMargin": 1.2,
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
                "accountGroupID": "Silver1"
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


def check_base(base_request, service, case_id, bid_base, offer_base):
    extract_table_request = ExtractRatesTileTableValuesRequest(details=base_request)
    extraction_id = bca.client_orderid(4)
    extract_table_request.set_extraction_id(extraction_id)
    extract_table_request.set_ask_extraction_field(ExtractionDetail("rateTile.askBase", "Base"))
    extract_table_request.set_bid_extraction_field(ExtractionDetail("rateTile.bidBase", "Base"))
    response = call(service.extractRatesTileTableValues, extract_table_request.build())

    verifier = Verifier(case_id)
    verifier.set_event_name("Check base margins")
    verifier.compare_values("Base", bid_base, response["rateTile.bidBase"])
    verifier.compare_values("Base", offer_base, response["rateTile.askBase"])
    verifier.verify()


def check_effective(base_request, service):
    extract_table_request = ExtractRatesTileTableValuesRequest(details=base_request)
    extraction_id = bca.client_orderid(4)
    extract_table_request.set_extraction_id(extraction_id)
    extract_table_request.set_bid_extraction_field(ExtractionDetail("rateTile.bidEffect", "-"))
    extract_table_request.set_bid_extraction_field(ExtractionDetail("rateTile.askEffect", "+"))
    response = call(service.extractRatesTileTableValues, extract_table_request.build())
    return str(response["rateTile.askEffect"])


def create_or_get_rates_tile(base_request, service):
    call(service.createRatesTile, base_request.build())


def modify_rates_tile(base_request, service, instrument, client):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.set_client_tier(client)
    modify_request.set_instrument(instrument)
    call(service.modifyRatesTile, modify_request.build())


def check_price(case_id, send_px, effective, actual_px):
    expected_px = float(send_px) + float(effective) / 10000
    expected_px = round(expected_px, 5)

    verifier = Verifier(case_id)
    verifier.set_event_name("Check price calculation")
    verifier.compare_values("Price", str(expected_px), str(actual_px))
    verifier.verify()


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)

    set_base(session_id, case_id)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    simulator = Stubs.simulator
    act = Stubs.fix_act

    api_service = Stubs.api_service
    cp_service = Stubs.win_act_cp_service
    case_base_request = get_base_request(session_id, case_id)
    base_details = BaseTileDetails(base=case_base_request)

    client_tier = "Silver"
    account = "Silver1"
    symbol = "GBP/USD"
    instrument = "GBP/USD-SPOT"
    security_type_spo = "FXSPOT"
    settle_date = spo()
    settle_type = "0"
    currency = "GBP"
    settle_currency = "USD"
    side = "1"
    qty = "1000000"
    bid_margin = "2"
    offer_margin = "3"
    offer_px = "1.18150"
    bid_px = "1.1825"
    try:
        # Step 1
        set_spread_and_margin(api_service, case_id, "2", "10", bid_margin, offer_margin)
        # Step 2
        mdu_params_spo = {
            "MDReqID": simulator.getMDRefIDForConnection314(
                request=RequestMDRefID(
                    symbol="GBP/USD:SPO:REG:HSBC",
                    connection_id=ConnectionID(session_alias="fix-fh-314-luna"))).MDRefID,
            'Instrument': {
                'Symbol': 'GBP/USD',
                'SecurityType': 'FXSPOT'
            },
            "NoMDEntries": [
                {
                    "MDEntryType": "0",
                    "MDEntryPx": offer_px,
                    "MDEntrySize": 1000000,
                    "MDEntryPositionNo": 1,
                    'SettlDate': spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": bid_px,
                    "MDEntrySize": 1000000,
                    "MDEntryPositionNo": 1,
                    'SettlDate': spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                }
            ]
        }

        act.sendMessage(
            bca.convert_to_request(
                'Send Market Data SPOT',
                'fix-fh-314-luna',
                case_id,
                bca.message_to_grpc('MarketDataSnapshotFullRefresh', mdu_params_spo, 'fix-fh-314-luna')
            ))
        create_or_get_rates_tile(base_details, cp_service)
        modify_rates_tile(base_details, cp_service, instrument, client_tier)
        check_base(base_details, cp_service, case_id, bid_margin, offer_margin)
        effective = check_effective(base_details, cp_service)
        params_spot = CaseParamsSellRfq(account, case_id, orderqty=qty, symbol=symbol,
                                        securitytype=security_type_spo, settldate=settle_date,
                                        settltype=settle_type, securityid=symbol,
                                        currency=currency, side=side, settlcurrency=settle_currency,
                                        account=account)

        rfq = FixClientSellRfq(params_spot)
        rfq.send_request_for_quote()
        rfq.verify_quote_pending()
        price_from_quote = rfq.extract_filed("OfferPx")
        check_price(case_id, bid_px, effective, price_from_quote)

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
    finally:
        try:
            # Close tile
            call(cp_service.closeRatesTile, base_details.build())

        except Exception:
            logging.error("Error execution", exc_info=True)
