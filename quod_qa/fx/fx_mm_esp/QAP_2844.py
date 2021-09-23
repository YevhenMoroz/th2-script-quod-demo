import logging
from datetime import datetime
from pathlib import Path
from custom.verifier import Verifier, VerificationMethod
from stubs import Stubs
from custom import basic_custom_actions as bca
from win_gui_modules.client_pricing_wrappers import BaseTileDetails
from th2_grpc_act_rest_quod.act_rest_quod_pb2 import SubmitMessageRequest
from win_gui_modules.utils import get_base_request, call

api = Stubs.api_service
ob_act = Stubs.win_act_order_book
cp_service = Stubs.win_act_cp_service
pos_service = Stubs.act_fx_dealing_positions
client = 'Silver1'
client_tier = 'Silver'
account = 'Silver1_1'
instrument = 'USD/DKK-Spot'
status_true = 'true'
status_false = 'false'
timestamp = str(datetime.now().timestamp())
timestamp = timestamp.split(".", 1)
timestamp = timestamp[0]
case_venue = "MS"


def modify_venue_instrsymbol(status, case_id, service, venue):
    modify_params = {
        "instrSymbol": "USD/DKK",
        "quoteTTL": 120,
        "clientTierID": 2200009,
        "alive": "true",
        "clientTierInstrSymbolQty": [
            {
                "upperQty": 1000000,
                "indiceUpperQty": 1,
                "publishPrices": "true"
            },
            {
                "upperQty": 2000000,
                "indiceUpperQty": 2,
                "publishPrices": "true"
            },
            {
                "upperQty": 3000000,
                "indiceUpperQty": 3,
                "publishPrices": "true"
            }
        ],
        "clientTierInstrSymbolTenor": [
            {
                "tenor": "SPO",
                "minSpread": "0",
                "maxSpread": "300",
                "marginPriceType": "PIP",
                "lastUpdateTime": timestamp,
                "MDQuoteType": "TRD",
                "activeQuote": "true",
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
                    },
                    {
                        "MDQuoteType": "TRD",
                        "activeQuote": "true",
                        "indiceUpperQty": 3
                    }
                ]
            },
            {
                "tenor": "WK1",
                "minSpread": "0",
                "maxSpread": "300",
                "marginPriceType": "PIP",
                "lastUpdateTime": timestamp,
                "MDQuoteType": "TRD",
                "activeQuote": "true",
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
                    },
                    {
                        "MDQuoteType": "TRD",
                        "activeQuote": "true",
                        "indiceUpperQty": 3
                    }
                ]
            }
        ],
        "clientTierInstrSymbolVenue": [
            {
                "venueID": venue,
                'excludeWhenUnhealthy': status,
                'criticalVenue': 'false'
            }
        ],
        "clientTierInstrSymbolActGrp": [
            {
                "accountGroupID": "Silver1"
            }
        ],
        "clientTierInstrSymbolFwdVenue": [
            {
                "venueID": venue,
                'excludeWhenUnhealthy': 'false',
            }
        ]
    }
    service.sendMessage(
        request=SubmitMessageRequest(
            message=bca.wrap_message(modify_params, 'ModifyClientTierInstrSymbol', 'rest_wa314luna'),
            parent_event_id=case_id))


def modify_venue_status(status, case_id, service, venue):
    modify_params = {
        'alive': 'true',
        'venueID': venue,
        'venueStatusMetric': [
            {
                'venueMetricType': "LUP",
                'enableMetric': status,
                'metricErrorThreshold': -1,
                'metricWarningThreshold': 25
            }
        ]
    }
    service.sendMessage(
        request=SubmitMessageRequest(
            message=bca.wrap_message(modify_params, 'ModifyVenueStatus', 'rest_wa314luna'),
            parent_event_id=case_id))


def create_or_get_pricing_tile(base_request, service):
    call(service.createRatesTile, base_request.build())


def modify_pricing_tile(base_request, service, instrument, client):
    from win_gui_modules.client_pricing_wrappers import ModifyRatesTileRequest
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.set_instrument(instrument)
    modify_request.set_client_tier(client)
    call(service.modifyRatesTile, modify_request.build())


def extract_price_from_pricing_tile(base_request, service, case_id, name, bid_price, ask_price):
    from win_gui_modules.client_pricing_wrappers import ExtractRatesTileValues
    extract_value_request = ExtractRatesTileValues(details=base_request)
    extraction_id = bca.client_orderid(4)
    extract_value_request.set_extraction_id(extraction_id)
    extract_value_request.extract_ask_large_value("rates_tile.ask_large")
    extract_value_request.extract_bid_large_value("rates_tile.bid_large")
    extract_value_request.extract_ask_pips("rates_tile.ask_pips")
    extract_value_request.extract_bid_pips("rates_tile.bid_pips")
    response = call(service.extractRateTileValues, extract_value_request.build())
    bid = response["rates_tile.bid_large"] + response["rates_tile.bid_pips"]
    ask = response["rates_tile.ask_large"] + response["rates_tile.ask_pips"]
    verifier = Verifier(case_id)
    verifier.set_event_name(name)
    verifier.compare_values("Bid price", bid_price, bid, VerificationMethod.NOT_EQUALS)
    verifier.compare_values("Ask price", ask_price, ask, VerificationMethod.NOT_EQUALS)
    verifier.verify()
    return [bid, ask]


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    case_base_request = get_base_request(session_id, case_id)
    base_details = BaseTileDetails(base=case_base_request)
    try:
        # Precondition
        modify_venue_status(status_false, case_id, api, case_venue)
        modify_venue_instrsymbol(status_false, case_id, api, case_venue)
        # Step 1
        create_or_get_pricing_tile(base_details, cp_service)
        modify_pricing_tile(base_details, cp_service, instrument, client_tier)
        prices = extract_price_from_pricing_tile(base_details, cp_service, case_id, 'Checking that prices presented',
                                                 '', '')
        # Step 2
        modify_venue_instrsymbol(status_true, case_id, api, case_venue)
        modify_venue_status(status_true, case_id, api, case_venue)
        extract_price_from_pricing_tile(base_details, cp_service, case_id, 'Checking that prices now null',
                                        prices[0], prices[1])
    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
    finally:
        try:
            # Close tiles
            call(cp_service.closeRatesTile, base_details.build())
            # Set settings back
            modify_venue_status(status_false, case_id, api, case_venue)
            modify_venue_instrsymbol(status_false, case_id, api, case_venue)
        except Exception:
            logging.error("Error execution", exc_info=True)

