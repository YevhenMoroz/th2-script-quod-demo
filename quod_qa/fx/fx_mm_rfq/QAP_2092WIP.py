import logging
import time
from datetime import date
from pathlib import Path
from random import randint

from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import wk1, spo
from custom.verifier import Verifier
from quod_qa.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from quod_qa.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq
from stubs import Stubs
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.utils import call, get_base_request
from win_gui_modules.wrappers import set_base


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)

    set_base(session_id, case_id)

    ob_service = Stubs.win_act_order_book

    case_base_request = get_base_request(session_id, case_id)
    base_details = BaseTileDetails(base=case_base_request)

    client_tier = "Iridium1"
    symbol = "GBP/USD"
    security_type_spo = "FXSPOT"
    settle_date = spo()
    settle_type = 0
    currency = "GBP"
    side="1"
    qty = str(randint(1000000, 2000000))

    try:
        # Step 1
        # Step 2
        params = CaseParamsSellRfq(client_tier, case_id, orderqty=qty, symbol=symbol,
                                   securitytype=security_type_spo, settldate=settle_date, settltype=settle_type,
                                   currency=currency,
                                   account=client_tier)
        rfq = FixClientSellRfq(params)
        rfq.send_request_for_quote()
        rfq.verify_quote_pending()

        quote_id = bca.client_orderid(20)
        offer_px = rfq.extract_filed("OfferPx")
        rfq.send_new_order_single(price=offer_px, side=side, quote_id=quote_id)
        rfq.verify_order_rejected()
        # rfq.verify_order_filled()

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
