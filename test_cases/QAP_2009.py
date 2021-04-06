import logging
from datetime import datetime
from custom import basic_custom_actions as bca, tenor_settlement_date as tsd
from stubs import Stubs
from th2_grpc_common.common_pb2 import ConnectionID
from th2_grpc_sim_quod.sim_pb2 import RequestMDRefID


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(case_name, report_id, case_params):
    act = Stubs.fix_act
    event_store = Stubs.event_store
    verifier = Stubs.verifier
    simulator = Stubs.simulator
    quote_request_qty = 500000
    instrument = 'EUR/USD'
    tenor = 'FXSPOT'

    seconds, nanos = bca.timestamps()  # Store case start time
    case_id = bca.create_event(case_name, report_id)

    instrument = {
        'Symbol': 'EUR/USD',
        'Product': '4',
        'SettlDate': tsd.spo(),
        'SecurityType': 'FXSPOT'
    }

    mdu_params_hsbc = {
        "MDReqID": simulator.getMDRefIDForConnection303(
                request=RequestMDRefID(
                        symbol='EUR/USD:SPO:REG:HSBC',
                        connection_id=ConnectionID(session_alias="fix-fh-fx-esp"))).MDRefID,
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
                "MDEntryPx": 1.02,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.026,
                "MDEntrySize": 2000000,
                "MDEntryPositionNo": 2,
            }
        ]
    }

    act.sendMessage(
        bca.convert_to_request(
            'Send MDU EUR/USD:SPO:REG:HSBC',
            'fix-fh-fx-esp',
            case_id,
            bca.message_to_grpc('MarketDataSnapshotFullRefresh', mdu_params_hsbc, 'fix-fh-fx-esp')
        ))

    mdu_params_citi = {
        "MDReqID": simulator.getMDRefIDForConnection303(
            request=RequestMDRefID(
                symbol='EUR/USD:SPO:REG:CITI',
                connection_id=ConnectionID(session_alias="fix-fh-fx-esp"))).MDRefID,
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
                "MDEntryPx": 1.02,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.025,
                "MDEntrySize": 5000000,
                "MDEntryPositionNo": 2,
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.04,
                "MDEntrySize": 10000000,
                "MDEntryPositionNo": 3,
            }
        ]
    }

    act.sendMessage(
        bca.convert_to_request(
            'Send MDU EUR/USD:SPO:REG:CITI',
            'fix-fh-fx-esp',
            case_id,
            bca.message_to_grpc('MarketDataSnapshotFullRefresh', mdu_params_citi, 'fix-fh-fx-esp')
        ))

    mdu_params_gs = {
        "MDReqID": simulator.getMDRefIDForConnection303(
            request=RequestMDRefID(
                symbol='EUR/USD:SPO:REG:GS',
                connection_id=ConnectionID(session_alias="fix-fh-fx-esp"))).MDRefID,
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
                "MDEntryPx": 1.01,
                "MDEntrySize": 1000000,
                "MDEntryPositionNo": 1,
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.02,
                "MDEntrySize": 5000000,
                "MDEntryPositionNo": 2,
            },
            {
                "MDEntryType": "1",
                "MDEntryPx": 1.03,
                "MDEntrySize": 10000000,
                "MDEntryPositionNo": 3,
            }
        ]
    }

    act.sendMessage(
        bca.convert_to_request(
            'Send MDU EUR/USD:SPO:REG:GS',
            'fix-fh-fx-esp',
            case_id,
            bca.message_to_grpc('MarketDataSnapshotFullRefresh', mdu_params_gs, 'fix-fh-fx-esp')
        ))

    subscribe_params = {
        'SenderSubID': 'MMCLIENT1',
        'MDReqID': '1111222001',
        'SubscriptionRequestType': '1',
        'MarketDepth': '0',
        'MDUpdateType': '0',
        'NoMDEntryTypes': [{'MDEntryType': '0'}, {'MDEntryType': '1'}],
        'NoRelatedSymbols': [
            {
                'Instrument': instrument
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
                'SettlDate': instrument['SettlDate'],
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
                'SettlDate': instrument['SettlDate'],
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
                'SettlDate': instrument['SettlDate'],
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
                'SettlDate': instrument['SettlDate'],
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
                'SettlDate': instrument['SettlDate'],
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
                'SettlDate': instrument['SettlDate'],
                'MDQuoteType': 1,
                'MDEntryPositionNo': 3,
                'MDEntryDate': '*',
                'MDEntryType': 1
            }
        ]
    }

    verifier.submitCheckRule(
        bca.create_check_rule(
            'Receive MarketDataSnapshotFullRefresh',
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

    logger.info("Case {} was executed in {} sec.".format(
        case_name, str(round(datetime.now().timestamp() - seconds))))
