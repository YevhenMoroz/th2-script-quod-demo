from th2_grpc_act_gui_quod import child_order_book_pb2


class ExtractChildOrderBookDataDetails:
    def __init__(self, base_request=None):
        if base_request:
            self._child_order_details = child_order_book_pb2.ExtractChildOrderBookDataDetails()
            self._child_order_details.base.CopyFrom(base_request)
        else:
            self._child_order_details = child_order_book_pb2.ExtractChildOrderBookDataDetails()

    def set_default_param(self, base_request):
        self._child_order_details.base.CopyFrom(base_request)

    def set_filter(self, filter_dict: dict):
        self._child_order_details.filter.update(filter_dict)

    def set_extraction_columns(self, list_of_column: list):
        for column in list_of_column:
            self._child_order_details.columnNames.append(column)

    def build(self):
        return self._child_order_details


class ExtractSubLvlDataDetails:
    def __init__(self, extract_order_data: ExtractChildOrderBookDataDetails = None, rows_number: int = None,
                 tab_name: str = None):
        self._request = child_order_book_pb2.ExtractChildOrderBookSubLvlDataDetails()
        if extract_order_data:
            self._request.extractDetails.CopyFrom(extract_order_data)
        if rows_number:
            self._request.rowsNumber = rows_number
        if tab_name:
            self._request.tabName = tab_name

    def set_extract_order_data(self, extract_order_data: ExtractChildOrderBookDataDetails):
        self._request.extractDetails.CopyFrom(extract_order_data)

    def set_rows_number(self, rows_number: int):
        self._request.rowsNumber = rows_number

    def set_tab_name(self, tab_name: str):
        self._request.tabName = tab_name

    def build(self):
        return self._request
