import logging
from datetime import datetime, timedelta
from custom import basic_custom_actions as bca, tenor_settlement_date as tsd
from pathlib import Path

from quod_qa.fx.fx_wrapper.CaseParamsBuy import CaseParamsBuy
from quod_qa.fx.fx_wrapper.CaseParamsSellEsp import CaseParamsSellEsp
from quod_qa.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from quod_qa.fx.fx_wrapper.FixClientBuy import FixClientBuy
from quod_qa.fx.fx_wrapper.FixClientSellEsp import FixClientSellEsp
from quod_qa.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True
client = 'Palladium2'
account = 'Palladium2_2'
settltype = 'W3'
symbol = 'GBP/USD'
securityid = 'GBP/USD'
currency = 'GBP'
settlcurrency = 'USD'
side = '2'
securitytype = 'FXFWD'
securityidsource = '8'
orderqty = '1000000'
settldate = tsd.spo()
defaultmdsymbol='GBP/USD:SPO:REG:HSBC'
bid_px_expected='1.19596'

def execute(report_id):
    try:
        case_name = Path(__file__).name[:-3]
        case_id = bca.create_event(case_name, report_id)
        #Precondition
        FixClientSellEsp(CaseParamsSellEsp(client, case_id, settltype=settltype, settldate=settldate, symbol=symbol, securitytype=securitytype,
                                           securityid=securityid,currency=currency, settlcurrency=settlcurrency)).\
            send_md_request().send_md_unsubscribe()
        FixClientBuy(CaseParamsBuy(case_id, defaultmdsymbol, symbol, securitytype)).send_market_data_spot()

        # Step 1-2
        params = CaseParamsSellRfq(client, case_id, orderqty=orderqty, symbol=symbol, securityid=securityid,securitytype=securitytype,settldate=settldate,
                                   settltype=settltype, currency=currency, settlcurrency=settlcurrency,account=account)

        rfq = FixClientSellRfq(params)
        rfq.send_request_for_quote()
        rfq.verify_quote_pending()

        # Step 3-4
        bid_px = rfq.extruct_filed('BidPx')
        rfq.send_new_order_single(bid_px,side=side)
        rfq.verify_order_pending()
        # rfq.verify_order_new()
        rfq.verify_order_filled_fwd(price=bid_px)







    except Exception as e:
        logging.error('Error execution', exc_info=True)
    finally:
        pass
