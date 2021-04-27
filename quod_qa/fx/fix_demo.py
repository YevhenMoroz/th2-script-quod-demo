import logging
from datetime import datetime
from pathlib import Path

from custom import basic_custom_actions as bca, tenor_settlement_date as tsd
from stubs import Stubs
from th2_grpc_common.common_pb2 import ConnectionID
from th2_grpc_sim_quod.sim_pb2 import RequestMDRefID
from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd
import time

from win_gui_modules.utils import set_session_id, get_base_request
from win_gui_modules.wrappers import set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True

# Logger setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Services setup
fix_act = Stubs.fix_act
verifier = Stubs.verifier
common_act = Stubs.win_act
ob_act = Stubs.win_act_order_book

# Case parameters setup

case_params = {
    'Connectivity': 'fix-qsesp-303',
    'MDReqID': bca.client_orderid(10),
    'ClOrdID': bca.client_orderid(9),
    'Account': 'MMCLIENT1',
    'HandlInst': '1',
    'Side': '1',
    'OrderQty': 1000000,
    'OrdType': '2',
    # 'Price': 35.002,
    'TimeInForce': '3',
    'Currency': 'EUR',
    'SettlCurrency': 'USD',
    'SettlType': 0,
    'SettlDate': (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y%m%d %H:%M:%S'),
    'Instrument': {
        'Symbol': 'EUR/USD',
        'SecurityType': 'FXSPOT',
        'SecurityIDSource': '8',
        'SecurityID': 'EUR/USD',
        'SecurityExchange': 'XQFX',
        'Product': '4'
        }
    }


# Send MarketDataRequest subscribe method
def send_md_subscribe(case_id):
    md_params = {
        'SenderSubID': case_params['Account'],
        'MDReqID': case_params['MDReqID'],
        'SubscriptionRequestType': '1',
        'MarketDepth': '0',
        'MDUpdateType': '0',
        'NoMDEntryTypes': [{'MDEntryType': '0'}, {'MDEntryType': '1'}],
        'NoRelatedSymbols': [
            {
                'Instrument': {
                    'Symbol': case_params['Instrument']['Symbol'],
                    'SecurityType': case_params['Instrument']['SecurityType'],
                    'Product': case_params['Instrument']['Product']
                    },
                'SettlDate': case_params['SettlDate'],
                'SettlType': case_params['SettlType']
                }
            ],
        }

    subscribe = fix_act.placeMarketDataRequestFIX(
            bca.convert_to_request('Send MDR (subscribe)', case_params['Connectivity'], case_id,
                                   bca.message_to_grpc('MarketDataRequest', md_params, case_params['Connectivity'])
                                   ))

    time.sleep(3)

    case_params['Price'] = \
        subscribe.response_messages_list[0].fields['NoMDEntries'].message_value.fields['NoMDEntries'].list_value.values[
            1].message_value.fields['MDEntryPx'].simple_value

    print(f"Price is: {case_params['Price']}")

    md_subscribe_response = {
        'MDReqID': md_params['MDReqID'],
        'Instrument': {
            'Symbol': case_params['Instrument']['Symbol']
            },
        'LastUpdateTime': '*',
        'NoMDEntries': [
            {
                'SettlType': 0,
                'MDEntryPx': '*',
                'MDEntryTime': '*',
                'MDEntryID': '*',
                'MDEntrySize': '*',
                'QuoteEntryID': '*',
                'MDOriginType': 1,
                'SettlDate': case_params['SettlDate'].split(' ')[0],
                'MDQuoteType': 1,
                'MDEntryPositionNo': 1,
                'MDEntryDate': '*',
                'MDEntryType': 0
                },
            {
                'SettlType': 0,
                'MDEntryPx': '*',
                'MDEntryTime': '*',
                'MDEntryID': '*',
                'MDEntrySize': '*',
                'QuoteEntryID': '*',
                'MDOriginType': 1,
                'SettlDate': case_params['SettlDate'].split(' ')[0],
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
                'SettlDate': case_params['SettlDate'].split(' ')[0],
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
                'SettlDate': case_params['SettlDate'].split(' ')[0],
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
                'SettlDate': case_params['SettlDate'].split(' ')[0],
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
                'SettlDate': case_params['SettlDate'].split(' ')[0],
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
                    bca.filter_to_grpc('MarketDataSnapshotFullRefresh', md_subscribe_response, ['MDReqID']),
                    subscribe.checkpoint_id,
                    case_params['Connectivity'],
                    case_id
                    )
            )

    # Return MarketDataRequest params for unsubscribe in future
    return md_params


# Send MarketDataRequest unsubscribe method
def send_md_unsubscribe(self, md_params, case_id):
    md_params['SubscriptionRequestType'] = '2'

    fix_act.sendMessage(
            bca.convert_to_request(
                    'Send MDR (unsubscribe)',
                    case_params['Connectivity'],
                    case_id,
                    bca.message_to_grpc('MarketDataRequest', md_params, case_params['Connectivity'])
                    ))


def execute(report_id,case_params):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    session_id = set_session_id()
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    act = Stubs.fix_act
    event_store = Stubs.event_store
    verifier = Stubs.verifier
    simulator = Stubs.simulator
    quote_request_qty = 500000
    instrument = 'EUR/USD'
    tenor = 'FXSPOT'

    seconds, nanos = bca.timestamps()  # Store case start time
    case_id = bca.create_event(case_name, report_id)

    mdu_params_spo = {
        "MDReqID": simulator.getMDRefIDForConnection303(request=RequestMDRefID(symbol="EUR/USD:SPO:REG:HSBC",
                                                                               connection_id=ConnectionID(
                                                                                       session_alias="fix-fh-fx-esp"))).MDRefID,
        # "MDReqID": "EUR/AED=EUR/AED:SPO:REG:HSBC_38",
        # "MDReportID": "1",
        # "MDTime": "TBU",
        # "MDArrivalTime": "TBU",
        # "OrigMDTime": "TBU",
        # "OrigMDArrivalTime": "TBU",
        # "ReplyReceivedTime": "TBU",
        'Instrument': {
            'Symbol': 'EUR/USD',
            'SecurityType': 'FXSPOT'
            },
        # "LastUpdateTime": "TBU",
        "NoMDEntries": [
            {
                "MDEntryType": "1",
                "MDEntryPx": 2.18,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                "MDEntrySpotRate": 1.18,
                "MDEntryForwardPoints": 0.0002,
                'SettlDate': tsd.spo(),
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                # "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S'),
                # "QuoteCondition": "A"
                },
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.17,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
                "MDEntrySpotRate": 1.17,
                "MDEntryForwardPoints": 0.0002,
                'SettlDate': tsd.spo(),
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S'),
                # "QuoteCondition": "A"
                },
            {
                "MDEntryType": "1",
                "MDEntryPx": 2.1810,
                "MDEntrySize": 5000000,
                "MDEntryPositionNo": 2,
                "MDEntrySpotRate": 1.18,
                "MDEntryForwardPoints": 0.0002,
                'SettlDate': tsd.spo(),
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S'),
                # "QuoteCondition": "A"
                },
            {
                "MDEntryType": "0",
                "MDEntryPx": 1.1690,
                "MDEntrySize": 5000000,
                "MDEntryPositionNo": 2,
                "MDEntrySpotRate": 1.17,
                "MDEntryForwardPoints": 0.0002,
                'SettlDate': tsd.spo(),
                "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S'),
                # "QuoteCondition": "A"
                },
            ]
        }

    act.sendMessage(
            bca.convert_to_request(
                    'Send MDU',
                    'fix-fh-fx-esp',
                    case_id,
                    bca.message_to_grpc('MarketDataSnapshotFullRefresh', mdu_params_spo, 'fix-fh-fx-esp')
                    ))
