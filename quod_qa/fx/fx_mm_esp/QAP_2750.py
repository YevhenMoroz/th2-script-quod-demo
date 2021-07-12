import logging
from datetime import datetime
from custom import basic_custom_actions as bca, tenor_settlement_date as tsd
from pathlib import Path

from quod_qa.fx.fx_wrapper.CaseParamsBuy import CaseParamsBuy
from quod_qa.fx.fx_wrapper.FixClientBuy import FixClientBuy
from quod_qa.fx.fx_wrapper.FixClientSellEsp import FixClientSellEsp
from stubs import Stubs
from th2_grpc_common.common_pb2 import ConnectionID
from th2_grpc_sim_quod.sim_pb2 import RequestMDRefID
from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd
from quod_qa.fx.fx_wrapper.CaseParamsSellEsp import CaseParamsSellEsp

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True
client = 'Palladium2'
settltype_spo = '0'
settltype_mo1 = 'MO1'
symbol = 'EUR/USD'
securitytype_spo = 'FXSPOT'
securitytype_fwd = 'FXFWD'
securityidsource = '8'
securityid = 'EUR/USD'
bands = [1000000,5000000,10000000]
md = None
settldate_spo= tsd.spo()
# settldate_mo1 = (tm(datetime.utcnow().isoformat()) + bd(n=24)).date().strftime('%Y%m%d %H:%M:%S')
settldate_mo1 = tsd.m1()
spo = tsd.spo()
# mo1 = (tm(datetime.utcnow().isoformat()) + bd(n=24)).date().strftime('%Y%m%d %H:%M:%S').split(' ')[0]
mo1 = tsd.m1()
fwd_pts_offer = '0.0000101'
fwd_pts_bid = '-0.0000099'

defmdsymb_eur_usd_spo="EUR/USD:SPO:REG:HSBC"
no_md_entries_spo=[
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
defmdsymb_eur_usd_mo1="EUR/USD:FXF:MO1:HSBC"
no_md_entries_mo1=[
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

no_md_entries = [
    {
        'SettlType': 'M1',
        'MDEntryPx': '*',
        'MDEntryTime': '*',
        'MDEntryID': '*',
        'MDEntrySize': '1000000',
        'QuoteEntryID': '*',
        'MDOriginType': 1,
        'SettlDate': mo1,
        'MDQuoteType': 1,
        'MDEntryPositionNo': 1,
        'MDEntryDate': '*',
        'MDEntryType': 0,
        'MDEntryForwardPoints': fwd_pts_bid,
        'MDEntrySpotRate': '1.19596',
    },
    {
        'SettlType': 'M1',
        'MDEntryPx': '*',
        'MDEntryTime': '*',
        'MDEntryID': '*',
        'MDEntrySize': '1000000',
        'QuoteEntryID': '*',
        'MDOriginType': 1,
        'SettlDate': mo1,
        'MDQuoteType': 1,
        'MDEntryPositionNo': 1,
        'MDEntryDate': '*',
        'MDEntryType': 1,
        'MDEntryForwardPoints': fwd_pts_offer,
        'MDEntrySpotRate': '1.1961',
    },
    {
        'SettlType': 'M1',
        'MDEntryPx': '*',
        'MDEntryTime': '*',
        'MDEntryID': '*',
        'MDEntrySize': '5000000',
        'QuoteEntryID': '*',
        'MDOriginType': 1,
        'SettlDate': mo1,
        'MDQuoteType': 1,
        'MDEntryPositionNo': 2,
        'MDEntryDate': '*',
        'MDEntryType': 0,
        'MDEntryForwardPoints': fwd_pts_bid,
        'MDEntrySpotRate': '1.19592',
    },
    {
        'SettlType': 'M1',
        'MDEntryPx': '*',
        'MDEntryTime': '*',
        'MDEntryID': '*',
        'MDEntrySize': '5000000',
        'QuoteEntryID': '*',
        'MDOriginType': 1,
        'SettlDate': mo1,
        'MDQuoteType': 1,
        'MDEntryPositionNo': 2,
        'MDEntryDate': '*',
        'MDEntryType': 1,
        'MDEntryForwardPoints': fwd_pts_offer,
        'MDEntrySpotRate': '1.19614',
    },
    {
        'SettlType': 'M1',
        'MDEntryPx': '*',
        'MDEntryTime': '*',
        'MDEntryID': '*',
        'MDEntrySize': '10000000',
        'QuoteEntryID': '*',
        'MDOriginType': 1,
        'SettlDate': mo1,
        'MDQuoteType': 1,
        'MDEntryPositionNo': 3,
        'MDEntryDate': '*',
        'MDEntryType': 0,
        'MDEntryForwardPoints': fwd_pts_bid,
        'MDEntrySpotRate': '1.19588',
    },
    {
        'SettlType': 'M1',
        'MDEntryPx': '*',
        'MDEntryTime': '*',
        'MDEntryID': '*',
        'MDEntrySize': '10000000',
        'QuoteEntryID': '*',
        'MDOriginType': 1,
        'SettlDate': mo1,
        'MDQuoteType': 1,
        'MDEntryPositionNo': 3,
        'MDEntryDate': '*',
        'MDEntryType': 1,
        'MDEntryForwardPoints': fwd_pts_offer,
        'MDEntrySpotRate': '1.19618',
    },

]

def execute(report_id):
    try:
        case_name = Path(__file__).name[:-3]
        case_id = bca.create_event(case_name, report_id)

        #Send MD for Spot HSBC
        FixClientSellEsp(CaseParamsSellEsp(client, case_id, symbol=symbol, securitytype=securitytype_spo,
                                   settldate=settldate_spo, settltype=settltype_spo)).send_md_request().send_md_unsubscribe()
        FixClientBuy(CaseParamsBuy(case_id, defmdsymb_eur_usd_spo, symbol, securitytype_spo).
                     prepare_custom_md_spot(no_md_entries_spo)).send_market_data_spot()

        #Send MD for MO1 HSBC
        FixClientSellEsp(CaseParamsSellEsp(client, case_id, symbol=symbol, securitytype=securitytype_fwd,
                                   settldate=settldate_mo1, settltype=settltype_mo1)).send_md_request().send_md_unsubscribe()
        FixClientBuy(CaseParamsBuy(case_id, defmdsymb_eur_usd_mo1, symbol, securitytype_fwd).
                     prepare_custom_md_fwd(no_md_entries_mo1)).send_market_data_fwd()




        params = CaseParamsSellEsp(client, case_id, settltype=settltype_mo1, settldate= settldate_mo1, symbol=symbol,
                                   securitytype=securitytype_fwd,securityidsource=securityidsource, securityid=securityid)
        params.prepare_md_for_verification_custom(no_md_entries)
        md = FixClientSellEsp(params).send_md_request().verify_md_pending()



    except Exception as e:
        logging.error('Error execution', exc_info=True)
    finally:
        md.send_md_unsubscribe()
        pass
