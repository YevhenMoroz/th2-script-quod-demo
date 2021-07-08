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
leg1_side = '1'
leg2_side = '2'
orderqty = '1000000'
leg1_ordqty = '1000000'
leg2_ordqty = '1000000'
leg1_settltype = '0'
leg2_settltype = 'W1'

symbol = 'EUR/USD'
leg1_symbol = 'EUR/USD'
leg2_symbol = 'EUR/USD'
securityid = 'EUR/USD'
currency = 'EUR'
settlcurrency = 'USD'
securitytype_swap = 'FXSWAP'
leg1_securitytype = 'FXSPOT'
leg2_securitytype = 'FXFWD'
securityidsource = '8'
settldate = tsd.spo()
leg1_settldate = tsd.spo()
leg2_settldate = tsd.wk1()



defaultmdsymbol_spo='GBP/USD:SPO:REG:HSBC'
defaultmdsymbol_fwr='GBP/USD:FXF:WK3:HSBC'
bid_px_expected='1.1959203'
offer_px_expected='1.1961401'
bid_forward_points='-0.0000497'
offer_forward_points='0.0000501'
bid_spot_rate='1.19597'
offer_spot_rate='1.19609'



def execute(report_id):
    try:
        case_name = Path(__file__).name[:-3]
        case_id = bca.create_event(case_name, report_id)
        #Precondition
        # FixClientSellEsp(CaseParamsSellEsp(client, case_id, settltype=settltype, settldate=settldate, symbol=symbol, securitytype=securitytype_fwd,
        #                                    securityid=securityid,currency=currency, settlcurrency=settlcurrency)).\
        #     send_md_request().send_md_unsubscribe()
        # FixClientBuy(CaseParamsBuy(case_id, defaultmdsymbol_spo, symbol, securitytype_spo)).send_market_data_spot()
        # FixClientBuy(CaseParamsBuy(case_id, defaultmdsymbol_fwr, symbol, securitytype_fwd)).send_market_data_fwd()

        # Step 1-2
        params = CaseParamsSellRfq(client, case_id, side=side, leg1_side=leg1_side, leg2_side=leg2_side,
                                   orderqty=orderqty,leg1_ordqty=leg1_ordqty,leg2_ordqty=leg2_ordqty,
                                   currency=currency,settlcurrency=settlcurrency,
                                   leg1_settltype=leg1_settltype,leg2_settltype=leg2_settltype,
                                   settldate=settldate, leg1_settldate=leg1_settldate, leg2_settldate=leg2_settldate,
                                   symbol=symbol, leg1_symbol=leg1_symbol, leg2_symbol=leg2_symbol,
                                   securitytype=securitytype_swap, leg1_securitytype=leg1_securitytype, leg2_securitytype=leg2_securitytype,
                                   securityid=securityid, account=account)

        rfq_swap = FixClientSellRfq(params)
        rfq_swap.send_request_for_quote_swap()
        rfq_swap.verify_quote_pending_swap()
        rfq_swap.send_new_order_multi_leg()







    except Exception as e:
        logging.error('Error execution', exc_info=True)
    finally:
        pass
