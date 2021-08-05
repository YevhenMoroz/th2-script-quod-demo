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
settltype = '0'
securitytype = 'FXSPOT'
symbol_nok_sek = 'USD/CHF'
md = None
settldate = tsd.spo()
symbol_usd_chf = 'USD/CHF'

defmdsymb_usd_chf_gs = 'USD/CHF:SPO:REG:GS'
no_md_entries_usd_chf_gs = [
    {
        "MDEntryType": "0",
        "MDEntryPx": 1.005,
        "MDEntrySize": 1000000,
        "MDEntryPositionNo": 1,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "1",
        "MDEntryPx": 1.016,
        "MDEntrySize": 1000000,
        "MDEntryPositionNo": 1,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "0",
        "MDEntryPx": 1.004,
        "MDEntrySize": 2000000,
        "MDEntryPositionNo": 2,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "1",
        "MDEntryPx": 1.017,
        "MDEntrySize": 2000000,
        "MDEntryPositionNo": 2,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "0",
        "MDEntryPx": 1.003,
        "MDEntrySize": 20000000,
        "MDEntryPositionNo": 3,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "1",
        "MDEntryPx": 1.018,
        "MDEntrySize": 20000000,
        "MDEntryPositionNo": 3,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
]

defmdsymb_usd_chf_citi = 'USD/CHF:SPO:REG:CITI'
no_md_entries_usd_chf_citi = [
    {
        "MDEntryType": "0",
        "MDEntryPx": 1.008,
        "MDEntrySize": 1000000,
        "MDEntryPositionNo": 1,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "1",
        "MDEntryPx": 1.019,
        "MDEntrySize": 1000000,
        "MDEntryPositionNo": 1,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "0",
        "MDEntryPx": 1.007,
        "MDEntrySize": 5000000,
        "MDEntryPositionNo": 2,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "1",
        "MDEntryPx": 1.020,
        "MDEntrySize": 5000000,
        "MDEntryPositionNo": 2,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "0",
        "MDEntryPx": 1.006,
        "MDEntrySize": 10000000,
        "MDEntryPositionNo": 3,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "1",
        "MDEntryPx": 1.021,
        "MDEntrySize": 10000000,
        "MDEntryPositionNo": 3,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    }
]

defmdsymb_usd_chf_ms = 'USD/CHF:SPO:REG:MS'
no_md_entries_usd_chf_ms = [
    {
        "MDEntryType": "0",
        "MDEntryPx": 1.011,
        "MDEntrySize": 1000000,
        "MDEntryPositionNo": 1,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "1",
        "MDEntryPx": 1.022,
        "MDEntrySize": 1000000,
        "MDEntryPositionNo": 1,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "0",
        "MDEntryPx": 1.010,
        "MDEntrySize": 5000000,
        "MDEntryPositionNo": 2,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "1",
        "MDEntryPx": 1.023,
        "MDEntrySize": 5000000,
        "MDEntryPositionNo": 2,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "0",
        "MDEntryPx": 1.009,
        "MDEntrySize": 10000000,
        "MDEntryPositionNo": 3,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "1",
        "MDEntryPx": 1.024,
        "MDEntrySize": 10000000,
        "MDEntryPositionNo": 3,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
]

no_md_entries = [
    {
        'SettlType': 0,
        'MDEntryPx': '1.011',
        'MDEntryTime': '*',
        'MDEntryID': '*',
        'MDEntrySize': '1000000',
        'QuoteEntryID': '*',
        'MDOriginType': 1,
        'SettlDate': tsd.spo(),
        'MDQuoteType': 1,
        'MDEntryPositionNo': 1,
        'MDEntryDate': '*',
        'MDEntryType': 0
    },
    {
        'SettlType': 0,
        'MDEntryPx': '1.016',
        'MDEntryTime': '*',
        'MDEntryID': '*',
        'MDEntrySize': '1000000',
        'QuoteEntryID': '*',
        'MDOriginType': 1,
        'SettlDate': tsd.spo(),
        'MDQuoteType': 1,
        'MDEntryPositionNo': 1,
        'MDEntryDate': '*',
        'MDEntryType': 1
    }, {
        'SettlType': 0,
        'MDEntryPx': '1.01',
        'MDEntryTime': '*',
        'MDEntryID': '*',
        'MDEntrySize': '5000000',
        'QuoteEntryID': '*',
        'MDOriginType': 1,
        'SettlDate': tsd.spo(),
        'MDQuoteType': 1,
        'MDEntryPositionNo': 2,
        'MDEntryDate': '*',
        'MDEntryType': 0
    },
    {
        'SettlType': 0,
        'MDEntryPx': '1.0176',
        'MDEntryTime': '*',
        'MDEntryID': '*',
        'MDEntrySize': '5000000',
        'QuoteEntryID': '*',
        'MDOriginType': 1,
        'SettlDate': tsd.spo(),
        'MDQuoteType': 1,
        'MDEntryPositionNo': 2,
        'MDEntryDate': '*',
        'MDEntryType': 1
    }, {
        'SettlType': 0,
        'MDEntryPx': '1.009',
        'MDEntryTime': '*',
        'MDEntryID': '*',
        'MDEntrySize': '10000000',
        'QuoteEntryID': '*',
        'MDOriginType': 1,
        'SettlDate': tsd.spo(),
        'MDQuoteType': 1,
        'MDEntryPositionNo': 3,
        'MDEntryDate': '*',
        'MDEntryType': 0
    },
    {
        'SettlType': 0,
        'MDEntryPx': '1.018',
        'MDEntryTime': '*',
        'MDEntryID': '*',
        'MDEntrySize': '10000000',
        'QuoteEntryID': '*',
        'MDOriginType': 1,
        'SettlDate': tsd.spo(),
        'MDQuoteType': 1,
        'MDEntryPositionNo': 3,
        'MDEntryDate': '*',
        'MDEntryType': 1
    }

]


def execute(report_id):
    try:
        case_name = Path(__file__).name[:-3]
        case_id = bca.create_event(case_name, report_id)
        # Step 1 SEND MARKET DATA
        FixClientSellEsp(CaseParamsSellEsp(client, case_id, symbol=symbol_usd_chf, securitytype=securitytype,
                                   settldate=settldate, settltype=settltype)).\
            send_md_request(). \
            send_md_unsubscribe()
        # SEND MD USD/CHF spot GS
        FixClientBuy(CaseParamsBuy(case_id, defmdsymb_usd_chf_gs, symbol_usd_chf, securitytype).
                     prepare_custom_md_spot(no_md_entries_usd_chf_gs)).send_market_data_spot()

        # SEND MD USD/CHF spot CITI
        FixClientBuy(CaseParamsBuy(case_id, defmdsymb_usd_chf_citi, symbol_usd_chf, securitytype).
                     prepare_custom_md_spot(no_md_entries_usd_chf_citi)).send_market_data_spot()

        # SEND MD USD/CHF spot MS
        FixClientBuy(CaseParamsBuy(case_id, defmdsymb_usd_chf_ms, symbol_usd_chf, securitytype).
                     prepare_custom_md_spot(no_md_entries_usd_chf_ms)).send_market_data_spot()

        # Step 2
        params = CaseParamsSellEsp(client, case_id, symbol=symbol_usd_chf, securitytype=securitytype,
                                   settldate=settldate, settltype=settltype)
        md = FixClientSellEsp(params). \
            send_md_request()
        params.prepare_md_for_verification_custom(no_md_entries)
        md.verify_md_pending()



    except Exception as e:
        logging.error('Error execution', exc_info=True)
    finally:
        md.send_md_unsubscribe()
        pass
