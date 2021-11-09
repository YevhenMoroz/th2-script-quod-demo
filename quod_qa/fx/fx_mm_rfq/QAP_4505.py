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
        # simulator = Stubs.test_sim
        act = Stubs.fix_act
        # alias = "fix-fh-q-314-luna"
        alias = "fix-fh-314-luna"


        mdu_params_spo3 = {
            "MDReqID": simulator.getMDRefIDForConnection314(
                request=RequestMDRefID(
                    symbol="EUR/USD:SPO:REG:CITI",
                    connection_id=ConnectionID(session_alias="fix-fh-314-luna"))).MDRefID,
            'Instrument': {
                'Symbol': 'EUR/USD',
                'SecurityType': 'FXSPOT'
            },
            "NoMDEntries": [
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.18079,
                    "MDEntrySize": 1000000,
                    "MDEntryPositionNo": 1,
                    "MDQuoteType": 1,
                    'SettlDate': tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.18140,
                    "MDEntrySize": 1000000,
                    "MDEntryPositionNo": 1,
                    "MDQuoteType": 1,
                    'SettlDate': tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
            ]
        }
        # simulator.updateStorage(mdu_params_spo3)
        act.sendMessage(
            bca.convert_to_request(
                'Send Market Data SPOT',
                'fix-fh-314-luna',
                case_id,
                bca.message_to_grpc('MarketDataSnapshotFullRefresh', mdu_params_spo3, 'fix-fh-314-luna')
            ))

        mdu_params_spo3 = {
            "MDReqID": simulator.getMDRefIDForConnection314(
                request=RequestMDRefID(
                    symbol="EUR/USD:SPO:REG:CITI",
                    connection_id=ConnectionID(session_alias="fix-fh-314-luna"))).MDRefID,
            'Instrument': {
                'Symbol': 'EUR/USD',
                'SecurityType': 'FXSPOT'
            },
            "NoMDEntries": [
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.17079,
                    "MDEntrySize": 2000000,
                    "MDEntryPositionNo": 1,
                    "MDQuoteType": 1,
                    'SettlDate': tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.17140,
                    "MDEntrySize": 2000000,
                    "MDEntryPositionNo": 1,
                    "MDQuoteType": 1,
                    'SettlDate': tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
            ]
        }
        # simulator.updateStorage(mdu_params_spo3)
        act.sendMessage(
            bca.convert_to_request(
                'Send Market Data SPOT',
                'fix-fh-314-luna',
                case_id,
                bca.message_to_grpc('MarketDataSnapshotFullRefresh', mdu_params_spo3, 'fix-fh-314-luna')
            ))

        mdu_params_spo3 = {
            "MDReqID": simulator.getMDRefIDForConnection314(
                request=RequestMDRefID(
                    symbol="EUR/USD:SPO:REG:CITI",
                    connection_id=ConnectionID(session_alias="fix-fh-314-luna"))).MDRefID,
            'Instrument': {
                'Symbol': 'EUR/USD',
                'SecurityType': 'FXSPOT'
            },
            "NoMDEntries": [
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.16079,
                    "MDEntrySize": 3000000,
                    "MDEntryPositionNo": 1,
                    "MDQuoteType": 1,
                    'SettlDate': tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.16140,
                    "MDEntrySize": 3000000,
                    "MDEntryPositionNo": 1,
                    "MDQuoteType": 1,
                    'SettlDate': tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
            ]
        }
        # simulator.updateStorage(mdu_params_spo3)
        act.sendMessage(
            bca.convert_to_request(
                'Send Market Data SPOT',
                'fix-fh-314-luna',
                case_id,
                bca.message_to_grpc('MarketDataSnapshotFullRefresh', mdu_params_spo3, 'fix-fh-314-luna')
            ))

        mdu_params_spo3 = {
            "MDReqID": simulator.getMDRefIDForConnection314(
                request=RequestMDRefID(
                    symbol="EUR/USD:SPO:REG:CITI",
                    connection_id=ConnectionID(session_alias="fix-fh-314-luna"))).MDRefID,
            'Instrument': {
                'Symbol': 'EUR/USD',
                'SecurityType': 'FXSPOT'
            },
            "NoMDEntries": [
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.15079,
                    "MDEntrySize": 3000000,
                    "MDEntryPositionNo": 1,
                    "MDQuoteType": 1,
                    'SettlDate': tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.15140,
                    "MDEntrySize": 3000000,
                    "MDEntryPositionNo": 1,
                    "MDQuoteType": 1,
                    'SettlDate': tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
            ]
        }
        # simulator.updateStorage(mdu_params_spo3)
        act.sendMessage(
            bca.convert_to_request(
                'Send Market Data SPOT',
                'fix-fh-314-luna',
                case_id,
                bca.message_to_grpc('MarketDataSnapshotFullRefresh', mdu_params_spo3, 'fix-fh-314-luna')
            ))






    except Exception as e:
        logging.error('Error execution', exc_info=True)
    finally:
        # md.send_md_unsubscribe()
        pass
