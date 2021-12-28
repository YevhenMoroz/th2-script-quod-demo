import logging
from datetime import datetime
from pathlib import Path
from th2_grpc_act_rest_quod.act_rest_quod_pb2 import SubmitMessageRequest
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_framework.win_gui_wrappers.fe_trading_constant import PriceNaming
from test_framework.win_gui_wrappers.forex.client_rates_tile import ClientRatesTile
from win_gui_modules.wrappers import set_base

timestamp = str(datetime.now().timestamp())
timestamp = timestamp.split(".", 1)
timestamp = timestamp[0]


def set_spread_and_margin(service, case_id, min_spread, max_spread):
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
                "MDQuoteType": "TRD",
                "activeQuote": "true",
                "marginPriceType": "PIP",
                "lastUpdateTime": timestamp,
                "validatePriceSlippage": "false",
                "priceSlippageRange": 0,
                "clientTierInstrSymbolTenorQty": [
                    {
                        "MDQuoteType": "TRD",
                        "activeQuote": "true",
                        "defaultOfferMargin": 3,
                        "defaultBidMargin": 2,
                        "indiceUpperQty": 1
                    }
                ]
            },
            {
                "tenor": "WK1",
                "minSpread": 0.1,
                "maxSpread": 0.2,
                "MDQuoteType": "TRD",
                "activeQuote": "true",
                "marginPriceType": "PIP",
                "lastUpdateTime": timestamp,
                "validatePriceSlippage": "false",
                "priceSlippageRange": 0,
                "clientTierInstrSymbolTenorQty": [
                    {
                        "MDQuoteType": "TRD",
                        "activeQuote": "true",
                        "defaultOfferMargin": 1.2,
                        "defaultBidMargin": 1,
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


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)

    set_base(session_id, case_id)

    api_service = Stubs.api_service
    client_tier = "Silver"
    instrument = "GBP/USD-SPOT"
    min_spread = "0"
    max_spread = "2.0"
    pn = PriceNaming
    rates_tile = None
    try:
        # Step 1
        set_spread_and_margin(api_service, case_id, min_spread, max_spread)
        # Step 2
        rates_tile = ClientRatesTile(case_id, session_id)
        rates_tile.modify_client_tile(instrument=instrument, client_tier=client_tier)
        spread = rates_tile.extract_prices_from_tile(pn.spread)
        rates_tile.compare_values(expected_value=max_spread, actual_value=spread[pn.spread.value],
                                  event_name="Check spread", value_name="Spread")

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
    finally:
        try:
            rates_tile.close_tile()

        except Exception:
            logging.error("Error execution", exc_info=True)
