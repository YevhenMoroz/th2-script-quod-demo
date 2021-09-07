import time

from quod_qa.fx.fx_wrapper.CaseParamsSell import CaseParamsSell
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
bands=[1000000,2000000,3000000]
md=None
settldate1 = (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y%m%d %H:%M:%S')
settldate2 = (tm(datetime.utcnow().isoformat()) + bd(n=7)).date().strftime('%Y%m%d %H:%M:%S')


a = bands[0]


def execute(report_id):
    try:
        case_id = bca.create_event('1554', report_id)
        params = CaseParamsSell(connectivity, client, case_id, side=side, orderqty=orderqty1, ordtype=ordtype, timeinforce=timeinforce,
                                currency=currency, settlcurrency=settlcurrency, settltype=settltype1, settldate= settldate1, symbol=symbol,
                                securitytype=securitytype1, securityidsource=securityidsource, securityid=securityid)

        #Steps 1-2
        md = MarketDataRequst(params)
        md.set_md_params().send_md_request().\
            verify_md_pending(bands)
        md.send_md_unsubscribe()

        #Steps 3-4
        params.settltype=settltype2
        params.settldate=settldate2
        params.securitytype=securitytype2
        params.orderqty=orderqty2
        params.mdreqid=bca.client_orderid(10)
        params.clordid=bca.client_orderid(9)


        md = MarketDataRequst(params)
        md.set_md_params().send_md_request().\
            verify_md_pending(bands)







    except Exception as e:
        logging.error('Error execution', exc_info=True)
    finally:
        md.send_md_unsubscribe()



