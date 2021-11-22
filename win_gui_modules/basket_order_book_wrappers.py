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


class RemoveChildOrderFromBasketDetails:
    def __init__(self, base_request=None, filter: dict = None, rows_numbers: list = None):
        if base_request is not None:
            self._request = basket_book_pb2.RemoveChildOrderFromBasketDetails(base=base_request)
        else:
            self._request = basket_book_pb2.RemoveChildOrderFromBasketDetails()

        if filter is not None:
            self._request.filter.update(filter)

        if rows_numbers is not None:
            for number in rows_numbers:
                self._request.rowsNumbers.append(number)

    def set_base_details(self, base_details):
        self._request.base.CopyFrom(base_details)

    def set_filter(self, filter: dict):
        self._request.filter.update(filter)

    def set_rows_numbers(self, rows_number: list):
        for number in rows_number:
            self._request.rowsNumbers.append(number)

    def build(self):
        return self._request
