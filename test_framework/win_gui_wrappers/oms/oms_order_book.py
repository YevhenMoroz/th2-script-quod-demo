from th2_grpc_act_gui_quod import middle_office_pb2, common_pb2
from th2_grpc_act_gui_quod.act_ui_win_pb2 import ExtractDirectsValuesRequest
from th2_grpc_act_gui_quod.common_pb2 import ScrollingOperation
from th2_grpc_act_gui_quod.order_book_pb2 import ReassignOrderDetails, GroupModifyDetails

from stubs import Stubs
from test_framework.win_gui_wrappers.base_order_book import BaseOrderBook
from win_gui_modules.common_wrappers import GridScrollingDetails, RowsNumbersForGrid, CommissionsDetails
from win_gui_modules.middle_office_wrappers import TicketDetails, SettlementDetails, FeesDetails, MiscDetails
from win_gui_modules.order_book_wrappers import OrdersDetails, OrderInfo, CancelOrderDetails, ModifyOrderDetails, \
    MenuItemDetails, SuspendOrderDetails, BaseOrdersDetails, MassExecSummaryAveragePriceDetails, DiscloseFlagDetails, \
    AddToBasketDetails, CreateBasketDetails, ManualExecutingDetails, SecondLevelTabDetails, \
    SecondLevelExtractionDetails, SplitBookingDetails, ManualCrossDetails, TransferOrderDetails, \
    TransferPoolDetailsCLass, InternalTransferActionDetails, MassManualExecutionDetails, \
    UnmatchAndTransferDetails, SubLvlInfo, GetSubLvlDetails, MassExecSummaryDetails, QuickButtonCreationDetails, \
    ActionsHotKeysDetails, ForceCancelOrderDetails
from win_gui_modules.order_ticket_wrappers import NewOrderDetails


