import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import spo_ndf
from quod_qa.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from quod_qa.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq


def execute(report_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)

    client_tier = "Iridium1"
    symbol = "EUR/RUB"
    security_type_spo = "FXSPOT"
    settle_date = spo_ndf()
    settle_type = 0
    currency = "EUR"
    qty = "1000000"
    text = 'no available Bid depth on EUR/RUB SPO'

    try:
        # Step 1
        params = CaseParamsSellRfq(client_tier, case_id, orderqty=qty, symbol=symbol, side="1",
                                   securitytype=security_type_spo, settldate=settle_date, settltype=settle_type,
                                   currency=currency,
                                   account=client_tier)
        rfq = FixClientSellRfq(params)
        rfq.send_request_for_quote()
        # Step 2
        rfq.verify_quote_reject(text=text)

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
