from th2_grpc_act_gui_quod.order_ticket_pb2 import DiscloseFlagEnum
from test_framework.win_gui_wrappers.base_order_ticket import BaseOrderTicket
from stubs import Stubs
from win_gui_modules.order_book_wrappers import ModifyOrderDetails
from win_gui_modules.order_ticket import OrderTicketDetails, OrderTicketExtractedValue, ExtractOrderTicketValuesRequest, \
    ExtractOrderTicketErrorsRequest
from win_gui_modules.order_ticket_wrappers import NewOrderDetails
from win_gui_modules.utils import call


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
                          capacity=None, desk=None, partial_desk=False,  disclose_flag=DiscloseFlagEnum.DEFAULT_VALUE):
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
        if desk is not None:
            self.order_details.set_care_order(desk, partial_desk, disclose_flag)
        return self

    # endregion
    # region Actions
    def oms_create_order(self, lookup):
        new_order_details = self.new_order_details
        new_order_details.set_lookup_instr(lookup)
        new_order_details.set_order_details(self.order_details)
        call(self.place_order_call, self.new_order_details.build())
        self.clear_details([self.new_order_details, self.order_details])
    # endregion
