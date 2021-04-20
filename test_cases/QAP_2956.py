import logging
from copy import deepcopy
import time
from datetime import datetime
from custom import basic_custom_actions as bca, tenor_settlement_date as tsd
from stubs import Stubs

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(case_name, report_id, case_params):

    act = Stubs.fix_act
    verifier = Stubs.verifier

    seconds, nanos = bca.timestamps()  # Store case start time
    case_name = "QAP-2956"

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)
    instrument = {
        'Symbol': 'EUR/USD',
        'Product': '4',
        # 'SettlDate': tsd.spo(),
        'SecurityType': 'FXSPOT'
    }

    subscribe_params = {
        'SenderSubID': 'MMCLIENT1',
        'MDReqID': bca.client_orderid(7),
        'SubscriptionRequestType': '1',
        'MarketDepth': '0',
        'MDUpdateType': '0',
        'NoMDEntryTypes': [{'MDEntryType': '0'}, {'MDEntryType': '1'}],
        'NoRelatedSymbols': [
            {
                'Instrument': instrument,
                'SettlDate': tsd.spo()
            }
        ]
    }

    subscribe = act.placeMarketDataRequestFIX(
        bca.convert_to_request(
            'MarketDataRequest (subscribe)',
            case_params['Connectivity'],
            case_id,
            bca.message_to_grpc('MarketDataRequest', subscribe_params, case_params['Connectivity'])
        ))

    market_data_response = {
        'MDReqID': '1111222001',
        'Instrument': {
            'Symbol': instrument['Symbol']
        },
        'LastUpdateTime': '*',
        'OrigMDArrivalTime': '*',
        'OrigMDTime': '*',
        'MDTime': '*',
        'NoMDEntries': [
            {
                'SettlType': 0,
                'MDEntryPx': '34.999',
                'MDEntryTime': '*',
                'MDEntryID': '*',
                'MDEntrySize': 1000000,
                'QuoteEntryID': '*',
                'MDOriginType': 1,
                'SettlDate': tsd.spo(),
                'MDQuoteType': 1,
                'MDEntryPositionNo': 1,
                'MDEntryDate': '*',
                'MDEntryType': 0
            },
            {
                'SettlType': 0,
                'MDEntryPx': '35.001',
                'MDEntryTime': '*',
                'MDEntryID': '*',
                'MDEntrySize': 1000000,
                'QuoteEntryID': '*',
                'MDOriginType': 1,
                'SettlDate':  tsd.spo(),
                'MDQuoteType': 1,
                'MDEntryPositionNo': 1,
                'MDEntryDate': '*',
                'MDEntryType': 1
            },
            {
                'SettlType': 0,
                'MDEntryTime': '*',
                'MDEntryID': '*',
                'QuoteEntryID': '*',
                'MDOriginType': 1,
                'SettlDate':  tsd.spo(),
                'MDQuoteType': 1,
                'MDEntryPositionNo': 2,
                'MDEntryDate': '*',
                'MDEntryType': 0
            },
            {
                'SettlType': 0,
                'MDEntryTime': '*',
                'MDEntryID': '*',
                'QuoteEntryID': '*',
                'MDOriginType': 1,
                'SettlDate':  tsd.spo(),
                'MDQuoteType': 1,
                'MDEntryPositionNo': 2,
                'MDEntryDate': '*',
                'MDEntryType': 1
            },
            {
                'SettlType': 0,
                'MDEntryTime': '*',
                'MDEntryID': '*',
                'QuoteEntryID': '*',
                'MDOriginType': 1,
                'SettlDate':  tsd.spo(),
                'MDQuoteType': 1,
                'MDEntryPositionNo': 3,
                'MDEntryDate': '*',
                'MDEntryType': 0
            },
            {
                'SettlType': 0,
                'MDEntryTime': '*',
                'MDEntryID': '*',
                'QuoteEntryID': '*',
                'MDOriginType': 1,
                'SettlDate':  tsd.spo(),
                'MDQuoteType': 1,
                'MDEntryPositionNo': 3,
                'MDEntryDate': '*',
                'MDEntryType': 1
            }
        ]
    }

    verifier.submitCheckRule(
        bca.create_check_rule(
            'Receive MarketDataSnapshotFullRefresh (pending)',
            bca.filter_to_grpc('MarketDataSnapshotFullRefresh', market_data_response, ['MDReqID']),
            subscribe.checkpoint_id,
            case_params['Connectivity'],
            case_id
        )
    )

    subscribe_params['SubscriptionRequestType'] = '2'

    unsubscribe = act.placeMarketDataRequestFIX(
        bca.convert_to_request(
            'MarketDataRequest (subscribe)',
            case_params['Connectivity'],
            case_id,
            bca.message_to_grpc('MarketDataRequest', subscribe_params, case_params['Connectivity'])
        ))
