from custom.verifier import VerificationMethod
from test_framework.win_gui_wrappers.base_window import BaseWindow
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction
from win_gui_modules.trades_blotter_wrappers import ModifyTradesDetails
from win_gui_modules.utils import call


class BaseTradesBook(BaseWindow):
    # region Base constructor
    def __init__(self, case_id, base_request):
        super().__init__(case_id, base_request)
        # Need to override
        self.order_info = None
        self.order_details = None
        self.match_details = None
        self.cancel_manual_execution_details = None
        self.manual_match_call = None
        self.cancel_manual_execution_call = None
        self.get_trade_book_details_call = None
        self.un_match_call = None
        self.manual_match_n_to_1_call = None
        self.extract_trades_book_sub_lvl_data_details = None
        self.extract_trades_book_sub_lvl_data_call = None

    # endregion
    # region Common func
    def set_order_details(self):
        self.order_details.set_extraction_id(self.extraction_id)
        self.order_details.set_default_params(base_request=self.base_request)

    def set_filter(self, filter_list: list):
        """
        Receives list as an argument, where the elements
        are in order - key, value, key, value, ...
        For example ["Qty", "123456", "Owner", "QA1", etc]
        """
        self.order_details.set_filter(filter_list)
        return self

    # region Get
    def extract_field(self, column_name: str) -> str:
        field = ExtractionDetail("tradeBook." + column_name, column_name)
        self.order_details.add_single_order_info(
            self.order_info.create(
                action=ExtractionAction.create_extraction_action(extraction_details=[field])
            )
        )
        response = call(self.get_trade_book_details_call, self.order_details.request())
        return response[field.name]

    def extract_fields(self, fields: dict) -> dict:
        """
        Receives dict as an argument, where the key is column name what
        we extract from GUI and return new dict where
        key = key and value is extracted field from FE
        """
        list_of_fields = []
        for field in fields.items():
            key = list(field)[0]
            field = ExtractionDetail(key, key)
            list_of_fields.append(field)
        self.order_details.add_single_order_info(
            self.order_info.create(
                action=ExtractionAction.create_extraction_action(extraction_details=list_of_fields)
            )
        )
        response = call(self.get_trade_book_details_call, self.order_details.request())
        return response

    def extract_sub_lvl_fields(self, column_names: list, tab_name, row_count: int, filter: dict = None):
        self.extract_trades_book_sub_lvl_data_details.set_default_params(self.base_request)
        self.extract_trades_book_sub_lvl_data_details.set_filter(filter)
        self.extract_trades_book_sub_lvl_data_details.set_column_names(column_names)
        self.extract_trades_book_sub_lvl_data_details.set_tab_name(tab_name)
        self.extract_trades_book_sub_lvl_data_details.set_row_number(row_count)
        call(self.extract_trades_book_sub_lvl_data_call, self.extract_trades_book_sub_lvl_data_details.build())

    # endregion
    # region Action
    def manual_match(self, qty_to_match=None, order_filter_list=None, trades_filter_list=None, error_expected=False):
        if order_filter_list is not None:
            self.match_details.set_filter(order_filter_list)
        if qty_to_match is not None:
            self.match_details.set_qty_to_match(qty_to_match)
        if error_expected:
            self.match_details.set_expected_error()
        self.match_details.click_match()
        modify_trades_details = ModifyTradesDetails(self.match_details)
        modify_trades_details.set_default_params(self.base_request)
        if trades_filter_list is not None:
            modify_trades_details.set_filter(trades_filter_list)
        result = call(self.manual_match_call, modify_trades_details.build())
        return result

    def manual_match_n_to_1(self, order_to_match=None, exec_rows_list=None, trades_filter_list=None):
        self.match_details.click_match()
        modify_trades_details = ModifyTradesDetails(self.match_details)
        modify_trades_details.set_default_params(self.base_request)
        if trades_filter_list is not None:
            modify_trades_details.set_filter(trades_filter_list)
        if exec_rows_list is not None:
            modify_trades_details.set_selected_rows(exec_rows_list)
        if order_to_match is not None:
            modify_trades_details.set_order_to_match(order_to_match)
        call(self.manual_match_n_to_1_call, modify_trades_details.build())

    def un_match(self, qty_to_match=None, trades_filter_list=None):
        if qty_to_match is not None:
            self.match_details.set_qty_to_match(qty_to_match)
        self.match_details.click_match()
        modify_trades_details = ModifyTradesDetails(self.match_details)
        modify_trades_details.set_default_params(self.base_request)
        if trades_filter_list is not None:
            modify_trades_details.set_filter(trades_filter_list)
        call(self.un_match_call, modify_trades_details.build())

    def cancel_execution(self, trades_filter_list=None):
        self.cancel_manual_execution_details.set_default_params(self.base_request)
        if trades_filter_list is not None:
            self.cancel_manual_execution_details.set_filter(trades_filter_list)
        call(self.cancel_manual_execution_call, self.cancel_manual_execution_details.build())

    # endregion
    # region Check

    def check_trade_fields_list(self, expected_fields: dict, event_name="Check Trade Book",
                                verification_method: VerificationMethod = VerificationMethod.EQUALS):

        actual_list = self.extract_fields(expected_fields)
        for items in expected_fields.items():
            key = list(items)[0]
            value = list(items)[1]
            self.verifier.set_event_name(event_name)
            self.verifier.compare_values(key, str(value).replace(',', ''), str(actual_list[key]).replace(',', ''),
                                         verification_method)
        self.verifier.verify()

    # endregion
