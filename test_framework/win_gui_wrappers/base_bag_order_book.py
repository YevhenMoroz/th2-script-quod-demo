from test_framework.win_gui_wrappers.base_window import BaseWindow
from win_gui_modules.utils import call


class BaseBasketOrderBook(BaseWindow):
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

    # endregion

    # region Set details
    def set_order_bag_wave_details(self, price=None, qty=None, display_qty=None, price_type=None, price_offset=None,
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
    def extract_order_bag_book_details(self, extraction_id, extraction_fields: list, filter: list,
                                       sub_extraction_fields: list, sub_filter: list):
        self.bag_order_details.set_default_params(self.base_request)
        self.bag_order_details.set_extraction_id(extraction_id)
        self.bag_order_details.set_filter(filter)
        fields = []
        for field in extraction_fields:
            fields.append(self.extraction_bag_fields_details("orderbagwave." + field, field))

        lvl1_info = self.bag_order_info.create(
            action=self.extraction_bag_order_action.create_extraction_action(
                extraction_details=fields))

        lvl1_details = self.get_order_bag_book_details_request.create(info=lvl1_info)
        lvl1_details.set_filter(sub_filter)

        self.bag_order_details.add_single_bag_order_info(
            self.bag_order_info.create(
                action=self.extraction_bag_order_action.create_extraction_action(
                    extraction_details=sub_extraction_fields),
                sub_orders=lvl1_details))

        response = call(self.order_bag_wave_extraction_call, self.bag_order_details.build())
        return response

    # endregion

    # region Action
    def wave_bag(self):
        call(self.wave_bag_creation_call, self.bag_wave_creation.build())

    def modify_wave_bag(self):
        call(self.modify_wave_bag_call, self.bag_wave_creation.build())
    # endregion
