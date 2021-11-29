from test_framework.win_gui_wrappers.base_client_inbox import BaseClientInbox
from stubs import Stubs
from win_gui_modules.wrappers import accept_order_request, reject_order_request, direct_order_request, \
    direct_moc_request_correct, direct_loc_request_correct, direct_poc_request_correct


class OMSClientInbox(BaseClientInbox):

    # region Base constructor
    def __init__(self, case_id, session_id):
        super().__init__(case_id, session_id)
        self.accept_order_request = accept_order_request
        self.reject_order_request = reject_order_request
        self.direct_order_request = direct_order_request
        self.direct_moc_request = direct_moc_request_correct
        self.direct_loc_request = direct_loc_request_correct
        self.direct_poc_request = direct_poc_request_correct
        self.accept_order_call = Stubs.win_act.acceptOrder
        self.accept_modify_plus_child_call = Stubs.win_act.acceptModifyPlusChild
        self.accept_and_cancel_children_call = Stubs.win_act.acceptAndCancelChildren
        self.reject_order_call = Stubs.win_act.rejectOrder
        self.client_inbox_direct_call = Stubs.win_act.clientInboxDirectOrder
        self.client_inbox_direct_moc_call = Stubs.win_act.clientInboxDirectMoc
        self.client_inbox_direct_loc_call = Stubs.win_act.clientInboxDirectLoc
        self.client_inbox_direct_poc_call = Stubs.win_act.clientInboxDirectPoc
    # endregion