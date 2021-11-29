from test_framework.win_gui_wrappers.base_middle_office_book import BaseMiddleOfficeBook
from stubs import Stubs
from win_gui_modules.middle_office_wrappers import ModifyTicketDetails, ViewOrderExtractionDetails, \
    ExtractMiddleOfficeBlotterValuesRequest, AllocationsExtractionDetails
from win_gui_modules.order_book_wrappers import ExtractionDetail


class OMSMiddleOfficeBook(BaseMiddleOfficeBook):
    # region Base constructor
    def __init__(self, case_id, session_id):
        super().__init__(case_id, session_id)
        # Need to override
        self.extraction_detail = ExtractionDetail
        self.modify_ticket_details = ModifyTicketDetails(self.base_request)
        self.view_order_extraction_details = ViewOrderExtractionDetails(self.base_request)
        self.extract_middle_office_blotter_values_request = ExtractMiddleOfficeBlotterValuesRequest(self.base_request)
        self.book_order_call = Stubs.win_act_middle_office_service.bookOrder
        self.amend_block_call = Stubs.win_act_middle_office_service.amendMiddleOfficeTicket
        self.unbook_order_call = Stubs.win_act_middle_office_service.unBookOrder
        self.approve_block_call = Stubs.win_act_middle_office_service.approveMiddleOfficeTicket
        self.amend_allocate_call = Stubs.win_act_middle_office_service.amendAllocations
        self.allocate_block_call = Stubs.win_act_middle_office_service.allocateMiddleOfficeTicket
        self.unallocate_block_call = Stubs.win_act_middle_office_service.unAllocateMiddleOfficeTicket
        self.extract_view_orders_table_data_call = Stubs.win_act_middle_office_service.extractViewOrdersTableData
        self.extract_middle_office_blotter_values_call = Stubs.win_act_middle_office_service.extractMiddleOfficeBlotterValues
        self.extract_allocation_details = AllocationsExtractionDetails(self.base_request)
        self.extract_allocations_table_data = Stubs.win_act_middle_office_service.extractAllocationsTableData
        # endregion