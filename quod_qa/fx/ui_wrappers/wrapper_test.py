import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import wk1, wk2, spo, broken_2, wk3, broken_w1w2
from quod_qa.fx.fx_wrapper.common_tools import random_qty
from quod_qa.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from quod_qa.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq
from quod_qa.fx.ui_wrappers.forex_order_book import FxOrderBook
from quod_qa.win_gui_wrappers.base_order_book import BaseOrderBook
from quod_qa.win_gui_wrappers.forex.fx_order_book import FXOrderBook
from win_gui_modules.utils import get_base_request
from win_gui_modules.wrappers import set_base

client_tier = "Iridium1"
account = "Iridium1_1"
symbol = "EUR/USD"
security_type_spo = "FXSPOT"
settle_date_spo = spo()
settle_type_spo = "0"
currency = "EUR"
settle_currency = "USD"
side = "1"


def send_rfq_and_filled_order(case_id, qty_1):
    params_spot = CaseParamsSellRfq(client_tier, case_id, orderqty=qty_1, symbol=symbol,
                                    securitytype=security_type_spo, settldate=settle_date_spo,
                                    settltype=settle_type_spo, securityid=symbol,
                                    currency=currency, side=side,
                                    account=account)

    rfq = FixClientSellRfq(params_spot)
    rfq.send_request_for_quote()
    rfq.verify_quote_pending()
    price = rfq.extract_filed("OfferPx")
    rfq.send_new_order_single(price)
    rfq.verify_order_pending().verify_order_filled()


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)

    set_base(session_id, case_id)
    case_base_request = get_base_request(session_id, case_id)

    qty = random_qty(1, 3, 7)

    try:
        # Step 1
        # send_rfq_and_filled_order(case_id, qty)

        order_book = FXOrderBook(case_id, case_base_request)
        order_book.set_filter(["Qty", "1000000"]).check_order_filled("Terminated", "Filled")

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
