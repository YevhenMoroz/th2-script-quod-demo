import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import wk1, wk2, spo, broken_2, wk3, broken_1, broken_w1w2
from custom.verifier import Verifier
from quod_qa.common_tools import random_qty
from quod_qa.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from quod_qa.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq
from win_gui_modules.wrappers import set_base

client = 'Argentina1'
account = 'Argentina1_1'
client_tier = 'Argentina'
symbol = "EUR/GBP"
security_type_swap = "FXSWAP"
security_type_fwd = "FXFWD"
security_type_spo = "FXSPOT"
settle_date_spo = spo()
settle_date_w1 = wk1()
settle_date_w2 = wk2()
settle_date_w3 = wk3()
settle_date_br = broken_2()
settle_date_br_2=broken_w1w2()
settle_type_spo = "0"
settle_type_w1 = "W1"
settle_type_w2 = "W2"
settle_type_w3 = "W3"
settle_type_broken = "B"
currency = "EUR"
settle_currency = "GBP"
qty = '1000000'
side = "1"
leg1_side = "2"
leg2_side = "1"


def send_swap_and_filled(case_id, qty_1, qty_2):
    params_swap = CaseParamsSellRfq(client, case_id, side=2, leg1_side=1, leg2_side=2,
                                    orderqty=qty_1, leg1_ordqty=qty_1, leg2_ordqty=qty_2,
                                    currency=settle_currency, settlcurrency=currency,
                                    leg1_settltype=settle_type_broken, leg2_settltype=settle_type_broken,
                                    settldate=settle_date_br, leg1_settldate=settle_date_br,
                                    leg2_settldate=settle_date_br_2,
                                    symbol=symbol, leg1_symbol=symbol, leg2_symbol=symbol,
                                    securitytype=security_type_swap, leg1_securitytype=security_type_fwd,
                                    leg2_securitytype=security_type_fwd,
                                    securityid=symbol, account=account)
    rfq = FixClientSellRfq(params_swap)
    rfq.send_request_for_quote_swap()
    rfq.verify_quote_pending_swap()
    price = rfq.extract_filed("BidPx")
    size = rfq.extract_filed('BidSize')
    print(size)
    rfq.send_new_order_multi_leg(price, side=2)
    rfq.verify_order_pending_swap(price=price, side=2)
    rfq.verify_order_filled_swap(price=price)


def execute(report_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    try:
        send_swap_and_filled(case_id, qty, qty)
    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
