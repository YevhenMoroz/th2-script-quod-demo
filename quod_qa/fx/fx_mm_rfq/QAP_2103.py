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
side = ''
leg1_side = '2'
leg2_side = '1'
orderqty = '1000000'
leg1_ordqty = '1000000'
leg2_ordqty = '1000000'
leg1_settltype = '0'
leg2_settltype = 'W1'

symbol = 'EUR/USD'
leg1_symbol = 'EUR/USD'
leg2_symbol = 'EUR/USD'
securityid = 'EUR/USD'
currency = 'USD'
settlcurrency = 'EUR'
securitytype_swap = 'FXSWAP'
leg1_securitytype = 'FXSPOT'
leg2_securitytype = 'FXFWD'
securityidsource = '8'
settldate = tsd.spo()
leg1_settldate = tsd.spo()
leg2_settldate = tsd.wk1()

defaultmdsymbol_spo = 'EUR/USD:SPO:REG:HSBC'
defaultmdsymbol_fwr = 'EUR/USD:FXF:WK1:HSBC'

offer_swap_p_ex = '0.0000101'
bid_swap_p_ex = '-0.0000097'
bid_px_expected = '-0.0000097'
offer_px_expected = '0.0000101'
leg_last_px_near = '1.19603'
leg_last_px_far = '1.1960203'


def execute(report_id):
    try:
        case_name = Path(__file__).name[:-3]
        case_id = bca.create_event(case_name, report_id)
        try:
            # Precondition
            md1 = FixClientSellEsp(
                CaseParamsSellEsp(client, case_id, settltype=leg1_settldate, settldate=settldate, symbol=symbol,
                                  securitytype=leg1_securitytype,
                                  securityid=securityid, currency=currency, settlcurrency=settlcurrency))
            md1.send_md_request().send_md_unsubscribe()
            FixClientBuy(CaseParamsBuy(case_id, defaultmdsymbol_spo, symbol, leg1_securitytype)).send_market_data_spot()
            FixClientBuy(CaseParamsBuy(case_id, defaultmdsymbol_fwr, symbol, leg2_securitytype)).send_market_data_fwd()

            params = CaseParamsSellRfq(client, case_id, side=side, leg1_side=leg1_side, leg2_side=leg2_side,
                                       orderqty=orderqty, leg1_ordqty=leg1_ordqty, leg2_ordqty=leg2_ordqty,
                                       currency=currency, settlcurrency=settlcurrency,
                                       leg1_settltype=leg1_settltype, leg2_settltype=leg2_settltype,
                                       settldate=settldate, leg1_settldate=leg1_settldate,
                                       leg2_settldate=leg2_settldate,
                                       symbol=symbol, leg1_symbol=leg1_symbol, leg2_symbol=leg2_symbol,
                                       securitytype=securitytype_swap, leg1_securitytype=leg1_securitytype,
                                       leg2_securitytype=leg2_securitytype,
                                       securityid=securityid, account=account)
            # Step 1
            rfq_swap = FixClientSellRfq(params)
            rfq_swap.send_request_for_quote_swap()
            rfq_swap.verify_quote_pending_swap(offer_size=orderqty, bid_size=orderqty,
                                               offer_swap_points=offer_swap_p_ex,
                                               bid_swap_points=bid_swap_p_ex, offer_px=offer_px_expected,
                                               bid_px=bid_px_expected, leg_of_fwd_p=offer_swap_p_ex,
                                               leg_bid_fwd_p=bid_swap_p_ex)
            price = rfq_swap.extract_filed('BidPx')
            spot_rate = rfq_swap.extract_filed('BidSpotRate')
            # Step 2,4
            # rfq_swap.case_params_sell_rfq.order_multi_leg_params['Currency']=settlcurrency
            rfq_swap.send_new_order_multi_leg(price)
            rfq_swap.verify_order_pending_swap(price)
            rfq_swap.verify_order_filled_swap(price, spot_rate=spot_rate, leg_last_px_near=leg_last_px_near,
                                              leg_last_px_far=leg_last_px_far)
        except Exception as e:
            try:
                md1.send_md_unsubscribe()
            except:
                bca.create_event('Unsubscribe failed', status='FAILED', parent_id=case_id)
            logging.error('Error execution', exc_info=True)
            bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
    except Exception as e:
        logging.error('Error execution', exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)

