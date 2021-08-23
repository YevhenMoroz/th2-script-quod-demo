from th2_grpc_act_gui_quod import ar_operations_pb2
from th2_grpc_act_gui_quod.common_pb2 import EmptyRequest
from win_gui_modules.order_book_wrappers import ExtractionDetail


class QuoteDetailsRequest:
    def __init__(self, base: EmptyRequest = None):
        if base is not None:
            self._request = ar_operations_pb2.QuoteDetailsRequest(base=base)
        else:
            self._request = ar_operations_pb2.QuoteDetailsRequest()

    def set_filter(self, filter_list: list):
        length = len(filter_list)
        i = 0
        while i < length:
            self._request.filter[filter_list[i]] = filter_list[i + 1]
            i += 2

    def set_default_params(self, base_request):
        self._request.base.CopyFrom(base_request)

    def add_extraction_detail(self, detail: ExtractionDetail):
        var = self._request.extractionFields.add()
        var.name = detail.name
        var.colName = detail.column_name

    def add_extraction_detail(self, detail: ExtractionDetail):
        var = self._request.extractionFields.add()
        var.name = detail.name
        var.colName = detail.column_name

    def add_child_extraction_detail(self, detail: ExtractionDetail):
        var = self._request.childExtractionFields.add()
        var.name = detail.name
        var.colName = detail.column_name

    def add_extraction_details(self, details: list):
        for detail in details:
            self.add_extraction_detail(detail)

    def add_child_extraction_details(self, details: list):
        for detail in details:
            self.add_child_extraction_detail(detail)

    def set_extraction_id(self, extraction_id: str):
        self._request.extractionId = extraction_id

    def set_row_number(self, row_number: int):
        self._request.rowNumber = row_number

    def request(self) -> ar_operations_pb2.QuoteDetailsRequest:
        return self._request
