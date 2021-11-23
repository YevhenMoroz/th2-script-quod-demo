import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import wk1, wk3
from quod_qa.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from quod_qa.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq

client_tier = "Iridium1"
account = "Iridium1_1"

symbol = "GBP/USD"
security_type_fwd = "FXFWD"
settle_date_w1 = wk3()
settle_type_w1 = "W3"
currency = "GBP"
settle_currency = "USD"

side = "1"


def send_rfq_and_check_reject(case_id, qty_1):
    params_spot = CaseParamsSellRfq(client_tier, case_id, orderqty=qty_1, symbol=symbol,
                                    securitytype=security_type_fwd, settldate=settle_date_w1,
                                    settltype=settle_type_w1, securityid=symbol,
                                    currency=currency, side=side, settlcurrency=settle_currency,
                                    account=account)

    rfq = FixClientSellRfq(params_spot)
    rfq.send_request_for_quote()
    text = "failed to get forward points through RFQ"
    rfq.verify_quote_reject(text=text)


def execute(report_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)

    try:
        # Step 1
        send_rfq_and_check_reject(case_id, "1000000")

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
