import logging
from datetime import datetime
from custom import basic_custom_actions as bca, tenor_settlement_date as tsd
from pathlib import Path
from stubs import Stubs
from th2_grpc_common.common_pb2 import ConnectionID
from th2_grpc_sim_fix_quod.sim_pb2 import RequestMDRefID


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)



def execute(report_id):
    try:
        case_name = Path(__file__).name[:-3]
        case_id = bca.create_event(case_name, report_id)
        simulator = Stubs.simulator
        act = Stubs.fix_act
        alias = "fix-fh-314-luna"



        mdu_params_spo2 = {
            "MDReqID": simulator.getMDRefIDForConnection314(
                request=RequestMDRefID(
                    symbol="GBP/NOK:SPO:REG:BARX",
                    connection_id=ConnectionID(session_alias=alias))).MDRefID,
            'Instrument': {
                'Symbol': 'GBP/NOK',
                'SecurityType': 'FXSPOT'
            },
            "NoMDEntries": [
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.19599,
                    "MDEntrySize": 1000000,
                    "MDEntryPositionNo": 1,
                    "MDQuoteType": 0,
                    'SettlDate': tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.1981,
                    "MDEntrySize": 1000000,
                    "MDEntryPositionNo": 1,
                    "MDQuoteType": 0,
                    'SettlDate': tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.19397,
                    "MDEntrySize": 6000000,
                    "MDEntryPositionNo": 1,
                    "MDQuoteType": 0,
                    'SettlDate': tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.19909,
                    "MDEntrySize": 6000000,
                    "MDEntryPositionNo": 1,
                    "MDQuoteType": 0,
                    'SettlDate': tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.19301,
                    "MDEntrySize": 12000000,
                    "MDEntryPositionNo": 1,
                    "MDQuoteType": 0,
                    'SettlDate': tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.19999,
                    "MDEntrySize": 12000000,
                    "MDEntryPositionNo": 1,
                    "MDQuoteType": 0,
                    'SettlDate': tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
            ]
        }
        print(mdu_params_spo2)
        act.sendMessage(
            bca.convert_to_request(
                'Send Market Data SPOT',
                alias,
                case_id,
                bca.message_to_grpc('MarketDataSnapshotFullRefresh', mdu_params_spo2, alias)
            ))

        mdu_params_spo3 = {
            "MDReqID": simulator.getMDRefIDForConnection314(
                request=RequestMDRefID(
                    symbol="GBP/NOK:SPO:REG:BARX",
                    connection_id=ConnectionID(session_alias=alias))).MDRefID,
            'Instrument': {
                'Symbol': 'GBP/NOK',
                'SecurityType': 'FXSPOT'
            },
            "NoMDEntries": [
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.19599,
                    "MDEntrySize": 1000000,
                    "MDEntryPositionNo": 1,
                    "MDQuoteType": 1,
                    'SettlDate': tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.1981,
                    "MDEntrySize": 1000000,
                    "MDEntryPositionNo": 1,
                    "MDQuoteType": 1,
                    'SettlDate': tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.19397,
                    "MDEntrySize": 6000000,
                    "MDEntryPositionNo": 1,
                    "MDQuoteType": 1,
                    'SettlDate': tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.19909,
                    "MDEntrySize": 6000000,
                    "MDEntryPositionNo": 1,
                    "MDQuoteType": 1,
                    'SettlDate': tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.19301,
                    "MDEntrySize": 12000000,
                    "MDEntryPositionNo": 1,
                    "MDQuoteType": 1,
                    'SettlDate': tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.19999,
                    "MDEntrySize": 12000000,
                    "MDEntryPositionNo": 1,
                    "MDQuoteType": 1,
                    'SettlDate': tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
            ]
        }
        print(mdu_params_spo3)
        act.sendMessage(
            bca.convert_to_request(
                'Send Market Data SPOT',
                alias,
                case_id,
                bca.message_to_grpc('MarketDataSnapshotFullRefresh', mdu_params_spo3, alias)
            ))






    except Exception as e:
        logging.error('Error execution', exc_info=True)
    finally:
        # md.send_md_unsubscribe()
        pass
