import time

from quod_qa.fx.fx_wrapper.CaseParamsSell import CaseParamsSell
from quod_qa.fx.fx_wrapper.MarketDataRequst import MarketDataRequst
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
connectivity = 'fix-ss-308-mercury-standard'
side = '1'
orderqty = 1
ordtype = '2'
timeinforce = '4'
currency= 'EUR'
settlcurrency = 'USD'
settltype=0
symbol='EUR/USD'
securitytype='FXSPOT'
securityidsource='8'
securityid='EUR/USD'
bands=[1000000,2000000,3000000]
ord_status='Filled'
md=None
settldate = (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y%m%d %H:%M:%S')





def execute(report_id):
    try:
        case_id = bca.create_event('QAP_3555', report_id)
        params = CaseParamsSell(connectivity, client, case_id, side=side, orderqty=orderqty, ordtype=ordtype, timeinforce=timeinforce,
                                currency=currency, settlcurrency=settlcurrency, settltype=settltype, settldate= settldate, symbol=symbol, securitytype=securitytype,
                                securityidsource=securityidsource, securityid=securityid)
        params.mdreqid = bca.client_orderid(10)
        params.clordid= bca.client_orderid(9)
        md = MarketDataRequst(params)
        md.set_md_params()\
            .send_md_request()
        md.verify_md_pending(bands)
        price = md.extruct_filed('Price', 0)
        mdEntryPx1=md.extruct_filed('MDEntryID',0)
        mdEntryPx2=md.extruct_filed('MDEntryID',1)
        time.sleep(5)





    except Exception as e:
        logging.error('Error execution', exc_info=True)
    finally:
        md.send_md_unsubscribe()



