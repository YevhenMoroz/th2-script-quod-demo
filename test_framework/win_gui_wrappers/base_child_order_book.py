from test_framework.win_gui_wrappers.base_window import BaseWindow
from win_gui_modules.utils import call


class BaseChildOrderBook(BaseWindow):
    # region Base constructor
    def __init__(self, case_id, session_id):
        super().__init__(case_id, session_id)
        self.extract_child_order_book_data_details = None
        self.extract_child_order_book_sub_lvl_data_details = None
        self.extract_child_order_book_data_call = None
        self.extract_child_order_book_sub_lvl_data_call = None
    # endregion

    # region Get
    def get_child_order_value(self, column_name, child_book_filter: dict = None):
        self.extract_child_order_book_data_details.set_default_param(self.base_request)
        self.extract_child_order_book_data_details.set_extraction_columns([column_name])
        if child_book_filter is not None:
            self.extract_child_order_book_data_details.set_filter(child_book_filter)
        result = call(self.extract_child_order_book_data_call, self.extract_child_order_book_data_details.build())
        self.clear_details([self.extract_child_order_book_data_details])
        return result[column_name]

    def get_child_order_sub_lvl_value(self, row_count: int, extract_value, tab_name, child_book_filter: dict = None):
        self.extract_child_order_book_data_details.set_default_param(self.base_request)
        if child_book_filter is not None:
            self.extract_child_order_book_data_details.set_filter(child_book_filter)  # Set filter for parent order
        self.extract_child_order_book_data_details.set_extraction_columns(
            [extract_value])  # Set column for child orders which data be extracted
        self.extract_child_order_book_sub_lvl_data_details.set_extract_order_data(
            self.extract_child_order_book_data_details.build())
        self.extract_child_order_book_sub_lvl_data_details.set_rows_number(row_count)
        self.extract_child_order_book_sub_lvl_data_details.set_tab_name(tab_name)
        result = call(self.extract_child_order_book_sub_lvl_data_call,
                      self.extract_child_order_book_sub_lvl_data_details.build())
        self.clear_details([self.extract_child_order_book_data_details, self.extract_child_order_book_sub_lvl_data_call])
        return result[str(row_count)]
    # endregion
