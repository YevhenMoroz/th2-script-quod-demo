from quod_qa.fx.fx_mm_esp.fx_wrapper.CaseParams import CaseParams
from quod_qa.fx.fx_mm_esp.fx_wrapper.MarketDataRequst import MarketDataRequst
from custom import basic_custom_actions as bca
import logging
from quod_qa.fx.fx_mm_esp.fx_wrapper.NewOrderSingle import NewOrderSingle

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





def execute(report_id):
    try:
        case_id = bca.create_event('QAP_1518', report_id)
        params = CaseParams(connectivity, client, case_id, side=side, orderqty=orderqty, ordtype=ordtype, timeinforce=timeinforce,
                            currency=currency, settlcurrency=settlcurrency, settltype=settltype, symbol=symbol, securitytype=securitytype,
                            securityidsource=securityidsource, securityid=securityid)
        md = MarketDataRequst(params)
        md.set_md_params().send_md_request().\
            verify_md_pending(bands)
        price = md.extruct_filed('Price')
        NewOrderSingle(params).send_new_order_single(price).\
            verify_order(ord_status,account)




    except Exception as e:
        logging.error('Error execution', exc_info=True)
    finally:
        md.send_md_unsubscribe()



