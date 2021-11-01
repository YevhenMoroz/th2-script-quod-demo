from quod_qa.win_gui_wrappers.base_window import BaseWindow
from win_gui_modules.order_book_wrappers import ExtractionDetail
from win_gui_modules.utils import call


class BaseQuoteBook(BaseWindow):
    def __init__(self, case_id, base_request):
        super().__init__(case_id, base_request)
        self.quote_book_details = None
        self.grpc_call = None

    # region Common func
    def set_quote_book_details(self):
        self.quote_book_details.set_extraction_id(self.extraction_id)

    def set_filter(self, filter_list: list):
        """
        Receives list as an argument, where the elements
        are in order - key, value, key, value, ...
        For example ["Qty", "123456", "Owner", "QA1", etc]
        """
        self.quote_book_details.set_filter(filter_list)
        return self

    # endregion

    # region Get
    def extract_field(self, column_name: str) -> str:
        field = ExtractionDetail("quoteBook." + column_name, column_name)
        self.quote_book_details.add_extraction_detail(field)
        response = call(self.grpc_call, self.quote_book_details.request())
        return response[field.name]

    def extract_fields_list(self, list_fields: dict) -> dict:
        """
        Receives dict as an argument, where the key is column name what
        we extract from GUI and return new dict where
        key = key and value is extracted field from FE
        """
        list_of_fields = []
        for field in list_fields.items():
            key = list(field)[0]
            field = ExtractionDetail(key, key)
            list_of_fields.append(field)
        self.quote_book_details.add_extraction_details(list_of_fields)
        response = call(self.grpc_call, self.quote_book_details.request())
        return response

    # endregion

    # region Check
    def check_quote_book_fields_list(self, expected_fields: dict, event_name="Check Quote Book"):
        """
        Receives dict as an argument, where the key is column name what
        we extract from GUI and value is expected result
        For example {"Sts": "Terminated", "Owner": "QA1", etc}
        """
        actual_list = self.extract_fields_list(expected_fields)
        for items in expected_fields.items():
            key = list(items)[0]
            value = list(items)[1]
            self.verifier.set_event_name(event_name)
            self.verifier.compare_values(key, value, actual_list[key])
        self.verifier.verify()
    # endregion

    # region Actions
    # TODO Add action for QuoteBook
    # endregion
