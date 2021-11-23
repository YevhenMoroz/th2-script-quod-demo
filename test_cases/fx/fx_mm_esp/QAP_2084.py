from pathlib import Path

from custom.tenor_settlement_date import spo
from test_cases.fx.fx_wrapper.CaseParamsBuy import CaseParamsBuy
from test_cases.fx.fx_wrapper.CaseParamsSellEsp import CaseParamsSellEsp
from test_cases.fx.fx_wrapper.FixClientBuy import FixClientBuy
from test_cases.fx.fx_wrapper.FixClientSellEsp import FixClientSellEsp
from custom import basic_custom_actions as bca
import logging
from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd
from datetime import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True
client = 'Palladium1'
side = '1'
orderqty = 1000000
new_orderqty = 52000000
ordtype = '2'
timeinforce = '4'
currency= 'EUR'
settlcurrency = 'USD'
settltype=0
symbol='EUR/USD'
securitytype='FXSPOT'
securityidsource='8'
securityid='EUR/USD'
bands=[2000000,6000000,12000000]
ord_status='Rejected'
settldate = spo()
md=None
defaultmdsymbol_spo='EUR/USD:SPO:REG:HSBC'






def execute(report_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    try:

        #Precondition
        FixClientSellEsp(CaseParamsSellEsp(client, case_id, settltype=settltype, settldate=settldate, symbol=symbol, securitytype=securitytype)).\
            send_md_request().send_md_unsubscribe()
        FixClientBuy(CaseParamsBuy(case_id, defaultmdsymbol_spo, symbol, securitytype)).send_market_data_spot()

        #Step 1
        params = CaseParamsSellEsp(client, case_id, side=side, orderqty=orderqty, ordtype=ordtype, timeinforce=timeinforce,
                                   currency=currency, settlcurrency=settlcurrency, settltype=settltype, settldate=settldate, symbol=symbol,
                                   securitytype=securitytype, securityidsource=securityidsource, securityid=securityid)
        params.prepare_md_for_verification(bands)
        md = FixClientSellEsp(params).send_md_request().verify_md_pending()
        price= md.extract_filed('Price')

        text='not enough quantity in book'
        params.orderqty=new_orderqty
        params.set_new_order_single_params()
        md.send_new_order_single(price).\
            verify_order_pending().\
            verify_order_rejected(text)
    except Exception as e:
        logging.error('Error execution', exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
    finally:
        try:
            md.send_md_unsubscribe()
        except:
            bca.create_event('Fail test event', status='FAILED', parent_id=case_id)



