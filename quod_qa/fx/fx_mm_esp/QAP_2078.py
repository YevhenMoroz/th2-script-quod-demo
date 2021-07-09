from pathlib import Path

from custom.tenor_settlement_date import spo, wk1
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
account = 'Palladium1_1'
side = '1'
orderqty = '1000000'
ordtype = '2'
timeinforce = '3'
currency = 'EUR'
settlcurrency = 'USD'
settltype = 'W1'
symbol = 'EUR/USD'
securitytype_spo = 'FXSPOT'
securitytype_w = 'FXFWD'
securityidsource = '8'
securityid = 'EUR/USD'
bands = [2000000, 6000000, 12000000]
md = None
settldate_spo = spo()
settldate_w1 = wk1()
defaultmdsymbol_spo = 'EUR/USD:SPO:REG:HSBC'


def execute(report_id):
    try:
        case_name = Path(__file__).name[:-3]
        case_id = bca.create_event(case_name, report_id)
        # Precondition
        FixClientSellEsp(CaseParamsSellEsp(client, case_id, settltype=settltype, settldate=settldate_spo, symbol=symbol,
                                           securitytype=securitytype_spo)). \
            send_md_request().send_md_unsubscribe()
        FixClientBuy(CaseParamsBuy(case_id, defaultmdsymbol_spo, symbol, securitytype_spo)).send_market_data_spot()

        # Step 1...
        params = CaseParamsSellEsp(client, case_id, side=side, orderqty=orderqty, ordtype=ordtype,
                                   timeinforce=timeinforce, currency=currency,
                                   settlcurrency=settlcurrency, settltype=settltype, settldate=settldate_w1,
                                   symbol=symbol, securitytype=securitytype_w,
                                   securityidsource=securityidsource, securityid=securityid, account=account)
        params.prepare_md_for_verification(bands)
        md = FixClientSellEsp(params).send_md_request().verify_md_pending()
        price = md.extruct_filed('Price')
        md.send_new_order_single(price). \
            verify_order_pending(). \
            verify_order_filled_fwd()



    except Exception as e:
        logging.error('Error execution', exc_info=True)
    finally:
        md.send_md_unsubscribe()
