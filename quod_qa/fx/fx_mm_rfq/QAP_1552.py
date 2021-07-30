import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import spo
from quod_qa.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from quod_qa.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq


def execute(report_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)

    client_tier = "Iridium1"
    account = "Iridium1_1"
    qty_1 = 1000000
    symbol = "GBP/USD"
    security_type_spo = "FXSPOT"
    settle_date_spo = spo()
    currency = "GBP"
    settle_type = '0'
    side = "1"
    leg1_side = "1"
    leg2_side = "2"

    try:
        # Step 1
        params_spot = CaseParamsSellRfq(client_tier, case_id, orderqty=qty_1, symbol=symbol,
                                        settldate=settle_date_spo,
                                        settltype=settle_type, securitytype=security_type_spo,
                                        currency=currency,
                                        account=client_tier)

        rfq = FixClientSellRfq(params_spot)
        rfq.send_request_for_quote().verify_quote_pending()
        offer_px = rfq.extract_filed('OfferPx')
        rfq.send_new_order_single(offer_px)
        rfq.verify_order_pending()
        rfq.verify_order_filled()
        # Step 2

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
