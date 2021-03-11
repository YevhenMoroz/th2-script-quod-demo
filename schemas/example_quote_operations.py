import logging
from datetime import datetime

from custom import basic_custom_actions as bca
from stubs import Stubs

from win_gui_modules.quote_wrappers import QuoteDetailsRequest
from win_gui_modules.order_book_wrappers import ExtractionDetail
from win_gui_modules.utils import set_session_id, prepare_fe_2, close_fe_2, get_base_request, call
from win_gui_modules.wrappers import set_base


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# IMPORTANT: workspace must have only one tab!

def execute(report_id):

    # Store case start time
    seconds, nanos = bca.timestamps()
    case_name = "quote operations example"
    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)
    session_id = set_session_id()
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    ar_service = Stubs.win_act_aggregated_rates_service

    if not Stubs.frontend_is_open:
        prepare_fe_2(case_id, session_id)

    try:
        quote_request_book = QuoteDetailsRequest(base=base_request)
        quote_request_book.set_extraction_id("TestExtractionId0")
        quote_request_book.set_filter(["Id", "1234567890"])
        quote_request_book_ext_field = ExtractionDetail("quoteRequestBook.id", "Id")
        quote_request_book.add_extraction_detail(quote_request_book_ext_field)
        # quote_request_book.add_extraction_details([quote_request_book_ext_field])
        call(ar_service.getQuoteRequestBookDetails, quote_request_book.request())

        # check quote book
        quote_book = QuoteDetailsRequest(base=base_request)
        quote_book.set_extraction_id("TestExtractionId1")
        quote_book.set_filter(["Id", "1234567890"])
        quote_book_ext_field = ExtractionDetail("quoteBook.id", "Id")
        quote_book.add_extraction_detail(quote_book_ext_field)
        # quote_request_book.add_extraction_details([quote_book_ext_field])
        call(ar_service.getQuoteBookDetails, quote_book.request())

    except Exception as e:
        logging.error("Error execution", exc_info=True)

    close_fe_2(case_id, session_id)
    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
