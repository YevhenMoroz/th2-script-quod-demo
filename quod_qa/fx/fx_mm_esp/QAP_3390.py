import logging
from datetime import datetime
from custom import basic_custom_actions as bca, tenor_settlement_date as tsd
from pathlib import Path
from custom.tenor_settlement_date import spo, wk1
from quod_qa.fx.fx_wrapper.CaseParamsBuy import CaseParamsBuy
from quod_qa.fx.fx_wrapper.FixClientBuy import FixClientBuy
from quod_qa.fx.fx_wrapper.FixClientSellEsp import FixClientSellEsp
from quod_qa.fx.fx_wrapper.CaseParamsSellEsp import CaseParamsSellEsp

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True
client = 'Palladium2'
settltype_spo = '0'
settltype_fwd = 'W1'
symbol = 'GBP/USD'
securitytype_spo = 'FXSPOT'
securitytype_fwd = 'FXFWD'

securityidsource = '8'
securityid = 'GBP/USD'
qty = 1000000
md = None
settdate_spo = spo()
settldate_fwd = wk1()
fwd_pts_offer = 0.00021
fwd_pts_bid = 0.00019

symbol_gbp_usd = 'GBP/USD'
defmdsymb_gbp_usd_spo = "GBP/USD:SPO:REG:HSBC"
no_md_entries_spo = [
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
defmdsymb_gbp_usd_fwd = "GBP/USD:FXF:WK1:HSBC"
no_md_entries_fwd = [
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

no_md_entries = [
    {
        'SettlType': settltype_fwd,
        'MDEntryPx': '*',
        'MDEntryTime': '*',
        'MDEntryID': '*',
        'MDEntrySize': qty,
        'QuoteEntryID': '*',
        'MDOriginType': 1,
        'SettlDate': settldate_fwd,
        'MDQuoteType': 1,
        'MDEntryPositionNo': 1,
        'MDEntryDate': '*',
        'MDEntryType': 0,
        'MDEntryForwardPoints': fwd_pts_bid,
        'MDEntrySpotRate': '1.35785',
    },
    {
        'SettlType': settltype_fwd,
        'MDEntryPx': '*',
        'MDEntryTime': '*',
        'MDEntryID': '*',
        'MDEntrySize': qty,
        'QuoteEntryID': '*',
        'MDOriginType': 1,
        'SettlDate': settldate_fwd,
        'MDQuoteType': 1,
        'MDEntryPositionNo': 1,
        'MDEntryDate': '*',
        'MDEntryType': 1,
        'MDEntryForwardPoints': fwd_pts_offer,
        'MDEntrySpotRate': '1.35791',
    },
]


def execute(report_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    try:

        # Step 3
        # Send MD for Spot HSBC
        FixClientSellEsp(CaseParamsSellEsp(client, case_id, symbol=symbol_gbp_usd, securitytype=securitytype_spo,
                                           settltype=settltype_spo)).send_md_request().send_md_unsubscribe()
        FixClientBuy(CaseParamsBuy(case_id, defmdsymb_gbp_usd_spo, symbol_gbp_usd, securitytype_spo).
                     prepare_custom_md_spot(no_md_entries_spo)).send_market_data_spot()

        # Send MD for WK1 HSBC
        FixClientSellEsp(CaseParamsSellEsp(client, case_id, symbol=symbol_gbp_usd, securitytype=securitytype_fwd,
                                           settldate=settldate_fwd,
                                           settltype=settltype_fwd)).send_md_request().send_md_unsubscribe()
        FixClientBuy(CaseParamsBuy(case_id, defmdsymb_gbp_usd_fwd, symbol_gbp_usd, securitytype_fwd).
                     prepare_custom_md_fwd(no_md_entries_fwd)).send_market_data_fwd()

        # Step4
        params = CaseParamsSellEsp(client, case_id, settltype=settltype_fwd, settldate=settldate_fwd, symbol=symbol,
                                   securitytype=securitytype_fwd, securityid=securityid)
        params.prepare_md_for_verification_custom(no_md_entries)
        md = FixClientSellEsp(params).send_md_request().verify_md_pending()
    except Exception as e:
        logging.error('Error execution', exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
    finally:
        try:
            md.send_md_unsubscribe()
        except:
            bca.create_event('Unsubscribe failed', status='FAILED', parent_id=case_id)
