import logging
from datetime import datetime, timedelta
from custom import basic_custom_actions as bca, tenor_settlement_date as tsd
from pathlib import Path
from quod_qa.fx.fx_wrapper.CaseParamsBuy import CaseParamsBuy
from quod_qa.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from quod_qa.fx.fx_wrapper.FixClientBuy import FixClientBuy
from quod_qa.fx.fx_wrapper.FixClientSellEsp import FixClientSellEsp
from quod_qa.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq
from quod_qa.fx.fx_wrapper.CaseParamsSellEsp import CaseParamsSellEsp


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True
client = 'Palladium1'
settltype = '0'
symbol = 'EUR/USD'
currency = 'EUR'
securitytype = 'FXSPOT'
securityidsource = '8'
side = ''
orderqty = '1000000'
securityid = 'EUR/USD'
bands = [1000000]
md = None
settldate = tsd.spo()
ExpireTime = (datetime.now() + timedelta(seconds=120)).strftime("%Y%m%d-%H:%M:%S.000"),
TransactTime = (datetime.utcnow().isoformat())
defaultmdsymbol_spo = 'EUR/USD:SPO:REG:HSBC'


def execute(report_id):
    try:
        case_name = Path(__file__).name[:-3]
        case_id = bca.create_event(case_name, report_id)

        #Preconditions
        params_sell = CaseParamsSellEsp(client, case_id, settltype=settltype, settldate=settldate,
                                        symbol=symbol, securitytype=securitytype)
        FixClientSellEsp(params_sell).send_md_request().send_md_unsubscribe()
        # Send market data to the HSBC venue EUR/USD spot
        FixClientBuy(CaseParamsBuy(case_id, defaultmdsymbol_spo, symbol, securitytype)). \
            send_market_data_spot()

        # Step 1-2
        params = CaseParamsSellRfq(client, case_id, side=side, orderqty=orderqty, symbol=symbol,
                                   securitytype=securitytype,
                                   settldate=settldate, settltype=settltype, currency=currency)

        rfq = (FixClientSellRfq(params). \
               send_request_for_quote(). \
               rfq.verify_quote_pending())
        rfq.send_quote_cancel()

        #Step 3
        #ostronov

        #Step 4
        #ostronov




    except Exception as e:
        logging.error('Error execution', exc_info=True)
    finally:
        pass
