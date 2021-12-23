import logging
from datetime import datetime
from pathlib import Path
from time import sleep

from custom.verifier import Verifier, VerificationMethod
from stubs import Stubs
from custom import basic_custom_actions as bca
from test_framework.fix_wrappers import DataSet
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.RestApiMessages import RestApiMessages
from test_framework.win_gui_wrappers import data_set
from test_framework.win_gui_wrappers.data_set import PriceNaming
from test_framework.win_gui_wrappers.forex.client_rates_tile import ClientRatesTile
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
instrument = 'USD/DKK-1W'
status_true = 'true'
status_false = 'false'
timestamp = str(datetime.now().timestamp())
timestamp = timestamp.split(".", 1)
timestamp = timestamp[0]
case_venue = "MS"
case_session_alias = 'rest_wa314luna'

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
            "venueID": case_venue,
            'excludeWhenUnhealthy': 'false',
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
            "venueID": case_venue,
            'excludeWhenUnhealthy': status_false,
        }
    ]
}

def check_prices(case_id, name, bid_act, ask_act, bid_exp, ask_exp):
    verifier = Verifier(case_id)
    verifier.set_event_name(name)
    verifier.compare_values("Bid price", bid_exp, bid_act, VerificationMethod.NOT_EQUALS)
    verifier.compare_values("Ask price", ask_exp, ask_act, VerificationMethod.NOT_EQUALS)
    verifier.verify()


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    case_base_request = get_base_request(session_id, case_id)
    base_details = BaseTileDetails(base=case_base_request)
    modify_venue_message = RestApiMessages()
    modify_instrument_message = RestApiMessages()
    rest_manager = RestApiManager(case_session_alias, case_id)
    try:
        # Precondition
        modify_venue_message.modify_venue_status_metric(case_venue)
        modify_instrument_message.modify_client_tier_instrument(modify_params)

        rest_manager.send_post_request(modify_venue_message)
        rest_manager.send_post_request(modify_instrument_message)
        sleep(10)
        # Step 1
        rates_tile = ClientRatesTile(case_id, session_id)
        rates_tile.modify_client_tile(instrument, client_tier)
        prices_init = rates_tile.extract_prices_from_tile(PriceNaming.ask_pips, PriceNaming.bid_pips)
        check_prices(case_id, 'Checking that prices not null',
                     prices_init[PriceNaming.ask_pips.value],
                     prices_init[PriceNaming.bid_pips.value], '', '')
        # Step 2
        modify_venue_message.modify_venue_status_metric(case_venue, status_true)
        modify_params["clientTierInstrSymbolFwdVenue"][0]['excludeWhenUnhealthy'] = status_true
        modify_instrument_message.modify_client_tier_instrument(modify_params)
        rest_manager.send_post_request(modify_venue_message)
        rest_manager.send_post_request(modify_instrument_message)
        sleep(10)
        prices_new = rates_tile.extract_prices_from_tile(PriceNaming.ask_pips, PriceNaming.bid_pips)
        check_prices(case_id, 'Checking that prices now null',
                     prices_new[PriceNaming.ask_pips.value],
                     prices_new[PriceNaming.bid_pips.value],
                     prices_init[PriceNaming.ask_pips.value],
                     prices_init[PriceNaming.bid_pips.value])
    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
    finally:
        try:
            # Close tiles
            call(cp_service.closeRatesTile, base_details.build())
            # Set settings back
            modify_venue_message.modify_venue_status_metric(case_venue)
            modify_params["clientTierInstrSymbolFwdVenue"][0]['excludeWhenUnhealthy'] = status_false
            modify_instrument_message.modify_client_tier_instrument(modify_params)
            rest_manager.send_post_request(modify_venue_message)
            rest_manager.send_post_request(modify_instrument_message)
        except Exception:
            logging.error("Error execution", exc_info=True)

