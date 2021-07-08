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
client = 'Palladium1'
account = 'Palladium1_1'
side = '1'
orderqty = '1000000'
ordtype = '2'
timeinforce = '4'
currency = 'EUR'
settlcurrency = 'USD'
settltype = 0
symbol = 'EUR/USD'
securitytype = 'FXSPOT'
securityid = 'EUR/USD'
bands = [2000000, 6000000, 12000000]
md = None
settldate = tsd.spo()
defaultmdsymbol_spo = 'EUR/USD:SPO:REG:HSBC'


def execute(report_id):
    try:
        case_name = Path(__file__).name[:-3]
        case_id = bca.create_event(case_name, report_id)
        params_1 = CaseParamsSellEsp(client, case_id, side=side, orderqty=orderqty, ordtype=ordtype,
                                     timeinforce=timeinforce, currency=currency,
                                     settlcurrency=settlcurrency, settltype=settltype, settldate=settldate,
                                     symbol=symbol, securitytype=securitytype,
                                     securityid=securityid, account=account)
        md_1 = FixClientSellEsp(params_1)
        try:
            # Preconditions
            params_0 = CaseParamsSellEsp(client, case_id, side=side, orderqty=orderqty, ordtype=ordtype,
                                         timeinforce=timeinforce, currency=currency,
                                         settlcurrency=settlcurrency, settltype=settltype, settldate=settldate,
                                         symbol=symbol, securitytype=securitytype,
                                         securityid=securityid, account=account)
            md_0 = FixClientSellEsp(params_0).send_md_request().send_md_unsubscribe()
            # Send market data to the HSBC venue EUR/USD spot
            FixClientBuy(CaseParamsBuy(case_id, defaultmdsymbol_spo, symbol, securitytype)). \
                send_market_data_spot()
            time.sleep(5)

            # Step 1

            params_1.prepare_md_for_verification(bands)
            md_1.send_md_request(). \
                verify_md_pending()
            price = md_1.extruct_filed('Price')
            # Step 2-5
            md_1.send_new_order_single(price) \
                .verify_order_pending() \
                .verify_order_new() \
                .verify_order_filled()

        except Exception:
            logging.error('Error execution', exc_info=True)
        finally:
            md_1.send_md_unsubscribe()
    except Exception:
        logging.error('Error execution', exc_info=True)
