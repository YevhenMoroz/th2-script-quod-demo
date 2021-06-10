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
md=None
settldate = (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y%m%d %H:%M:%S')
settldate_report = (tm(datetime.utcnow().isoformat()).strftime('%Y-%B-%d'))
new_settldate = (tm(datetime.utcnow().isoformat()) - bd(n=2)).date().strftime('%Y%m%d %H:%M:%S')
new_settldate_report = (tm(datetime.utcnow().isoformat()) - bd(n=2)).date().strftime('%Y-%B-%d')





def execute(report_id):
    try:

        case_id = bca.create_event('QAP_3841', report_id)
        params = CaseParamsSellEsp(connectivity, client, case_id, side=side, orderqty=orderqty, ordtype=ordtype, timeinforce=timeinforce,
                                   currency=currency, settlcurrency=settlcurrency, settltype=settltype, settldate= settldate, symbol=symbol,
                                   securitytype=securitytype, securityidsource=securityidsource, securityid=securityid)
        md = MarketDataRequst(params)
        md.set_md_params().send_md_request().\
            verify_md_pending(bands)
        price=md.extruct_filed('Price')

        text='11734 \'TradeDate\' ({0}) is later than \'SettlDate\' ({1}) / 11697 No listing found for order with currency EUR'.\
            format(settldate_report,new_settldate_report)
        params.settldate = new_settldate
        NewOrderSingle(params).\
            send_new_order_single(price).\
            verify_order_rejected(text,'algo')





    except Exception as e:
        logging.error('Error execution', exc_info=True)
    finally:
        md.send_md_unsubscribe()



