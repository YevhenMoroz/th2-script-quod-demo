import logging
from datetime import date
from pathlib import Path
from random import randint

from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import wk1, wk2
from quod_qa.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from quod_qa.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq


def execute(report_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)

    client_tier = "Iridium1"
    account = "Iridium1_1"
    qty = str(randint(1000000, 2000000))
    symbol = "GBP/USD"
    security_type_swap = "FXSWAP"
    security_type = "FXFWD"
    settle_date = wk1()
    leg2_settle_date = wk2()
    settle_type_leg1 = "W1"
    settle_type_leg2 = "W2"
    currency = "GBP"
    settle_currency = "USD"

    side = ""
    leg1_side = "1"
    leg2_side = "2"

    try:
        # Step 1
        params = CaseParamsSellRfq(client_tier, case_id, side=side, leg1_side=leg1_side, leg2_side=leg2_side,
                                   orderqty=qty, leg1_ordqty=qty, leg2_ordqty=qty,
                                   currency=currency, settlcurrency=settle_currency,
                                   leg1_settltype=settle_type_leg1, leg2_settltype=settle_type_leg2,
                                   settldate=settle_date, leg1_settldate=settle_date, leg2_settldate=leg2_settle_date,
                                   symbol=symbol, leg1_symbol=symbol, leg2_symbol=symbol,
                                   securitytype=security_type_swap, leg1_securitytype=security_type,
                                   leg2_securitytype=security_type,
                                   securityid=symbol, account=account)

        rfq = FixClientSellRfq(params)
        rfq.send_request_for_quote_swap()
        # Step 3
        rfq.send_quote_cancel()

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
