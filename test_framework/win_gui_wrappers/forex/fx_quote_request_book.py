from test_framework.win_gui_wrappers.forex.fx_quote_book import FXQuoteBook
from stubs import Stubs


class FXQuoteRequestBook(FXQuoteBook):

    def __init__(self, case_id, session_id):
        super().__init__(case_id, session_id)
        self.set_quote_book_details()
        self.grpc_call = Stubs.win_act_aggregated_rates_service.getQuoteRequestBookDetails

    def check_quote_book_fields_list(self, expected_fields: dict, event_name=""):
        super().check_quote_book_fields_list(expected_fields, "Check Quote Request book")
