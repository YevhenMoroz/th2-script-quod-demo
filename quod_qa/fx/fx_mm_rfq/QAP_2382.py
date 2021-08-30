import logging
from datetime import datetime, timedelta
from custom import basic_custom_actions as bca, tenor_settlement_date as tsd
from pathlib import Path

from custom.tenor_settlement_date import spo
from quod_qa.fx.fx_wrapper.CaseParamsBuy import CaseParamsBuy
from quod_qa.fx.fx_wrapper.CaseParamsSellEsp import CaseParamsSellEsp
from quod_qa.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from quod_qa.fx.fx_wrapper.FixClientBuy import FixClientBuy
from quod_qa.fx.fx_wrapper.FixClientSellEsp import FixClientSellEsp
from quod_qa.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True
client = 'Argentina1'
account = 'Argentina1_1'
side = '2'
leg1_side = '1'
leg2_side = '2'
orderqty = '3000000'
leg1_ordqty = '1000000'
leg2_ordqty = '3000000'
leg1_settltype = 'W1'
leg2_settltype = 'W2'

# da = float(leg2_ordqty)
# dr = float(leg1_ordqty)
# ds =str(da - dr)
# size = ds.split('.')
# drer = size[0]
# edr = size[1]

symbol = 'EUR/USD'
leg1_symbol = 'EUR/USD'
leg2_symbol = 'EUR/USD'
currency = 'EUR'
settlcurrency = 'USD'
securitytype_swap = 'FXSWAP'
leg1_securitytype = 'FXSPOT'
leg2_securitytype = 'FXFWD'
settldate = tsd.spo()
leg1_settldate = tsd.wk1()
leg2_settldate = tsd.wk2()
ttl = 15
expire_time = (datetime.now() + timedelta(seconds=ttl) - timedelta(hours=3)).strftime("%Y%m%d-%H:%M:%S.000")

defaultmdsymbol_spo = 'EUR/USD:SPO:REG:MS'
defaultmdsymbol_wk1 = 'EUR/USD:FXF:WK1:MS'
defaultmdsymbol_wk2 = 'EUR/USD:FXF:WK2:MS'
no_md_entries_spo = [
    {
        "MDEntryType": "0",
        "MDEntryPx": 1.19599,
        "MDEntrySize": 1000000,
        "MDEntryPositionNo": 1,
        'SettlDate': tsd.spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "1",
        "MDEntryPx": 1.19810,
        "MDEntrySize": 1000000,
        "MDEntryPositionNo": 1,
        'SettlDate': tsd.spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "0",
        "MDEntryPx": 1.19397,
        "MDEntrySize": 2000000,
        "MDEntryPositionNo": 1,
        'SettlDate': tsd.spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "1",
        "MDEntryPx": 1.19909,
        "MDEntrySize": 2000000,
        "MDEntryPositionNo": 1,
        'SettlDate': tsd.spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "0",
        "MDEntryPx": 1.19301,
        "MDEntrySize": 3000000,
        "MDEntryPositionNo": 2,
        'SettlDate': tsd.spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "1",
        "MDEntryPx": 1.19999,
        "MDEntrySize": 3000000,
        "MDEntryPositionNo": 2,
        'SettlDate': tsd.spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },

]
no_md_entries_wk1 = [
    {
        "MDEntryType": "0",
        "MDEntryPx": 1.19585,
        "MDEntrySize": 1000000,
        "MDEntryPositionNo": 1,
        "MDEntryForwardPoints": '0.0002',
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "1",
        "MDEntryPx": 1.19615,
        "MDEntrySize": 1000000,
        "MDEntryPositionNo": 1,
        "MDEntryForwardPoints": '0.0002',
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
]
no_md_entries_wk2 = [
    {
        "MDEntryType": "0",
        "MDEntryPx": 1.19575,
        "MDEntrySize": 1000000,
        "MDEntryPositionNo": 1,
        "MDEntryForwardPoints": '0.0003',
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "1",
        "MDEntryPx": 1.19625,
        "MDEntrySize": 1000000,
        "MDEntryPositionNo": 1,
        "MDEntryForwardPoints": '0.0003',
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
]

offer_spot_rate = '1.1986'
bid_spot_rate = '1.19498'
bid_swap_points = '0.0003'
leg_off_fwd_p = '0.0003'
leg_bid_fwd_p = '0.0003'
bid_px = '0.0003'


def execute(report_id):
    try:
        case_name = Path(__file__).name[:-3]
        case_id = bca.create_event(case_name, report_id)
        try:
            # Precondition
            md1 = FixClientSellEsp(CaseParamsSellEsp(client, case_id, settldate=settldate, symbol=symbol))
            md1.send_md_request().send_md_unsubscribe()
            FixClientBuy(CaseParamsBuy(case_id, defaultmdsymbol_spo, symbol).prepare_custom_md_spot(
                no_md_entries_spo)).send_market_data_spot()
            FixClientBuy(CaseParamsBuy(case_id, defaultmdsymbol_wk1, symbol).prepare_custom_md_fwd(
                no_md_entries_wk1)).send_market_data_fwd()
            FixClientBuy(CaseParamsBuy(case_id, defaultmdsymbol_wk2, symbol).prepare_custom_md_fwd(
                no_md_entries_wk2)).send_market_data_fwd()

            # Step 1-2
            params = CaseParamsSellRfq(client, case_id, leg1_side=leg1_side, leg2_side=leg2_side, side=side,
                                       orderqty=orderqty, leg1_ordqty=leg1_ordqty, leg2_ordqty=leg2_ordqty,
                                       currency=currency, settlcurrency=settlcurrency,
                                       leg1_settltype=leg1_settltype, leg2_settltype=leg2_settltype,
                                       settldate=settldate, leg1_settldate=leg1_settldate,
                                       leg2_settldate=leg2_settldate,
                                       symbol=symbol, leg1_symbol=leg1_symbol, leg2_symbol=leg2_symbol,
                                       securitytype=securitytype_swap, leg1_securitytype=leg1_securitytype,
                                       leg2_securitytype=leg2_securitytype, account=account)

            rfq_swap = FixClientSellRfq(params)
            rfq_swap.send_request_for_quote_swap(expire_time)
            rfq_swap.verify_quote_pending_swap(offer_spot_rate=offer_spot_rate, bid_spot_rate=bid_spot_rate,
                                               bid_px=bid_px,
                                               bid_swap_points=bid_swap_points, leg_bid_fwd_p=leg_bid_fwd_p,
                                               leg_of_fwd_p=leg_off_fwd_p)
        except Exception as e:
            try:
                md1.send_md_unsubscribe()
            except:
                bca.create_event('Unsubscribe failed', status='FAILED', parent_id=case_id)
            logging.error('Error execution', exc_info=True)
            bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
    except Exception as e:
        logging.error('Error execution', exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
