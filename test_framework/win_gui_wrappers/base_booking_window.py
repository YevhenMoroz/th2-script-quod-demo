from test_framework.win_gui_wrappers.base_window import BaseWindow
from win_gui_modules.utils import call


class BaseBookingWindow(BaseWindow):
    def __init__(self, case_id, session_id):
        super().__init__(case_id, session_id)
        self.booking_extraction_call = None
        self.extract_booking_details = None
        self.extract_second_level_details = None
        self.second_level_tab_extraction_call = None

    def set_extraction_details(self,
                               columns_of_extraction: list = None,
                               filter_dict: dict = None):
        if columns_of_extraction:
            self.extract_booking_details.set_extraction_columns(columns_of_extraction)
        if filter_dict:
            self.extract_booking_details.set_filter(filter_dict)

    def extract_from_booking_window(self):
        result = call(self.booking_extraction_call, self.extract_booking_details.build())
        self.clear_details([self.extract_booking_details])
        return result

    def extract_from_second_level_tab(self, tab_name: str, row_numbers: int = 1):
        self.extract_second_level_details.set_sub_level_details(self.extract_booking_details, tab_name, row_numbers)
        result = call(self.second_level_tab_extraction_call, self.extract_second_level_details.build())
        self.clear_details([self.extract_second_level_details, self.extract_booking_details])
        return result
