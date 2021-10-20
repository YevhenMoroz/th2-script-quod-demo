from quod_qa.win_gui_wrappers.forex.fx_quote_book import FXQuoteBook
from stubs import Stubs
from win_gui_modules.quote_wrappers import QuoteDetailsRequest


class FXQuoteRequestBook(FXQuoteBook):

    def __init__(self, case_id, base_request):
        super().__init__(case_id, base_request)
        self.set_quote_book_details()
        self.grpc_call = Stubs.win_act_aggregated_rates_service.getQuoteRequestBookDetails

    def check_quote_book_fields_list(self, expected_fields: dict, event_name=""):
        super().check_quote_book_fields_list(expected_fields, "Check Quote Request book")
