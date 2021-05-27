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
connectivity = 'fix-ss-308-mercury-standard'
side = '1'
orderqty = 1000000
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
ord_status='Rejected'
settldate = (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y%m%d %H:%M:%S')
md=None






def execute(report_id):
    try:
        case_id = bca.create_event('QAP_2086', report_id)
        params = CaseParams(connectivity, client, case_id, side=side, orderqty=orderqty, ordtype=ordtype, timeinforce=timeinforce,
                            currency=currency, settlcurrency=settlcurrency, settltype=settltype,settldate=settldate, symbol=symbol,
                            securitytype=securitytype,securityidsource=securityidsource, securityid=securityid)
        md = MarketDataRequst(params)
        md.set_md_params().send_md_request().\
            verify_md_pending(bands)
        price=md.extruct_filed('Price')
        new_price = round(float(price)-0.1,5)
        text='order price ({0}) lower than offer ({1})'.format(new_price, price)
        NewOrderSingle(params).send_new_order_single(new_price).\
            verify_order_pending(). \
            verify_order_rejected(text)





    except Exception as e:
        logging.error('Error execution', exc_info=True)
    finally:
        md.send_md_unsubscribe()



