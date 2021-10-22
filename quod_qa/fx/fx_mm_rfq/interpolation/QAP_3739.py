import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import broken_2
from quod_qa.fx.fx_wrapper.common_tools import random_qty
from quod_qa.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from quod_qa.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq

client = 'Argentina1'
account = 'Argentina1_1'
symbol = "EUR/GBP"
security_type_fwd = "FXFWD"
settle_date_br = broken_2()
settle_type_broken = "B"
currency = "EUR"
settle_currency = "GBP"

side = "1"


def send_rfq_and_filled_order_broken(case_id, qty_1):
    params_spot = CaseParamsSellRfq(client, case_id, orderqty=qty_1, symbol=symbol,
                                    securitytype=security_type_fwd, settldate=settle_date_br,
                                    settltype=settle_type_broken, currency=currency, settlcurrency=settle_currency,
                                    side=side, account=account, securityid=symbol)
    rfq = FixClientSellRfq(params_spot)
    rfq.send_request_for_quote()
    rfq.verify_quote_pending()
    price = rfq.extract_filed("OfferPx")
    rfq.send_new_order_single(price)
    rfq.verify_order_pending().\
        verify_order_filled_fwd()


def execute(report_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    qty_1 = random_qty(1, 3, 7)
    try:
        send_rfq_and_filled_order_broken(case_id, qty_1)
    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
