from quod_qa.fx.fx_wrapper.CaseParamsSell import CaseParamsSell
from quod_qa.fx.fx_wrapper.FixClientSell import FixClientSell
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





def execute(report_id):
    try:
        case_name = Path(__file__).name[:-3]
        case_id = bca.create_event(case_name, report_id)
        params = CaseParamsSell(client, case_id, side, orderqty, ordtype, timeinforce, currency,
                                settlcurrency, settltype, settldate, symbol, securitytype, securityid,
                                account=account)
        params.prepare_md_for_verification(bands)

        md = FixClientSell(params)
        md.send_md_request_timeout(10000)








    except Exception as e:
        logging.error('Error execution', exc_info=True)
    finally:
        md.send_md_unsubscribe()



