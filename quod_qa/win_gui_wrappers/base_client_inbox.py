from quod_qa.win_gui_wrappers.base_window import BaseWindow
from win_gui_modules.utils import call


class BaseClientInbox(BaseWindow):

    # region Base constructor
    def __init__(self, case_id, base_request):
        super().__init__(case_id, base_request)
        self.accept_order_request = None
        self.reject_order_request = None
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
    def accept_order(self, instr: str, qty: str, limit: str):
        call(self.accept_order_call, self.accept_order_request(instr, qty, limit))

    def accept_modify_plus_child(self, instr: str, qty: str, limit: str):
        call(self.accept_modify_plus_child_call, self.accept_order_request(instr, qty, limit))

    def accept_and_cancel_children(self, instr: str, qty: str, limit: str):
        call(self.accept_and_cancel_children_call, self.accept_order_request(instr, qty, limit))

    def reject_order(self, instr: str, qty: str, limit: str):
        call(self.reject_order_call, self.reject_order_request(instr, qty, limit))

    def direct_order(self, instr: str, qty: str, limit: str, qty_percentage: str):
        call(self.client_inbox_direct_call, self.direct_order_request(instr, qty, limit, qty_percentage))

    def client_inbox_direct_moc(self, qty_type: str, qty_percentage: str, route: str):
        call(self.client_inbox_direct_moc_call, self.direct_moc_request(qty_type, qty_percentage, route))

    def client_inbox_direct_loc(self, qty_type: str, qty_percentage: str, route: str):
        call(self.client_inbox_direct_loc_call, self.direct_loc_request(qty_type, qty_percentage, route))

    def client_inbox_direct_poc(self, qty_type, reference_price, percentage, qty_percentage, route):
        call(self.client_inbox_direct_poc_call, self.direct_poc_request(qty_type, reference_price,
                                                                        percentage, qty_percentage, route))
    # end region
