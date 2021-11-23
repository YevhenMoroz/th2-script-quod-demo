import logging
from custom import basic_custom_actions as bca
from pathlib import Path
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


def check_quote_request_b(base_request, service, case_id, status, qty):
    qrb = QuoteDetailsRequest(base=base_request)
    extraction_id = bca.client_orderid(4)
    qrb.set_extraction_id(extraction_id)
    qrb.set_filter(["Qty", qty])
    qrb_status = ExtractionDetail("quoteRequestBook.status", "Status")
    qrb.add_extraction_details([qrb_status])
    response = call(service.getQuoteRequestBookDetails, qrb.request())

    verifier = Verifier(case_id)
    verifier.set_event_name("Check QuoteRequest book")
    verifier.compare_values("Status", status, response[qrb_status.name])
    verifier.verify()


def check_quote_book(base_request, service, case_id, status, qty):
    qb = QuoteDetailsRequest(base=base_request)
    extraction_id = bca.client_orderid(4)
    qb.set_extraction_id(extraction_id)
    qb.set_filter(["OrdQty", qty])
    qb_quote_status = ExtractionDetail("quoteBook.quotestatus", "QuoteStatus")
    qb.add_extraction_details([qb_quote_status])
    response = call(service.getQuoteBookDetails, qb.request())

    verifier = Verifier(case_id)
    verifier.set_event_name("Check Quote book")
    verifier.compare_values("QuoteStatus", status, response[qb_quote_status.name])
    verifier.verify()


def execute(report_id, session_id):

    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    set_base(session_id, case_id)

    ar_service = Stubs.win_act_aggregated_rates_service
    case_base_request = get_base_request(session_id, case_id)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    client = 'Palladium1'
    settle_type = '0'
    symbol = 'EUR/USD'
    currency = 'EUR'
    security_type = 'FXSPOT'
    side = ''
    order_qty = random_qty(1, 5, 7)
    settle_date = spo()

    try:
        # Step 1-2
        params = CaseParamsSellRfq(client, case_id, side=side, orderqty=order_qty, symbol=symbol,
                                   securitytype=security_type,
                                   settldate=settle_date, settltype=settle_type, currency=currency)

        rfq = FixClientSellRfq(params). \
            send_request_for_quote(). \
            verify_quote_pending()
        rfq.send_quote_cancel()
        # Step 3
        # TODO Wait for new QRB check
        check_quote_request_b(case_base_request, ar_service, case_id, "Terminated", order_qty)
        # Step 4
        check_quote_book(case_base_request, ar_service, case_id, "Canceled", order_qty)

    except Exception:
        logging.error('Error execution', exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
