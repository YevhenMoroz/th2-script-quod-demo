import logging
from datetime import datetime, timedelta
from custom import basic_custom_actions as bca, tenor_settlement_date as tsd
from pathlib import Path

from custom.tenor_settlement_date import spo
from test_cases.fx.fx_wrapper.CaseParamsBuy import CaseParamsBuy
from test_cases.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from test_cases.fx.fx_wrapper.FixClientBuy import FixClientBuy
from test_cases.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True
client = 'Palladium1'
settltype = '0'
symbol = 'USD/JPY'
currency1 = 'USD'
currency2 = 'JPY'
securitytype = 'FXSPOT'
securityidsource = '8'
orderqty = '3000000'
securityid = 'EUR/USD'
bands = [1000000, 2000000]
md = None
settldate = tsd.spo()
bid_px_ccy1='104.63'
offer_px_ccy1='104.635'
bid_px_ccy2='104.632'
offer_px_ccy2='104.633'
defaultmdsymbol_spo = 'USD/JPY:SPO:REG:CITI'
no_md_entries_usd_jpy_citi = [
    {
        "MDEntryType": "0",
        "MDEntryPx": 104.632,
        "MDEntrySize": 1000000,
        "MDEntryPositionNo": 1,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "1",
        "MDEntryPx": 104.633,
        "MDEntrySize": 1000000,
        "MDEntryPositionNo": 1,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "0",
        "MDEntryPx": 104.630,
        "MDEntrySize": 2000000,
        "MDEntryPositionNo": 2,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "1",
        "MDEntryPx": 104.635,
        "MDEntrySize": 2000000,
        "MDEntryPositionNo": 2,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },

]


def execute(report_id):
    try:
        case_name = Path(__file__).name[:-3]
        case_id = bca.create_event(case_name, report_id)
        try:
            # Preconditions
            FixClientBuy(CaseParamsBuy(case_id, defaultmdsymbol_spo, symbol, securitytype)). \
                send_market_data_spot('Custom Market Data from BUY SIDE USD/JPY')

            FixClientBuy(CaseParamsBuy(case_id, defaultmdsymbol_spo, symbol, securitytype).
                         prepare_custom_md_spot(no_md_entries_usd_jpy_citi)).send_market_data_spot()
        except Exception as e:
            logging.error('Error execution', exc_info=True)
            bca.create_event('Fail test event', status='FAILED', parent_id=case_id)

        #Step 1
        params_ccy1 = CaseParamsSellRfq(client, case_id, orderqty=orderqty, symbol=symbol,securitytype=securitytype,
                                   settldate=settldate, settltype=settltype, currency=currency1,ttl=5)

        rfq_1 = FixClientSellRfq(params_ccy1)
        rfq_1.send_request_for_quote()
        rfq_1.verify_quote_pending(offer_px=offer_px_ccy1, bid_px=bid_px_ccy1)

        #Step 2
        params_ccy2 = CaseParamsSellRfq(client, case_id, orderqty=orderqty, symbol=symbol,securitytype=securitytype,
                                   settldate=settldate, settltype=settltype, currency=currency2,ttl=5)

        rfq_2 = FixClientSellRfq(params_ccy2)
        rfq_2.send_request_for_quote()
        rfq_2.verify_quote_pending(offer_px=offer_px_ccy2, bid_px=bid_px_ccy2)






    except Exception as e:
        logging.error('Error execution', exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
    finally:
        pass
