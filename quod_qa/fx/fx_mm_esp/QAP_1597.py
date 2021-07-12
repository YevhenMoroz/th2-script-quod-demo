from pathlib import Path

from custom.tenor_settlement_date import spo
from quod_qa.fx.fx_wrapper.CaseParamsSellEsp import CaseParamsSellEsp
from quod_qa.fx.fx_wrapper.FixClientSellEsp import FixClientSellEsp
from custom import basic_custom_actions as bca
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True
client = 'Palladium1'
account = 'Palladium1_1'
side = '1'
orderqty = 1
ordtype = '2'
timeinforce = '4'
currency = 'EUR'
settlcurrency = 'USD'
settltype = 0
symbol = 'EUR/XXX'
securitytype = 'FXSPOT'
securityidsource = '8'
securityid = 'EUR/USD'
bands = [1000000, 2000000, 3000000]
ord_status = 'Filled'
md = None
settldate = spo()
text = 'no active client tier'
defaultmdsymbol_spo = 'EUR/USD:SPO:REG:HSBC'


def execute(report_id):
    try:
        case_name = Path(__file__).name[:-3]
        case_id = bca.create_event(case_name, report_id)

        params = CaseParamsSellEsp(client, case_id, side=side, orderqty=orderqty, ordtype=ordtype,
                                   timeinforce=timeinforce,
                                   currency=currency, settlcurrency=settlcurrency, settltype=settltype,
                                   settldate=settldate, symbol=symbol, securitytype=securitytype,
                                   securityidsource=securityidsource, securityid=securityid, account=account)
        md = FixClientSellEsp(params). \
            send_md_request(). \
            verify_md_rejected(text)


    except Exception as e:
        logging.error('Error execution', exc_info=True)
    finally:
        md.send_md_unsubscribe()
