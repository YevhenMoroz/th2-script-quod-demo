import logging
from pathlib import Path
from random import randint

from custom import basic_custom_actions as bca, verifier
from custom.tenor_settlement_date import spo
from custom.verifier import Verifier
from test_cases.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from test_cases.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq
from stubs import Stubs
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.order_book_wrappers import OrdersDetails, ExtractionDetail, OrderInfo, ExtractionAction
from win_gui_modules.utils import call, get_base_request
from win_gui_modules.wrappers import set_base


def check_order_book(base_request, act_ob, case_id, qty, notes):
    ob = OrdersDetails()
    extraction_id = bca.client_orderid(4)
    ob.set_default_params(base_request)
    ob.set_extraction_id(extraction_id)
    ob.set_filter(["Qty", qty])
    ob_notes = ExtractionDetail("orderBook.freeNotes", "FreeNotes")
    ob_status=ExtractionDetail("orderBook.sts", "Sts")
    ob.add_single_order_info(
        OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[ob_notes, ob_status])))
    response = call(act_ob.getOrdersDetails, ob.request())

    verifier = Verifier(case_id)
    verifier.set_event_name("Check Order book")
    verifier.compare_values("Status", "Rejected", response[ob_status.name])
    verifier.compare_values("Free notes", notes, response[ob_notes.name])
    verifier.verify()


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)

    set_base(session_id, case_id)

    ob_service = Stubs.win_act_order_book
    case_base_request = get_base_request(session_id, case_id)

    client_tier = "Iridium1"
    symbol = "GBP/USD"
    security_type_spo = "FXSPOT"
    settle_date = spo()
    settle_type = 0
    currency = "GBP"
    side = "1"
    notes = "not a live quote entry"
    qty = str(randint(1000000, 2000000))

    try:
        # Step 1
        params = CaseParamsSellRfq(client_tier, case_id, orderqty=qty, symbol=symbol, securityid=symbol,
                                   securitytype=security_type_spo, settldate=settle_date, settltype=settle_type,
                                   currency=currency, account=client_tier)
        rfq = FixClientSellRfq(params)
        rfq.send_request_for_quote()
        rfq.verify_quote_pending()

        quote_id = bca.client_orderid(20)
        offer_px = rfq.extract_filed("OfferPx")
        rfq.send_new_order_single(price=offer_px, side=side, quote_id=quote_id)
        rfq.verify_order_rejected(text=notes, side=side)
        check_order_book(case_base_request, ob_service, case_id, qty, notes)

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
