from test_framework.win_gui_wrappers.base_middle_office import BaseMiddleOffice
from stubs import Stubs
from win_gui_modules.middle_office_wrappers import ModifyTicketDetails, ViewOrderExtractionDetails, \
    ExtractMiddleOfficeBlotterValuesRequest, AllocationsExtractionDetails, AllocationBlockExtractionDetails, \
    MassApproveDetails
from win_gui_modules.order_book_wrappers import ExtractionDetail


class OMSMiddleOffice(BaseMiddleOffice):
    # region Base constructor
    def __init__(self, case_id, session_id):
        super().__init__(case_id, session_id)
        # Need to override
        self.extraction_detail = ExtractionDetail
        self.modify_ticket_details = ModifyTicketDetails(self.base_request)
        self.view_order_extraction_details = ViewOrderExtractionDetails(self.base_request)
        self.extract_middle_office_blotter_values_request = ExtractMiddleOfficeBlotterValuesRequest(self.base_request)
        self.allocation_ticket_extraction_details_call = Stubs.win_act_middle_office_service.extractAllocationBlockValues
        self.amend_ticket_book_extraction_details_call = Stubs.win_act_middle_office_service.extractAmendBlockValues
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
        self.mass_approve_details = MassApproveDetails(self.base_request)
        self.mass_approve_call = Stubs.win_act_middle_office_service.massApprove
        self.mass_allocate_call = Stubs.win_act_middle_office_service.massAllocate
        self.mass_unallocate_call = Stubs.win_act_middle_office_service.massUnAllocate
        self.extract_value_from_tab_of_allocation_ticket_call = Stubs.win_act_middle_office_service.extractAllocationBlockValuesAllocationTicket
        # endregion