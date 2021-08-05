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
bands=[2000000,6000000,12000000]
ord_status='Rejected'
md=None
settldate = (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y%m%d %H:%M:%S')
settldate_report = (tm(datetime.utcnow().isoformat()).strftime('%Y-%b-%d'))
new_settldate = (tm(datetime.utcnow().isoformat()) - bd(n=2)).date().strftime('%Y%m%d %H:%M:%S')
new_settldate_report = (tm(datetime.utcnow().isoformat()) - bd(n=2)).date().strftime('%Y-%b-%d')

defaultmdsymbol_spo='EUR/USD:SPO:REG:HSBC'




def execute(report_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    try:
        #Precondition
        FixClientSellEsp(CaseParamsSellEsp(client, case_id, settltype=settltype, settldate=settldate, symbol=symbol, securitytype=securitytype)).\
            send_md_request().send_md_unsubscribe()
        FixClientBuy(CaseParamsBuy(case_id, defaultmdsymbol_spo, symbol, securitytype)).send_market_data_spot()

        params = CaseParamsSellEsp(client, case_id, side=side, orderqty=orderqty, ordtype=ordtype, timeinforce=timeinforce,
                                   currency=currency, settlcurrency=settlcurrency, settltype=settltype, settldate= settldate, symbol=symbol,
                                   securitytype=securitytype, securityidsource=securityidsource, securityid=securityid)
        params.prepare_md_for_verification(bands)
        md = FixClientSellEsp(params).\
            send_md_request().\
            verify_md_pending()
        price= md.extract_filed('Price')

        text='11734 \'TradeDate\' ({0}) is later than \'SettlDate\' ({1}) / 11697 No listing found for order with currency EUR'.\
            format(settldate_report,new_settldate_report)
        params.settldate = new_settldate
        params.set_new_order_single_params()

        md.send_new_order_single(price).\
            verify_order_pending().\
            verify_order_algo_rejected(text)
    except Exception as e:
        logging.error('Error execution', exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
    finally:
        try:
            md.send_md_unsubscribe()
        except:
            bca.create_event('Unsubscribe failed', status='FAILED', parent_id=case_id)



