import time

from quod_qa.fx.fx_wrapper.CaseParamsBuy import CaseParamsBuy
from quod_qa.fx.fx_wrapper.CaseParamsSellEsp import CaseParamsSellEsp
from quod_qa.fx.fx_wrapper.FixClientBuy import FixClientBuy
from quod_qa.fx.fx_wrapper.FixClientSellEsp import FixClientSellEsp
import logging
from pathlib import Path
from custom import basic_custom_actions as bca, tenor_settlement_date as tsd

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True
client = 'Palladium2'
account = 'Palladium2_2'
side = '1'
orderqty1 = '1000000'
orderqty2 = '2000000'
ordtype = '2'
timeinforce = '4'
currency= 'EUR'
settlcurrency = 'SEK'
settltype='W1'
symbol='EUR/SEK'
securitytype_fwd='FXFWD'
securitytype_spo='FXSPOT'
securityid='EUR/SEK'
bands=[1000000,2000000]
md=None
settldate_wk1=tsd.wk1()
settldate_spo=tsd.spo()
defaultmdsymbol_spo='EUR/SEK:SPO:REG:HSBC'






def execute(report_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    try:

        # Preconditions
        params_sell= CaseParamsSellEsp(client, case_id, settltype=settltype, settldate=settldate_spo, symbol=symbol, securitytype=securitytype_spo)
        FixClientSellEsp(params_sell).send_md_request().send_md_unsubscribe()
        #Send market data to the HSBC venue EUR/SEK spot
        FixClientBuy(CaseParamsBuy(case_id,defaultmdsymbol_spo,symbol,securitytype_spo)).\
            send_market_data_spot()

        #Step 1-3
        params = CaseParamsSellEsp(client, case_id, side=side, orderqty=orderqty1, ordtype=ordtype, timeinforce=timeinforce, currency=currency,
                                   settlcurrency=settlcurrency, settltype=settltype, settldate=settldate_wk1, symbol=symbol, securitytype=securitytype_fwd,
                                   securityid=securityid)
        params.prepare_md_for_verification(bands, published=False)
        md = FixClientSellEsp(params).\
            send_md_request().\
            verify_md_pending()
        price=md.extract_filed('Price')

        #Step 4
        text='empty book'
        md.send_new_order_single(price).\
            verify_order_pending().\
            verify_order_rejected(text)

        #Step 5
        params.orderqty=orderqty2
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
            bca.create_event('Unsubscribe failed', status='FAILED', parent_id=case_id)



