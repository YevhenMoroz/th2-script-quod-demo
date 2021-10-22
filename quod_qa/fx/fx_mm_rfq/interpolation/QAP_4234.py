import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import wk1, wk2, spo
from quod_qa.fx.fx_wrapper.CaseParamsBuy import CaseParamsBuy
from quod_qa.fx.fx_wrapper.CaseParamsSellEsp import CaseParamsSellEsp
from quod_qa.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from quod_qa.fx.fx_wrapper.FixClientBuy import FixClientBuy
from quod_qa.fx.fx_wrapper.FixClientSellEsp import FixClientSellEsp
from quod_qa.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq

client = 'Argentina1'
account = 'Argentina1_1'
client_tier = 'Argentina'
symbol = "GBP/USD"
security_type_swap = "FXSWAP"
security_type_fwd = "FXFWD"
security_type_spo = "FXSPO"
settle_date_spo = spo()
settle_date_w1 = wk1()
settle_type_spo = "0"
settle_type_w1 = "W1"
currency = "GBP"
settle_currency = "USD"
qty = '1000000'
side = "1"
leg1_side = "2"
leg2_side = "1"
price_to_check = '0.000005'
leg_last_px_near = '1.196045'
leg_last_px_far = '1.19605'
last_spot_rate = '1.19603'


def send_swap_and_filled(case_id):

    params_swap = CaseParamsSellRfq(client, case_id, side=side, leg1_side=leg1_side, leg2_side=leg2_side,
                                    orderqty=qty, leg1_ordqty=qty, leg2_ordqty=qty,
                                    currency=currency, settlcurrency=settle_currency,
                                    leg1_settltype=settle_type_spo, leg2_settltype=settle_type_w1,
                                    settldate=settle_date_spo, leg1_settldate=settle_date_spo,
                                    leg2_settldate=settle_date_w1,
                                    symbol=symbol, leg1_symbol=symbol, leg2_symbol=symbol,
                                    securitytype=security_type_swap, leg1_securitytype=security_type_spo,
                                    leg2_securitytype=security_type_fwd,
                                    securityid=symbol, account=account)
    # Step 1
    rfq = FixClientSellRfq(params_swap)
    rfq.send_request_for_quote_swap()
    rfq.verify_quote_reject(text='no bid forward points for client tier `2600011\' on GBP/USD WK1 on QUODFX')


def execute(report_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    try:
        send_swap_and_filled(case_id)
    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
