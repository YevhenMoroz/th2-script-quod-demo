import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import wk1, wk2, spo, broken_2, broken_w1w2
from quod_qa.fx.fx_wrapper.CaseParamsBuy import CaseParamsBuy
from quod_qa.fx.fx_wrapper.CaseParamsSellEsp import CaseParamsSellEsp
from quod_qa.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from quod_qa.fx.fx_wrapper.FixClientBuy import FixClientBuy
from quod_qa.fx.fx_wrapper.FixClientSellEsp import FixClientSellEsp
from quod_qa.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq

client = 'Argentina1'
account = 'Argentina1_1'
symbol = "USD/SEK"
security_type_fwd = "FXFWD"
settle_type_broken = "B"
settle_date_br = broken_w1w2()
currency = "USD"
settle_currency = "SEK"
qty = '1000000'
side = "1"


def send_swap_and_filled(case_id):
    # Precondition
    params_broken = CaseParamsSellRfq(client, case_id, side=side, orderqty=qty,
                                      currency=currency, settlcurrency=settle_currency,
                                      settldate=settle_date_br, settltype=settle_type_broken, symbol=symbol,
                                      securitytype=security_type_fwd, securityid=symbol, account=account)
    # Step 1
    rfq = FixClientSellRfq(params_broken) \
        .send_request_for_quote()


def execute(report_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    try:
        send_swap_and_filled(case_id)
    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
