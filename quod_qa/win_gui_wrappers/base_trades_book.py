from quod_qa.win_gui_wrappers.base_window import BaseWindow
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction
from win_gui_modules.utils import call


class BaseTradesBook(BaseWindow):
    # region Base constructor
    def __init__(self, case_id, base_request):
        super().__init__(case_id, base_request)
        # Need to override
        self.order_info = None
        self.order_details = None
        self.match_details = None
        self.modify_trades_details = None
        self.cancel_manual_execution_details = None
        self.manual_match_call = None
        self.cancel_manual_execution_call = None
        self.get_trade_book_details_call = None

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

    # endregion
    # region Action
    def manual_match(self, qty_to_match=None, order_filter_list=None, trades_filter_list=None):
        if order_filter_list is not None:
            self.match_details.set_filter(order_filter_list)
        if qty_to_match is not None:
            self.match_details.set_qty_to_match(qty_to_match)
        self.match_details.click_match()
        self.modify_trades_details.set_match_details(self.match_details)
        self.modify_trades_details.set_default_params(self.base_request)
        if trades_filter_list is not None:
            self.modify_trades_details.set_filter(trades_filter_list)
        call(self.manual_match_call, self.modify_trades_details.build())

    def cancel_execution(self, trades_filter_list=None):
        self.cancel_manual_execution_details.set_default_params(self.base_request)
        if trades_filter_list is not None:
            self.cancel_manual_execution_details.set_filter(trades_filter_list)
        call(self.cancel_manual_execution_call, self.cancel_manual_execution_details.build())
    # endregion
