from stubs import Stubs
from test_framework.win_gui_wrappers.base_order_book_archive import BaseOrderBookArchive
from win_gui_modules.order_book_archive_wrappers import OrderBookArchiveDetails


class OMSOrderBookArchive(BaseOrderBookArchive):
    # region Base constructor
    def __init__(self, case_id, session_id):
        super().__init__(case_id, session_id)
        self.order_book_archive_details = OrderBookArchiveDetails(self.base_request)
        self.import_order_from_db_call = Stubs.win_act_order_book_archive.importOrderFromDb
        # Need to override