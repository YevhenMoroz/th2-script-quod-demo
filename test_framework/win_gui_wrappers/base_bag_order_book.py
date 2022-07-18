import enum
from copy import deepcopy
from enum import Enum

from stubs import Stubs
from test_framework.win_gui_wrappers.base_window import BaseWindow
from win_gui_modules.bag_order_ticket import GetOrderBagBookDetails, BagOrderInfo
from win_gui_modules.middle_office_wrappers import ModifyTicketDetails
from win_gui_modules.order_ticket import OrderTicketDetails
from win_gui_modules.utils import call


@enum.unique
class EnumBagCreationPolitic(Enum):
    SPLIT_BY_AVG_PX = Stubs.win_act_bag_management_service.splitBagByQtyPriority
    SPLIT_BY_QTY_PRIORITY = Stubs.win_act_bag_management_service.splitBagByQtyPriority
    BAG_BY_AVG_PX_PRIORITY = Stubs.win_act_bag_management_service.bagByAvgPxPriority
    GROUP_INTO_BAG_FOR_GROUPING = Stubs.win_act_bag_management_service.groupIntoBagForGrouping


class BaseBagOrderBook(BaseWindow):
    # region Base constructor
    def __init__(self, case_id, session_id):
        super().__init__(case_id, session_id)
        self.bag_wave_creation = None
        self.bag_book_details = None
        self.pegs_details = None
        self.sub_level_details = None
        self.bag_order_details = None
        self.extraction_bag_fields_details = None
        self.bag_order_info = None
        self.extraction_bag_order_action = None
        self.get_order_bag_book_details_request = None
        self.wave_bag_creation_call = None
        self.modify_wave_bag_call = None
        self.order_bag_wave_extraction_call = None
        self.order_bag_creation_details = None
        self.order_bag_extraction_call = None
        self.extraction_bag_order_action_static = None
        self.order_bag_modification_call = None
        self.order_bag_cancel_bag_call = None
        self.order_bag_dissociate_bag_call = None
        self.order_bag_complete_details = None
        self.order_bag_complete_call = None
        self.order_bag_uncomplete_call = None
        self.order_bag_book_call = None
        self.create_order_call = None
        self.create_order_details = None
        self.modify_sub_level_order_details = None
        self.modify_sub_level_order_call = None
        self.extract_wave_ticket_values_request = None
        self.extract_wave_ticket_values_call = None
        self.cancel_wave_call = None
        self.scanario_details = None
        self.split_booking_call = None
        self.split_booking_details = None

    # endregion

    # region Set details
    def set_order_bag_wave_details(self, tif: str = None, expire_date: str = None, price=None, qty=None,
                                   display_qty=None,
                                   price_type=None,
                                   price_offset=None,
                                   offset_type=None,
                                   scope=None, sub_lvl_number: int = None, sub_lvl_filter: list = None,
                                   wave_filter: list = None):
        self.bag_wave_creation.set_default_params(self.base_request)
        if tif:
            self.bag_book_details.set_tif(tif)
        if expire_date:
            self.bag_book_details.set_expire_date(expire_date)
        if price is not None:
            self.bag_book_details.set_price(price)
        if qty is not None:
            self.bag_book_details.set_qty(qty)
        if display_qty is not None:
            self.bag_book_details.set_display_qty(display_qty)
        if price_type is not None:
            self.pegs_details.set_price_type(price_type)
        if price_offset is not None:
            self.pegs_details.set_price_offset(price_offset)
        if offset_type is not None:
            self.pegs_details.set_offset_type(offset_type)
        if scope is not None:
            self.pegs_details.set_scope(scope)
        if sub_lvl_number is not None:
            self.sub_level_details.set_number(sub_lvl_number)
        if sub_lvl_filter is not None:
            self.sub_level_details.set_filter(sub_lvl_filter)
        if sub_lvl_number or sub_lvl_filter is not None:
            self.bag_book_details.modify_wave_bag_details(self.sub_level_details.build())
        if price_type or price_offset or offset_type or scope is not None:
            self.bag_book_details.add_pegs_details(self.pegs_details.build())
        if wave_filter is not None:
            self.bag_wave_creation.set_filter(wave_filter)
        self.bag_wave_creation.add_bag_ticket_details(self.bag_book_details)
        return self.bag_wave_creation

    # endregion
    def set_twap_strategy(self, scenario: str,
                          strategy: str, start_date=None, start_date_offset="", end_date=None,
                          end_date_offset=""):
        self.scanario_details.set_scenario(scenario)
        self.scanario_details.set_strategy(strategy)
        twap_values = self.scanario_details.add_twap_strategy_param()
        if start_date and end_date is not None:
            twap_values.set_start_date(start_date, start_date_offset)
            twap_values.set_end_date(end_date, end_date_offset)
        self.bag_book_details.add_scenario_details(self.scanario_details.build())

    # region Get details
    def extract_order_bag_book_details(self, extraction_id, extraction_fields: list, filter: list = None):
        self.bag_order_details.set_default_params(self.base_request)
        self.bag_order_details.set_extraction_id(extraction_id)
        if filter is not None:
            self.bag_order_details.set_filter(filter)
        fields = []
        for field in extraction_fields:
            fields.append(self.extraction_bag_fields_details(field, field))

        bag_order_info = self.bag_order_info()
        bag_order_info.set_number(1)
        self.extraction_bag_order_action.add_details(fields)
        bag_order_info.add_single_extraction_action(self.extraction_bag_order_action)
        self.bag_order_details.add_single_bag_order_info(bag_order_info)
        response = call(self.order_bag_extraction_call, self.bag_order_details.build())
        self.clear_details([self.bag_order_details, self.extraction_bag_order_action])
        return response

    # endregion

    def extract_from_order_bag_book_and_other_tab(self, extraction_id, extraction_fields: list = None,
                                                  sub_extraction_fields: list = None, sub_filter: list = None,
                                                  filter: list = None, table_name: str = None):
        self.bag_order_details.set_default_params(self.base_request)
        self.bag_order_details.set_extraction_id(extraction_id)
        if filter is not None:
            self.bag_order_details.set_filter(filter)
        fields = []
        sub_fields = []
        if extraction_fields is not None:
            for field in extraction_fields:
                fields.append(self.extraction_bag_fields_details(field, field))
        for sub_field in sub_extraction_fields:
            sub_fields.append(self.extraction_bag_fields_details(sub_field, sub_field))
        lvl_2 = self.extraction_bag_order_action_static.create_extraction_action(extraction_details=sub_fields)
        if fields:
            lvl_1 = self.extraction_bag_order_action_static.create_extraction_action(extraction_details=fields)
        else:
            lvl_1 = self.extraction_bag_order_action_static.create_extraction_action()
        bag_order_info_second_level = self.bag_order_info()
        bag_order_info_second_level.add_single_extraction_action(lvl_2)
        order_bag_book_details = GetOrderBagBookDetails.create(info=bag_order_info_second_level)
        if sub_filter is not None:
            order_bag_book_details.set_filter(sub_filter)
        bag_order_ingo_main = BagOrderInfo.create(action=lvl_1, sub_orders=order_bag_book_details)
        if table_name:
            bag_order_ingo_main.set_sub_level_tab(table_name)
        self.bag_order_details.add_single_bag_order_info(bag_order_ingo_main)
        response = call(self.order_bag_extraction_call, self.bag_order_details.build())
        self.clear_details([self.bag_order_details, self.extraction_bag_order_action])
        return response

    def extraction_from_sub_levels_and_others_tab(self, extraction_id, extraction_fields, dict_of_filters: dict,
                                                  list_of_tab_name, count_of_levels: int):
        self.bag_order_details.set_default_params(self.base_request)
        self.bag_order_details.set_extraction_id(extraction_id)
        bag_order_info_list = []
        order_bag_book_details_list = []
        sub_fields = []
        for sub_field in extraction_fields:
            sub_fields.append(self.extraction_bag_fields_details(sub_field, sub_field))
        extraction_details = self.extraction_bag_order_action_static.create_extraction_action(
            extraction_details=sub_fields)
        for index in range(count_of_levels):
            bag_order_info_list.append(self.bag_order_info())
        bag_order_info_list[len(bag_order_info_list) - 1].add_single_extraction_action(extraction_details)
        for index in range(count_of_levels - 1):
            bag_order_info_list[index].set_sub_level_tab(list_of_tab_name[index])
            undefined_extraction_details = self.extraction_bag_order_action_static.create_extraction_action()
            bag_order_info_list[index].add_single_extraction_action(undefined_extraction_details)
        index_of_bag_book_details = 0
        for index in range(count_of_levels - 1, 0, -1):
            order_bag_book_details_list.append(GetOrderBagBookDetails.create(info=bag_order_info_list[index]))
            if dict_of_filters.get(count_of_levels):
                order_bag_book_details_list[index_of_bag_book_details].set_filter(dict_of_filters.get(count_of_levels))
            bag_order_info_list[index - 1].set_sub_orders_details(
                order_bag_book_details_list[index_of_bag_book_details])
            index_of_bag_book_details = index_of_bag_book_details + 1
            count_of_levels = count_of_levels - 1
        self.bag_order_details.add_single_bag_order_info(bag_order_info_list[0])
        if dict_of_filters.get(count_of_levels):
            self.bag_order_details.set_filter(dict_of_filters.get(count_of_levels))
        response = call(self.order_bag_extraction_call, self.bag_order_details.build())
        self.clear_details([self.bag_order_details])
        return response

    # region Action
    def wave_bag(self):
        result = call(self.wave_bag_creation_call, self.bag_wave_creation.build())
        self.clear_details([self.bag_wave_creation])
        return result

    def modify_wave_bag(self):
        call(self.modify_wave_bag_call, self.bag_wave_creation.build())
        self.clear_details([self.bag_wave_creation])

    # endregion
    def create_bag_details(self, rows_list: list, name_of_bag: str, price: str = None):
        self.order_bag_creation_details.set_rows(rows_list)
        if price:
            self.bag_book_details.set_price(price)
        if name_of_bag:
            self.bag_book_details.set_name(name_of_bag)
        self.order_bag_creation_details.set_order_bag_ticket_details(deepcopy(self.bag_book_details))
        self.clear_details([self.bag_book_details])

    def create_bag(self, politic_of_creation: EnumBagCreationPolitic = None):
        if politic_of_creation:
            call(politic_of_creation, self.order_bag_creation_details.build())
        else:
            call(EnumBagCreationPolitic.SPLIT_BY_AVG_PX, self.order_bag_creation_details.build())
        self.clear_details([self.order_bag_creation_details])

    # TODO rewrite it
    def modify_bag(self, price: int = None, name: str = None, on_deleting: bool = False,
                   filter_of_orders: list = None):
        if price:
            self.bag_book_details.set_price(price)
        if name:
            self.bag_book_details.set_name(name)
        self.bag_book_details.clear(on_deleting)
        # for i in range(0, len(filter_of_orders)):
        sub_level_details1 = deepcopy(self.sub_level_details)
        sub_level_details1.set_filter(['Id', 'CO1220401104827028001'])
        sub_level_details1.set_number(1)
        sub_level_details2 = deepcopy(self.sub_level_details)
        sub_level_details2.set_filter(['Id', 'CO1220401104823028001'])
        sub_level_details2.set_number(1)
        self.bag_book_details.modify_wave_bag_details([sub_level_details1.build()])
        self.bag_book_details.modify_wave_bag_details([sub_level_details2.build()])
        self.bag_wave_creation.add_bag_ticket_details(self.bag_book_details)
        call(self.order_bag_modification_call, self.bag_wave_creation.build())
        self.clear_details([self.bag_wave_creation, self.bag_book_details])

    def cancel_bag(self, filter_list: list):
        self.bag_wave_creation.set_filter = filter_list
        call(self.order_bag_cancel_bag_call, self.bag_wave_creation.build())
        self.clear_details([self.bag_wave_creation])

    def dissociate_bag(self, filter_list):
        self.bag_wave_creation.set_filter = filter_list
        call(self.order_bag_dissociate_bag_call, self.bag_wave_creation.build())
        self.clear_details([self.bag_wave_creation])

    def complete_or_un_complete_bag(self, filter_dict: dict, is_complete: bool = True):
        self.order_bag_complete_details.set_filter(filter_dict)
        self.order_bag_complete_details.set_is_complete(is_complete)
        if is_complete:
            call(self.order_bag_complete_call, self.order_bag_complete_details.build())
        else:
            call(self.order_bag_uncomplete_call, self.order_bag_complete_details.build())
        self.clear_details([self.order_bag_complete_details])

    def book_bag(self, modifyTicketDetails: ModifyTicketDetails):
        call(self.order_bag_book_call, modifyTicketDetails.build())
        self.clear_details([modifyTicketDetails])

    def set_create_order_details(self, filter_dict: dict, order_details: OrderTicketDetails):
        self.create_order_details.set_order_details(order_details)
        self.create_order_details.set_filter(filter_dict)
        call(self.create_order_call, self.create_order_details.build())
        self.clear_details([self.create_order_details, order_details])

    def set_modify_sub_level_order_details(self, filtel_dict: dict, order_details: OrderTicketDetails,
                                           sub_filter: dict):
        self.modify_sub_level_order_details.set_order_details(order_details)
        self.modify_sub_level_order_details.set_filter(filtel_dict)
        self.modify_sub_level_order_details.set_sub_filter(sub_filter)
        call(self.modify_sub_level_order_call, self.modify_sub_level_order_details.build())
        self.clear_details([self.modify_sub_level_order_details, order_details])

    def extract_values_from_wave_ticket(self, tif: bool = True, filter_dict: dict = None, error_message: bool = False,
                                        qty_to_release: bool = False):
        if self.bag_book_details:
            self.extract_wave_ticket_values_request.set_bag_order_details(self.bag_book_details)
        if filter_dict:
            self.extract_wave_ticket_values_request.set_filter(filter_dict)
        if tif:
            self.extract_wave_ticket_values_request.get_tif_state()
        if error_message:
            self.extract_wave_ticket_values_request.get_error_message()
        if qty_to_release:
            self.extract_wave_ticket_values_request.get_qty_to_release()
        result = call(self.extract_wave_ticket_values_call,
                      self.extract_wave_ticket_values_request.build())
        self.clear_details([self.extract_wave_ticket_values_request, self.bag_book_details])
        return result

    def cancel_wave(self):
        call(self.cancel_wave_call, self.bag_wave_creation.build())
        self.clear_details(self.bag_wave_creation)

    def split_book(self, split_booking_parameters: list, error_expected: bool = False, row_numbers: list = [1]):
        self.split_booking_details.set_split_booking_parameter(split_booking_parameters)
        self.split_booking_details.set_error_expected(error_expected)
        self.split_booking_details.set_rows_numbers(row_numbers)
        call(self.split_booking_call, self.split_booking_details.build())
