from th2_grpc_act_gui_quod import common_pb2
from th2_grpc_act_gui_quod.order_ticket_pb2 import DiscloseFlagEnum

from stubs import Stubs
from test_framework.win_gui_wrappers.base_order_ticket import BaseOrderTicket
from win_gui_modules.common_wrappers import CommissionsDetails, CommissionsTabTableParams, SettlementTabDetails
from win_gui_modules.order_book_wrappers import ModifyOrderDetails
from win_gui_modules.order_ticket import OrderTicketDetails, OrderTicketExtractedValue, ExtractOrderTicketValuesRequest, \
    ExtractOrderTicketErrorsRequest, AllocationsGridRowDetails, MoreTabAllocationsDetails, AdwOrdTabDetails, \
    MiscsOrdDetails, PartiesTabDetails
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
        self.re_order_call = Stubs.win_act_order_book.reOrder
        self.re_order_leaves_call = Stubs.win_act_order_book.reOrderLeaves
        self.re_order_order_call = Stubs.win_act_order_book.reOrder
        self.extract_order_ticket_values_call = Stubs.win_act_order_ticket.extractOrderTicketValues
        self.extract_order_ticket_errors_call = Stubs.win_act_order_ticket.extractOrderTicketErrors
        self.mass_modify_order_call = Stubs.win_act_order_book.massModify
        self.allocations_grid_row_details = AllocationsGridRowDetails()
        self.more_tab_allocations_details = MoreTabAllocationsDetails()
        self.commissions_tab_table_details = CommissionsTabTableParams()
        self.commissions_details = CommissionsDetails()
        self.adw_ord_tab_details = AdwOrdTabDetails()
        self.miscs_ord_tab_details = MiscsOrdDetails()
        self.settlement_details = SettlementTabDetails()
        self.parties_tab_details = PartiesTabDetails()
        # endregion

    # region Set
    def set_order_details(self, client=None, limit=None, stop_price=None, qty=None, expire_date=None, order_type=None,
                          tif=None, account=None, display_qty=None, is_sell_side=False, instrument=None, washbook=None,
                          capacity=None, settl_date=None, recipient=None, partial_desk=False,
                          disclose_flag=DiscloseFlagEnum.DEFAULT_VALUE,
                          alloc_details: dict = None, error_expected=None, set_alt_account: bool = False,
                          set_qty=True):
        self.order_details = super().set_order_details(client=client, limit=limit, stop_price=stop_price, qty=qty,
                                                       order_type=order_type, tif=tif, account=account,
                                                       display_qty=display_qty, is_sell_side=is_sell_side,
                                                       error_expected=error_expected)
        if expire_date is not None:
            self.order_details.set_expire_date(expire_date)
        if instrument is not None:
            self.order_details.set_instrument(instrument)
        if washbook is not None:
            self.order_details.set_washbook(washbook)
        if capacity is not None:
            self.order_details.set_capacity(capacity)
        if settl_date is not None:
            self.order_details.set_settl_date(settl_date)
        if recipient is not None:
            self.order_details.set_care_order(recipient, partial_desk, disclose_flag)
        if alloc_details and set_alt_account:
            allocation_row_details = list()
            for account_name, percent in alloc_details.items():
                allocation_row_details.append(AllocationsGridRowDetails(alt_account=account_name, percentage=percent).build())
            more_tab_allocation_details = MoreTabAllocationsDetails(allocation_row_details)
            more_tab_allocation_details.set_alt_acc_checkbox(True)
            allocation_details = more_tab_allocation_details.build()
            self.order_details.set_allocations_details(allocation_details)
        else:
            if alloc_details is not None:
                allocation_row_details = list()
                for account_name, qty in alloc_details.items():
                    allocation_row_details.append(AllocationsGridRowDetails(account=account_name, qty=qty).build())
                more_tab_allocation_details = MoreTabAllocationsDetails(allocation_row_details)
                allocation_details = more_tab_allocation_details.build()
                self.order_details.set_allocations_details(allocation_details)
        return self

    # endregion
