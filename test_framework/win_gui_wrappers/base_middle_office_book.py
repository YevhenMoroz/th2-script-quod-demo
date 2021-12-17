from test_framework.win_gui_wrappers.base_window import BaseWindow
from win_gui_modules.middle_office_wrappers import AllocationBlockExtractionDetails, ExtractionPanelDetails
from win_gui_modules.order_book_wrappers import ExtractionDetail
from win_gui_modules.utils import call


class BaseMiddleOfficeBook(BaseWindow):
    # region Base constructor
    def __init__(self, case_id, session_id):
        super().__init__(case_id, session_id)
        # Need to override
        self.extraction_detail = None
        self.modify_ticket_details = None
        self.view_order_extraction_details = None
        self.extract_middle_office_blotter_values_request = None
        self.allocation_ticket_extraction_details = None
        self.extraction_panel_details = None
        self.book_order_call = None
        self.amend_block_call = None
        self.unbook_order_call = None
        self.approve_block_call = None
        self.amend_allocate_call = None
        self.allocate_block_call = None
        self.unallocate_block_call = None
        self.extract_view_orders_table_data_call = None
        self.extract_middle_office_blotter_values_call = None
        self.allocation_ticket_extraction_details_call = None
        self.extract_allocation_details = None
        self.extract_allocations_table_data = None
        self.amend_ticket_book_extraction_details_call = None

    # endregion
    # region Common func

    def set_filter(self, filter_list: list):
        self.extract_middle_office_blotter_values_request.set_filter(filter_list)

    # endregion
    # region Check
    def check_booking_toggle_manual(self):
        self.modify_ticket_details.add_commissions_details()
        extraction_details = self.modify_ticket_details.add_extraction_details()
        extraction_details.set_extraction_id("BookExtractionId")
        extraction_details.extract_manual_checkbox_state("book.manualCheckboxState")
        return call(self.book_order_call, self.modify_ticket_details.build())

    def check_error_in_book(self):
        self.modify_ticket_details.set_partial_error_message("error_in_book")
        error = call(self.book_order_call, self.modify_ticket_details.build())
        self.clear_details([self.modify_ticket_details])
        return error

    # endregion
    # region Get
    def extract_block_field(self, column_name, filter_list: list = None, row_number: int = None):
        self.extract_middle_office_blotter_values_request.set_extraction_id("MiddleOfficeExtractionId")
        extraction_detail = ExtractionDetail(column_name, column_name)
        self.extract_middle_office_blotter_values_request.add_extraction_details([extraction_detail])
        if filter_list:
            self.extract_middle_office_blotter_values_request.set_filter(filter_list)
        if row_number:
            self.extract_middle_office_blotter_values_request.set_row_number(row_number)
        response = call(self.extract_middle_office_blotter_values_call,
                        self.extract_middle_office_blotter_values_request.build())
        self.clear_details([self.extract_middle_office_blotter_values_request])
        return response

    def extract_allocate_value(self, column_name, account=None, order_number=1):
        if account is not None:
            self.extract_allocation_details.set_allocations_filter({"Account ID": account})
        extraction_detail = self.extraction_detail(column_name, column_name)
        order_details = self.extract_allocation_details.add_order_details()
        order_details.set_order_number(order_number)
        order_details.add_extraction_details([extraction_detail])
        response = call(self.extract_allocations_table_data, self.extract_allocation_details.build())
        self.clear_details([self.extract_allocation_details])
        return response

    # endregion
    # region Set
    def set_modify_ticket_details(self, is_alloc_amend=False, client=None, trade_date=None, agreed_price=None,
                                  net_gross_ind=None, give_up_broker=None, selected_row_count: int = None, comm_basis=None,
                                  comm_rate=None, remove_comm=False, fee_type=None, fee_basis=None, fee_rate=None,
                                  fee_category=None, remove_fee=False, settl_type=None, settl_date=None,
                                  settl_amount=None, bo_notes=None, settl_currency=None, exchange_rate=None,
                                  exchange_rate_calc=None, toggle_recompute=False, misc_trade_date=None,
                                  bo_fields: list = None, extract_book=False, extract_alloc=False, toggle_manual=False,
                                  arr_allocation_param: [] = None):
        """extract_data can be book or alloc"""
        if selected_row_count is not None:
            self.modify_ticket_details.set_selected_row_count(selected_row_count)
        if is_alloc_amend:
            ticket_details = self.modify_ticket_details.add_amend_allocations_details()
        else:
            ticket_details = self.modify_ticket_details.add_ticket_details()
        if client is not None:
            ticket_details.set_client(client)
        if trade_date is not None:
            ticket_details.set_trade_date(trade_date)
        if agreed_price is not None:
            ticket_details.set_agreed_price(agreed_price)
        if net_gross_ind is not None:
            ticket_details.set_net_gross_ind(net_gross_ind)
        if give_up_broker is not None:
            ticket_details.set_give_up_broker(give_up_broker)
        commission_details = self.modify_ticket_details.add_commissions_details()
        if comm_basis or comm_rate is not None:
            if toggle_manual:
                commission_details.toggle_manual()
            commission_details.add_commission(comm_basis, comm_rate)
        if remove_comm:
            commission_details.remove_commissions()
        fees_details = self.modify_ticket_details.add_fees_details()
        if fee_type or fee_basis or fee_rate or fee_category is not None:
            fees_details.add_fees(fee_type, fee_basis, fee_rate, category=fee_category)
        if remove_fee:
            fees_details.remove_fees()
        settlement_details = self.modify_ticket_details.add_settlement_details()
        if settl_type is not None:
            settlement_details.set_settlement_type(settl_type)
        if settl_date is not None:
            settlement_details.set_settlement_date(settl_date)
        if exchange_rate is not None:
            settlement_details.set_exchange_rate(exchange_rate)
        if exchange_rate_calc is not None:
            settlement_details.set_exchange_rate_calc(exchange_rate_calc)
        if settl_amount is not None:
            settlement_details.set_settlement_amount(settl_amount)
        if settl_currency is not None:
            settlement_details.set_settlement_currency(settl_currency)
        if toggle_recompute:
            settlement_details.toggle_recompute()

        if misc_trade_date or bo_fields or bo_notes is not None:
            misc_details = self.modify_ticket_details.add_misc_details()
            if misc_trade_date is not None:
                misc_details.set_trade_type(misc_trade_date)
            if bo_fields is not None:
                i = 0
                for field in bo_fields:
                    i += 1
                    getattr(misc_details, "set_bo_field_" + str(i))(field)
            if bo_notes is not None:
                misc_details.set_bo_notes_value(bo_notes)
        if extract_book or extract_alloc:
            if extract_book:
                extract_data = "book"
            else:
                extract_data = "alloc"
            extraction_details = self.modify_ticket_details.add_extraction_details()
            extraction_details.set_extraction_id("BookExtractionId")
            extraction_details.extract_net_price(extract_data + ".totalAllocQty")
            extraction_details.extract_net_price(extract_data + ".netPrice")
            extraction_details.extract_net_amount(extract_data + ".netAmount")
            extraction_details.extract_total_comm(extract_data + ".totalComm")
            extraction_details.extract_gross_amount(extract_data + ".grossAmount")
            extraction_details.extract_total_fees(extract_data + ".totalFees")
            extraction_details.extract_agreed_price(extract_data + ".agreedPrice")
            extraction_details.extract_pset_bic(extract_data + ".psetBic")
            extraction_details.extract_exchange_rate(extract_data + ".settlementType")
            extraction_details.extract_settlement_type(extract_data + ".exchangeRate")

        if arr_allocation_param is not None:
            allocation_details = self.modify_ticket_details.add_allocation_details()
            for params_for_allocate in arr_allocation_param:
                allocation_details.add_allocation_param(params_for_allocate)
        return self.modify_ticket_details

    # endregion

    # region Action
    def book_order(self):
        response = call(self.book_order_call, self.modify_ticket_details.build())
        self.clear_details([self.modify_ticket_details])
        return response

    def amend_block(self):
        response = call(self.amend_block_call, self.modify_ticket_details.build())
        self.clear_details([self.modify_ticket_details])
        return response

    def un_book_order(self):
        call(self.unbook_order_call, self.modify_ticket_details.build())
        self.clear_details([self.modify_ticket_details])

    def allocate_block(self):
        response = call(self.allocate_block_call, self.modify_ticket_details.build())
        self.clear_details([self.modify_ticket_details])
        return response

    def amend_allocate(self):
        response = call(self.amend_allocate_call, self.modify_ticket_details.build())
        self.clear_details([self.modify_ticket_details])
        return response

    def unallocate_order(self):
        response = call(self.unallocate_block_call, self.modify_ticket_details.build())
        self.clear_details([self.modify_ticket_details])
        return response

    def view_orders_for_block(self, count: int):
        self.view_order_extraction_details.extract_length("middleOffice.viewOrdersCount")
        for i in range(1, count + 1):
            order_details = self.view_order_extraction_details.add_order_details()
            order_details.set_order_number(i)
            dma_order_id_view = self.extraction_detail("middleOffice.orderId", "Order ID")
            order_details.add_extraction_detail(dma_order_id_view)
        response = call(self.extract_view_orders_table_data_call,
                        self.view_order_extraction_details.build())
        self.clear_details([self.modify_ticket_details])
        return response

    def approve_block(self):
        call(self.approve_block_call, self.view_order_extraction_details.build())
        self.clear_details([self.modify_ticket_details])

    # endregion

    def extract_block_values_from_allocation_ticket(self, filter_dict: dict, list_extraction: list = None):
        self.allocation_ticket_extraction_details = AllocationBlockExtractionDetails(self.base_request,
                                                                                     filter_middle_office_grid=filter_dict,
                                                                                     filter_allocations_grid=None,
                                                                                     panels=list_extraction)
        result = call(self.allocation_ticket_extraction_details_call, self.allocation_ticket_extraction_details.build())
        return result

    def extracting_values_from_amend_ticket(self, filter_dict, list_extraction):
        self.extraction_panel_details = ExtractionPanelDetails(self.base_request,
                                                               filter_dict,
                                                               list_extraction
                                                               )
        result = call(self.amend_ticket_book_extraction_details_call, self.extraction_panel_details.build())
        return result
    '''
    ********************************************************************************************
    FYI(OMS TEAM) list for list_extraction at extract_block_values_from_allocation_ticket method
    [
    PanelForExtraction.MAIN_PANEL,
    PanelForExtraction.SETTLEMENT,
    PanelForExtraction.COMMISSION,
    PanelForExtraction.FEES,
    PanelForExtraction.MISC
    ]
    ********************************************************************************************
    '''
