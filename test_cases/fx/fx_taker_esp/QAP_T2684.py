import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import spo
from test_cases.fx.fx_wrapper.common_tools import random_qty
from test_cases.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from test_cases.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq
from stubs import Stubs


def execute(report_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)

    client_tier = "Iridium1"
    account = "Iridium1_1"
    symbol = "EUR/USD"
    security_type_spo = "FXSPOT"
    settle_date_spo = spo()
    settle_type_spo = "0"
    currency = "EUR"
    settle_currency = "USD"
    qty_1 = random_qty(1, 2, 7)

    side = "1"

    try:
        # Step 1-2
        params_spot = CaseParamsSellRfq(client_tier, case_id, orderqty=qty_1, symbol=symbol,
                                        securitytype=security_type_spo, settldate=settle_date_spo,
                                        settltype=settle_type_spo, securityid=symbol, settlcurrency=settle_currency,
                                        currency=currency, side=side,
                                        account=account)

        rfq = FixClientSellRfq(params_spot)
        rfq.send_request_for_quote()
        rfq.verify_quote_pending()
        price = rfq.extract_filed("OfferPx")
        checkpoint_response = Stubs.verifier.createCheckpoint(bca.create_checkpoint_request(case_id))
        checkpoint_id = checkpoint_response.checkpoint
        rfq.send_new_order_single(price)

        rfq.verify_order_pending().verify_order_filled()
        rfq.verify_drop_copy(checkpoint_id)
    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
