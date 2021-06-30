import logging
from datetime import datetime, timedelta
from custom import basic_custom_actions as bca, tenor_settlement_date as tsd
from pathlib import Path
from quod_qa.fx.fx_wrapper.CaseParamsBuy import CaseParamsBuy
from quod_qa.fx.fx_wrapper.FixClientBuy import FixClientBuy




logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
symbol_eurusd='EUR/USD'
symbol_gbpusd='GBP/USD'
symbol_eurnok='EUR/NOK'
securitytype='FXSPOT'

defaultmdsymbol_spo_eurusd = 'EUR/USD:SPO:REG:GS'
md_md_entries_eurusd=[
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.19597,
                    "MDEntrySize": 2000000,
                    "MDEntryPositionNo": 1,
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.19609,
                    "MDEntrySize": 2000000,
                    "MDEntryPositionNo": 1,
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.19594,
                    "MDEntrySize": 6000000,
                    "MDEntryPositionNo": 2,
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.19612,
                    "MDEntrySize": 6000000,
                    "MDEntryPositionNo": 2,
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 1.19591,
                    "MDEntrySize": 12000000,
                    "MDEntryPositionNo": 3,
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 1.19615,
                    "MDEntrySize": 12000000,
                    "MDEntryPositionNo": 3,
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
            ]

defaultmdsymbol_spo_eurnok = 'EUR/NOK:SPO:REG:GS'
md_md_entries_eurnok=[
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 8.890282,
                    "MDEntrySize": 2000000,
                    "MDEntryPositionNo": 1,
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 8.890292,
                    "MDEntrySize": 2000000,
                    "MDEntryPositionNo": 1,
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 8.890277,
                    "MDEntrySize": 6000000,
                    "MDEntryPositionNo": 2,
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 8.890297,
                    "MDEntrySize": 6000000,
                    "MDEntryPositionNo": 2,
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 8.890272,
                    "MDEntrySize": 12000000,
                    "MDEntryPositionNo": 3,
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 8.890302,
                    "MDEntrySize": 12000000,
                    "MDEntryPositionNo": 3,
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
            ]

defaultmdsymbol_spo_usdgbp = 'GBP/USD:SPO:REG:GS'
md_md_entries_gbpusd=[
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 5.75178,
                    "MDEntrySize": 2000000,
                    "MDEntryPositionNo": 1,
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 5.75179,
                    "MDEntrySize": 2000000,
                    "MDEntryPositionNo": 1,
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "0",
                    "MDEntryPx": 5.751775,
                    "MDEntrySize": 6000000,
                    "MDEntryPositionNo": 2,
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
                {
                    "MDEntryType": "1",
                    "MDEntryPx": 5.751795,
                    "MDEntrySize": 6000000,
                    "MDEntryPositionNo": 2,
                    "MDEntryTime": datetime.utcnow().strftime('%Y%m%d'),
                },
            ]

def execute(report_id):
    try:
        case_name = Path(__file__).name[:-3]
        case_id = bca.create_event(case_name, report_id)


        # Send market data to the HSBC venue EUR/USD spot
        params = CaseParamsBuy(case_id, defaultmdsymbol_spo_eurusd, symbol_eurusd, securitytype).prepare_custom_md_spot(md_md_entries_eurusd)
        FixClientBuy(params).send_market_data_spot()

        # Send market data to the HSBC venue EUR/NOK spot
        params = CaseParamsBuy(case_id, defaultmdsymbol_spo_eurnok, symbol_eurnok, securitytype).prepare_custom_md_spot(md_md_entries_eurnok)
        FixClientBuy(params).send_market_data_spot()

        # Send market data to the HSBC venue GBP/USD spot
        params = CaseParamsBuy(case_id, defaultmdsymbol_spo_usdgbp, symbol_gbpusd, securitytype).prepare_custom_md_spot(md_md_entries_gbpusd)
        FixClientBuy(params).send_market_data_spot()

        # params = CaseParamsSellRfq(client, case_id, side=side, orderqty=orderqty,symbol=symbol, securitytype=securitytype,
        #                            settldate=settldate,settltype=settltype, currency=currency)
        #
        # qt = FixClientSellRfq(params)
        # qt.send_request_for_quote()
        # qt.verify_quote_pending()


        # FixClientSell(params).send_request_for_quote_swap()
    except Exception as e:
        logging.error('Error execution', exc_info=True)
    finally:

        pass

