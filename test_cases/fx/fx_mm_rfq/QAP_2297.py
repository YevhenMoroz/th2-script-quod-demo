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
    currency = "GBP"
    settle_currency = "EUR"
    side = ""
    qty = "1000000"

    try:
        # Step 1-2
        params = CaseParamsSellRfq(client_tier, case_id, orderqty=qty, symbol=symbol,
                                   securitytype=security_type_spo, settldate=settle_date, settltype=settle_type,
                                   currency=currency, side=side, securityid=symbol, settlcurrency=settle_currency,
                                   account=account)
        rfq = FixClientSellRfq(params)
        rfq.send_request_for_quote()
        bid_fwd_pts = rfq.extract_filed("BidForwardPoints")
        rfq.verify_quote_pending(bid_forward_points=bid_fwd_pts)
        # Step 3
        price = rfq.extract_filed("BidPx")
        range_above = str(float(price) + 0.0001)
        range_bellow = str(float(price) - 0.0001)
        price_above = str(float(price) + 0.002)
        rfq.send_new_order_single(price_above, side="1")
        rfq.verify_order_rejected(text=f"order price is not ranging in [{range_bellow}, {range_above}]", side="1")
        rfq.send_new_order_single(price, side="1")
        rfq.verify_order_pending(side="1").verify_order_filled_fwd(side="1")

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
