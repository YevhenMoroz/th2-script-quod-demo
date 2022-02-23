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


class ExtractSubLvlDataDetails:
    def __init__(self, extract_order_data: ExtractOrderDataDetails = None, rows_number: int = None,
                 tab_name: str = None):
        self._request = basket_book_pb2.ExtractChildOrderDataDetails()
        self._request.extractDetails.CopyFrom(extract_order_data)
        self._request.rowsNumber = rows_number
        self._request.tabName = tab_name

    def set_extract_order_data(self, extract_order_data: ExtractOrderDataDetails):
        self._request.extractDetails.CopyFrom(extract_order_data)

    def set_rows_number(self, rows_number: int):
        self._request.rowsNumber = rows_number

    def set_tab_name(self, tab_name: str):
        self._request.tabName = tab_name

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


class BasketWaveRowDetails:
    def __init__(self):
        self._request = basket_book_pb2.BasketWaveRowDetails()

    def set_filtration_value(self, filtration_value: str):
        self._request.filtrationValue = filtration_value

    def set_remove_row(self, remove_row: bool):
        self._request.removeRow = remove_row

    def build(self):
        return self._request


class WaveBasketDetails:
    def __init__(self, base_request=None, filter: dict = None, percentage_profile: str = None,
                 qty_percentage: str = None, route: str = None, row_details: list = None):

        if base_request is not None:
            self._request = basket_book_pb2.WaveBasketDetails(base=base_request)
        else:
            self._request = basket_book_pb2.WaveBasketDetails()

        if filter is not None:
            self._request.filter.update(filter)

        if percentage_profile is not None:
            self._request.percentageProfile = percentage_profile

        if qty_percentage is not None:
            self._request.qtyPercentage = (qty_percentage)

        if route is not None:
            self._request.route = route

        if row_details is not None:
            self._request.rowsDetails.append(row_details)

    def set_base_details(self, base_details):
        self._request.base.CopyFrom(base_details)

    def set_filter(self, filter: dict):
        self._request.filter.update(filter)

    def set_percentage_profile(self, percentage_profile: str):
        self._request.percentageProfile = percentage_profile

    def set_qty_percentage(self, qty_percentage: str):
        self._request.qtyPercentage = qty_percentage

    def set_route(self, route: str):
        self._request.route = route

    def set_row_details_list(self, row_details: list):
        for row_detail in row_details:
            self._request.rowsDetails.append(row_detail)

    def set_row_details(self, row_details):
        self._request.rowsDetails.append(row_details)

    def set_sub_lvl_rows(self, sub_lvl_rows: list):
        self._request.subLvlRows.extend(sub_lvl_rows)

    def build(self):
        return self._request
