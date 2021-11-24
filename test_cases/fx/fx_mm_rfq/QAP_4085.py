import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import wk1, wk2
from test_cases.fx.fx_wrapper.common_tools import random_qty
from test_cases.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from test_cases.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq


def execute(report_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)

    qty_1 = random_qty(1, 3, 7)
    qty_2 = random_qty(1, 10, 7)
    client_tier = "Iridium1"
    account = "Iridium1_1"

    symbol = "GBP/USD"
    security_type_swap = "FXSWAP"
    security_type_fwd = "FXFWD"
    settle_date_w1 = wk1()
    settle_date_w2 = wk2()
    settle_type_w1 = "W1"
    settle_type_w2 = "W2"
    currency = "GBP"
    settle_currency = "USD"

    side = "2"
    leg1_side = "1"
    leg2_side = "2"

    try:
        params_swap = CaseParamsSellRfq(client_tier, case_id, side=side, leg1_side=leg1_side, leg2_side=leg2_side,
                                        orderqty=qty_1, leg1_ordqty=qty_1, leg2_ordqty=qty_2,
                                        currency=settle_currency, settlcurrency=currency,
                                        leg1_settltype=settle_type_w1, leg2_settltype=settle_type_w2,
                                        settldate=settle_date_w1, leg1_settldate=settle_date_w1,
                                        leg2_settldate=settle_date_w2,
                                        symbol=symbol, leg1_symbol=symbol, leg2_symbol=symbol,
                                        securitytype=security_type_swap, leg1_securitytype=security_type_fwd,
                                        leg2_securitytype=security_type_fwd,
                                        securityid=symbol, account=account)

        rfq = FixClientSellRfq(params_swap)
        rfq.send_request_for_quote_swap()
        rfq.verify_quote_pending_swap()
        price = rfq.extract_filed("BidPx")
        rfq.send_new_order_multi_leg(price, side=1)
        rfq.verify_order_rejected(text="order side (B) doesn't match quote", side=1, price=price)

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
