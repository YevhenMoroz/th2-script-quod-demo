import time
from datetime import datetime

from custom.tenor_settlement_date import spo
from quod_qa.fx.fx_wrapper.CaseParamsBuy import CaseParamsBuy
from quod_qa.fx.fx_wrapper.CaseParamsSell import CaseParamsSell
from quod_qa.fx.fx_wrapper.FixClientBuy import FixClientBuy
from quod_qa.fx.fx_wrapper.FixClientSell import FixClientSell
import logging
from pathlib import Path
from custom import basic_custom_actions as bca, tenor_settlement_date as tsd

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True
client = 'Palladium1'
settltype = '0'
securitytype = 'FXSPOT'
symbol_nok_sek = 'NOK/SEK'
md = None
settldate = tsd.spo()

defmdsymb_spo_eur_usd = 'EUR/USD:SPO:REG:HSBC'
symbol_eur_usd = 'EUR/USD'
no_md_entries_eur_usd = [
    {
        "MDEntryType": "0",
        "MDEntryPx": 1.19597,
        "MDEntrySize": 2000000,
        "MDEntryPositionNo": 1,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "1",
        "MDEntryPx": 1.19609,
        "MDEntrySize": 2000000,
        "MDEntryPositionNo": 1,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "0",
        "MDEntryPx": 1.19594,
        "MDEntrySize": 6000000,
        "MDEntryPositionNo": 2,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "1",
        "MDEntryPx": 1.19612,
        "MDEntrySize": 6000000,
        "MDEntryPositionNo": 2,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "0",
        "MDEntryPx": 1.19591,
        "MDEntrySize": 12000000,
        "MDEntryPositionNo": 3,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "1",
        "MDEntryPx": 1.19615,
        "MDEntrySize": 12000000,
        "MDEntryPositionNo": 3,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
]

defmdsymb_spo_eur_nok = 'EUR/NOK:SPO:REG:HSBC'
symbol_eur_nok = 'EUR/NOK'
no_md_entries_eur_nok = [
    {
        "MDEntryType": "0",
        "MDEntryPx": 9.39868,
        "MDEntrySize": 3000000,
        "MDEntryPositionNo": 1,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "1",
        "MDEntryPx": 9.3988,
        "MDEntrySize": 3000000,
        "MDEntryPositionNo": 1,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "0",
        "MDEntryPx": 9.39865,
        "MDEntrySize": 8000000,
        "MDEntryPositionNo": 2,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "1",
        "MDEntryPx": 9.39883,
        "MDEntrySize": 8000000,
        "MDEntryPositionNo": 2,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "0",
        "MDEntryPx": 9.39862,
        "MDEntrySize": 12000000,
        "MDEntryPositionNo": 3,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "1",
        "MDEntryPx": 9.39886,
        "MDEntrySize": 12000000,
        "MDEntryPositionNo": 3,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    }
]

defmdsymb_spo_usd_sek = 'USD/SEK:SPO:REG:HSBC'
symbol_usd_sek = 'USD/SEK'
no_md_entries_usd_sek = [
    {
        "MDEntryType": "0",
        "MDEntryPx": 6.771406,
        "MDEntrySize": 1000000,
        "MDEntryPositionNo": 1,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "1",
        "MDEntryPx": 6.771416,
        "MDEntrySize": 1000000,
        "MDEntryPositionNo": 1,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "0",
        "MDEntryPx": 6.771401,
        "MDEntrySize": 6000000,
        "MDEntryPositionNo": 2,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "1",
        "MDEntryPx": 6.771421,
        "MDEntrySize": 6000000,
        "MDEntryPositionNo": 2,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "0",
        "MDEntryPx": 6.771396,
        "MDEntrySize": 12000000,
        "MDEntryPositionNo": 3,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
    {
        "MDEntryType": "1",
        "MDEntryPx": 6.771426,
        "MDEntrySize": 12000000,
        "MDEntryPositionNo": 3,
        'SettlDate': spo(),
        "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
    },
]

no_md_entries=[
                {
                    'SettlType': 0,
                    'MDEntryPx': '0.86162',
                    'MDEntryTime': '*',
                    'MDEntryID': '*',
                    'MDEntrySize': '10000000',
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
                    'MDEntryPx': '0.86177',
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
                },{
                    'SettlType': 0,
                    'MDEntryPx': '0.86162',
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
                    'MDEntryPx': '0.86177',
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
                },{
                    'SettlType': 0,
                    'MDEntryPx': '0.86162',
                    'MDEntryTime': '*',
                    'MDEntryID': '*',
                    'MDEntrySize': '1000000',
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
                    'MDEntryPx': '0.86177',
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

        # SEND MD EUR/USD spot
        # FixClientSell(CaseParamsSell(client, case_id, symbol=symbol_eur_usd,securitytype=securitytype,settldate=settldate, settltype=settltype)).\
        #     send_md_request().send_md_unsubscribe()
        # FixClientBuy(CaseParamsBuy(case_id,defmdsymb_spo_eur_usd,symbol_eur_usd,securitytype).
        #              prepare_custom_md_spot(no_md_entries_eur_usd)).send_market_data_spot()
        #
        # #SEND MD EUR/NOK spot
        # FixClientSell(CaseParamsSell(client, case_id, symbol=symbol_eur_nok,securitytype=securitytype,settldate=settldate, settltype=settltype))\
        #     .send_md_request().send_md_unsubscribe()
        # FixClientBuy(CaseParamsBuy(case_id,defmdsymb_spo_eur_nok,symbol_eur_nok,securitytype).
        #              prepare_custom_md_spot(no_md_entries_eur_nok)).send_market_data_spot()
        #
        # #SEND MD USD/SEK spot
        # FixClientSell(CaseParamsSell(client, case_id, symbol=symbol_usd_sek,securitytype=securitytype,settldate=settldate, settltype=settltype)).\
        #     send_md_request().send_md_unsubscribe()
        # FixClientBuy(CaseParamsBuy(case_id,defmdsymb_spo_usd_sek,symbol_usd_sek,securitytype).
        #              prepare_custom_md_spot(no_md_entries_usd_sek)).send_market_data_spot()

        # SEND MD USD/SEK spot
        params_eur_usd = CaseParamsSell(client, case_id, symbol=symbol_nok_sek, securitytype=securitytype,
                                        settldate=settldate, settltype=settltype)
        params_eur_usd.prepare_md_for_verification_custom(no_md_entries)
        md_nok_sek = FixClientSell(params_eur_usd)
        md_nok_sek.send_md_request()


        # Step 2

        md_nok_sek.verify_md_pending()




    except Exception as e:
        logging.error('Error execution', exc_info=True)
    finally:
        md_nok_sek.send_md_unsubscribe()
        pass
