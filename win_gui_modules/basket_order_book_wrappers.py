from th2_grpc_act_gui_quod import basket_book_pb2


class ExtractOrderDataDetails:
    def __init__(self):
        self._request = basket_book_pb2.ExtractOrderDataDetails()

    def set_default_params(self, base_request):
        self._request.base.CopyFrom(base_request)

    def set_filter(self, filter: dict):
        self._request.filter.update(filter)

    def set_column_names(self, column_names: list):
        for name in column_names:
            self._request.columnNames.append(name)

    def build(self):
        return self._request


class ExtractChildOrderDataDetails:
    def __init__(self, extract_order_data: ExtractOrderDataDetails = None, rows_number: int = None):
        self._request = basket_book_pb2.ExtractChildOrderDataDetails()
        self._request.extractDetails.CopyFrom(extract_order_data)
        self._request.rowsNumber = rows_number

    def set_extract_order_data(self, extract_order_data: ExtractOrderDataDetails):
        self._request.extractDetails.CopyFrom(extract_order_data)

    def set_rows_number(self, rows_number: int):
        self._request.rowsNumber = rows_number

    def build(self):
        return self._request
