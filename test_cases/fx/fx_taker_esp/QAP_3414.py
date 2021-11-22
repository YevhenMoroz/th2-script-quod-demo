import logging
import time
from datetime import datetime
from pathlib import Path
from th2_grpc_common.common_pb2 import ConnectionID
from th2_grpc_sim_fix_quod.sim_pb2 import RequestMDRefID
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import spo
from custom.verifier import Verifier
from test_cases.fx.fx_wrapper.common_tools import read_median_file
from stubs import Stubs


def verify_median(case_id, expected, actual):
    verifier = Verifier(case_id)
    verifier.set_event_name("Compare median")
    verifier.compare_values("Median", expected, actual)
    verifier.verify()


def execute(report_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    simulator = Stubs.simulator
    act = Stubs.fix_act
    connectivity = "fix-fh-q-314-luna"
    security_type = 'FXSPOT'
    symbol = 'EUR/USD'
    default_md_symbol_db = 'EUR/USD:SPO:REG:DB'
    default_md_symbol_ebs = 'EUR/USD:SPO:REG:EBS-CITI'
    expected_median = "EUR/USD;EXC;;1.18517;6000000;1.19632;12000000'"

    try:
        mdu_params_spo = {
            "MDReqID": simulator.getMDRefIDForConnection314(
                request=RequestMDRefID(
                    symbol=default_md_symbol_db,
                    connection_id=ConnectionID(session_alias=connectivity))).MDRefID,
            'Instrument': {
                'Symbol': symbol,
                'SecurityType': security_type
            },
            "NoMDEntries": [
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.19550,
                    "MDEntrySize": 1000000,
                    "MDEntryPositionNo": 1,
                    'SettlDate': spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.19674,
                    "MDEntrySize": 1000000,
                    "MDEntryPositionNo": 1,
                    'SettlDate': spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.18517,
                    "MDEntrySize": 6000000,
                    "MDEntryPositionNo": 2,
                    'SettlDate': spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.19625,
                    "MDEntrySize": 6000000,
                    "MDEntryPositionNo": 2,
                    'SettlDate': spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                }
            ]
        }
        act.sendMessage(
            bca.convert_to_request(
                'Send Market Data SPOT',
                connectivity,
                case_id,
                bca.message_to_grpc('MarketDataSnapshotFullRefresh', mdu_params_spo, connectivity)
            ))
        mdu_params_spo_ebs = {
            "MDReqID": simulator.getMDRefIDForConnection314(
                request=RequestMDRefID(
                    symbol=default_md_symbol_ebs,
                    connection_id=ConnectionID(session_alias=connectivity))).MDRefID,
            'Instrument': {
                'Symbol': symbol,
                'SecurityType': security_type
            },
            "NoMDEntries": [
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.19568,
                    "MDEntrySize": 1000000,
                    "MDEntryPositionNo": 1,
                    'SettlDate': spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.19679,
                    "MDEntrySize": 1000000,
                    "MDEntryPositionNo": 1,
                    'SettlDate': spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.18507,
                    "MDEntrySize": 6000000,
                    "MDEntryPositionNo": 2,
                    'SettlDate': spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.19628,
                    "MDEntrySize": 6000000,
                    "MDEntryPositionNo": 2,
                    'SettlDate': spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.18400,
                    "MDEntrySize": 12000000,
                    "MDEntryPositionNo": 3,
                    'SettlDate': spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.19632,
                    "MDEntrySize": 12000000,
                    "MDEntryPositionNo": 3,
                    'SettlDate': spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
            ]
        }
        act.sendMessage(
            bca.convert_to_request(
                'Send Market Data SPOT',
                connectivity,
                case_id,
                bca.message_to_grpc('MarketDataSnapshotFullRefresh', mdu_params_spo_ebs, connectivity)
            ))
        time.sleep(10)
        actual_median = read_median_file()[45:]
        verify_median(case_id, expected_median, actual_median)

    except Exception:
        logging.error('Error execution', exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
