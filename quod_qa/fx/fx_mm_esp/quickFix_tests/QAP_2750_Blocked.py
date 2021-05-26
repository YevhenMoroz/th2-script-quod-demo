import logging
from datetime import datetime
from custom import basic_custom_actions as bca, tenor_settlement_date as tsd
from pathlib import Path
from stubs import Stubs
from th2_grpc_common.common_pb2 import ConnectionID
from th2_grpc_sim_quod.sim_pb2 import RequestMDRefID
from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd
from quod_qa.fx.fx_wrapper.CaseParams import CaseParams
from quod_qa.fx.fx_wrapper.MarketDataRequst import MarketDataRequst

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True
client = 'Palladium2'
connectivity = 'fix-ss-esp-314-luna-standard'
settltype = 'W1'
symbol = 'GBP/USD'
securitytype = 'FXFWD'
securityidsource = '8'
securityid = 'GBP/USD'
bands = [1000000]
md = None
settldate = (tm(datetime.utcnow().isoformat()) + bd(n=7)).date().strftime('%Y%m%d %H:%M:%S')
fwd_pts_offer = 0.00021
fwd_pts_bid = 0.00019


def execute(report_id):
    try:
        case_name = Path(__file__).name[:-3]
        case_id = bca.create_event(case_name, report_id)
        simulator = Stubs.simulator
        act = Stubs.fix_act

        mdu_params_spo = {
            "MDReqID": simulator.getMDRefIDForConnection303(
                request=RequestMDRefID(
                    symbol="EUR/USD:SPO:REG:HSBC",
                    connection_id=ConnectionID(session_alias="fix-fh-314-luna"))).MDRefID,
            'Instrument': {
                'Symbol': 'EUR/USD',
                'SecurityType': 'FXSPOT'
            },
            "NoMDEntries": [
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.19597,
                    "MDEntrySize": 2000000,
                    "MDEntryPositionNo": 1,
                    'SettlDate': tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.19609,
                    "MDEntrySize": 2000000,
                    "MDEntryPositionNo": 1,
                    'SettlDate': tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.19594,
                    "MDEntrySize": 6000000,
                    "MDEntryPositionNo": 2,
                    'SettlDate': tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.19612,
                    "MDEntrySize": 6000000,
                    "MDEntryPositionNo": 2,
                    'SettlDate': tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.19591,
                    "MDEntrySize": 12000000,
                    "MDEntryPositionNo": 3,
                    'SettlDate': tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.19615,
                    "MDEntrySize": 12000000,
                    "MDEntryPositionNo": 3,
                    'SettlDate': tsd.spo(),
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
            ]
        }

        # act.sendMessage(
        #     bca.convert_to_request(
        #         'Send Market Data SPOT',
        #         'fix-fh-314-luna',
        #         case_id,
        #         bca.message_to_grpc('MarketDataSnapshotFullRefresh', mdu_params_spo, 'fix-fh-314-luna')
        #     ))

        mdu_params_fwd = {
            "MDReqID": simulator.getMDRefIDForConnection303(
                request=RequestMDRefID(
                    symbol="EUR/USD:FXF:MO1:HSBC",
                    connection_id=ConnectionID(session_alias="fix-fh-314-luna"))).MDRefID,
            'Instrument': {
                'Symbol': 'EUR/USD',
                'SecurityType': 'FXFWD'
            },
            "NoMDEntries": [
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.19585,
                    "MDEntrySize": 1000000,
                    "MDEntryPositionNo": 1,
                    "MDEntryForwardPoints": '0.00005',
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.19615,
                    "MDEntrySize": 1000000,
                    "MDEntryPositionNo": 1,
                    "MDEntryForwardPoints": '0.00005',
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
            ]
        }

        act.sendMessage(
            bca.convert_to_request(
                'Send Market Data MO1',
                'fix-fh-314-luna',
                case_id,
                bca.message_to_grpc('MarketDataSnapshotFullRefresh', mdu_params_fwd, 'fix-fh-314-luna')
            ))



    except Exception as e:
        logging.error('Error execution', exc_info=True)
    finally:
        # md.send_md_unsubscribe()
        pass
