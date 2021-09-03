import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import spo, wk1, wk2
from quod_qa.common_tools import random_qty
from quod_qa.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from quod_qa.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq
from stubs import Stubs


def execute(report_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)

    client_tier = "Argentina1"
    account = "Argentina1_1"
    symbol = "GBP/USD"
    security_type_swap = "FXSWAP"
    security_type_fwd = "FXFWD"
    settle_date_spo = spo()
    settle_date_w1 = wk1()
    settle_date_w2 = wk2()
    settle_type_w1 = "W1"
    settle_type_w2 = "W2"
    currency = "GBP"
    settle_currency = "USD"

    side = "2"
    leg1_side = "1"
    leg2_side = "2"
    qty_1 = random_qty(1, 2, 7)

    try:
        # Step 1-2
        params_swap = CaseParamsSellRfq(client_tier, case_id, side=side, leg1_side=leg1_side, leg2_side=leg2_side,
                                        orderqty=qty_1, leg1_ordqty=qty_1, leg2_ordqty=qty_1,
                                        currency=currency, settlcurrency=settle_currency,
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
        checkpoint_response1 = Stubs.verifier.createCheckpoint(bca.create_checkpoint_request(case_id))
        checkpoint_id1 = checkpoint_response1.checkpoint
        rfq.send_new_order_multi_leg(price, side=side)
        rfq.verify_order_pending_swap(price)
        rfq.verify_order_filled_swap(price)
        rfq.verify_order_filled_swap_drop_copy(side=side, price=price, check_point=checkpoint_id1,
                                               spot_date=settle_date_spo)
    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
