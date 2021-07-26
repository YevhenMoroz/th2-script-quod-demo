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
client = 'Palladium1'
account = 'Palladium1_1'
settltype = '0'
symbol = 'EUR/USD'
currency = 'EUR'
securitytype = 'FXSPOT'
securityidsource = '8'
side = '2'
orderqty = '1000000'
securityid = 'EUR/USD'
settldate = tsd.spo()
defaultmdsymbol_spo='EUR/USD:SPO:REG:HSBC'
bid_px_expected='1.19596'

def execute(report_id):
    try:
        case_name = Path(__file__).name[:-3]
        case_id = bca.create_event(case_name, report_id)
        #Precondition
        FixClientSellEsp(CaseParamsSellEsp(client, case_id, settltype=settltype, settldate=settldate, symbol=symbol, securitytype=securitytype)).\
            send_md_request().send_md_unsubscribe()
        FixClientBuy(CaseParamsBuy(case_id, defaultmdsymbol_spo, symbol, securitytype)).send_market_data_spot()

        # Step 1-2
        params = CaseParamsSellRfq(client, case_id, side=side, orderqty=orderqty, symbol=symbol,
                                   securitytype=securitytype,settldate=settldate, settltype=settltype, currency=currency,
                                   account=account)

        rfq = FixClientSellRfq(params)
        rfq.send_request_for_quote()
        rfq.verify_quote_pending(bid_size=orderqty, bid_px=bid_px_expected, bid_spot_rate=bid_px_expected)

        # Step 3-4
        bid_px = rfq.extract_filed('BidPx')
        rfq.send_new_order_single(bid_px)
        rfq.verify_order_pending()
        # rfq.verify_order_new()
        rfq.verify_order_filled(price=bid_px)







    except Exception as e:
        logging.error('Error execution', exc_info=True)
    finally:
        pass
