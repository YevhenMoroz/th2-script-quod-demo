import typing

from test_framework.win_gui_wrappers.base_window import BaseWindow
from win_gui_modules.middle_office_wrappers import AllocationBlockExtractionDetails, ExtractionPanelDetails,  ModifyTicketDetails
from win_gui_modules.order_book_wrappers import ExtractionDetail
from win_gui_modules.utils import call


class BaseMiddleOffice(BaseWindow):
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
        self.mass_approve_details = None
        self.mass_approve_call = None
        self.mass_allocate_call = None
        self.mass_unallocate_call = None
        self.extract_value_from_tab_of_allocation_ticket_call = None
        self.override_confirmation_service_call = None
        self.booking_ticket_closing_and_opening_details = None
        self.only_open_booking_ticket_call = None
        self.only_set_details_in_booking_ticket_call = None
        self.only_extraction_from_booking_ticket_call = None
        self.only_closing_booking_ticket_call = None
        self.internal_extraction_details = None
        self.extract_allocation_sub_lvl_data_details = None
        self.extract_value_from_second_level_of_allocation = None

    # endregion
    # region Common func

    def set_filter(self, filter_list: list):
        self.extract_middle_office_blotter_values_request.set_filter(filter_list)

    def clear_filter(self):
        self.extract_middle_office_blotter_values_request.clear_filter()

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

    def extract_list_of_block_fields(self, list_of_column: list, filter_list: list = None, row_number=1) -> dict:
        self.extract_middle_office_blotter_values_request.set_extraction_id("MiddleOfficeExtractionId")
        list_of_extraction = []
        for column in list_of_column:
            field = self.extraction_detail(column, column)
            list_of_extraction.append(field)
        if filter_list:
            self.extract_middle_office_blotter_values_request.set_filter(filter_list)
        self.extract_middle_office_blotter_values_request.add_extraction_details(list_of_extraction)
        if row_number:
            self.extract_middle_office_blotter_values_request.set_row_number(row_number)
        response = call(self.extract_middle_office_blotter_values_call,
                        self.extract_middle_office_blotter_values_request.build())
        self.clear_details([self.extract_middle_office_blotter_values_request])
        return response

    def extract_list_of_allocate_fields(self, list_of_column: list, filter_dict_allocate: dict = None,
                                        allocate_number=1, filter_dict_block: dict = None,
                                        clear_filter_from_allocation: bool = False,
                                        clear_filter_from_block=False) -> dict:
        list_of_extraction = []
        for column in list_of_column:
            field = self.extraction_detail(column, column)
            list_of_extraction.append(field)
        if filter_dict_allocate:
            self.extract_allocation_details.set_allocations_filter(filter_dict_allocate)
        if filter_dict_block:
            self.extract_allocation_details.set_block_filter(filter_dict_block)
        order_details = self.extract_allocation_details.add_order_details()
        order_details.set_order_number(allocate_number)
        order_details.add_extraction_details(list_of_extraction)
        if clear_filter_from_allocation:
            order_details.clear_filter()
        if clear_filter_from_block:
            order_details.clear_filter_from_book()
        response = call(self.extract_allocations_table_data,
                        self.extract_allocation_details.build())
        self.clear_details([self.extract_allocation_details])
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

    def extract_values_from_amend_allocation_ticket(self, panels_extraction: list = None,
                                                    block_panels_extraction: list = None,
                                                    block_filter_dict: dict = None, alloc_filter_dict: dict = None):
        self.allocation_ticket_extraction_details = AllocationBlockExtractionDetails(self.base_request)
        if block_filter_dict is not None:
            self.allocation_ticket_extraction_details.set_filter_middle_office_grid(block_filter_dict)
        self.allocation_ticket_extraction_details.set_filter_allocations_grid(alloc_filter_dict)
        self.allocation_ticket_extraction_details.set_panels(panels_extraction)
        self.allocation_ticket_extraction_details.set_block_panels(block_panels_extraction)
        result = call(self.allocation_ticket_extraction_details_call, self.allocation_ticket_extraction_details.build())
        return result

    def extracting_values_from_amend_ticket(self, list_extraction, filter_dict=None):
        self.extraction_panel_details = ExtractionPanelDetails(self.base_request,
                                                               filter_dict,
                                                               list_extraction
                                                               )
        result = call(self.amend_ticket_book_extraction_details_call, self.extraction_panel_details.build())
        return result

    def extracting_values_from_allocation_ticket(self, panels_extraction: list, block_filter_dict: dict):
        self.allocation_ticket_extraction_details = AllocationBlockExtractionDetails(self.base_request)
        self.allocation_ticket_extraction_details.set_filter_middle_office_grid(block_filter_dict)
        self.allocation_ticket_extraction_details.set_panels(panels_extraction)
        result = call(self.extract_value_from_tab_of_allocation_ticket_call,
                      self.allocation_ticket_extraction_details.build())
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

    # endregion
    # region Set
    def set_modify_ticket_details(self, is_alloc_amend=False, client=None, trade_date=None, agreed_price=None,
                                  net_gross_ind=None, give_up_broker=None, selected_row_count: int = None,
                                  comm_basis=None,
                                  comm_rate=None, remove_comm=False, fee_type=None, fee_basis=None, fee_rate=None,
                                  fee_category=None, remove_fee=False, settl_type=None, settl_date=None,
                                  settl_amount=None, bo_notes=None, settl_currency=None, exchange_rate=None,
                                  exchange_rate_calc=None, toggle_recompute=False, misc_trade_date=None,
                                  bo_fields: list = None, extract_book=False, extract_alloc=False, toggle_manual=False,
                                  alloc_account_filter=None, alloc_row_number: int = None, arr_allocation_param=None,
                                  clear_alloc_greed=False, pset=None, clear_filter=False, net_price: str = None):
        """
            1)extract_data can be book or alloc
            2)example of arr_allocation_param:param=[{"Security Account": "YM_client_SA1", "Alloc Qty": "200"},
           {"Security Account": "YM_client_SA2", "Alloc Qty": "200"}]
        """
        if selected_row_count is not None:
            self.modify_ticket_details.set_selected_row_count(selected_row_count)
        if clear_filter:
            self.modify_ticket_details.clear_filter()
        if is_alloc_amend:
            amend_allocations_details = self.modify_ticket_details.add_amend_allocations_details()
            if alloc_account_filter is not None:
                amend_allocations_details.set_filter({"Account ID": alloc_account_filter})
            if alloc_row_number is not None:
                amend_allocations_details.set_row_number(alloc_row_number)
        ticket_details = self.modify_ticket_details.add_ticket_details()
        allocations_details = self.modify_ticket_details.add_allocations_details()
        if arr_allocation_param is not None:
            for i in arr_allocation_param:
                allocations_details.add_allocation_param(i)
        if clear_alloc_greed:
            allocations_details.clear_greed()
        if net_price:
            ticket_details.set_net_price(net_price)
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
        if comm_basis or comm_rate is not None or remove_comm:
            commission_details = self.modify_ticket_details.add_commissions_details()
            if toggle_manual:
                commission_details.toggle_manual()
            if comm_basis or comm_rate is not None:
                commission_details.add_commission(comm_basis, comm_rate)
            if remove_comm:
                commission_details.remove_commissions()

        if fee_type or fee_basis or fee_rate or fee_category is not None or remove_fee:
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
        if settl_amount is not None:
            settlement_details.set_settlement_amount(settl_amount)
        if settl_currency is not None:
            settlement_details.set_settlement_currency(settl_currency)
        if exchange_rate is not None:
            settlement_details.set_exchange_rate(exchange_rate)
        if exchange_rate_calc is not None:
            settlement_details.set_exchange_rate_calc(exchange_rate_calc)
        if pset:
            settlement_details.set_pset(pset)
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
            extraction_details.extract_exchange_rate(extract_data + ".exchangeRate")
            extraction_details.extract_settlement_type(extract_data + ".settlementType")
            extraction_details.extract_fees_row(extract_data + ".Fees")
            extraction_details.extract_commission_row(extract_data + ".Commission")
        return self.modify_ticket_details

    # endregion

    # region Action
    def book_order(self, filter: typing.List[str] = None):
        if filter:
            self.modify_ticket_details.set_filter(filter)
        response = call(self.book_order_call, self.modify_ticket_details.build())
        self.clear_details([self.modify_ticket_details])
        return response

    def amend_block(self, filter: typing.List[str] = None):
        if filter:
            self.modify_ticket_details.set_filter(filter)
        response = call(self.amend_block_call, self.modify_ticket_details.build())
        self.clear_details([self.modify_ticket_details])
        return response

    def un_book_order(self, filter: typing.List[str] = None):
        if filter:
            self.modify_ticket_details.set_filter(filter)
        call(self.unbook_order_call, self.modify_ticket_details.build())
        self.clear_details([self.modify_ticket_details])

    def allocate_block(self, filter: typing.List[str] = None):
        if filter:
            self.modify_ticket_details.set_filter(filter)
        response = call(self.allocate_block_call, self.modify_ticket_details.build())
        self.clear_details([self.modify_ticket_details])
        return response

    def amend_allocate(self, filter: typing.List[str] = None):
        if filter:
            self.modify_ticket_details.set_filter(filter)
        response = call(self.amend_allocate_call, self.modify_ticket_details.build())
        self.clear_details([self.modify_ticket_details])
        return response

    def unallocate_order(self, filter: typing.List[str] = None):
        if filter:
            self.modify_ticket_details.set_filter(filter)
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

    def approve_block(self, filter_list: typing.List[str] = None):
        if filter_list:
            self.modify_ticket_details.set_filter(filter_list)
        call(self.approve_block_call, self.modify_ticket_details.build())
        self.clear_details([self.modify_ticket_details])

        '''
        positions_of_block = [1,2,3,4], something like it
        '''

    def mass_approve(self, positions_of_block: list):
        self.mass_approve_details.set_rows_number(positions_of_block)
        call(self.mass_approve_call, self.mass_approve_details.build())
        self.clear_details([self.mass_approve_details])

    def mass_allocate(self, positions_of_block: list):
        self.mass_approve_details.set_rows_number(positions_of_block)
        call(self.mass_allocate_call, self.mass_approve_details.build())
        self.clear_details([self.mass_approve_details])

    def mass_unallocate(self, position_of_block: list):
        self.mass_approve_details.set_rows_number(position_of_block)
        call(self.mass_unallocate_call, self.mass_approve_details.build())
        self.clear_details([self.mass_approve_details])

    # endregion

    def check_error_in_book(self):
        self.modify_ticket_details.set_partial_error_message("error_in_book")
        error = call(self.book_order_call, self.modify_ticket_details.build())
        self.clear_details(self.modify_ticket_details)
        return error

    def override_confirmation_service(self, filter_dict: dict = None):
        if filter_dict is not None:
            self.mass_approve_details.set_filter(filter_dict)
        call(self.override_confirmation_service_call, self.mass_approve_details.build())
        self.clear_details([self.mass_approve_details])

    def only_opening_booking_ticket(self, selected_row: int = 1, filter_dict: dict = None):
        if filter_dict is not None:
            self.booking_ticket_closing_and_opening_details.set_filter(filter_dict)
        self.booking_ticket_closing_and_opening_details.set_selected_row(selected_row)
        call(self.only_open_booking_ticket_call, self.booking_ticket_closing_and_opening_details.build())
        self.clear_details([self.booking_ticket_closing_and_opening_details])

    def only_set_details_to_booking_ticket(self, details: ModifyTicketDetails):
        call(self.only_set_details_in_booking_ticket_call, details.build())
        self.clear_details([self.modify_ticket_details])

    def only_extract_value_from_booking_ticket(self, list_extraction):
        self.extraction_panel_details = ExtractionPanelDetails(self.base_request, panels=list_extraction)
        result = call(self.only_extraction_from_booking_ticket_call, self.extraction_panel_details.build())
        self.clear_details([self.extraction_panel_details])
        return result

    def only_close_booking_ticket(self):
        call(self.only_closing_booking_ticket_call, self.booking_ticket_closing_and_opening_details.build())

    def set_extract_sub_lvl_fields(self, column_names: list, tab_name, row_count: int):
        self.internal_extraction_details.set_default_params(self.base_request)
        self.internal_extraction_details.set_column_names(column_names)
        self.internal_extraction_details.set_tab_name(tab_name)
        self.internal_extraction_details.set_row_number(row_count)

    def extract_allocation_sub_lvl(self, block_filter: dict, allocation_filter: dict):
        self.extract_allocation_sub_lvl_data_details.set_internal_extraction_details(
            self.internal_extraction_details.build())
        self.extract_allocation_sub_lvl_data_details.set_allocation_filter(allocation_filter)
        self.extract_allocation_sub_lvl_data_details.set_block_filter(block_filter)
        result = call(self.extract_value_from_second_level_of_allocation,
                      self.extract_allocation_sub_lvl_data_details.build())
        self.clear_details([self.internal_extraction_details, self.extract_allocation_sub_lvl_data_details])
        return result
