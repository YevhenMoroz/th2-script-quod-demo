from quod_qa.win_gui_wrappers.base_window import BaseWindow, split_2lvl_values
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction
from win_gui_modules.utils import call


class BaseOrderBook(BaseWindow):
    # region Base constructor
    def __init__(self, case_id, base_request):
        super().__init__(case_id, base_request)
        # Need to override
        self.order_info = None
        self.order_details = None
        self.new_order_details = None
        self.menu_item_details = None
        self.base_order_details = None
        self.basket_row_details = None
        self.modify_order_details = None
        self.cancel_order_details = None
        self.rows_numbers_for_grid = None
        self.suspend_order_details = None
        self.disclose_flag_details = None
        self.add_to_basket_details = None
        self.create_basket_details = None
        self.reassign_order_details = None
        self.manual_executing_details = None
        self.second_level_tab_details = None
        self.second_level_extraction_details = None
        self.mass_exec_summary_average_price_detail = None
        self.extraction_from_second_level_tabs_call = None
        self.mass_exec_summary_average_price_call = None
        self.manual_execution_order_call = None
        self.is_menu_item_present_call = None
        self.group_modify_order_call = None
        self.get_orders_details_call = None
        self.un_complete_order_call = None
        self.notify_dfd_order_call = None
        self.check_out_order_call = None
        self.reassign_order_call = None
        self.complete_order_call = None
        self.check_in_order_call = None
        self.suspend_order_call = None
        self.release_order_call = None
        self.disclose_flag_call = None
        self.add_to_basket_call = None
        self.create_basket_call = None
        self.cancel_order_call = None
        self.mass_unbook_call = None
        self.mass_book_call = None

    # endregion
    # region Common func
    def set_order_details(self):
        self.order_details.set_extraction_id(self.extraction_id)
        self.order_details.set_default_params(base_request=self.base_request)

    def set_filter(self, filter_list: list):
        """
        Receives list as an argument, where the elements
        are in order - key, value, key, value, ...
        For example ["Qty", "123456", "Owner", "QA1", etc]
        """
        self.order_details.set_filter(filter_list)
        return self

    # endregion
    # region Get
    def extract_field(self, column_name: str) -> str:
        field = ExtractionDetail("orderBook." + column_name, column_name)
        self.order_details.add_single_order_info(
            self.order_info.create(
                action=ExtractionAction.create_extraction_action(extraction_details=[field])
            )
        )
        response = call(self.get_orders_details_call, self.order_details.request())
        return response[field.name]

    def extract_fields_list(self, list_fields: dict, row_number: int) -> dict:
        """
        Receives dict as an argument, where the key is column name what
        we extract from GUI and return new dict where
        key = key and value is extracted field from FE
        """
        list_of_fields = []
        for field in list_fields.items():
            key = list(field)[0]
            field = ExtractionDetail(key, key)
            list_of_fields.append(field)
        info = self.order_info.create(
            action=ExtractionAction.create_extraction_action(extraction_details=list_of_fields))
        info.set_number(row_number)
        self.order_details.add_single_order_info(info)
        response = call(self.get_orders_details_call, self.order_details.request())
        return response

    def extract_second_lvl_fields_list(self, list_fields: dict, row_number: int) -> dict:
        """
            Receives dict as an argument, where the key is column name what
            we extract from GUI and return new dict where
            key = key and value is extracted field from FE
            """
        list_of_fields = []
        for field in list_fields.items():
            key = list(field)[0]
            field = ExtractionDetail(key, key)
            list_of_fields.append(field)

        child_info = self.order_info.create(
            action=ExtractionAction.create_extraction_action(extraction_details=list_of_fields))
        child_info.set_number(row_number)
        child_details = self.order_details.create(info=child_info)

        self.order_details.add_single_order_info(
            self.order_info.create(
                action=ExtractionAction.create_extraction_action(), sub_order_details=child_details)
        )
        response = call(self.get_orders_details_call, self.order_details.request())
        return response

    def extract_2lvl_fields(self, tab: str, column_names: [str], rows: [int], filter_dict: dict = None):
        """
        return arr of dict for avery rows
        """
        self.second_level_tab_details.set_tab_name(tab)
        self.second_level_tab_details.set_columns_names(column_names)
        self.second_level_tab_details.set_rows_numbers(rows)
        self.second_level_extraction_details.set_default_params(self.base_request)
        if filter_dict is not None:
            self.second_level_extraction_details.set_filter(filter_dict)
        self.second_level_extraction_details.set_tabs_details([self.second_level_tab_details.build()])
        result = call(self.extraction_from_second_level_tabs_call, self.second_level_extraction_details.build())
        self.clear_details([self.second_level_extraction_details, self.second_level_tab_details])
        return split_2lvl_values(result)

    # endregion
    # region Check
    def check_order_fields_list(self, expected_fields: dict, event_name="Check Order Book"):
        """
        Receives dict as an argument, where the key is column name what
        we extract from GUI and value is expected result
        For example {"Sts": "Terminated", "Owner": "QA1", etc}
        """
        actual_list = self.extract_fields_list(expected_fields)
        for items in expected_fields.items():
            key = list(items)[0]
            value = list(items)[1]
            self.verifier.set_event_name(event_name)
            self.verifier.compare_values(key, value, actual_list[key])
        self.verifier.verify()

    def is_menu_item_present(self, menu_item, filter_list=None):
        """
        check order context menu and return a bool value
        """
        self.menu_item_details.set_menu_item(menu_item)
        if filter_list is not None:
            self.menu_item_details.set_filter(filter)
        result = call(self.is_menu_item_present_call, self.menu_item_details.build())
        return result['isMenuItemPresent']

    # endregion
    # region Actions
    def cancel_order(self, cancel_children: bool = None, row_count: int = None, comment=None,
                     filter_list: list = None):
        if cancel_children is not None:
            self.cancel_order_details.set_cancel_children(cancel_children)
        if row_count is not None:
            self.cancel_order_details.set_selected_row_count(row_count)
        if comment is not None:
            self.cancel_order_details.set_comment(comment)
        if filter_list is not None:
            self.cancel_order_details.set_filter(filter_list)
        call(self.cancel_order_call, self.cancel_order_details.build())

    def complete_order(self, row_count=None, filter_list=None):
        if filter_list is not None:
            self.modify_order_details.set_filter()
        if row_count is not None:
            self.modify_order_details.set_selected_row_count()
        call(self.complete_order_call, self.modify_order_details.build())

    def un_complete_order(self, row_count=None, filter_list=None):
        if filter_list is not None:
            self.modify_order_details.set_filter()
        if row_count is not None:
            self.modify_order_details.set_selected_row_count()
        call(self.un_complete_order_call, self.modify_order_details.build())

    def notify_dfd(self, row_count=None, filter_list=None):
        if filter_list is not None:
            self.modify_order_details.set_filter()
        if row_count is not None:
            self.modify_order_details.set_selected_row_count()
        call(self.notify_dfd_order_call, self.modify_order_details.build())

    def group_modify(self, client=None, security_account=None, routes=None, free_notes=None, filter_list=None):
        if filter_list is not None:
            self.modify_order_details.set_filter()
        if client is not None:
            self.modify_order_details.client = client
        if security_account is not None:
            self.modify_order_details.securityAccount = security_account
        if routes is not None:
            self.modify_order_details.routes = routes
        if free_notes is not None:
            self.modify_order_details.freeNotes = free_notes
        call(self.group_modify_order_call, self.modify_order_details.build())

    def reassign_order(self, recipient):
        self.reassign_order_details.base.CopyFrom(self.base_request)
        self.reassign_order_details.desk = recipient
        call(self.reassign_order_call, self.reassign_order_details)

    def check_in_order(self, filter_list=None):
        if filter_list is not None:
            self.modify_order_details.set_filter()
        call(self.check_in_order_call, self.modify_order_details.build())

    def check_out_order(self, filter_list=None):
        if filter_list is not None:
            self.modify_order_details.set_filter()
        call(self.check_out_order_call, self.modify_order_details.build())

    def suspend_order(self, cancel_children: bool = None, filter_list=None):
        if filter_list is not None:
            self.suspend_order_details.set_filter(filter_list)
        if cancel_children is not None:
            self.suspend_order_details.set_cancel_children(cancel_children)
        call(self.suspend_order_call, self.suspend_order_details.build())

    def release_order(self, filter_list=None):
        if filter_list is not None:
            self.base_order_details.set_filter(filter_list)
        call(self.release_order_call, self.base_order_details.build())

    def mass_execution_summary_at_average_price(self, row_count: int):
        self.mass_exec_summary_average_price_detail.set_count_of_selected_rows(row_count)
        call(self.mass_exec_summary_average_price_call, self.mass_exec_summary_average_price_detail)

    def set_disclose_flag_via_order_book(self, type_disclose: str, row_numbers=None):
        """ type_disclose - can have next values: disable, real_time, manual """
        self.disclose_flag_details = getattr(self.disclose_flag_details, type_disclose)
        self.disclose_flag_details.set_row_numbers(row_numbers)
        call(self.cancel_order_call, self.disclose_flag_details.build())

    def add_to_basket(self, list_row_numbers: [] = None, basket_name=None):
        if basket_name is not None:
            self.add_to_basket_details.set_basket_name(basket_name)
        if list_row_numbers is not None:
            self.add_to_basket_details.set_row_numbers(list_row_numbers)
        call(self.add_to_basket_call, self.add_to_basket_details.build())

    def create_basket(self, orders_rows: [] = None, basket_name=None):
        """
        orders_rows - select rows from order book
        """
        if basket_name is not None:
            self.create_basket_details.set_name(basket_name)
        if orders_rows is not None:
            self.create_basket_details.set_row_numbers(orders_rows)
        call(self.create_basket_call, self.create_basket_details.build())

    def manual_execution(self, qty=None, price=None, execution_firm=None, contra_firm=None,
                         last_capacity=None, settl_date: int = None):
        if qty is not None:
            self.manual_executing_details.add_executions_details().set_quantity(qty)
        if price is not None:
            self.manual_executing_details.add_executions_details().set_price(price)
        if execution_firm is not None:
            self.manual_executing_details.add_executions_details().set_executing_firm(execution_firm)
        if contra_firm is not None:
            self.manual_executing_details.add_executions_details().set_contra_firm(contra_firm)
        if settl_date is not None:
            self.manual_executing_details.add_executions_details().set_settlement_date_offset(settl_date)
        if last_capacity is not None:
            self.manual_executing_details.add_executions_details().set_last_capacity(last_capacity)
        call(self.manual_execution_order_call, self.manual_executing_details.build())

    def mass_book(self, row_list: list):
        self.rows_numbers_for_grid.set_rows_numbers(row_list)
        call(self.mass_book_call, self.rows_numbers_for_grid.build())
        self.clear_details([self.rows_numbers_for_grid])

    def mass_unbook(self, row_list: list):
        self.rows_numbers_for_grid.set_rows_numbers(row_list)
        call(self.mass_unbook_call, self.rows_numbers_for_grid.build())
        self.clear_details([self.rows_numbers_for_grid])
    # endregion
