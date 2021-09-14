from pathlib import Path

from quod_qa.fx.fx_wrapper.CaseParamsBuy import CaseParamsBuy
from quod_qa.fx.fx_wrapper.CaseParamsSellEsp import CaseParamsSellEsp
from quod_qa.fx.fx_wrapper.FixClientBuy import FixClientBuy
from quod_qa.fx.fx_wrapper.FixClientSellEsp import FixClientSellEsp
from custom import basic_custom_actions as bca
import logging
from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd
from datetime import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True
client = 'Palladium1'
account = 'Palladium1_1'
side = '1'
orderqty1 = '1000000'
orderqty2 = '2000000'
ordtype = '2'
timeinforce = '4'
currency= 'EUR'
settlcurrency = 'CAD'
settltype1='0'
settltype2='W1'
symbol='EUR/USD'
securitytype1='FXSPOT'
securitytype2='FXFWD'
securityidsource='8'
securityid='EUR/USD'
bands=[2000000,6000000,12000000]
md=None
settldate1 = (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y%m%d %H:%M:%S')
settldate2 = (tm(datetime.utcnow().isoformat()) + bd(n=7)).date().strftime('%Y%m%d %H:%M:%S')
defaultmdsymbol_spo='EUR/USD:SPO:REG:HSBC'




def execute(report_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    try:

        #Precondition
        FixClientSellEsp(CaseParamsSellEsp(client, case_id, settltype=settltype1, settldate=settldate1, symbol=symbol, securitytype=securitytype1)).\
            send_md_request().send_md_unsubscribe()
        FixClientBuy(CaseParamsBuy(case_id, defaultmdsymbol_spo, symbol, securitytype1)).send_market_data_spot()

        params = CaseParamsSellEsp(client, case_id, side=side, orderqty=orderqty1, ordtype=ordtype, timeinforce=timeinforce,
                                   currency=currency, settlcurrency=settlcurrency, settltype=settltype1, settldate= settldate1, symbol=symbol,
                                   securitytype=securitytype1, securityidsource=securityidsource, securityid=securityid)
        params.prepare_md_for_verification(bands)
        #Steps 1-2
        FixClientSellEsp(params).\
            send_md_request().\
            verify_md_pending().\
            send_md_unsubscribe()

        #Steps 3-4
        params2 = CaseParamsSellEsp(client, case_id, side=side, orderqty=orderqty2, ordtype=ordtype, timeinforce=timeinforce,
                                   currency=currency, settlcurrency=settlcurrency, settltype=settltype2, settldate= settldate2, symbol=symbol,
                                   securitytype=securitytype2, securityidsource=securityidsource, securityid=securityid)
        params2.prepare_md_for_verification(bands)
        FixClientSellEsp(params2).\
            send_md_request().\
            verify_md_pending().\
            send_md_unsubscribe()
    except Exception as e:
        logging.error('Error execution', exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
    finally:
        pass



