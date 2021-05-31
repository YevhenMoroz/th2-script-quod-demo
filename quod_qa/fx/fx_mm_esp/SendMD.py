import logging
from datetime import datetime
from custom import basic_custom_actions as bca, tenor_settlement_date as tsd
from pathlib import Path
from stubs import Stubs
from th2_grpc_common.common_pb2 import ConnectionID
from th2_grpc_sim_quod.sim_pb2 import RequestMDRefID
from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd
from quod_qa.fx.fx_wrapper.CaseParamsSell import CaseParamsSell
from quod_qa.fx.fx_wrapper.MarketDataRequst import MarketDataRequst

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True
client = 'Palladium2'
connectivity = 'fix-ss-esp-314-luna-standard'
settltype = 'MO1'
symbol = 'EUR/USD'
securitytype = 'FXFWD'
securityidsource = '8'
securityid = 'EUR/USD'
bands = [1000000,5000000,10000000]
md = None
settldate = (tm(datetime.utcnow().isoformat()) + bd(n=23)).date().strftime('%Y%m%d %H:%M:%S')
fwd_pts_offer = '-0.099'
fwd_pts_bid = '0.101'
symbol_md1="EUR/CAD:SPO:REG:HSBC"
symbol_md2="USD/CAD:SPO:REG:HSBC"


def execute(report_id):
    try:
        case_name = Path(__file__).name[:-3]
        case_id = bca.create_event(case_name, report_id)
        simulator = Stubs.simulator
        act = Stubs.fix_act

        mdu_params_spo = {
            "MDReqID": simulator.getMDRefIDForConnection303(
                request=RequestMDRefID(
                    symbol="EUR/CAD:SPO:REG:HSBC",
                    connection_id=ConnectionID(session_alias="fix-fh-314-luna"))).MDRefID,
            'Instrument': {
                'Symbol': 'EUR/CAD',
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

        act.sendMessage(
            bca.convert_to_request(
                'Send Market Data SPOT',
                'fix-fh-314-luna',
                case_id,
                bca.message_to_grpc('MarketDataSnapshotFullRefresh', mdu_params_spo, 'fix-fh-314-luna')
            ))

        mdu_params_fwd = {
            "MDReqID": simulator.getMDRefIDForConnection303(
                request=RequestMDRefID(
                    symbol="EUR/CAD:FXF:WK1:HSBC",
                    connection_id=ConnectionID(session_alias="fix-fh-314-luna"))).MDRefID,
            'Instrument': {
                'Symbol': 'EUR/CAD',
                'SecurityType': 'FXFWD'
            },
            "NoMDEntries": [
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.19585,
                    "MDEntrySize": 10000000,
                    "MDEntryPositionNo": 1,
                    "MDEntryForwardPoints": '0.0000001',
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.19615,
                    "MDEntrySize": 10000000,
                    "MDEntryPositionNo": 1,
                    "MDEntryForwardPoints": '0.0000001',
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
