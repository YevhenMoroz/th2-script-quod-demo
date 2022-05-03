from test_framework.win_gui_wrappers.base_window import BaseWindow
from win_gui_modules.firm_position_wrappers import ExtractPositionsDetails
from win_gui_modules.utils import call


class BaseFirmPositionWindow(BaseWindow):
    def __init__(self, case_id, session_id):
        super().__init__(case_id, session_id)
        self.firm_position_extraction_call = None
        self.extract_position_details = None

    def set_extraction_details(self, security_account: str,
                               columns_of_extraction: list = None,
                               fields_of_extraction: list = None,
                               filter_dict: dict = None):
        if columns_of_extraction:
            self.extract_position_details.set_extraction_of_columns(columns_of_extraction)
        if fields_of_extraction:
            self.extract_position_details.set_field_from_panel(fields_of_extraction)
        if filter_dict:
            self.extract_position_details.set_filter(filter_dict)
        self.extract_position_details.set_security_account(security_account)

    def extract_from_firm_position(self):
        result = call(self.firm_position_extraction_call, self.extract_position_details.build())
        self.clear_details([self.extract_position_details])
        return result
