from test_framework.win_gui_wrappers.base_window import BaseWindow
from win_gui_modules.utils import call


class BaseOrderBookArchive(BaseWindow):
    # region Base constructor
    def __init__(self, case_id, session_id):
        super().__init__(case_id, session_id)
        self.order_book_archive_details = None
        self.import_order_from_db_call = None
        # Need to override

    # endregion
    # region Actions
    def import_order_from_db(self, creation_date_from=None, creation_date_until=None, client=None, side=None,
                             ord_status=None, exec_policy=None, sec_account=None, instr_symbol=None, cl_ord_id=None,
                             ord_id=None, client_group=None, owner=None, route=None, venue=None,
                             security_id_source=None, security_id=None, remove_all=False, filter_dict=None,
                             column_names=None, get_total_orders=False):
        self.order_book_archive_details.set_creation_date_from(creation_date_from)
        self.order_book_archive_details.set_creation_date_until(creation_date_until)
        self.order_book_archive_details.set_client(client)
        self.order_book_archive_details.set_side(side)
        self.order_book_archive_details.set_status(ord_status)
        self.order_book_archive_details.set_execution_policy(exec_policy)
        self.order_book_archive_details.set_security_account(sec_account)
        self.order_book_archive_details.set_instrument_symbol(instr_symbol)
        self.order_book_archive_details.set_client_order_id(cl_ord_id)
        self.order_book_archive_details.set_quod_order_id(ord_id)
        self.order_book_archive_details.set_client_group(client_group)
        self.order_book_archive_details.set_owner(owner)
        self.order_book_archive_details.set_route(route)
        self.order_book_archive_details.set_venue(venue)
        self.order_book_archive_details.set_security_id_source(security_id_source)
        self.order_book_archive_details.set_security_id(security_id)
        self.order_book_archive_details.set_remove_all(remove_all)
        self.order_book_archive_details.set_filter(filter_dict)
        self.order_book_archive_details.set_column_names(column_names)
        self.order_book_archive_details.get_row_count(get_total_orders)
        result = call(self.import_order_from_db_call, self.order_book_archive_details.build())
        self.clear_details([self.order_book_archive_details])
        return result
    # endregion
