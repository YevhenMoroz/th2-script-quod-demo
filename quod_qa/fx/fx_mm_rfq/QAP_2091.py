import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import spo, wk1, wk1_ndf
from quod_qa.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from quod_qa.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq


def execute(report_id):
    case_name = Path(__file__).name[:-3]

    client_tier = "Iridium1"
    account = "Iridium1_1"
    settle_type = "6"
    symbol = "USD/PHP"
    currency = "USD"
    settle_currency="PHP"
    security_type = "FXNDF"
    side = "1"
    order_qty = "1000000"
    settle_date = wk1_ndf()

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)

    try:
        rfq = FixClientSellRfq(
            CaseParamsSellRfq(client_tier, case_id, side=side, orderqty=order_qty, symbol=symbol,
                              securitytype=security_type, securityid=symbol,
                              settldate=settle_date, settlcurrency=settle_currency,
                              settltype=settle_type, currency=currency, account=account)). \
            send_request_for_quote(). \
            verify_quote_pending()
        price = rfq.extract_filed("OfferPx")
        rfq.send_new_order_single(price). \
            verify_order_pending(). \
            verify_order_filled_fwd()
    # Step 2

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
