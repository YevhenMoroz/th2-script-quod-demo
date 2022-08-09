import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import wk1
from test_cases.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from test_cases.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq
from win_gui_modules.wrappers import set_base


def execute(report_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)

    client_tier = "Iridium1"
    account = "Iridium1_1"
    symbol = "EUR/GBP"
    security_type_spo = "FXFWD"
    settle_date = wk1()
    settle_type = "W1"
    currency = "EUR"
    settle_currency = "GBP"
    side = "1"
    qty = "1000000"

    try:
        # Step 1-2
        params = CaseParamsSellRfq(client_tier, case_id, orderqty=qty, symbol=symbol,
                                   securitytype=security_type_spo, settldate=settle_date, settltype=settle_type,
                                   currency=currency, side=side, securityid=symbol, settlcurrency=settle_currency,
                                   account=account)
        rfq = FixClientSellRfq(params)
        rfq.send_request_for_quote()
        rfq.verify_quote_pending()
        # Step 3
        price = rfq.extract_filed("OfferPx")
        range_above = str(round(float(price) + 0.0001, 5))
        range_bellow = str(round(float(price) - 0.0001, 5))
        price_above = str(float(price) + 0.002)
        rfq.send_new_order_single(price_above)
        rfq.verify_order_rejected(text=f"order price is not ranging in [{range_bellow}, {range_above}]")
        rfq.send_new_order_single(price)
        rfq.verify_order_pending().verify_order_filled_fwd()

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
