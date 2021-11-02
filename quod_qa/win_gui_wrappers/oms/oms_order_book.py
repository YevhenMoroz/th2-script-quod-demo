from th2_grpc_act_gui_quod.order_book_pb2 import ReassignOrderDetails
from win_gui_modules.common_wrappers import GridScrollingDetails
from quod_qa.win_gui_wrappers.base_order_book import BaseOrderBook
from th2_grpc_act_gui_quod.common_pb2 import ScrollingOperation
from stubs import Stubs
from win_gui_modules.order_book_wrappers import OrdersDetails, OrderInfo, CancelOrderDetails, ModifyOrderDetails, \
    MenuItemDetails, SuspendOrderDetails, BaseOrdersDetails, MassExecSummaryAveragePriceDetails, DiscloseFlagDetails, \
    AddToBasketDetails, CreateBasketDetails, ManualExecutingDetails, SecondLevelTabDetails, SecondLevelExtractionDetails
from win_gui_modules.order_ticket_wrappers import NewOrderDetails


class OMSOrderBook(BaseOrderBook):
    # region Constructor
    def __init__(self, case_id, base_request):
        super().__init__(case_id, base_request)
        self.order_info = OrderInfo()
        self.order_details = OrdersDetails()
        self.set_order_details()
        self.scrolling_details = GridScrollingDetails()
        self.new_order_details = NewOrderDetails(base_request)
        self.menu_item_details = MenuItemDetails(base_request)
        self.base_order_details = BaseOrdersDetails(base_request)
        self.scrolling_operation = ScrollingOperation
        self.modify_order_details = ModifyOrderDetails(base_request)
        self.cancel_order_details = CancelOrderDetails(base_request)
        self.suspend_order_details = SuspendOrderDetails(base_request)
        self.disclose_flag_details = DiscloseFlagDetails(base_request)
        self.add_to_basket_details = AddToBasketDetails(base_request)
        self.create_basket_details = CreateBasketDetails(base_request)
        self.reassign_order_details = ReassignOrderDetails()
        self.manual_executing_details = ManualExecutingDetails(base_request)
        self.second_level_tab_details = SecondLevelTabDetails()
        self.second_level_extraction_details = SecondLevelExtractionDetails()
        self.mass_exec_summary_average_price_detail = MassExecSummaryAveragePriceDetails(base_request)
        self.extraction_from_second_level_tabs_call = Stubs.win_act_order_book.extractionFromSecondLevelTabs
        self.mass_exec_summary_average_price_call = Stubs.win_act_order_book.massExecSummaryAtAveragePrice
        self.order_book_grid_scrolling_call = Stubs.win_act_order_book.orderBookGridScrolling
        self.manual_execution_order_call = Stubs.win_act_order_book.manualExecution
        self.is_menu_item_present_call = Stubs.win_act_order_book.isMenuItemPresent
        self.get_orders_details_call = Stubs.win_act_order_book.getOrdersDetails
        self.group_modify_order_call = Stubs.win_act_order_book.groupModify
        self.un_complete_order_call = Stubs.win_act_order_book.unCompleteOrder
        self.check_out_order_call = Stubs.win_act_order_book.checkOutOrder
        self.check_in_order_call = Stubs.win_act_order_book.checkInOrder
        self.notify_dfd_order_call = Stubs.win_act_order_book.notifyDFD
        self.reassign_order_call = Stubs.win_act_order_book.reassignOrder
        self.complete_order_call = Stubs.win_act_order_book.completeOrder
        self.suspend_order_call = Stubs.win_act_order_book.suspendOrder
        self.release_order_call = Stubs.win_act_order_book.releaseOrder
        self.disclose_flag_call = Stubs.win_act_order_book.discloseFlag
        self.create_basket_call = Stubs.win_act_order_book.createBasket
        self.cancel_order_call = Stubs.win_act_order_book.cancelOrder
    # endregion

