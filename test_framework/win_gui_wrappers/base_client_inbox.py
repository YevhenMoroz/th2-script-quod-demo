from test_framework.win_gui_wrappers.base_window import BaseWindow
from win_gui_modules.utils import call


class BaseClientInbox(BaseWindow):

    # region Base constructor
    def __init__(self, case_id, session_id):
        super().__init__(case_id, session_id)
        self.accept_order_request = None
        self.direct_order_request = None
        self.direct_moc_request = None
        self.direct_loc_request = None
        self.direct_poc_request = None
        self.accept_order_call = None
        self.accept_modify_plus_child_call = None
        self.accept_and_cancel_children_call = None
        self.reject_order_call = None
        self.client_inbox_direct_call = None
        self.client_inbox_direct_moc_call = None
        self.client_inbox_direct_loc_call = None
        self.client_inbox_direct_poc_call = None

    # endregion

    # region Actions
    def accept_order(self, *args, filter: dict = None):
        call(self.accept_order_call, self.accept_order_request(self.base_request, filter))

    def accept_modify_plus_child(self, *args, filter: dict = None):
        call(self.accept_modify_plus_child_call, self.accept_order_request(self.base_request, filter))

    def accept_and_cancel_children(self, *args, filter: dict = None):
        call(self.accept_and_cancel_children_call, self.accept_order_request(self.base_request, filter))

    def reject_order(self, *args, filter: dict = None):
        call(self.reject_order_call, self.accept_order_request(self.base_request, filter))

    def direct_order(self, instr: str, qty: str, limit: str, qty_percentage: str, filter: dict = None):
        call(self.client_inbox_direct_call, self.direct_order_request(instr, qty, limit, qty_percentage, filter))

    def client_inbox_direct_moc(self, qty_type: str, qty_percentage: str, route: str, filter: dict = None):
        call(self.client_inbox_direct_moc_call, self.direct_moc_request(qty_type, qty_percentage, route, filter))

    def client_inbox_direct_loc(self, qty_type: str, qty_percentage: str, route: str, filter: dict = None):
        call(self.client_inbox_direct_loc_call,
             self.direct_loc_request(qty_type, qty_percentage, route, filter))

    def client_inbox_direct_poc(self, qty_type, reference_price, percentage, qty_percentage, route,
                                filter: dict = None, instruction=''):
        call(self.client_inbox_direct_poc_call, self.direct_poc_request(qty_type, reference_price,
                                                                        percentage, qty_percentage, route, filter,
                                                                        instruction))
    # end region