class OMSOrderBook(BaseOrderBook):
    # region Constructor
    def __init__(self, case_id, session_id):
        super().__init__(case_id, session_id)
        self.order_info = OrderInfo()
        self.order_details = OrdersDetails()
        self.set_order_details()
        self.scrolling_details = GridScrollingDetails()
        self.new_order_details = NewOrderDetails(self.base_request)
        self.menu_item_details = MenuItemDetails(self.base_request)
        self.base_order_details = BaseOrdersDetails(self.base_request)
        self.scrolling_operation = ScrollingOperation
        self.modify_order_details = ModifyOrderDetails(self.base_request)
        self.manual_cross_details = ManualCrossDetails(self.base_request)
        self.cancel_order_details = CancelOrderDetails(self.base_request)
        self.rows_numbers_for_grid = RowsNumbersForGrid(self.base_request)
        self.suspend_order_details = SuspendOrderDetails(self.base_request)
        self.disclose_flag_details = DiscloseFlagDetails(self.base_request)
        self.add_to_basket_details = AddToBasketDetails(self.base_request)
        self.create_basket_details = CreateBasketDetails(self.base_request)
        self.quick_button_details = QuickButtonCreationDetails(self.base_request)
        self.reassign_order_details = ReassignOrderDetails()
        self.manual_executing_details = ManualExecutingDetails(self.base_request)
        self.second_level_tab_details = SecondLevelTabDetails()
        self.second_level_extraction_details = SecondLevelExtractionDetails()
        self.mass_exec_summary_average_price_detail = MassExecSummaryAveragePriceDetails(self.base_request)
        self.mass_exec_summary_detail = MassExecSummaryDetails(self.base_request)
        self.extraction_error_message_details = ExtractDirectsValuesRequest.DirectsExtractedValue()
        self.extract_direct_values = ExtractDirectsValuesRequest()
        self.hot_keys_details = ActionsHotKeysDetails(self.base_request)
        self.extraction_from_second_level_tabs_call = Stubs.win_act_order_book.extractionFromSecondLevelTabs
        self.mass_exec_summary_average_price_call = Stubs.win_act_order_book.massExecSummaryAtAveragePrice
        self.mass_exec_summary_call = Stubs.win_act_order_book.massExecSummary
        self.extract_booking_block_values_call = Stubs.win_act_order_book.extractBookingBlockValues
        self.direct_moc_request_correct_call = Stubs.win_act_order_book.orderBookDirectMoc
        self.direct_child_care_call = Stubs.win_act_order_book.orderBookDirectChildCare
        self.order_book_grid_scrolling_call = Stubs.win_act_order_book.orderBookGridScrolling
        self.manual_execution_order_call = Stubs.win_act_order_book.manualExecution
        self.house_fill_call = Stubs.win_act_order_book.houseFill
        self.is_menu_item_present_call = Stubs.win_act_order_book.isMenuItemPresent
        self.group_modify_order_call = Stubs.win_act_order_book.groupModify
        self.get_orders_details_call = Stubs.win_act_order_book.getOrdersDetails
        self.un_complete_order_call = Stubs.win_act_order_book.unCompleteOrder
        self.notify_dfd_order_call = Stubs.win_act_order_book.notifyDFD
        self.check_out_order_call = Stubs.win_act_order_book.checkOutOrder
        self.reassign_order_call = Stubs.win_act_order_book.reassignOrder
        self.complete_order_call = Stubs.win_act_order_book.completeOrder
        self.check_in_order_call = Stubs.win_act_order_book.checkInOrder
        self.suspend_order_call = Stubs.win_act_order_book.suspendOrder
        self.release_order_call = Stubs.win_act_order_book.releaseOrder
        self.disclose_flag_call = Stubs.win_act_order_book.discloseFlag
        self.add_to_basket_call = Stubs.win_act_order_book.addToBasket
        self.create_basket_call = Stubs.win_act_order_book.createBasket
        self.cancel_order_call = Stubs.win_act_order_book.cancelOrder
        self.refresh_order_call = Stubs.win_act_order_book.refreshOrder
        self.manual_cross_call = Stubs.win_act_order_book.manualCross
        self.mass_unbook_call = Stubs.win_act_order_book.massUnbook
        self.mass_book_call = Stubs.win_act_order_book.massBook
        self.ticket_details = TicketDetails(middle_office_pb2.TicketDetails())
        self.settlement_details = SettlementDetails(middle_office_pb2.SettlementDetails())
        self.commissions_details = CommissionsDetails(common_pb2.CommissionsDetails())
        self.fees_details = FeesDetails(middle_office_pb2.FeesDetails())
        self.misc_details = MiscDetails(middle_office_pb2.MiscDetails())
        self.split_booking_details = SplitBookingDetails(self.base_request)
        self.split_booking_call = Stubs.win_act_order_book.splitBooking
        self.direct_loc_request_correct_call = Stubs.win_act_order_book.orderBookDirectLoc
        self.mass_book_details = RowsNumbersForGrid(self.base_request)
        self.mass_book_call = Stubs.win_act_order_book.massBook
        self.transfer_order_details = TransferOrderDetails()
        self.transfer_order_call = Stubs.win_act_order_book.transferOrder
        self.transfer_pool_details = TransferPoolDetailsCLass()
        self.transfer_pool_call = Stubs.care_orders_action.internalTransferAction
        self.internal_transfer_action = InternalTransferActionDetails(self.base_request, self.transfer_pool_details.build())
        self.group_modify_details = GroupModifyDetails()
        self.direct_order_correct_call = Stubs.win_act_order_book.orderBookDirectOrder
        self.mass_manual_execution_call = Stubs.win_act_order_book.massManualExecution
        self.mass_manual_execution_details = MassManualExecutionDetails(self.base_request)
        self.direct_child_care_call = Stubs.win_act_order_book.orderBookDirectChildCare
        self.unmatch_and_transfer_details = UnmatchAndTransferDetails(self.base_request)
        self.unmatch_and_transfer_call = Stubs.win_act_order_book.unmatchAndTransfer
        self.get_empty_rows_call = Stubs.win_act_order_book.checkIfOBGridHaveNoRows
        self.sub_lvl_info_details = SubLvlInfo()
        self.get_sub_lvl_details = GetSubLvlDetails(self.base_request)
        self.extract_sub_lvl_details_call = Stubs.win_act_order_book.extractSubLvlDetails
        self.exec_summary_call = Stubs.win_act_order_book.execSummary
        self.create_quick_button_call = Stubs.win_act_order_book.createSplitShortcutCreationButton
        self.edit_quick_button_call = Stubs.win_act_order_book.editSplitShortcutCreationButton
        self.click_quick_button_call = Stubs.win_act_order_book.clickSplitShortcutCreationButton
        self.hot_keys_action_call = Stubs.win_act_order_book.selectedRowInOrderBook
        self.force_cancel_order_call = Stubs.win_act_order_book.forceCancelOrder
        self.force_cancel_order_details = ForceCancelOrderDetails(self.base_request)
        self.mark_reviewed_call = Stubs.win_act_order_book.markReviewed
        self.mark_unreviewed_call = Stubs.win_act_order_book.markUnreviewed
        # endregion
