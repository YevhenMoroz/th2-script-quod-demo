from stubs import Stubs
from test_framework.win_gui_wrappers.base_child_order_book import BaseChildOrderBook
from win_gui_modules.child_order_book_wrappers import ExtractChildOrderBookDataDetails, ExtractSubLvlDataDetails


class OMSChildOrderBook(BaseChildOrderBook):
    def __init__(self, case_id, session_id):
        super().__init__(case_id, session_id)
        self.extract_child_order_book_data_details = ExtractChildOrderBookDataDetails()
        self.extract_child_order_book_sub_lvl_data_details = ExtractSubLvlDataDetails()
        self.extract_child_order_book_data_call = Stubs.win_act_child_order_book.extractChildOrderBookData
        self.extract_child_order_book_sub_lvl_data_call = Stubs.win_act_child_order_book.extractChildOrderBookSubLvlData
        self.check_that_order_is_absent_call = Stubs.win_act_child_order_book.checkIfCOBGridHaveNoRows
