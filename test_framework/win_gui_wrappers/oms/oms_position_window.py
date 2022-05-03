from stubs import Stubs
from test_framework.win_gui_wrappers.base_position_window import BaseFirmPositionWindow
from win_gui_modules.firm_position_wrappers import ExtractPositionsDetails


class OMSFirmPositionWindow(BaseFirmPositionWindow):
    def __init__(self, case_id, session_id):
        super().__init__(case_id, session_id)
        self.extract_position_details = ExtractPositionsDetails(self.base_request)
        self.firm_position_extraction_call = Stubs.win_act_risk_management.firmPositionsExtraction
