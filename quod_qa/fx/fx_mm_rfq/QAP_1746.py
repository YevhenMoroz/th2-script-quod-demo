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
settltype = 'W1'
side ='1'
symbol = 'EUR/USD'
currency = 'EUR'
securitytype_fwd = 'FXFWD'
securitytype_spo = 'FXSPOT'
securityidsource = '8'
orderqty = '1000000'
securityid = 'EUR/USD'
settldate = tsd.wk1()
settldate_spo = tsd.spo()
defaultmdsymbol_spo='EUR/USD:SPO:REG:HSBC'
defaultmdsymbol_fwr='EUR/USD:FXF:WK1:HSBC'



def execute(report_id):
    try:
        case_name = Path(__file__).name[:-3]
        case_id = bca.create_event(case_name, report_id)
        #Precondition
        FixClientSellEsp(CaseParamsSellEsp(client, case_id, settltype=settltype, settldate=settldate, symbol=symbol, securitytype=securitytype_spo)).\
            send_md_request().send_md_unsubscribe()
        FixClientBuy(CaseParamsBuy(case_id, defaultmdsymbol_spo, symbol, securitytype_spo)).send_market_data_spot()
        FixClientBuy(CaseParamsBuy(case_id, defaultmdsymbol_fwr, symbol, securitytype_fwd)).send_market_data_fwd()

        # Step 1-2
        params = CaseParamsSellRfq(client, case_id, orderqty=orderqty, symbol=symbol,
                                   securitytype=securitytype_fwd,settldate=settldate, settltype=settltype, currency=currency,
                                   account=account)

        rfq = FixClientSellRfq(params)
        rfq.send_request_for_quote()
        bid_fwd_points='-0.0000097'
        of_fwd_points='0.0000101'
        rfq.verify_quote_pending(offer_forward_points=of_fwd_points, bid_forward_points=bid_fwd_points)

        # Step 3-4
        offer_px = rfq.extract_filed('OfferPx')
        last_spot_rate = rfq.extract_filed('OfferSpotRate')
        last_frw_points = rfq.extract_filed('OfferForwardPoints')
        rfq.send_new_order_single(offer_px, side)
        rfq.verify_order_pending(side=side)
        # rfq.verify_order_new()
        rfq.verify_order_filled_fwd(last_spot_rate=last_spot_rate,fwd_point=last_frw_points,side=side)







    except Exception as e:
        logging.error('Error execution', exc_info=True)
    finally:
        pass
