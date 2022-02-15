from custom.verifier import VerificationMethod, Verifier
from test_framework.win_gui_wrappers.base_window import BaseWindow
from win_gui_modules.dealing_positions_wrappers import ExtractionPositionsAction, ExtractionPositionsFieldsDetails
from win_gui_modules.order_book_wrappers import ExtractionAction
from win_gui_modules.utils import call


class BasePositionsBook(BaseWindow):
    # region Base constructor
    def __init__(self, case_id, session_id):
        super().__init__(case_id, session_id)
        # Need to override
        self.positions_info = None
        self.position_details = None
        self.base_positions_details = None
        self.second_level_tab_details = None
        self.second_level_extraction_details = None
        self.extraction_from_second_level_tabs_call = None
        self.get_positions_details_call = None
        # endregion

    # region Common func
    def set_positions_details(self):
        self.position_details.set_extraction_id(self.extraction_id)
        self.position_details.set_default_params(base_request=self.base_request)
        self.verifier = Verifier(self.case_id)


    def set_filter(self, filter_list: list):
        """
        Receives list as an argument, where the elements
        are in order - key, value, key, value, ...
        For example ["Qty", "123456", "Owner", "QA1", etc]
        """
        self.position_details.set_filter(filter_list)
        return self

    # endregion

    # region Get
    def extract_field(self, column_name: str, row_number: int = None) -> str:
        field = ExtractionPositionsFieldsDetails(column_name, column_name)
        info = self.positions_info.create(
            action=ExtractionPositionsAction.create_extraction_action(extraction_details=[field]))
        if row_number is not None:
            info.set_number(row_number)
        self.position_details.add_single_positions_info(info)
        response = call(self.get_positions_details_call, self.position_details.request())
        self.clear_details([self.position_details])
        self.set_positions_details()
        return response[column_name]

    def extract_fields_list(self, list_fields: dict, row_number: int = None) -> dict:
        """
        Receives dict as an argument, where the key is column name what
        we extract from GUI and return new dict where
        key = key and value is extracted field from FE
        """
        list_of_fields = []
        for field in list_fields.items():
            key = list(field)[0]
            field = ExtractionPositionsFieldsDetails(key, key)
            list_of_fields.append(field)
        info = self.positions_info.create(
            action=ExtractionPositionsAction.create_extraction_action(extraction_details=list_of_fields))
        if row_number is not None:
            info.set_number(row_number)
        self.position_details.add_single_positions_info(info)
        response = call(self.get_positions_details_call, self.position_details.request())
        self.clear_details([self.position_details])
        self.set_positions_details()
        return response

    # region Check
    def check_positions_fields_list(self, expected_fields: dict, event_name="Check Positions Book",
                                    row_number: int = 1,
                                    verification_method: VerificationMethod = VerificationMethod.EQUALS):
        """
        Receives dict as an argument, where the key is column name what
        we extract from GUI and value is expected result and row_number to check, 1 by default
        For example {"Sts": "Terminated", "Owner": "QA1", etc}
        """
        actual_list = self.extract_fields_list(expected_fields, row_number)
        for items in expected_fields.items():
            key = list(items)[0]
            value = list(items)[1]
            self.verifier.set_event_name(event_name)
            self.verifier.compare_values(key, str(value).replace(',', ''), str(actual_list[key]).replace(',', ''),
                                         verification_method)
        self.verifier.verify()

    def extract_second_lvl_fields_list(self, list_fields: dict, row_number: int = None) -> dict:
        """
        Receives dict as an argument, where the key is column name what
        we extract from GUI and return new dict where
        key = key and value is extracted field from FE
        """
        list_of_fields = []
        for field in list_fields.items():
            key = list(field)[0]
            field = ExtractionPositionsFieldsDetails(key, key)
            list_of_fields.append(field)
        child_info = self.positions_info.create(
            action=ExtractionPositionsAction.create_extraction_action(extraction_details=list_of_fields))
        if row_number is not None:
            child_info.set_number(row_number)
        child_details = self.position_details.create(info=child_info)
        self.position_details.add_single_positions_info(
            self.positions_info.create(
                action=ExtractionPositionsAction.create_extraction_action(
                    ExtractionPositionsFieldsDetails("dealingpositions.position", "Position")),
                positions_by_currency=child_details)
        )
        response = call(self.get_positions_details_call, self.position_details.request())
        self.clear_details([self.position_details])
        self.set_positions_details()
        return response

    def check_second_lvl_fields_list(self, expected_fields: dict, event_name="Check second lvl in Positions Book",
                                     row_number: int = 1,
                                     verification_method: VerificationMethod = VerificationMethod.EQUALS):
        """
        Receives dict as an argument, where the key is column name what
        we extract from GUI and value is expected result and row_number to check, 1 by default
        For example {"Sts": "Terminated", "Owner": "QA1", etc}
        """
        actual_list = self.extract_second_lvl_fields_list(expected_fields, row_number)
        for items in expected_fields.items():
            key = list(items)[0]
            value = list(items)[1]
            self.verifier.set_event_name(event_name)
            self.verifier.compare_values(key, str(value).replace(',', ''), str(actual_list[key]).replace(',', ''),
                                         verification_method)
        self.verifier.verify()

