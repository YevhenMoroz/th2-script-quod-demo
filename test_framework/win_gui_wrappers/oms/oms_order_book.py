from th2_grpc_act_gui_quod.common_pb2 import ScrollingOperation
from th2_grpc_act_gui_quod.order_book_pb2 import ReassignOrderDetails

from test_framework.win_gui_wrappers.base_order_book import BaseOrderBook
from stubs import Stubs
from win_gui_modules.common_wrappers import GridScrollingDetails
from win_gui_modules.order_book_wrappers import OrdersDetails, OrderInfo, CancelOrderDetails, ModifyOrderDetails, \
    MenuItemDetails, SuspendOrderDetails, BaseOrdersDetails, MassExecSummaryAveragePriceDetails, DiscloseFlagDetails, \
    AddToBasketDetails, CreateBasketDetails, ManualExecutingDetails, SecondLevelTabDetails, SecondLevelExtractionDetails
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
        self.cancel_order_details = CancelOrderDetails(self.base_request)
        self.rows_numbers_for_grid = None
        self.suspend_order_details = SuspendOrderDetails(self.base_request)
        self.disclose_flag_details = DiscloseFlagDetails(self.base_request)
        self.add_to_basket_details = AddToBasketDetails(self.base_request)
        self.create_basket_details = CreateBasketDetails(self.base_request)
        self.reassign_order_details = ReassignOrderDetails()
        self.manual_executing_details = ManualExecutingDetails(self.base_request)
        self.second_level_tab_details = SecondLevelTabDetails()
        self.second_level_extraction_details = SecondLevelExtractionDetails()
        self.mass_exec_summary_average_price_detail = MassExecSummaryAveragePriceDetails(self.base_request)
        self.extraction_from_second_level_tabs_call = Stubs.win_act_order_book.extractionFromSecondLevelTabs
        self.mass_exec_summary_average_price_call = Stubs.win_act_order_book.massExecSummaryAtAveragePrice
        self.order_book_grid_scrolling_call = Stubs.win_act_order_book.orderBookGridScrolling
        self.manual_execution_order_call = Stubs.win_act_order_book.manualExecution
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
        self.add_to_basket_call = None
        self.create_basket_call = Stubs.win_act_order_book.createBasket
        self.cancel_order_call = Stubs.win_act_order_book.cancelOrder
        self.mass_unbook_call = None
        self.extract_booking_block_values_call = Stubs.win_act_order_book.extractBookingBlockValues
        self.direct_moc_request_correct_call = Stubs.win_act_order_book.orderBookDirectMoc
        self.direct_loc_request_correct_call = Stubs.win_act_order_book.orderBookDirectLoc
    # endregion
