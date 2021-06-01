import time

from quod_qa.fx.fx_wrapper.CaseParamsBuy import CaseParamsBuy
from quod_qa.fx.fx_wrapper.CaseParamsSell import CaseParamsSell
from quod_qa.fx.fx_wrapper.FixClientBuy import FixClientBuy
from quod_qa.fx.fx_wrapper.FixClientSell import FixClientSell
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
settlcurrency = 'NOK'
settltype='W1'
symbol='EUR/NOK'
securitytype_fwd='FXFWD'
securitytype_spo='FXSPOT'
securityid='EUR/NOK'
bands=[1000000,2000000]
md=None
settldate_wk1=tsd.wk1()
defaultmdsymbol_spo='EUR/NOK:SPO:REG:HSBC'






def execute(report_id):
    try:
        case_name = Path(__file__).name[:-3]
        case_id = bca.create_event(case_name, report_id)
        # Preconditions
        params_sell=CaseParamsSell(client, case_id, side, orderqty1, ordtype, timeinforce, currency, settlcurrency,
                                   settltype, settldate_wk1, symbol, securitytype_fwd, securityid)
        md = FixClientSell(params_sell).send_md_request().send_md_unsubscribe()
        #Send market data to the HSBC venue EUR/NOK spot
        FixClientBuy(CaseParamsBuy(case_id,defaultmdsymbol_spo,symbol,securitytype_spo)).\
            send_market_data_spot()

        #Step 1-3
        params_sell.prepare_md_for_verification(bands, priced=False)
        md.send_md_request().\
            verify_md_pending()
        price=md.extruct_filed('Price')

        #Step 4
        text='empty book'
        md.send_new_order_single(price).\
            verify_order_pending().\
            verify_order_rejected(text)

        #Step 5
        params_sell.order_params['OrderQty']=orderqty2
        md.send_new_order_single(price).\
            verify_order_pending().\
            verify_order_rejected(text)


    except Exception as e:
        logging.error('Error execution', exc_info=True)
    finally:
        # md.send_md_unsubscribe()
        pass



