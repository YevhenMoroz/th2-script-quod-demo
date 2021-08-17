import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import spo
from quod_qa.common_tools import random_qty
from quod_qa.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from quod_qa.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id):
    # region Preparation
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)

    client_tier = "Iridium1"
    account = "Iridium1_1"

    symbol = "GBP/USD"
    security_type_spo = "FXSPOT"
    settle_date_spo = spo()

    settle_type_spo = "0"
    currency = "GBP"
    qty_1 = random_qty(1, 10, 7)
    side = "1"

    # endregion
    try:
        # Step 1
        params = CaseParamsSellRfq(client_tier, case_id, orderqty=qty_1, symbol=symbol,
                                   securitytype=security_type_spo, settldate=settle_date_spo,
                                   settltype=settle_type_spo, securityid=symbol,
                                   currency=currency, side=side, account=account)

        rfq = FixClientSellRfq(params)
        rfq.send_request_for_quote()
        rfq.verify_quote_pending()
        price = rfq.extract_filed("OfferPx")
        price_bellow = str(round(float(price) - 0.0001, 5))
        # Step 2
        rfq.send_new_order_single(price_bellow)
        # Step 3
        text = f"order price ({price_bellow}) lower than offer ({price})"
        rfq.verify_order_rejected(text=text)
        # Step 4
        params_new = CaseParamsSellRfq(client_tier, case_id, orderqty=qty_1, symbol=symbol,
                                       securitytype=security_type_spo, settldate=settle_date_spo,
                                       settltype=settle_type_spo, securityid=symbol,
                                       currency=currency, side=side,
                                       account=client_tier)

        rfq_new = FixClientSellRfq(params_new)
        rfq_new.send_request_for_quote()
        rfq_new.verify_quote_pending()
        new_price = rfq.extract_filed("OfferPx")
        price_above = str(round(float(new_price) + 0.003, 5))
        # Step 5
        rfq.send_new_order_single(price_above)
        rfq.verify_order_pending()
        rfq.verify_order_filled(price_above)
    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
