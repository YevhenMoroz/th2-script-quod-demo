from quod_qa.win_gui_wrappers.base_quote_book import BaseQuoteBook
from quod_qa.win_gui_wrappers.base_window import BaseWindow
from stubs import Stubs
from win_gui_modules.order_book_wrappers import ExtractionDetail
from win_gui_modules.quote_wrappers import QuoteDetailsRequest
from win_gui_modules.utils import call


class FXQuoteBook(BaseQuoteBook):
    def __init__(self, case_id, session_id):
        super().__init__(case_id, session_id)
        self.quote_book_details = QuoteDetailsRequest(base=self.base_request)
        self.set_quote_book_details()
        self.grpc_call = Stubs.win_act_aggregated_rates_service.getQuoteBookDetails
