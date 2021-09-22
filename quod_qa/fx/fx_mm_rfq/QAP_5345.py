import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import spo, wk1, wk1_ndf, wk2_ndf
from quod_qa.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from quod_qa.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq


def execute(report_id):
    case_name = Path(__file__).name[:-3]

    client_tier = "Iridium1"
    account = "Iridium1_1"
    order_qty = "1000000"
    symbol = "USD/PHP"
    security_type = "FXNDS"
    security_type_leg = "FXNDF"
    settle_type_w1 = "W1"
    settle_type_w2 = "W2"
    currency = "USD"
    settle_currency = "PHP"
    side = "1"
    leg1_side = "2"
    leg2_side = "1"
    settle_date_leg1 = wk1_ndf()
    settle_date_leg2 = wk2_ndf()
    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)

    try:
        params_swap = CaseParamsSellRfq(client_tier, case_id, side=side, leg1_side=leg1_side, leg2_side=leg2_side,
                                        orderqty=order_qty, leg1_ordqty=order_qty, leg2_ordqty=order_qty,
                                        currency=currency, settlcurrency=settle_currency,
                                        leg1_settltype=settle_type_w1, leg2_settltype=settle_type_w2,
                                        settldate=settle_date_leg1, leg1_settldate=settle_date_leg1,
                                        leg2_settldate=settle_date_leg2,
                                        symbol=symbol, leg1_symbol=symbol, leg2_symbol=symbol,
                                        securitytype=security_type, leg1_securitytype=security_type_leg,
                                        leg2_securitytype=security_type_leg,
                                        securityid=symbol, account=account)
        rfq = FixClientSellRfq(params_swap)
        rfq.send_request_for_quote_swap()
        rfq.verify_quote_pending_swap()
        price = rfq.extract_filed("BidPx")
        rfq.send_new_order_multi_leg(price, side=side)
        rfq.verify_order_pending_swap(price)
        rfq.verify_order_filled_swap()
    # Step 2

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
