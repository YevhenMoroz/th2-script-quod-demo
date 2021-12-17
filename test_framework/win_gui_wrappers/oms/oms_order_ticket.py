from th2_grpc_act_gui_quod.order_ticket_pb2 import DiscloseFlagEnum

from stubs import Stubs
from test_framework.win_gui_wrappers.base_order_ticket import BaseOrderTicket
from win_gui_modules.order_book_wrappers import ModifyOrderDetails
from win_gui_modules.order_ticket import OrderTicketDetails, OrderTicketExtractedValue, ExtractOrderTicketValuesRequest, \
    ExtractOrderTicketErrorsRequest, AllocationsGridRowDetails, MoreTabAllocationsDetails
from win_gui_modules.order_ticket_wrappers import NewOrderDetails


class OMSOrderTicket(BaseOrderTicket):
    # region Constructor
    def __init__(self, case_id, session_id):
        super().__init__(case_id, session_id)
        # Need to override
        self.order_details = OrderTicketDetails()
        self.new_order_details = NewOrderDetails(self.base_request)
        self.modify_order_details = ModifyOrderDetails(self.base_request)
        self.extract_order_ticket_values_request = ExtractOrderTicketValuesRequest(self.base_request)
        self.extract_order_ticket_errors_request = ExtractOrderTicketErrorsRequest(self.base_request)
        self.order_ticket_extracted_value = OrderTicketExtractedValue
        self.place_order_call = Stubs.win_act_order_ticket.placeOrder
        self.amend_order_call = Stubs.win_act_order_book.amendOrder
        self.split_limit_order_call = Stubs.win_act_order_book.splitLimit
        self.split_order_call = Stubs.win_act_order_book.splitOrder
        self.child_care_order_call = Stubs.win_act_order_book.childCare
        self.re_order_leaves_order_call = Stubs.win_act_order_book.reOrderLeaves
        self.re_order_order_call = Stubs.win_act_order_book.reOrder
        self.extract_order_ticket_values_call = Stubs.win_act_order_ticket.extractOrderTicketValues
        self.extract_order_ticket_errors_call = Stubs.win_act_order_ticket.extractOrderTicketErrors
        self.extract_order_ticket_errors_call = Stubs.win_act_order_ticket.extractOrderTicketErrors

    # endregion
    # region Set
    def set_order_details(self, client=None, limit=None, stop_price=None, qty=None, expire_date=None, order_type=None,
                          tif=None, account=None, display_qty=None, is_sell_side=False, instrument=None, washbook=None,
                          capacity=None, recipient=None, partial_desk=False,
                          disclose_flag=DiscloseFlagEnum.DEFAULT_VALUE,
                          alloc_details: dict = None):
        self.order_details = super().set_order_details(client=client, limit=limit, stop_price=stop_price, qty=qty,
                                                       order_type=order_type, tif=tif, account=account,
                                                       display_qty=display_qty, is_sell_side=is_sell_side)
        if expire_date is not None:
            self.order_details.set_expire_date(expire_date)
        if instrument is not None:
            self.order_details.set_instrument(instrument)
        if washbook is not None:
            self.order_details.set_washbook(washbook)
        if capacity is not None:
            self.order_details.set_capacity(capacity)
        if recipient is not None:
            self.order_details.set_care_order(recipient, partial_desk, disclose_flag)
        if alloc_details:
            allocation_row_details = list()
            for account_name, qty in alloc_details.items():
                allocation_row_details.append(AllocationsGridRowDetails(account_name, qty).build())
            allocation_details = MoreTabAllocationsDetails(allocation_row_details).build()
            self.order_details.set_allocations_details(allocation_details)
        return self

    # endregion
