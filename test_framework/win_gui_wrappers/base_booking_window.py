from test_framework.win_gui_wrappers.base_window import BaseWindow
from win_gui_modules.utils import call


class BaseBookingWindow(BaseWindow):
    def __init__(self, case_id, session_id):
        super().__init__(case_id, session_id)
        self.booking_extraction_call = None
        self.extract_booking_details = None

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
