import enum
from copy import deepcopy

from enum import Enum

from stubs import Stubs
from test_framework.win_gui_wrappers.base_window import BaseWindow
from win_gui_modules.bag_order_ticket import GetOrderBagBookDetails, BagOrderInfo
from win_gui_modules.middle_office_wrappers import ModifyTicketDetails
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

    # endregion

    # region Set details
    def set_order_bag_wave_details(self, tif: str, expire_date: str = None, price=None, qty=None, display_qty=None,
                                   price_type=None,
                                   price_offset=None,
                                   offset_type=None,
                                   scope=None, sub_lvl_number: int = None, sub_lvl_filter: list = None,
                                   wave_filter: list = None):
        self.bag_wave_creation.set_default_params(self.base_request)
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

    # region Get details
    def extract_order_bag_book_details(self, extraction_id, extraction_fields: list, filter: list = None):
        self.bag_order_details.set_default_params(self.base_request)
        self.bag_order_details.set_extraction_id(extraction_id)
        if filter is not None:
            self.bag_order_details.set_filter(filter)
        fields = []
        for field in extraction_fields:
            fields.append(self.extraction_bag_fields_details("order_bag." + field, field))

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
        for field in extraction_fields:
            fields.append(self.extraction_bag_fields_details("order_bag." + field, field))
        for sub_field in sub_extraction_fields:
            sub_fields.append(self.extraction_bag_fields_details("order_bag_second_level." + sub_field, sub_field))
        lvl_2 = self.extraction_bag_order_action_static.create_extraction_action(extraction_details=sub_fields)
        lvl_1 = self.extraction_bag_order_action_static.create_extraction_action(extraction_details=fields)
        bag_order_info_second_level = self.bag_order_info()
        bag_order_info_second_level.add_single_extraction_action(lvl_2)
        order_bag_book_details = GetOrderBagBookDetails.create(info=bag_order_info_second_level)
        if sub_filter is not None:
            order_bag_book_details.set_filter(sub_filter)
        bag_order_ingo_main = BagOrderInfo.create(action=lvl_1, sub_orders=order_bag_book_details)
        bag_order_ingo_main.set_sub_level_tab(table_name)
        self.bag_order_details.add_single_bag_order_info(bag_order_ingo_main)
        response = call(self.order_bag_extraction_call, self.bag_order_details.build())
        self.clear_details([self.bag_order_details, self.extraction_bag_order_action])
        return response

    # region Action
    def wave_bag(self):
        result = call(self.wave_bag_creation_call, self.bag_wave_creation.build())
        return result

    def modify_wave_bag(self):
        call(self.modify_wave_bag_call, self.bag_wave_creation.build())

    # endregion
    def create_bag_details(self, rows_list: list, name_of_bag: str, price: str = None):
        self.order_bag_creation_details.set_rows(rows_list)
        if price:
            self.bag_book_details.set_price(price)
        if name_of_bag:
            self.bag_book_details.set_name(name_of_bag)
        self.order_bag_creation_details.set_order_bag_ticket_details(deepcopy(self.bag_book_details))
        self.clear_details([self.bag_book_details])

    def create_bag(self, politic_of_creation: classmethod = None):
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
