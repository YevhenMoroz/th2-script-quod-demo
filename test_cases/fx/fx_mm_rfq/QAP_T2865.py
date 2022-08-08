import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import spo
from custom.verifier import Verifier
from test_cases.fx.fx_wrapper.common_tools import random_qty
from test_cases.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from test_cases.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq
from stubs import Stubs
from win_gui_modules.order_book_wrappers import ExtractionDetail
from win_gui_modules.quote_wrappers import QuoteDetailsRequest
from win_gui_modules.utils import call, get_base_request
from win_gui_modules.wrappers import set_base


def check_quote_request_b(base_request, service, case_id, qty, status, quote_status):
    qrb = QuoteDetailsRequest(base=base_request)
    extraction_id = bca.client_orderid(4)
    qrb.set_extraction_id(extraction_id)
    qrb.set_filter(["Qty", qty])
    qrb_status = ExtractionDetail("quoteRequestBook.status", "Status")
    qrb_quote_status = ExtractionDetail("quoteRequestBook.quoteStatus", "QuoteStatus")
    qrb.add_extraction_details([qrb_status])
    qrb.add_child_extraction_details([qrb_quote_status])
    response = call(service.getQuoteRequestBookDetails, qrb.request())

    verifier = Verifier(case_id)
    verifier.set_event_name("Check QuoteRequest book")
    verifier.compare_values("Quote Request Status", status, response[qrb_status.name])
    verifier.compare_values("Quote Status", quote_status, response[qrb_quote_status.name])
    verifier.verify()


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    set_base(session_id, case_id)

    ar_service = Stubs.win_act_aggregated_rates_service
    case_base_request = get_base_request(session_id, case_id)

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
        # Step 3
        check_quote_request_b(case_base_request, ar_service, case_id, qty_1, "New", "Accepted")
        price = rfq.extract_filed("OfferPx")
        # Step 4
        rfq.send_new_order_single(price)
        rfq.verify_order_pending().verify_order_filled()
        check_quote_request_b(case_base_request, ar_service, case_id, qty_1, "Terminated", "Filled")

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
