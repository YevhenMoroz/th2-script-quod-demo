from test_framework.win_gui_wrappers.base_window import BaseWindow
from win_gui_modules.basket_ticket_wrappers import BasketTicketDetails
from win_gui_modules.utils import call
from custom.verifier import VerificationMethod


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
        self.extract_basket_data_details = None
        self.extract_basket_order_details = None
        self.imported_file_mapping_field = None
        self.extract_template_details = None
        self.extract_child_order_data = None
        self.extract_order_data_details = None
        self.remove_from_basket_details = None
        self.imported_file_mapping_details = None
        self.basket_wave_row_details = None
        self.wave_basket_details = None
        self.extract_child_details = None
        self.menu_item_details = None
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
        self.extract_basket_data_details_call = None
        self.extract_basket_order_details_call = None
        self.wave_basket_call = None
        self.amend_template_call = None
        self.clone_template_call = None
        self.is_menu_item_present_call = None

    # endregion
    # region Common func
    def set_filter(self, filter_dict: dict):
        self.extract_template_details(self.base_request, filter_dict)
        self.clear_details([self.extract_template_details])

    # endregion

    # region Get
    def get_basket_template_details(self, templ_filter: dict, column_names: list):
        self.extract_template_details.set_base_details(self.base_request)
        self.extract_template_details.set_filter(templ_filter)
        self.extract_template_details.set_column_names(column_names)
        result = call(self.extract_template_data_call, self.extract_template_details.build())
        self.clear_details([self.extract_template_details])
        return result

    def get_basket_value(self, column_name, basket_book_filter: dict = None):
        self.extract_basket_data_details.set_default_params(self.base_request)
        self.extract_basket_data_details.set_column_names([column_name])
        if basket_book_filter is not None:
            self.extract_basket_data_details.set_filter(basket_book_filter)
        result = call(self.extract_basket_data_details_call, self.extract_basket_data_details.build())
        self.clear_details([self.extract_basket_data_details])
        return result[column_name]

    def get_basket_sub_lvl_value(self, row_count: int, extract_value, tab_name, basket_book_filter: dict = None):
        self.extract_basket_data_details.set_default_params(self.base_request)
        if basket_book_filter is not None:
            self.extract_basket_data_details.set_filter(basket_book_filter)  # Set filter for parent order
        self.extract_basket_data_details.set_column_names(
            [extract_value])  # Set column for child orders which data be extracted
        extract_basket_order_details = self.extract_basket_order_details(
            self.extract_basket_data_details.build(),
            row_count, tab_name)  # argument #2 - row numbers
        result = call(self.extract_basket_order_details_call, extract_basket_order_details.build())
        self.clear_details([self.extract_basket_data_details])
        return result

    def is_menu_item_present(self, menu_item: str, row_count: list = None, sub_lvl_tab: str = None,
                             filter_dict: dict = None):
        """
        check order context menu and return a bool value
        """
        if row_count is None:
            row_count = [1]
        self.menu_item_details.set_selected_rows(row_count)
        self.menu_item_details.set_menu_item(menu_item)
        if filter_dict is not None:
            self.menu_item_details.set_filter(filter_dict)
        if sub_lvl_tab is not None:
            self.menu_item_details.set_sub_lvl_tab(sub_lvl_tab)
        result = call(self.is_menu_item_present_call, self.menu_item_details.build())
        self.clear_details([self.menu_item_details])
        return result['isMenuItemPresent']

    # endregion

    # region Set
    def set_external_algo_twap_details(self, strategy_type, urgency):
        self.wave_basket_details.set_external_twap_stratagy(strategy_type, urgency)

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
    def check_basket_field(self, field: str, expected_result: str, event_name="Check Basket Book",
                           verification_method: VerificationMethod = VerificationMethod.EQUALS):
        actual_result = self.get_basket_value(field)
        self.verifier.set_event_name(event_name)
        self.verifier.compare_values(field, expected_result, actual_result,
                                     verification_method)
        self.verifier.verify()

    def check_basket_sub_lvl_field(self, row_count: int, field: str, tab_name: str, expected_result: str,
                                   event_name="Check 2nd lvl Basket Book",
                                   verification_method: VerificationMethod = VerificationMethod.EQUALS):
        actual_result = self.get_basket_sub_lvl_value(row_count, field, tab_name)
        self.verifier.set_event_name(event_name)
        self.verifier.compare_values(field, expected_result, actual_result[str(row_count)],
                                     verification_method)
        self.verifier.verify()




    # endregion

    # region Actions
    def add_basket_template(self, templ_name=None, descrip=None, client=None, tif=None, exec_policy=None,
                            symbol_source=None, has_header=False, header_row=None, data_row=None, delimiter=None,
                            spreadsheet_tab=None, templ: dict = None):
        if templ is not None:
            fields_details = []
            for key in templ:
                fields_details.append(self.imported_file_mapping_field_details(
                    self.imported_file_mapping_field.__dict__[key].value, templ.get(key)[0],
                    templ.get(key)[1]).build())
            details = self.imported_file_mapping_details(has_header, fields_details, header_row, data_row,
                                                         delimiter, spreadsheet_tab).build()
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

    def amend_basket_template(self, templ_name=None, descrip=None, client=None, tif=None, exec_policy=None,
                              symbol_source=None, has_header=False, header_row=None, data_row=None, delimiter=None,
                              spreadsheet_tab=None, templ: dict = None, templ_filter: dict = None):
        if templ is not None:
            fields_details = []
            for key in templ:
                fields_details.append(self.imported_file_mapping_field_details(
                    self.imported_file_mapping_field.__dict__[key].value, templ.get(key)[0],
                    templ.get(key)[1]).build())
            details = self.imported_file_mapping_details(has_header, fields_details, header_row, data_row,
                                                         delimiter, spreadsheet_tab).build()
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
        if templ_filter is not None:
            self.templates_details.set_filter(templ_filter)
        call(self.amend_template_call, self.templates_details.build())

    def clone_basket_template(self, templ_name=None, descrip=None, client=None, tif=None, exec_policy=None,
                              symbol_source=None, has_header=False, header_row=None, data_row=None, delimiter=None,
                              spreadsheet_tab=None, templ: dict = None, templ_filter: dict = None):
        if templ is not None:
            fields_details = []
            for key in templ:
                fields_details.append(self.imported_file_mapping_field_details(
                    self.imported_file_mapping_field.__dict__[key].value, templ.get(key)[0],
                    templ.get(key)[1]).build())
            details = self.imported_file_mapping_details(has_header, fields_details, header_row, data_row,
                                                         delimiter, spreadsheet_tab).build()
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
        if templ_filter is not None:
            self.templates_details.set_filter(templ_filter)
        call(self.clone_template_call, self.templates_details.build())

    def remove_basket_template(self, templ_filter):
        self.simple_request.set_filter(templ_filter)
        call(self.remove_template_call, self.simple_request.build())
        self.clear_details([self.simple_request])

    def create_basket_via_import(self, basket_name, basket_template_name, path, client=None, expire_date=None, tif=None,
                                 is_csv=False, amend_rows_details: [basket_row_details] = None):
        file_type = 1 if is_csv else 0
        self.basket_ticket_details = BasketTicketDetails()
        self.basket_ticket_details.set_file_details(self.file_details(file_type, path).build())
        self.basket_ticket_details.set_default_params(self.base_request)
        self.basket_ticket_details.set_name_value(basket_name)
        self.basket_ticket_details.set_basket_template_name(basket_template_name)
        if client:
            self.basket_ticket_details.set_client_value(client)
        if expire_date is not None:
            self.basket_ticket_details.set_date_value(expire_date)
        if tif is not None:
            self.basket_ticket_details.set_time_in_force_value(tif)
        if amend_rows_details is not None:
            self.basket_ticket_details.set_row_details(amend_rows_details)
        call(self.create_basket_via_import_call, self.basket_ticket_details.build())
        self.clear_details([self.basket_ticket_details])

    def complete_basket(self, filter_dict: dict = None):
        self.simple_request.set_filter(filter_dict)
        call(self.complete_basket_call, self.simple_request.build())
        self.clear_details([self.simple_request])

    def un_complete(self, filter_dict: dict = None):
        self.simple_request.set_filter(filter_dict)
        call(self.uncomplete_basket_call, self.simple_request.build())
        self.clear_details([self.simple_request])

    def book_basket(self, filter_dict: dict = None):
        self.simple_request.set_filter(filter_dict)
        call(self.book_basket_call, self.simple_request.build())
        self.clear_details([self.simple_request])

    def cancel_basket(self, filter_dict: dict = None):
        self.simple_request.set_filter(filter_dict)
        call(self.cancel_basket_call, self.simple_request.build())
        self.clear_details([self.simple_request])

    def remove_from_basket(self, filter_dict: dict = None, rows_numbers: list = None):
        remove_from_basket_details = self.remove_from_basket_details(self.base_request, filter_dict, rows_numbers)
        call(self.remove_from_basket_call, remove_from_basket_details.build())

    def wave_basket(self, qty_percentage=None, percentage_profile=None,  route=None, removed_orders: list = None,
                    sub_lvl_rows: list = None, basket_filter: dict = None):
        if qty_percentage is not None:
            self.wave_basket_details.set_qty_percentage(qty_percentage)
        if percentage_profile is not None:
            self.wave_basket_details.set_percentage_profile(percentage_profile)
        if route is not None:
            self.wave_basket_details.set_route(route)
        if basket_filter is not None:
            self.wave_basket_details.set_filter(basket_filter)
        if removed_orders is not None:
            for order in removed_orders:
                row_details = self.basket_wave_row_details
                row_details.set_filtration_value(order)
                row_details.set_remove_row(True)
                self.wave_basket_details.set_row_details(row_details.build())
        if sub_lvl_rows is not None:
            self.wave_basket_details.set_sub_lvl_rows(sub_lvl_rows)
        call(self.wave_basket_call, self.wave_basket_details.build())
        self.clear_details([self.wave_basket_details])
    # endregion
