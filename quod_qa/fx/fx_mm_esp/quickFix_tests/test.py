import time

from quod_qa.fx.fx_wrapper.CaseParams import CaseParams
from quod_qa.fx.fx_wrapper.MarketDataRequst import MarketDataRequst
from custom import basic_custom_actions as bca
import logging
from quod_qa.fx.fx_wrapper.NewOrderSingle import NewOrderSingle
from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd
from datetime import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True
client = 'Palladium1'
account = 'Palladium1_1'
connectivity = 'fix-ss-308-mercury-standard'
side = '1'
orderqty = '1000000'
ordtype = '2'
timeinforce = '4'
currency= 'EUR'
settlcurrency = 'CAD'
settltype='W1'
symbol='EUR/CAD'
securitytype='FXFWD'
securityidsource='8'
securityid='EUR/CAD'
bands=[1000000,2000000,3000000]
md=None
settldate = (tm(datetime.utcnow().isoformat()) + bd(n=7)).date().strftime('%Y%m%d %H:%M:%S')


a = bands[0]


def execute(report_id):
    try:
        case_id = bca.create_event('test', report_id)
        params = CaseParams(connectivity, client, case_id, side=side, orderqty=orderqty, ordtype=ordtype, timeinforce=timeinforce,
                            currency=currency, settlcurrency=settlcurrency, settltype=settltype, settldate= settldate, symbol=symbol, securitytype=securitytype,
                            securityidsource=securityidsource, securityid=securityid)

        md = MarketDataRequst(params)
        md.set_md_params().send_md_request().\
            verify_md_pending(bands,published=False)





    except Exception as e:
        logging.error('Error execution', exc_info=True)
    finally:
        md.send_md_unsubscribe()



