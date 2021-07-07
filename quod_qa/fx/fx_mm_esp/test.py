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
currency= 'EUR'
settlcurrency = 'USD'
settltype=0
symbol='EUR/USD'
securitytype='FXSPOT'
securityid='EUR/USD'
bands=[1000000,2000000,3000000]
md=None
settldate=tsd.spo()
defaultmdsymbol_spo='EUR/USD:SPO:REG:HSBC'





def execute(report_id):
    try:
        case_name = Path(__file__).name[:-3]
        case_id = bca.create_event(case_name, report_id)

        #Preconditions
        params = CaseParamsSellEsp(client, case_id, side, orderqty, ordtype, timeinforce, currency, settlcurrency,
                                   settltype, settldate, symbol, securitytype, securityid, account=account)
        md = FixClientSellEsp(params).send_md_request().send_md_unsubscribe()
        #Send market data to the HSBC venue EUR/USD spot
        FixClientBuy(CaseParamsBuy(case_id,defaultmdsymbol_spo,symbol,securitytype)).\
            send_market_data_spot()

        time.sleep(5)
        params.prepare_md_for_verification(bands)
        #Step 1
        md.send_md_request_timeout(15)




    except Exception as e:
        logging.error('Error execution', exc_info=True)
    finally:
        md.send_md_unsubscribe()



