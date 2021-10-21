from quod_qa.win_gui_wrappers.base_window import BaseWindow
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction
from win_gui_modules.utils import call


class BaseOrderBook(BaseWindow):
    def __init__(self, case_id, base_request):
        super().__init__(case_id, base_request)
        # Need to override
        self.order_info = None
        self.order_details = None
        self.new_order_details = None
        self.modify_order_details = None
        self.cancel_order_details = None
        self.reassign_order_details = None
        self.get_orders_details_call = None
        self.cancel_order_call = None
        self.order_book = None

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
    def cancel_order(self, cancel_children: bool = None, row_count: int = None, comment=None,
                     filter_list: list = None):
        if cancel_children is not None:
            self.cancel_order_details.set_cancel_children(cancel_children)
        if row_count is not None:
            self.cancel_order_details.set_selected_row_count(row_count)
        if comment is not None:
            self.cancel_order_details.set_comment(comment)
        if filter_list is not None:
            self.cancel_order_details.set_filter(filter_list)
        call(self.cancel_order_call.cancelOrder, self.cancel_order_details.build())

    def complete_order(self, filter_list=None, row_count=None):
        self.modify_order_details.set_default_params(self.base_request)
        if filter_list is not None:
            self.modify_order_details.set_filter()
        if row_count is not None:
            self.modify_order_details.set_selected_row_count()
        call(self.order_book.completeOrder, self.modify_order_details.build())

    def un_complete_order(self, filter_list=None, row_count=None):
        self.modify_order_details.set_default_params(self.base_request)
        if filter_list is not None:
            self.modify_order_details.set_filter()
        if row_count is not None:
            self.modify_order_details.set_selected_row_count()
        call(self.order_book.unCompleteOrder, self.modify_order_details.build())

    def notify_dfd(self, filter_list=None, row_count=None):
        self.modify_order_details.set_default_params(self.base_request)
        if filter_list is not None:
            self.modify_order_details.set_filter()
        if row_count is not None:
            self.modify_order_details.set_selected_row_count()
        call(self.order_book.notifyDFD, self.modify_order_details.build())

    def group_modify(self, client=None, security_account=None, routes=None, free_notes=None):
        self.modify_order_details.set_default_params(self.base_request)
        if client is not None:
            self.modify_order_details.client = client
        if security_account is not None:
            self.modify_order_details.securityAccount = security_account
        if routes is not None:
            self.modify_order_details.routes = routes
        if free_notes is not None:
            self.modify_order_details.freeNotes = free_notes
        call(self.order_book.groupModify, self.modify_order_details.build())

    def reassign_order(self, recipient):
        self.reassign_order_details.base.CopyFrom(self.base_request)
        self.reassign_order_details.desk = recipient
        call(self.order_book.reassignOrder, self.reassign_order_details)
    # endregion
