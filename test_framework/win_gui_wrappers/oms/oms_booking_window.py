from stubs import Stubs
from test_framework.win_gui_wrappers.base_booking_window import BaseBookingWindow
from win_gui_modules.booking_blotter_wrappers import ExtractBookingDataDetails, ExtractSubLvlDetails
from win_gui_modules.common_wrappers import SimpleRequest


class OMSBookingWindow(BaseBookingWindow):
    def __init__(self, case_id, session_id):
        super().__init__(case_id, session_id)
        self.booking_extraction_call = Stubs.win_act_booking_blotter_service.extractBookingData
        self.extract_booking_details = ExtractBookingDataDetails(self.base_request)
        self.extract_second_level_details = ExtractSubLvlDetails()
        self.second_level_tab_extraction_call = Stubs.win_act_booking_blotter_service.extractSubLvlBookingData
        self.simple_request = SimpleRequest(self.base_request)
        self.cancel_booking_call = Stubs.win_act_booking_blotter_service.cancelBooking
