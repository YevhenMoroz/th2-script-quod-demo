from stubs import Stubs
from test_framework.win_gui_wrappers.base_window import BaseWindow
from win_gui_modules.utils import call


class BaseBasketOrderBook(BaseWindow):
    # region Base constructor
    def __init__(self, case_id, session_id):
        super().__init__(case_id, session_id)
        self.imported_file_mapping_field_details = None
        self.templates_details = None
        self.row_details = None
        self.file_details = None
        self.simple_request = None
        self.basket_ticket_details = None
        self.imported_file_mapping_field = None
        self.extract_template_details = None
        self.extract_child_order_data = None
        self.extract_child_details = None
        self.extract_order_data_details = None
        self.manage_templates_call = None
        self.extract_template_data_call = None
        self.remove_template_call = None
        self.create_basket_via_import_call = None
        self.complete_basket_call = None
        self.uncomplete_basket_call = None
        self.book_basket_call = None
        self.cancel_basket_call = None
        self.remove_from_basket_call = None
        self.extract_basket_data_call = None
        self.extract_child_order_data_call = None


    # endregion
    # region Common func
    def set_filter(self, filter_dict: dict):
        self.extract_template_details(self.base_request, filter_dict)
        self.clear_details([self.extract_template_details])
    # endregion

    # region Get
    def get_basket_template_details(self, templ_name, column_names: []):
        self.extract_template_details(self.base_request, {'Name': templ_name}, column_names)
        result = call(self.extract_template_data_call, self.extract_template_details.build())
        self.clear_details([self.extract_template_details])
        return result
    # endregion

    # region Set
    def basket_row_details(self, row_filter=None, remove_row=False, symbol=None, side=None, qty=None, ord_type=None,
                           price=None, capacity=None, stop_price=None):
        if not remove_row:
            params = {}
            if symbol is not None:
                params.update({'Symbol': symbol})
            if side is not None:
                params.update({'Side': side})
            if qty is not None:
                params.update({'Qty': qty})
            if ord_type is not None:
                params.update({'Order Type': ord_type})
            if price is not None:
                params.update({'Price': price})
            if capacity is not None:
                params.update({'Capacity': capacity})
            if stop_price is not None:
                params.update({'Stop Price': stop_price})
            result = self.row_details(row_filter, False, params).build()
        else:
            result = self.row_details(row_filter, True).build()
        return result

    # endregion

    # region Check

    # endregion

    # region Actions
    def add_basket_template(self, templ_name=None, descrip=None, client=None, tif=None, exec_policy=None,
                            symbol_source=None, has_header=True, templ: dict = None):
        if templ is not None:
            fields_details = [
                self.imported_file_mapping_field_details(self.imported_file_mapping_field.SYMBOL,
                                                         templ.get('Symbol')[0],
                                                         templ.get('Symbol')[1]).build(),
                self.imported_file_mapping_field_details(self.imported_file_mapping_field.QUANTITY,
                                                         templ.get('Quantity')[0],
                                                         templ.get('Quantity')[1]).build(),
                self.imported_file_mapping_field_details(self.imported_file_mapping_field.PRICE, templ.get('Price')[0],
                                                         templ.get('Price')[1]).build(),
                self.imported_file_mapping_field_details(self.imported_file_mapping_field.SIDE, templ.get('Side')[0],
                                                         templ.get('Side')[1]).build(),
                self.imported_file_mapping_field_details(self.imported_file_mapping_field.ORD_TYPE,
                                                         templ.get('OrdType')[0],
                                                         templ.get('OrdType')[1]).build(),
                self.imported_file_mapping_field_details(self.imported_file_mapping_field.STOP_PRICE,
                                                         templ.get('StopPrice')[0],
                                                         templ.get('StopPrice')[1]).build(),
                self.imported_file_mapping_field_details(self.imported_file_mapping_field.ACCOUNT,
                                                         templ.get('Account')[0],
                                                         templ.get('Account')[1]).build(),
                self.imported_file_mapping_field_details(self.imported_file_mapping_field.CAPACITY,
                                                         templ.get('Capacity')[0],
                                                         templ.get('Capacity')[1]).build()
            ]
            details = self.imported_file_mapping_field_details(has_header, fields_details).build()
            self.templates_details.set_imported_file_mapping_details(details)
        self.templates_details.set_default_params(self.base_request)
        if templ_name is not None:
            self.templates_details.set_name_value(templ_name)
        if exec_policy is not None:
            self.templates_details.set_exec_policy(exec_policy)
        if client is not None:
            self.templates_details.set_default_client(client)
        if descrip is not None:
            self.templates_details.set_description(descrip)
        if symbol_source is not None:
            self.templates_details.set_symbol_source(symbol_source)
        if tif is not None:
            self.templates_details.set_time_in_force(tif)
        call(self.manage_templates_call, self.templates_details.build())
        self.clear_details([self.templates_details, self.imported_file_mapping_field_details])

    def remove_basket_template(self, name):
        self.simple_request(self.base_request, {'Name': name})
        call(self.remove_template_call, self.simple_request.build())
        self.clear_details([self.simple_request])

    def create_basket_via_import(self, basket_name, basket_template_name, path, client, expire_date=None, tif=None,
                                 is_csv=False, amend_rows_details: [basket_row_details] = None):
        file_type = 1 if is_csv else 0
        self.basket_ticket_details.set_file_details(self.file_details(file_type, path).build())
        self.basket_ticket_details.set_default_params(self.base_request)
        self.basket_ticket_details.set_name_value(basket_name)
        self.basket_ticket_details.set_basket_template_name(basket_template_name)
        self.basket_ticket_details.set_client_value(client)
        if expire_date is not None:
            self.basket_ticket_details.set_date_value(expire_date)
        if tif is not None:
            self.basket_ticket_details.set_time_in_force_value(tif)
        if amend_rows_details is not None:
            self.basket_ticket_details.set_row_details(amend_rows_details)
        call(self.create_basket_via_import_call, self.basket_ticket_details.build())
        self.clear_details([self.basket_ticket_details])

    def complete_basket(self, filter_list=None):
        call(self.complete_basket_call, self.simple_request(self.base_request, filter_list).build())
        self.clear_details([self.simple_request])

    def un_complete(self, filter_list=None):
        call(self.uncomplete_basket_call, self.simple_request(self.base_request, filter_list).build())
        self.clear_details([self.simple_request])

    def book_basket(self, filter_list=None):
        call(self.book_basket_call, self.simple_request(self.base_request, filter_list).build())
        self.clear_details([self.simple_request])

    def cancel_basket(self, filter_list=None):
        call(self.cancel_basket_call, self.simple_request(self.base_request, filter_list).build())
        self.clear_details([self.simple_request])
    # endregion
    def remove_from_basket(self, filter_dict: dict = None, rows_numbers: list = None):
        remove_from_basket_details = self.remove_from_basket_details(self.base_request, filter_dict, rows_numbers)
        call(self.remove_from_basket_call, remove_from_basket_details.build())

    # endregion

    def get_basket_orders_values(self, row_count, extract_value, basket_book_filter: dict = None):
        extract_order_details = self.extract_order_data_details()
        extract_order_details.set_default_params(self.base_request)
        if basket_book_filter is not None:
            extract_order_details.set_filter(basket_book_filter)
        extract_order_details.set_column_names([extract_value])
        extract_child_details = self.extract_child_details(extract_order_details.build(), row_count)
        result = call(self.ex, extract_child_details.build())
        self.clear_details([self.basket_ticket_details])
        return result