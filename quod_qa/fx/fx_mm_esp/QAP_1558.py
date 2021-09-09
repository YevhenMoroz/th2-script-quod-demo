import time
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
account = 'Palladium1_1'
side = '1'
orderqty = '1000000'
orderqty2 = '2000000'
ordtype = '2'
timeinforce = '4'
currency1 = 'USD'
currency2 = 'EUR'
settlcurrency = 'CAD'
settltype = 'W1'
symbol1 = 'USD/CAD'
symbol2 = 'EUR/CAD'
securitytype_spo = 'FXSPOT'
securitytype_fwd = 'FXFWD'
securityidsource = '8'
securityid1 = 'USD/CAD'
securityid2 = 'EUR/CAD'
bands = [1000000, 2000000, 3000000]
bands_not_published = [2000000, 3000000]
md = None
settldate1 = (tm(datetime.utcnow().isoformat()) + bd(n=6)).date().strftime('%Y%m%d %H:%M:%S')
settldate1_spo = (tm(datetime.utcnow().isoformat()) + bd(n=1)).date().strftime('%Y%m%d %H:%M:%S')
settldate2 = (tm(datetime.utcnow().isoformat()) + bd(n=7)).date().strftime('%Y%m%d %H:%M:%S')
settldate2_spo = (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y%m%d %H:%M:%S')

defaultmdsymbol_spo_1 = 'USD/CAD:SPO:REG:HSBC'
defaultmdsymbol_spo_2 = 'EUR/CAD:SPO:REG:HSBC'


def execute(report_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    try:

        params_2 = CaseParamsSellEsp(client, case_id, side=side, orderqty=orderqty, ordtype=ordtype,
                                     timeinforce=timeinforce, currency=currency2,
                                     settlcurrency=settlcurrency, settltype=settltype,
                                     symbol=symbol2, securitytype=securitytype_fwd,
                                     securityid=securityid2, account=account)
        params_2.prepare_md_for_verification(bands, published=False, which_bands_not_pb=bands_not_published)
        md2 = FixClientSellEsp(params_2)
        try:

            # Precondition
            params_usd_cad = CaseParamsSellEsp(client, case_id, settltype=settltype,
                                               symbol=symbol1, securitytype=securitytype_spo)
            params_eur_cad = CaseParamsSellEsp(client, case_id, settltype=settltype,
                                               symbol=symbol2, securitytype=securitytype_spo)
            FixClientSellEsp(params_usd_cad). \
                send_md_request(). \
                send_md_unsubscribe()
            FixClientSellEsp(params_eur_cad). \
                send_md_request(). \
                send_md_unsubscribe()
            FixClientBuy(
                CaseParamsBuy(case_id, defaultmdsymbol_spo_1, symbol1, securitytype_spo)). \
                send_market_data_spot()
            FixClientBuy(
                CaseParamsBuy(case_id, defaultmdsymbol_spo_2, symbol2, securitytype_spo)). \
                send_market_data_spot()

            # Steps 1-3
            params_1 = CaseParamsSellEsp(client, case_id, side=side, orderqty=orderqty, ordtype=ordtype,
                                         timeinforce=timeinforce, currency=currency1,
                                         settlcurrency=settlcurrency, settltype=settltype,
                                         symbol=symbol1, securitytype=securitytype_fwd,
                                         securityid=securityid1)
            params_1.prepare_md_for_verification(bands, published=False)
            md1 = FixClientSellEsp(params_1). \
                send_md_request(). \
                verify_md_pending()
            price1 = md1.extract_filed('Price')
            text = 'empty book'
            md1.send_new_order_single(price1). \
                verify_order_pending(). \
                verify_order_rejected(text). \
                send_md_unsubscribe()

            # Step 4-5
            params_2 = CaseParamsSellEsp(client, case_id, side=side, orderqty=orderqty, ordtype=ordtype,
                                         timeinforce=timeinforce, currency=currency2,
                                         settlcurrency=settlcurrency, settltype=settltype,
                                         symbol=symbol2, securitytype=securitytype_fwd,
                                         securityid=securityid2, account=account)
            params_2.prepare_md_for_verification(bands, published=False, which_bands_not_pb=bands_not_published)
            md2 = FixClientSellEsp(params_2)
            price2 = md2.send_md_request(). \
                verify_md_pending(). \
                extract_filed('Price')
            md2.send_new_order_single(price2). \
                verify_order_pending(). \
                verify_order_filled_fwd()

            # Step 6
            text = 'not enough quantity in book'
            params_2.orderqty = orderqty2
            params_2.set_new_order_single_params()
            md2.send_new_order_single(price2). \
                verify_order_pending(). \
                verify_order_rejected(text)
        except Exception as e:
            logging.error('Error execution', exc_info=True)
            bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
        finally:
            try:
                md2.send_md_unsubscribe()
            except:
                bca.create_event('Unsubscribe failed', status='FAILED', parent_id=case_id)
    except Exception:
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
        logging.error('Error execution', exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
