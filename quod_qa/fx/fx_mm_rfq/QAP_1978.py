import logging
from datetime import datetime, timedelta
from custom import basic_custom_actions as bca, tenor_settlement_date as tsd
from pathlib import Path
from quod_qa.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from quod_qa.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True
client = 'Palladium1'
account = 'Palladium1_1'
settltype = 'W1'
symbol = 'EUR/USD'
currency = 'EUR'
securitytype = 'FXFWD'
securityidsource = '8'
side = '1'
orderqty = '1000000'
securityid = 'EUR/USD'
settldate = tsd.wk1()


def execute(report_id):
    try:
        case_name = Path(__file__).name[:-3]
        case_id = bca.create_event(case_name, report_id)

        # Step 1-2
        params = CaseParamsSellRfq(client, case_id, side=side, orderqty=orderqty, symbol=symbol,
                                   securitytype=securitytype,settldate=settldate, settltype=settltype, currency=currency,
                                   account=account)

        rfq = FixClientSellRfq(params)
        rfq.send_request_for_quote()
        rfq.verify_quote_pending()

        # Step 3-4
        offer_px = rfq.extruct_filed('OfferPx')
        last_spot_rate = rfq.extruct_filed('OfferSpotRate')
        last_frw_points = rfq.extruct_filed('OfferForwardPoints')
        rfq.send_new_order_single(offer_px)
        rfq.verify_order_pending()
        # rfq.verify_order_new()
        rfq.verify_order_filled_fwd(last_spot_rate=last_spot_rate,fwd_point=last_frw_points)







    except Exception as e:
        logging.error('Error execution', exc_info=True)
    finally:
        pass
