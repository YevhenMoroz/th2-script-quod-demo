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
settltype = 'MO1'
symbol = 'EUR/USD'
securitytype = 'FXFWD'
securityidsource = '8'
securityid = 'EUR/USD'
bands = [1000000,5000000,10000000]
md = None
settldate = (tm(datetime.utcnow().isoformat()) + bd(n=24)).date().strftime('%Y%m%d %H:%M:%S')
spo = tsd.spo()
mo1 = tsd.m1()
fwd_pts_offer = '0.0000101'
fwd_pts_bid = '-0.0000099'


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
                    "MDEntryForwardPoints": '0.0000001',
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.19615,
                    "MDEntrySize": 1000000,
                    "MDEntryPositionNo": 1,
                    "MDEntryForwardPoints": '0.0000001',
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

        act.sendMessage(
            bca.convert_to_request(
                'Send Market Data MO1',
                'fix-fh-314-luna',
                case_id,
                bca.message_to_grpc('MarketDataSnapshotFullRefresh', mdu_params_fwd, 'fix-fh-314-luna')
            ))

        params = CaseParams(connectivity, client, case_id,  settltype=settltype, settldate= settldate, symbol=symbol, securitytype=securitytype,
                            securityidsource=securityidsource, securityid=securityid)
        md = MarketDataRequst(params)
        md.set_md_params()
        md.send_md_request()
        md.prepare_md_response(bands)

        #set forward points
        md.md_subscribe_response['NoMDEntries'][0]['MDEntryForwardPoints']=fwd_pts_bid
        md.md_subscribe_response['NoMDEntries'][1]['MDEntryForwardPoints']=fwd_pts_offer
        md.md_subscribe_response['NoMDEntries'][2]['MDEntryForwardPoints']=fwd_pts_bid
        md.md_subscribe_response['NoMDEntries'][3]['MDEntryForwardPoints']=fwd_pts_offer
        md.md_subscribe_response['NoMDEntries'][4]['MDEntryForwardPoints']=fwd_pts_bid
        md.md_subscribe_response['NoMDEntries'][5]['MDEntryForwardPoints']=fwd_pts_offer

        #set_price m1 (todo rewrite with caculation : spotrate+margins+fwdpoints)
        md.md_subscribe_response['NoMDEntries'][0]['MDEntryPx']='1.1959501'
        md.md_subscribe_response['NoMDEntries'][1]['MDEntryPx']='1.1961101'
        md.md_subscribe_response['NoMDEntries'][2]['MDEntryPx']='1.1959101'
        md.md_subscribe_response['NoMDEntries'][3]['MDEntryPx']='1.1961501'
        md.md_subscribe_response['NoMDEntries'][4]['MDEntryPx']='1.1958701'
        md.md_subscribe_response['NoMDEntries'][5]['MDEntryPx']='1.1961901'
        md.verify_md_pending()



    except Exception as e:
        logging.error('Error execution', exc_info=True)
    finally:
        md.send_md_unsubscribe()
        pass
