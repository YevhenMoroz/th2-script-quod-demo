from quod_qa.win_gui_wrappers.base_trades_book import BaseTradesBook
from stubs import Stubs
from win_gui_modules.order_book_wrappers import OrderInfo, OrdersDetails
from win_gui_modules.trades_blotter_wrappers import MatchDetails, ModifyTradesDetails, CancelManualExecutionDetails


class OMSTradesBook(BaseTradesBook):
    # region Base constructor
    def __init__(self, case_id, base_request):
        super().__init__(case_id, base_request)
        # Need to override
        self.order_info = OrderInfo()
        self.order_details = OrdersDetails()
        self.set_order_details()
        self.match_details = MatchDetails()
        self.modify_trades_details = ModifyTradesDetails()
        self.cancel_manual_execution_details = CancelManualExecutionDetails()
        self.manual_match_call = Stubs.win_act_trades.manualMatch
        self.cancel_manual_execution_call = Stubs.win_act_trades.cancelManualExecution
        self.get_trade_book_details_call = Stubs.win_act_order_book.getTradeBookDetails
