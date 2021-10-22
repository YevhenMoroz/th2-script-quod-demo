import logging
from pathlib import Path
from custom import basic_custom_actions as bca
from quod_qa.win_gui_wrappers.columns_names import OrderBookColumns
from quod_qa.win_gui_wrappers.forex.fx_order_book import FXOrderBook
from quod_qa.win_gui_wrappers.forex.fx_quote_book import FXQuoteBook
from quod_qa.win_gui_wrappers.forex.fx_quote_request_book import FXQuoteRequestBook
from win_gui_modules.utils import get_base_request
from win_gui_modules.wrappers import set_base


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)

    set_base(session_id, case_id)
    case_base_request = get_base_request(session_id, case_id)

    try:

        order_book = FXOrderBook(case_id, case_base_request)
        order_book.set_filter([OrderBookColumns.qty.value, "1000000"]).check_order_fields_list(
            {"Sts": "1", "ExecSts": "2"})
        order_book.cancel_order()

        quote_book = FXQuoteBook(case_id, case_base_request)
        quote_book.set_filter(["BidSize", "2000000"]).check_quote_book_fields_list({"BidPx": "1.181161"})

        quote_request_book = FXQuoteRequestBook(case_id, case_base_request)
        quote_request_book.set_filter(["Qty", "2000000"]).check_quote_book_fields_list(
            {"User": "ostronov", "Status": "Terminated"})

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
