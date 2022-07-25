from test_framework.win_gui_wrappers.base_window import BaseWindow
from win_gui_modules.utils import call


class BaseTradeBookArchive(BaseWindow):
    # region Base constructor
    def __init__(self, case_id, session_id):
        super().__init__(case_id, session_id)
        self.trade_book_archive_details = None
        self.import_trade_from_db_call = None
        # Need to override

    # endregion
    # region Actions
    def import_trade_from_db(self, creation_date_from=None, creation_date_until=None, client=None, side=None,
                             venue=None, execution_flag=None, sec_account=None, instr_symbol=None, cl_ord_id=None,
                             ord_id=None, execution_id=None, venue_execution_id=None, client_group=None, owner=None,
                             security_id_source=None, security_id=None, remove_all=False, filter_dict=None,
                             column_names=None, get_total_orders=False):
        self.trade_book_archive_details.set_creation_date_from(creation_date_from)
        self.trade_book_archive_details.set_creation_date_until(creation_date_until)
        self.trade_book_archive_details.set_client(client)
        self.trade_book_archive_details.set_side(side)
        self.trade_book_archive_details.set_venue(venue)
        self.trade_book_archive_details.set_exec_flag(execution_flag)
        self.trade_book_archive_details.set_security_account(sec_account)
        self.trade_book_archive_details.set_instrument_symbol(instr_symbol)
        self.trade_book_archive_details.set_client_order_id(cl_ord_id)
        self.trade_book_archive_details.set_quod_order_id(ord_id)
        self.trade_book_archive_details.set_execution_id(execution_id)
        self.trade_book_archive_details.set_venue_execution_id(venue_execution_id)
        self.trade_book_archive_details.set_client_group(client_group)
        self.trade_book_archive_details.set_owner(owner)
        self.trade_book_archive_details.set_security_id_source(security_id_source)
        self.trade_book_archive_details.set_security_id(security_id)
        self.trade_book_archive_details.set_remove_all(remove_all)
        self.trade_book_archive_details.set_filter(filter_dict)
        self.trade_book_archive_details.set_column_names(column_names)
        self.trade_book_archive_details.get_row_count(get_total_orders)
        result = call(self.import_trade_from_db_call, self.trade_book_archive_details.build())
        self.clear_details([self.trade_book_archive_details])
        return result
    # endregion
