import time
from datetime import datetime

from custom.tenor_settlement_date import spo
from quod_qa.fx.fx_wrapper.CaseParamsBuy import CaseParamsBuy
from quod_qa.fx.fx_wrapper.CaseParamsSellEsp import CaseParamsSellEsp
from quod_qa.fx.fx_wrapper.FixClientBuy import FixClientBuy
from quod_qa.fx.fx_wrapper.FixClientSellEsp import FixClientSellEsp
import logging
from pathlib import Path
from custom import basic_custom_actions as bca, tenor_settlement_date as tsd

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True
client = 'Palladium1'
account = 'Palladium1_1'
side = '1'
orderqty = '1000000'
ordtype = '2'
timeinforce = '4'
currency = 'EUR'
settlcurrency = 'USD'
settltype = 0
symbol = 'EUR/USD'
securitytype = 'FXSPOT'
securityid = 'EUR/USD'
bands = [2000000, 6000000, 12000000]
md = None
settldate = tsd.spo()
defaultmdsymbol_spo = 'EUR/USD:SPO:REG:HSBC'
no_md_entries_spo = [
    {
        "MDEntryType": "0",
        "MDEntryPx": 1.19581,
        "MDEntrySize": 1000000,
        "MDEntryPositionNo": 1,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "1",
        "MDEntryPx": 1.19611,
        "MDEntrySize": 1000000,
        "MDEntryPositionNo": 1,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "0",
        "MDEntryPx": 1.19575,
        "MDEntrySize": 5000000,
        "MDEntryPositionNo": 1,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "1",
        "MDEntryPx": 1.19625,
        "MDEntrySize": 5000000,
        "MDEntryPositionNo": 1,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "0",
        "MDEntryPx": 1.19570,
        "MDEntrySize": 15000000,
        "MDEntryPositionNo": 1,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "1",
        "MDEntryPx": 1.19630,
        "MDEntrySize": 15000000,
        "MDEntryPositionNo": 1,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    }
]


def execute(report_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    try:
        try:
            # Preconditions
            params_0 = CaseParamsSellEsp(client, case_id, side=side, orderqty=orderqty, ordtype=ordtype,
                                         timeinforce=timeinforce, currency=currency,
                                         settlcurrency=settlcurrency, settltype=settltype, settldate=settldate,
                                         symbol=symbol, securitytype=securitytype,
                                         securityid=securityid, account=account)
            md_0 = FixClientSellEsp(params_0).send_md_request().send_md_unsubscribe()
            # Send market data to the HSBC venue EUR/USD spot
            FixClientBuy(CaseParamsBuy(case_id, defaultmdsymbol_spo, symbol, securitytype).prepare_custom_md_spot(
                no_md_entries_spo)). \
                send_market_data_spot()
            time.sleep(5)

            # Step 1
            params_1 = CaseParamsSellEsp(client, case_id, side=side, orderqty=orderqty, ordtype=ordtype,
                                         timeinforce=timeinforce, currency=currency,
                                         settlcurrency=settlcurrency, settltype=settltype, settldate=settldate,
                                         symbol=symbol, securitytype=securitytype,
                                         securityid=securityid, account=account)
            md_1 = FixClientSellEsp(params_1)
            params_1.prepare_md_for_verification(bands)
            md_1.send_md_request(). \
                verify_md_pending()
            price = md_1.extract_filed('Price')
            # Step 2-5
            md_1.send_new_order_single(price)
            md_1.verify_order_pending()
            md_1.verify_order_new()
            md_1.verify_order_filled(spot_s_d=settldate)
        except Exception as e:
            logging.error('Error execution', exc_info=True)
            bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
        finally:
            try:
                md_1.send_md_unsubscribe()
            except:
                bca.create_event('Unsubscribe failed', status='FAILED', parent_id=case_id)
    except Exception:
        logging.error('Error execution', exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
