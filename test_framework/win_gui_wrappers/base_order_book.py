from th2_grpc_act_gui_quod.act_ui_win_pb2 import ExtractDirectsValuesRequest

from custom.verifier import VerificationMethod
from test_framework.win_gui_wrappers.base_window import BaseWindow
from win_gui_modules.middle_office_wrappers import ExtractionPanelDetails
from win_gui_modules.order_book_wrappers import ExtractionDetail, ExtractionAction, SplitBookingParameter
from win_gui_modules.utils import call
from win_gui_modules.wrappers import direct_moc_request_correct, direct_loc_request_correct, direct_loc_request, \
    direct_moc_request


class BaseOrderBook(BaseWindow):
    # region Base constructor
    def __init__(self, case_id, session_id):
        super().__init__(case_id, session_id)
        # Need to override
        self.order_info = None
        self.order_details = None
        self.scrolling_details = None
        self.new_order_details = None
        self.menu_item_details = None
        self.base_order_details = None
        self.scrolling_operation = None
        self.modify_order_details = None
        self.manual_cross_details = None
        self.cancel_order_details = None
        self.rows_numbers_for_grid = None
        self.suspend_order_details = None
        self.disclose_flag_details = None
        self.add_to_basket_details = None
        self.create_basket_details = None
        self.reassign_order_details = None
        self.manual_executing_details = None
        self.second_level_tab_details = None
        self.extraction_panel_details = None
        self.second_level_extraction_details = None
        self.mass_exec_summary_average_price_detail = None
        self.extraction_error_message_details = None
        self.extract_direct_values = None
        self.extraction_from_second_level_tabs_call = None
        self.mass_exec_summary_average_price_call = None
        self.extract_booking_block_values_call = None
        self.order_book_grid_scrolling_call = None
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
        self.manual_cross_call = None
        self.mass_unbook_call = None
        self.mass_book_call = None
        self.ticket_details = None
        self.settlement_details = None
        self.commissions_details = None
        self.fees_details = None
        self.misc_details = None
        self.split_booking_details = None
        self.split_booking_call = None
        self.direct_moc_request_correct_call = None
        self.direct_loc_request_correct_call = None

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

    def scroll_order_book(self, count: int = 1):
        self.scrolling_details.__class__.__init__(self=self.scrolling_details,
                                                  scrolling_operation=self.scrolling_operation.UP,
                                                  number_of_scrolls=count, base=self.base_request)
        call(self.order_book_grid_scrolling_call, self.scrolling_details.build())

    # endregion

    # region Get
    def extract_field(self, column_name: str, row_number: int = None) -> str:
        field = ExtractionDetail("orderBook." + column_name, column_name)
        info = self.order_info.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[field]))
        if row_number is not None:
            info.set_number(row_number)
        self.order_details.add_single_order_info(info)
        response = call(self.get_orders_details_call, self.order_details.request())
        self.clear_details([self.order_details])
        self.set_order_details()
        return response[field.name]

    def extract_fields_list(self, list_fields: dict, row_number: int = None) -> dict:
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
        if row_number is not None:
            info.set_number(row_number)
        self.order_details.add_single_order_info(info)
        response = call(self.get_orders_details_call, self.order_details.request())
        self.clear_details([self.order_details])
        self.set_order_details()
        return response

    def extract_second_lvl_fields_list(self, list_fields: dict, row_number: int = None) -> dict:
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
        if row_number is not None:
            child_info.set_number(row_number)
        child_details = self.order_details.create(info=child_info)

        self.order_details.add_single_order_info(
            self.order_info.create(
                action=ExtractionAction.create_extraction_action(), sub_order_details=child_details)
        )
        response = call(self.get_orders_details_call, self.order_details.request())
        self.clear_details([self.order_details])
        self.set_order_details()
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
        return BaseWindow.split_2lvl_values(result)

    # endregion

    # region Check
    def check_order_fields_list(self, expected_fields: dict, event_name="Check Order Book",
                                row_number: int = 1,
                                verification_method: VerificationMethod = VerificationMethod.EQUALS):
        """
        Receives dict as an argument, where the key is column name what
        we extract from GUI and value is expected result and row_number to check, 1 by default
        For example {"Sts": "Terminated", "Owner": "QA1", etc}
        """
        actual_list = self.extract_fields_list(expected_fields, row_number)
        for items in expected_fields.items():
            key = list(items)[0]
            value = list(items)[1]
            self.verifier.set_event_name(event_name)
            self.verifier.compare_values(key, value, actual_list[key], verification_method)
        self.verifier.verify()

    def check_second_lvl_fields_list(self, expected_fields: dict, event_name="Check second lvl in Order Book",
                                     row_number: int = 1,
                                     verification_method: VerificationMethod = VerificationMethod.EQUALS):
        """
        Receives dict as an argument, where the key is column name what
        we extract from GUI and value is expected result and row_number to check, 1 by default
        For example {"Sts": "Terminated", "Owner": "QA1", etc}
        """
        actual_list = self.extract_second_lvl_fields_list(expected_fields, row_number)
        for items in expected_fields.items():
            key = list(items)[0]
            value = list(items)[1]
            self.verifier.set_event_name(event_name)
            self.verifier.compare_values(key, value, actual_list[key], verification_method)
        self.verifier.verify()

    def is_menu_item_present(self, menu_item, filter_list=None):
        """
        check order context menu and return a bool value
        """
        self.menu_item_details.set_menu_item(menu_item)
        if filter_list is not None:
            self.menu_item_details.set_filter(filter_list)
        result = call(self.is_menu_item_present_call, self.menu_item_details.build())
        self.clear_details([self.menu_item_details])
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
        self.clear_details([self.cancel_order_details])

    def complete_order(self, row_count=None, filter_list=None):
        if filter_list is not None:
            self.modify_order_details.set_filter(filter_list)
        if row_count is not None:
            self.modify_order_details.set_selected_row_count(row_count)
        call(self.complete_order_call, self.modify_order_details.build())
        self.clear_details([self.modify_order_details])

    def un_complete_order(self, row_count=None, filter_list=None):
        if filter_list is not None:
            self.modify_order_details.set_filter()
        if row_count is not None:
            self.modify_order_details.set_selected_row_count()
        call(self.un_complete_order_call, self.modify_order_details.build())
        self.clear_details([self.modify_order_details])

    def notify_dfd(self, row_count=None, filter_list=None):
        if filter_list is not None:
            self.modify_order_details.set_filter()
        if row_count is not None:
            self.modify_order_details.set_selected_row_count()
        call(self.notify_dfd_order_call, self.modify_order_details.build())
        self.clear_details([self.modify_order_details])

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
        self.clear_details([self.modify_order_details])

    def reassign_order(self, recipient):
        self.reassign_order_details.base.CopyFrom(self.base_request)
        self.reassign_order_details.desk = recipient
        call(self.reassign_order_call, self.reassign_order_details)

    def check_in_order(self, filter_list=None):
        if filter_list is not None:
            self.modify_order_details.set_filter()
        call(self.check_in_order_call, self.modify_order_details.build())
        self.clear_details([self.modify_order_details])

    def check_out_order(self, filter_list=None):
        if filter_list is not None:
            self.modify_order_details.set_filter()
        call(self.check_out_order_call, self.modify_order_details.build())
        self.clear_details([self.modify_order_details])

    def suspend_order(self, cancel_children: bool = None, filter_list=None):
        if filter_list is not None:
            self.suspend_order_details.set_filter(filter_list)
        if cancel_children is not None:
            self.suspend_order_details.set_cancel_children(cancel_children)
        call(self.suspend_order_call, self.suspend_order_details.build())
        self.clear_details([self.suspend_order_details])

    def release_order(self, filter_list=None):
        if filter_list is not None:
            self.base_order_details.set_filter(filter_list)
        call(self.release_order_call, self.base_order_details.build())
        self.clear_details([self.base_order_details])

    def mass_execution_summary_at_average_price(self, row_count: int):
        self.mass_exec_summary_average_price_detail.set_count_of_selected_rows(row_count)
        call(self.mass_exec_summary_average_price_call, self.mass_exec_summary_average_price_detail)
        self.clear_details([self.mass_exec_summary_average_price_detail])

    def set_disclose_flag_via_order_book(self, type_disclose: str, row_numbers=None):
        """ type_disclose - can have next values: disable, real_time, manual """
        self.disclose_flag_details = getattr(self.disclose_flag_details, type_disclose)
        self.disclose_flag_details.set_row_numbers(row_numbers)
        call(self.cancel_order_call, self.disclose_flag_details.build())
        self.clear_details([self.disclose_flag_details])

    def add_to_basket(self, list_row_numbers: [] = None, basket_name=None):
        if basket_name is not None:
            self.add_to_basket_details.set_basket_name(basket_name)
        if list_row_numbers is not None:
            self.add_to_basket_details.set_row_numbers(list_row_numbers)
        call(self.add_to_basket_call, self.add_to_basket_details.build())
        self.clear_details([self.add_to_basket_details])

    def create_basket(self, orders_rows: [] = None, basket_name=None):
        """
        orders_rows - select rows from order book
        """
        if basket_name is not None:
            self.create_basket_details.set_name(basket_name)
        if orders_rows is not None:
            self.create_basket_details.set_row_numbers(orders_rows)
        call(self.create_basket_call, self.create_basket_details.build())
        self.clear_details([self.create_basket_details])

    def manual_execution(self, qty=None, price=None, execution_firm=None, contra_firm=None,
                         last_capacity=None, settl_date: int = None, error_expected=False):
        execution_details = self.manual_executing_details.add_executions_details()
        if qty is not None:
            execution_details.set_quantity(qty)
        if price is not None:
            execution_details.set_price(price)
        if execution_firm is not None:
            execution_details.set_executing_firm(execution_firm)
        if contra_firm is not None:
            execution_details.set_contra_firm(contra_firm)
        if settl_date is not None:
            execution_details.set_settlement_date_offset(settl_date)
        if last_capacity is not None:
            execution_details.set_last_capacity(last_capacity)
        if error_expected is True:
            self.manual_executing_details.set_error_expected(error_expected)
        result = call(self.manual_execution_order_call, self.manual_executing_details.build())
        self.clear_details([self.manual_executing_details])
        return result

    def manual_cross_orders(self, selected_rows: list, qty=None, price=None, last_mkt=None):
        if qty is not None:
            self.manual_cross_details.set_quantity(qty)
        if price is not None:
            self.manual_cross_details.set_price(price)
        if last_mkt is not None:
            self.manual_cross_details.set_last_mkt(last_mkt)
        self.manual_cross_details.set_selected_rows(selected_rows)
        call(self.manual_cross_call, self.manual_cross_details.build())

    def mass_book(self, row_list: list):
        self.rows_numbers_for_grid.set_rows_numbers(row_list)
        call(self.mass_book_call, self.rows_numbers_for_grid.build())
        self.clear_details([self.rows_numbers_for_grid])

    def mass_unbook(self, row_list: list):
        self.rows_numbers_for_grid.set_rows_numbers(row_list)
        call(self.mass_unbook_call, self.rows_numbers_for_grid.build())
        self.clear_details([self.rows_numbers_for_grid])

    # endregion

    '''
    Method extracting values from Booking Ticket
    '''

    def extracting_values_from_booking_ticket(self, panel_of_extraction: list, filter_dict: dict):
        self.extraction_panel_details = ExtractionPanelDetails(self.base_request,
                                                               filter_dict,
                                                               panel_of_extraction
                                                               )
        result = call(self.extract_booking_block_values_call, self.extraction_panel_details.build())
        self.clear_details([self.extraction_panel_details])
        return result

    def direct_moc_order_correct(self, qty, route):
        call(self.direct_moc_request_correct_call, direct_moc_request_correct("UnmatchedQty", qty, route))

    def direct_loc_order_correct(self, qty, route):
        call(self.direct_loc_request_correct_call, direct_loc_request_correct("UnmatchedQty", qty, route))

    def set_error_message_details(self):
        self.extraction_error_message_details.name = "ErrorMessage"
        self.extraction_error_message_details.type = ExtractDirectsValuesRequest.DirectsExtractedType.ERROR_MESSAGE

    def direct_loc_extract_error_message(self, qty, route):
        self.extract_direct_values.extractionId = "DirectErrorMessageExtractionID"
        self.extract_direct_values.extractedValues.append(self.extraction_error_message_details)
        response = call(self.direct_loc_request_correct_call,
                        direct_loc_request("UnmatchedQty", qty, route, self.extract_direct_values))
        self.clear_details([self.extraction_error_message_details, self.extract_direct_values])
        return response

    def create_split_booking_parameter(self, split_qty: str = None, client=None, trade_date: str = None,
                                       give_up_broker=None, net_gross_ind=None, agreed_price=None, settlement_type=None,
                                       settlement_currency=None, exchange_rate: str = None, exchange_rate_calc=None,
                                       settlement_date: str = None, pset=None, comm_basis=None, comm_rate=None,
                                       comm_amount=None, comm_currency=None, remove_comm=False, fee_type=None,
                                       fee_basis=None, fee_rate=None, fee_amount=None, fee_currency=None,
                                       fee_category=None, remove_fees=False, bo_notes=None, bo_fields=None,
                                       trade_type=None):
        """
        trade_date/settlement_date format: '10/19/2021'
        bo_fields format: [field1, field2, field3, field4, field5] [field1, None, field3, None, field5] etc.
        """
        ticket_details = self.__set_ticket_details(split_qty, client, trade_date, give_up_broker, net_gross_ind,
                                                   agreed_price)
        settlement_details = self.__set_settlement_details(exchange_rate, exchange_rate_calc, pset, settlement_currency,
                                                           settlement_date, settlement_type)
        commissions_details = self.__set_commission_details(comm_amount, comm_basis, comm_currency, comm_rate,
                                                            remove_comm)
        fees_details = self.__set_fees_details(fee_amount, fee_basis, fee_category, fee_currency, fee_rate, fee_type,
                                               remove_fees)
        misc_details = self.__set_misc_details(bo_fields, bo_notes, trade_type)
        return SplitBookingParameter(ticket_details, settlement_details, commissions_details, fees_details,
                                     misc_details).build()

    def __set_fees_details(self, fee_amount, fee_basis, fee_category, fee_currency, fee_rate, fee_type, remove_fees):
        if fee_type:
            fees_details = self.fees_details
            fees_details.add_fees(fee_type, fee_basis, fee_rate, fee_amount, fee_currency, fee_category)
            if remove_fees:
                fees_details.remove_fees()
            fees_details = fees_details.build()
        else:
            return None
        return fees_details

    def __set_commission_details(self, comm_amount, comm_basis, comm_currency, comm_rate, remove_comm):
        if comm_basis:
            commissions_details = self.commissions_details
            commissions_details.toggle_manual()
            commissions_details.add_commission(comm_basis, comm_rate, comm_amount, comm_currency)
            if remove_comm:
                commissions_details.remove_commissions()
            commissions_details = commissions_details.build()
        else:
            return None
        return commissions_details

    def __set_misc_details(self, bo_fields, bo_notes, trade_type):
        if trade_type or bo_fields or bo_notes is not None:
            misc_details = self.misc_details
            if trade_type:
                misc_details.set_trade_type(trade_type)
            if bo_notes:
                misc_details.set_bo_notes_value(bo_notes)
            if bo_fields:
                if bo_fields[0]:
                    misc_details.set_bo_field_1(bo_fields[0])
                if bo_fields[1]:
                    misc_details.set_bo_field_2(bo_fields[1])
                if bo_fields[2]:
                    misc_details.set_bo_field_3(bo_fields[2])
                if bo_fields[3]:
                    misc_details.set_bo_field_4(bo_fields[3])
                if bo_fields[4]:
                    misc_details.set_bo_field_5(bo_fields[4])
            return misc_details.build()
        else:
            return None

    def __set_settlement_details(self, exchange_rate, exchange_rate_calc, pset, settlement_currency, settlement_date,
                                 settlement_type):
        if exchange_rate or exchange_rate_calc or pset or settlement_currency or settlement_date or settlement_type:
            settlement_details = self.settlement_details
            if settlement_currency:
                settlement_details.set_settlement_type(settlement_type)
            if settlement_currency:
                settlement_details.set_settlement_currency(settlement_currency)
            if exchange_rate:
                settlement_details.set_exchange_rate(exchange_rate)
            if exchange_rate_calc:
                settlement_details.set_exchange_rate_calc(exchange_rate_calc)
            if settlement_date:
                settlement_details.set_settlement_date(settlement_date)
            if pset:
                settlement_details.set_pset(pset)
            return settlement_details.build()
        else:
            return None

    def __set_ticket_details(self, split_qty, client, trade_date, give_up_broker, net_gross_ind, agreed_price: str):
        if split_qty is not None:
            ticket_details = self.ticket_details
            ticket_details.set_split_quantity(split_qty)
            if client:
                ticket_details.set_client(client)
            if trade_date:
                ticket_details.set_trade_date(trade_date)
            if give_up_broker:
                ticket_details.set_give_up_broker(give_up_broker)
            if net_gross_ind:
                ticket_details.set_net_gross_ind(net_gross_ind)
            if agreed_price:
                ticket_details.set_agreed_price(agreed_price)
            return ticket_details.build()

    def split_book(self, split_booking_params: list, row_numbers: list = None):
        if row_numbers:
            self.split_booking_details.set_rows_numbers(row_numbers)
        self.split_booking_details.set_split_booking_parameter(split_booking_params)
        call(self.split_booking_call, self.split_booking_details.build())
        self.clear_details([self.split_booking_details])

    def direct_moc_extract_error_message(self, qty, route):
        self.extract_direct_values.extractionId = "DirectErrorMessageExtractionID"
        self.extract_direct_values.extractedValues.append(self.extraction_error_message_details)
        response = call(self.direct_moc_request_correct_call,
                        direct_moc_request("UnmatchedQty", qty, route, self.extract_direct_values))
        self.clear_details([self.extraction_error_message_details, self.extract_direct_values])
        return response
