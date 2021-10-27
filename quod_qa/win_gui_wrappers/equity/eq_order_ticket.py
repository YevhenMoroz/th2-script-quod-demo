from th2_grpc_act_gui_quod.order_ticket_pb2 import DiscloseFlagEnum
from quod_qa.win_gui_wrappers.base_order_ticket import BaseOrderTicket
from stubs import Stubs
from win_gui_modules.order_book_wrappers import ModifyOrderDetails
from win_gui_modules.order_ticket import OrderTicketDetails, OrderTicketExtractedValue, ExtractOrderTicketValuesRequest, \
    ExtractOrderTicketErrorsRequest
from win_gui_modules.order_ticket_wrappers import NewOrderDetails
from win_gui_modules.utils import call


class EqOrderTicket(BaseOrderTicket):
    def __init__(self, case_id, base_request):
        super().__init__(case_id, base_request)
        # Need to override
        self.order_details = OrderTicketDetails()
        self.new_order_details = NewOrderDetails(base_request)
        self.modify_order_details = ModifyOrderDetails(base_request)
        self.extract_order_ticket_values_request = ExtractOrderTicketValuesRequest(base_request)
        self.extract_order_ticket_errors_request = ExtractOrderTicketErrorsRequest(base_request)
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

    def set_order_details(self, client=None, limit=None, stop_price=None, qty=None, expire_date=None, order_type=None,
                          tif=None, account=None, display_qty=None, is_sell_side=False, instrument=None, washbook=None,
                          capacity=None, desk=None, partial_desk=False, disclose_flag: DiscloseFlagEnum = None):
        order_details = self.order_details
        if client is not None:
            order_details.set_client(client)
        if qty is not None:
            order_details.set_quantity(qty)
        if order_type is not None:
            order_details.set_order_type(order_type)
        if is_sell_side:
            order_details.sell()
        if tif is not None:
            order_details.set_tif(tif)
        if expire_date is not None:
            order_details.set_expire_date(expire_date)
        if limit is not None:
            order_details.set_expire_date(limit)
        if stop_price is not None:
            order_details.set_stop_price(stop_price)
        if account is not None:
            order_details.set_account(account)
        if display_qty is not None:
            order_details.set_display_qty(display_qty)
        if instrument is not None:
            order_details.set_instrument(instrument)
        if washbook is not None:
            order_details.set_washbook(washbook)
        if capacity is not None:
            order_details.set_capacity(capacity)
        if desk is not None:
            order_details.set_care_order(desk, partial_desk, disclose_flag)
        return order_details

    def create_order(self, lookup, order_details: OrderTicketDetails()):
        new_order_details = self.new_order_details
        new_order_details.set_lookup_instr(lookup)
        new_order_details.set_order_details(order_details)
        call(self.place_order_call, self.new_order_details.build())


