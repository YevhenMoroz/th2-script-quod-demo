from quod_qa.win_gui_wrappers.base_window import BaseWindow
from stubs import Stubs
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction, OrderInfo, \
    OrdersDetails
from win_gui_modules.utils import call


class BaseOrderBook(BaseWindow):
    def __init__(self, case_id, base_request):
        super().__init__(case_id, base_request)
        # Need to override
        self.order_info = None
        self.order_details = None
        self.cancel_order_details = None
        self.get_orders_details_call = None
        self.cancel_order_call = None

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

    # endregion

    # region Get
    def extract_field(self, column_name: str) -> str:
        field = ExtractionDetail("orderBook." + column_name, column_name)
        self.order_details.add_single_order_info(
            self.order_info.create(
                action=ExtractionAction.create_extraction_action(extraction_details=[field])
            )
        )
        response = call(self.get_orders_details_call, self.order_details.request())
        return response[field.name]

    def extract_fields_list(self, list_fields: dict) -> dict:
        """
        Receives dict as an argument, where the key is column name what
        we extract from GUI and return new dict where
        key = key and value is extracted field from FE
        """
        list_of_fields = []
        for field in list_fields.items():
            key = list(field)[0]
            field = ExtractionDetail(key, key)
            list_of_fields.append(field)
        self.order_details.add_single_order_info(
            self.order_info.create(
                action=ExtractionAction.create_extraction_action(extraction_details=list_of_fields)
            )
        )
        response = call(self.get_orders_details_call, self.order_details.request())
        return response

    # endregion

    # region Check
    def check_order_fields_list(self, expected_fields: dict, event_name="Check Order Book"):
        """
        Receives dict as an argument, where the key is column name what
        we extract from GUI and value is expected result
        For example {"Sts": "Terminated", "Owner": "QA1", etc}
        """
        actual_list = self.extract_fields_list(expected_fields)
        for items in expected_fields.items():
            key = list(items)[0]
            value = list(items)[1]
            self.verifier.set_event_name(event_name)
            self.verifier.compare_values(key, value, actual_list[key])
        self.verifier.verify()

    # endregion

    # region Actions
    def cancel_order(self, cancel_children: bool):
        self.cancel_order_details.set_default_params(self.base_request)
        self.cancel_order_details.set_cancel_children(cancel_children)
        call(self.cancel_order_call, self.cancel_order_details.build())
    # endregion
