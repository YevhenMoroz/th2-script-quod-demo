from copy import deepcopy

from test_framework.win_gui_wrappers.base_window import BaseWindow
from win_gui_modules.bag_order_ticket import GetOrderBagBookDetails, BagOrderInfo
from win_gui_modules.utils import call


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
        self.order_bag_creation_call = None
        self.order_bag_extraction_call = None
        self.extraction_bag_order_action_static = None

    # endregion

    # region Set details
    def set_order_bag_wave_details(self, price=None, qty=None, display_qty=None, price_type=None,
                                   price_offset=None,
                                   offset_type=None,
                                   scope=None, sub_lvl_number: int = None, sub_lvl_filter: list = None,
                                   wave_filter: list = None):
        self.bag_wave_creation.set_default_params(self.base_request)
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
        self.bag_wave_creation.add_bag_ticket_details(self.base_request, self.bag_book_details.build())
        return self.bag_wave_creation

    # endregion

    # region Get details
    def extract_order_bag_book_details(self, extraction_id, extraction_fields: list, filter: list = None):
        self.bag_order_details.set_default_params(self.base_request)
        self.bag_order_details.set_extraction_id(extraction_id)
        if filter is not None:
            self.bag_order_details.set_filter(filter)
        fields = []
        for field in extraction_fields:
            fields.append(self.extraction_bag_fields_details("order_bag." + field, field))

        self.bag_order_info = self.bag_order_info()
        self.bag_order_info.set_number(1)
        self.extraction_bag_order_action.add_details(fields)
        self.bag_order_info.add_single_extraction_action(self.extraction_bag_order_action)
        self.bag_order_details.add_single_bag_order_info(self.bag_order_info)
        self.clear_details([self.bag_order_details, self.extraction_bag_order_action])
        response = call(self.order_bag_extraction_call, self.bag_order_details.build())
        return response

    # endregion

    def extract_from_order_bag_book_and_wave_tab(self, extraction_id, extraction_fields: list,
                                                 sub_extraction_fields: list, sub_filter: list = None,
                                                 filter: list = None, tab_name : str = None):
        self.bag_order_details.set_default_params(self.base_request)
        self.bag_order_details.set_extraction_id(extraction_id)
        if filter is not None:
            self.bag_order_details.set_filter(filter)
        fields = []
        sub_fields = []
        for field in extraction_fields:
            fields.append(self.extraction_bag_fields_details("order_bag." + field, field))
        for sub_field in sub_extraction_fields:
            sub_fields.append(self.extraction_bag_fields_details("order_bag_wave." + sub_field, sub_field))
        lvl_2 = self.extraction_bag_order_action_static.create_extraction_action(extraction_details=sub_fields)
        lvl_1 = self.extraction_bag_order_action_static.create_extraction_action(extraction_details=fields)
        bag_order_info_second_level = self.bag_order_info()
        bag_order_info_second_level.add_single_extraction_action(lvl_2)
        if tab_name:
            bag_order_info_second_level.set_sub_orders_details(tab_name)
        order_bag_book_details = GetOrderBagBookDetails.create(info=bag_order_info_second_level)
        if sub_filter:
            order_bag_book_details.set_filter(sub_filter)
        bag_order_ingo_main = BagOrderInfo.create(action=lvl_1, sub_orders=order_bag_book_details)
        self.bag_order_details.add_single_bag_order_info(bag_order_ingo_main)
        response = call(self.order_bag_extraction_call, self.bag_order_details.build())
        self.clear_details([self.bag_order_details, self.extraction_bag_order_action])
        return response

    # region Action
    def wave_bag(self):
        call(self.wave_bag_creation_call, self.bag_wave_creation.build())

    def modify_wave_bag(self):
        call(self.modify_wave_bag_call, self.bag_wave_creation.build())

    # endregion
    def create_bag_details(self, rows_list: list, name_of_bag: str):
        self.order_bag_creation_details.set_rows(rows_list)
        self.order_bag_creation_details.set_order_bag_ticket_details(name_of_bag)
        return self.order_bag_creation_details

    def create_bag(self):
        call(self.order_bag_creation_call, self.order_bag_creation_details.build())
        self.clear_details([self.order_bag_creation_details, self.bag_book_details])
