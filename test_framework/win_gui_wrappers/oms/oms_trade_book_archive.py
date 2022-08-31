from stubs import Stubs
from test_framework.win_gui_wrappers.base_trade_book_archive import BaseTradeBookArchive
from win_gui_modules.trade_book_archive_wrappers import TradeBookArchiveDetails


class OMSTradeBookArchive(BaseTradeBookArchive):
    # region Base constructor
    def __init__(self, case_id, session_id):
        super().__init__(case_id, session_id)
        self.trade_book_archive_details = TradeBookArchiveDetails(self.base_request)
        self.import_trade_from_db_call = Stubs.win_act_trade_book_archive.importTradeFromDb
        # Need to override