import time

from quod_qa.fx.fx_wrapper.CaseParamsSellEsp import CaseParamsSellEsp
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
orderqty2 = '2000000'
ordtype = '2'
timeinforce = '4'
currency1= 'USD'
currency2= 'EUR'
settlcurrency = 'CAD'
settltype='W2'
symbol1='USD/CAD'
symbol2='EUR/CAD'
securitytype='FXFWD'
securityidsource='8'
securityid1='USD/CAD'
securityid2='EUR/CAD'
bands=[1000000,2000000,3000000]
md=None
settldate1 = (tm(datetime.utcnow().isoformat()) + bd(n=11)).date().strftime('%Y%m%d %H:%M:%S')
settldate2 = (tm(datetime.utcnow().isoformat()) + bd(n=12)).date().strftime('%Y%m%d %H:%M:%S')

a = bands[0]


def execute(report_id):
    try:
        case_id = bca.create_event('QAP_1559', report_id)
        params = CaseParamsSellEsp(connectivity, client, case_id, side=side, orderqty=orderqty, ordtype=ordtype, timeinforce=timeinforce,
                                   currency=currency1, settlcurrency=settlcurrency, settltype=settltype, settldate= settldate1, symbol=symbol1, securitytype=securitytype,
                                   securityidsource=securityidsource, securityid=securityid1)
        #Steps 1-3
        md = MarketDataRequst(params)
        md.set_md_params().send_md_request().\
            verify_md_pending(bands,priced=False)
        price1 = md.extruct_filed('Price')
        text = 'empty book'
        NewOrderSingle(params)\
            .send_new_order_single(price1).\
            verify_order_pending().\
            verify_order_rejected(text)
        md.send_md_unsubscribe()

        #Steps 4
        params.currency=currency2
        params.symbol=symbol2
        params.securityid=securityid2
        params.settldate=settldate2
        params.mdreqid=bca.client_orderid(10)
        params.clordid=bca.client_orderid(9)
        bands_not_published = [2000000,3000000]
        md = MarketDataRequst(params)
        md.set_md_params().send_md_request()
        md.verify_md_pending(bands,priced=False, which_bands_not_pr=bands_not_published)


        #Step 5
        price2 = md.extruct_filed('Price')
        NewOrderSingle(params)\
            .send_new_order_single(price2).\
            verify_order_pending().\
            verify_order_filled(account)

        #Step 6
        text = 'not enough quantity in book'
        params.orderqty=orderqty2
        NewOrderSingle(params)\
            .send_new_order_single(price2).\
            verify_order_pending().\
            verify_order_rejected(text)
        md.send_md_unsubscribe()


    except Exception as e:
        logging.error('Error execution', exc_info=True)
    finally:
        md.send_md_unsubscribe()



