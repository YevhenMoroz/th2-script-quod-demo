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
settltype='W1'
symbol='GBP/USD'
securitytype='FXFWD'
securityidsource='8'
securityid='GBP/USD'
bands=[1000000]
md=None
settldate = (tm(datetime.utcnow().isoformat()) + bd(n=7)).date().strftime('%Y%m%d %H:%M:%S')
fwd_pts_offer=0.00021
fwd_pts_bid=0.00019


def execute(report_id):
    try:
        case_name = Path(__file__).name[:-3]
        case_id = bca.create_event(case_name, report_id)
        simulator = Stubs.simulator
        act = Stubs.fix_act

        #Step 3
        #Send MD for Spot HSBC
        mdu_params_spo_hsbc = {
            "MDReqID": simulator.getMDRefIDForConnection303(request=RequestMDRefID(symbol="GBP/USD:SPO:REG:HSBC",
                                                                                   connection_id=ConnectionID(
                                                                                       session_alias="fix-fh-314-luna"))).MDRefID,
            'Instrument': {
                'Symbol': 'GBP/USD',
                'SecurityType': 'FXSPOT'
            },
            "NoMDEntries": [
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.35785,
                    "MDEntrySize": 1000000,
                    "MDEntryPositionNo": 1,
                    'SettlDate': tsd.spo(),
                    "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.35791,
                    "MDEntrySize": 1000000,
                    "MDEntryPositionNo": 1,
                    'SettlDate': tsd.spo(),
                    "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                },
            ]
        }

        act.sendMessage(
            bca.convert_to_request(
                'Send Market Data Spot',
                'fix-fh-314-luna',
                case_id,
                bca.message_to_grpc('MarketDataSnapshotFullRefresh', mdu_params_spo_hsbc, 'fix-fh-314-luna')
            ))

        #Send MD for WK1 HSBC

        mdu_params_fwd = {
            "MDReqID": simulator.getMDRefIDForConnection303(
                request=RequestMDRefID(
                    symbol="GBP/USD:FXF:WK1:HSBC",
                    connection_id=ConnectionID(session_alias="fix-fh-314-luna"))).MDRefID,
            'Instrument': {
                'Symbol': 'GBP/USD',
                'SecurityType': 'FXFWD'
            },
            "NoMDEntries": [
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 2.18192,
                    "MDEntrySize": 1000000,
                    "MDEntryPositionNo": 1,
                    "MDEntrySpotRate": 1.1819,
                    "MDEntryForwardPoints": 0.0002,
                    "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 2.18220,
                    "MDEntrySize": 1000000,
                    "MDEntryPositionNo": 1,
                    "MDEntrySpotRate": 1.1820,
                    "MDEntryForwardPoints": 0.0002,
                    "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
                },
            ]
        }

        act.sendMessage(
            bca.convert_to_request(
                'Send Market Data WK1',
                'fix-fh-314-luna',
                case_id,
                bca.message_to_grpc('MarketDataSnapshotFullRefresh', mdu_params_fwd, 'fix-fh-314-luna')
            ))

        #Step4
        params = CaseParamsSell(connectivity, client, case_id, settltype=settltype, settldate= settldate, symbol=symbol,
                                securitytype=securitytype, securityid=securityid)
        md = MarketDataRequst(params)
        md.set_md_params().send_md_request().prepare_md_response(bands)
        md.md_subscribe_response['NoMDEntries'][0]['MDEntryForwardPoints']=fwd_pts_bid
        md.md_subscribe_response['NoMDEntries'][1]['MDEntryForwardPoints']=fwd_pts_offer
        md.verify_md_pending()

    except Exception as e:
        logging.error('Error execution', exc_info=True)
    finally:
        md.send_md_unsubscribe()

