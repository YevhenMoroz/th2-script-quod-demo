from custom.verifier import Verifier
from test_framework.win_gui_wrappers.base_window import BaseWindow
from test_framework.win_gui_wrappers.fe_trading_constant import PriceNaming, ClientPrisingTileAction, RFQPanelValues, \
    RFQPanelPtsAndPx, RFQPanelQty, RFQPanelHeaderValues
from win_gui_modules.dealer_intervention_wrappers import ExtractionDetailsRequest, ModificationRequest
from win_gui_modules.order_book_wrappers import ExtractionDetail
from win_gui_modules.utils import call


class BaseDealerIntervention(BaseWindow):
    # region Base constructor
    def __init__(self, case_id, session_id):
        super().__init__(case_id, session_id)
        # Need to override
        self.base_data = None
        self.extraction_request = None
        self.rfq_extraction_request = None
        self.modification_request = None
        self.assign_to_me_call = None
        self.un_assign_to_me_call = None
        self.estimate_call = None
        self.modify_call = None
        self.getAssignedDetails_call = None
        self.getUnAssignedDetails_call = None
        self.getRFQDetail_call = None
        self.service = None

    # endregion
    # region Common func
    def set_default_params(self):
        self.extraction_request.set_extraction_id(self.extraction_id)
        self.extraction_request = ExtractionDetailsRequest(self.base_data)
        self.modification_request = ModificationRequest(base=self.base_request)
        self.verifier = Verifier(self.case_id)

    def set_list_filter(self, filter_list: list):
        """
        Receives list as an argument, where the elements
        are in order - key, value, key, value, ...
        For example ["Qty", "123456", "Owner", "QA1", etc]
        """
        self.base_data.set_filter_list(filter_list)
        return self

    def set_dict_filter(self, filter_dict: dict):
        """
        Receives dict as an argument, where the elements
        are in order - key:value, key:value, ...
        For example {"Qty": "123456", "Owner": "QA1", etc}
        """
        self.base_data.set_filter_dict(filter_dict)
        return self

    def clear_filters(self, row_number: int = None, assigned: bool = False, un_assigned: bool = False):
        """
        Clear filters for assigned or unassigned grid depend on received params,
        can clear for row
        """
        if row_number is not None:
            self.base_data.set_row_number(row_number)
        self.extraction_request.set_clear_flag()
        if assigned is True:
            call(self.getAssignedDetails_call, self.extraction_request.build())
        if un_assigned is True:
            call(self.getUnAssignedDetails_call, self.extraction_request.build())
        if assigned is False and un_assigned is False:
            call(self.getAssignedDetails_call, self.extraction_request.build())
            call(self.getUnAssignedDetails_call, self.extraction_request.build())

    # endregion
    # region Assigning and Actions
    def assign_quote(self, row_number: int = None):
        """
        Assigning to you quote from unassigned grid, can select row number
        """
        if row_number is not None:
            self.base_data.set_row_number(row_number)
        call(self.assign_to_me_call, self.base_data.build())

    def un_assign_quote(self, row_number: int = None):
        """
        Un assigning quote from assigned grid, can select row number
        """
        if row_number is not None:
            self.base_data.set_row_number(row_number)
        call(self.un_assign_to_me_call, self.base_data.build())

    def estimate_quote(self):
        """Estimate selected quote"""
        call(self.estimate_call, self.base_data.build())

    def send_quote(self):
        """
        Press send on tile
        """
        self.modification_request.send()
        call(self.modify_call, self.modification_request.build())
        self.clear_details([self.modification_request])
        self.set_default_params()

    def reject_quote(self):
        """
        Press reject on tile
        """
        self.modification_request.reject()
        call(self.modify_call, self.modification_request.build())
        self.clear_details([self.modification_request])
        self.set_default_params()

    def click_hedged_checkbox(self):
        """
        Click on Automatically Hedge Executions
        """
        self.modification_request.click_is_hedged_chec_box()
        call(self.modify_call, self.modification_request.build())
        self.clear_details([self.modification_request])
        self.set_default_params()
        # endregion

    def set_price_and_ttl(self, ttl: str = None, bid_large: str = None, bid_small: str = None, ask_large: str = None,
                          ask_small: str = None, spread: str = None):
        """
        Set price on tile in Dealer Intervention window
        -----Example of usage-----
        self.dealer_intervention.set_price_and_ttl(bid_large="1.18", ttl = "10")
        """
        if ttl is not None:
            self.modification_request.set_quote_ttl(ttl)
        if bid_large is not None:
            self.modification_request.set_bid_large(bid_large)
        if bid_small is not None:
            self.modification_request.set_bid_small(bid_small)
        if ask_large is not None:
            self.modification_request.set_ask_large(ask_large)
        if ask_small is not None:
            self.modification_request.set_ask_small(ask_small)
        if spread is not None:
            self.modification_request.set_spread_step(spread)
        call(self.modify_call, self.modification_request.build())
        self.clear_details([self.modification_request])
        self.set_default_params()

    def modify_spread(self, *args: ClientPrisingTileAction):
        """
        Modify spread on tile in Dealer Intervention window
         -----Example of usage-----
        action = ClientPrisingTileAction.widen_spread
        self.dealer_intervention.modify_spread(action)
        """
        if ClientPrisingTileAction.increase_ask in args:
            self.modification_request.increase_ask()
        if ClientPrisingTileAction.decrease_ask in args:
            self.modification_request.decrease_ask()
        if ClientPrisingTileAction.increase_bid in args:
            self.modification_request.increase_bid()
        if ClientPrisingTileAction.decrease_bid in args:
            self.modification_request.decrease_bid()
        if ClientPrisingTileAction.narrow_spread in args:
            self.modification_request.narrow_spread()
        if ClientPrisingTileAction.widen_spread in args:
            self.modification_request.widen_spread()
        if ClientPrisingTileAction.skew_towards_ask in args:
            self.modification_request.skew_towards_ask()
        if ClientPrisingTileAction.skew_towards_bid in args:
            self.modification_request.skew_towards_bid()
        call(self.modify_call, self.modification_request.build())
        self.clear_details([self.modification_request])
        self.set_default_params()

    # endregion
    # region Extraction and  Check
    def extract_field_from_unassigned(self, column_name: str, row_number: int = None) -> str:
        field = ExtractionDetail(column_name, column_name)
        self.extraction_request.add_extraction_detail(field)
        if row_number is not None:
            self.base_data.set_row_number(row_number)
        response = call(self.getUnAssignedDetails_call, self.extraction_request.build())
        self.clear_details([self.extraction_request])
        self.set_default_params()
        return response[column_name]

    def extract_field_from_assigned(self, column_name: str, row_number: int = None) -> str:
        self.extraction_request.add_extraction_detail(
            ExtractionDetail(column_name, column_name))
        if row_number is not None:
            self.base_data.set_row_number(row_number)
        response = call(self.getAssignedDetails_call, self.extraction_request.build())
        self.clear_details([self.extraction_request])
        self.set_default_params()
        return response[column_name]

    def extract_field_list_from_unassigned(self, list_fields: dict, row_number: int = None) -> dict:
        """
        Receives dict as an argument, where the key is column name what
        we extract from GUI and return new dict where
        key = key and value is extracted field from FE
        """
        if row_number is not None:
            self.base_data.set_row_number(row_number)
        list_of_fields = []
        for field in list_fields.items():
            key = list(field)[0]
            field = ExtractionDetail(key, key)
            list_of_fields.append(field)
        self.extraction_request.add_extraction_details(list_of_fields)
        response = call(self.getUnAssignedDetails_call, self.extraction_request.build())
        self.clear_details([self.extraction_request])
        self.set_default_params()
        return response

    def extract_field_list_from_assigned(self, list_fields: dict, row_number: int = None) -> dict:
        """
        Receives dict as an argument, where the key is column name what
        we extract from GUI and return new dict where
        key = key and value is extracted field from FE
        """
        if row_number is not None:
            self.base_data.set_row_number(row_number)
        list_of_fields = []
        for field in list_fields.items():
            key = list(field)[0]
            field = ExtractionDetail(key, key)
            list_of_fields.append(field)
        self.extraction_request.add_extraction_details(list_of_fields)
        response = call(self.getAssignedDetails_call, self.extraction_request.build())
        self.clear_details([self.extraction_request])
        self.set_default_params()
        return response

    def check_unassigned_fields(self, expected_fields: dict, event_name="Check Unassigned Dealer Intervention"):
        """
        Receives dict as an argument, where the key is column name what
        we extract from GUI and value is expected result
        For example {"Sts": "Terminated", "Owner": "QA1", etc}
        """
        actual_list = self.extract_field_list_from_unassigned(expected_fields)
        for items in expected_fields.items():
            key = list(items)[0]
            value = list(items)[1]
            self.verifier.set_event_name(event_name)
            self.verifier.compare_values(key, value, actual_list[key])
        self.verifier.verify()

    def check_assigned_fields(self, expected_fields: dict, event_name="Check Assigned Dealer Intervention"):
        """
        Receives dict as an argument, where the key is column name what
        we extract from GUI and value is expected result
        For example {"Sts": "Terminated", "Owner": "QA1", etc}
        """
        actual_list = self.extract_field_list_from_assigned(expected_fields)
        for items in expected_fields.items():
            key = list(items)[0]
            value = list(items)[1]
            self.verifier.set_event_name(event_name)
            self.verifier.compare_values(key, value, actual_list[key])
        self.verifier.verify()

    def extract_price_and_ttl_from_di_panel(self, *args: PriceNaming):
        """
        Extract prises and ttl from DI
        -----Example of usage-----
        bid_large = PriceNaming.ask_large
        extracted_value = self.dealer_intervention.extract_price_and_ttl_from_di_panel(bid_large)
        to receive extracted value -----> value = extracted_value[bid_large.value]
        """
        if PriceNaming.ask_large in args:
            self.rfq_extraction_request.extract_ask_price_large(PriceNaming.ask_large.value)
        if PriceNaming.ask_pips in args:
            self.rfq_extraction_request.extract_ask_price_pips(PriceNaming.ask_pips.value)
        if PriceNaming.bid_large in args:
            self.rfq_extraction_request.extract_bid_price_large(PriceNaming.bid_large.value)
        if PriceNaming.bid_pips in args:
            self.rfq_extraction_request.extract_bid_price_pips(PriceNaming.bid_pips.value)
        if PriceNaming.spread in args:
            self.rfq_extraction_request.extract_price_spread(PriceNaming.spread.value)
        if PriceNaming.ttl in args:
            self.rfq_extraction_request.extract_quote_ttl(PriceNaming.ttl.value)
        response = call(self.getRFQDetail_call, self.rfq_extraction_request.build())
        self.clear_details([self.rfq_extraction_request])
        self.set_default_params()
        return response

    def extract_header_part_from_di_panel(self, *args: RFQPanelHeaderValues):
        """
        Extract  instrument, tenors, settldates, party, sides, currency, states from DI panel
        -----Example of usage-----
        instrument = RFQPanelHeaderValues.instrument_label_control
        extracted_values = self.dealer_intervention.extract_header_part_from_di_panel(instrument)
        to receive extracted value-----> value = extracted_values[instrument.value]
        """
        if RFQPanelHeaderValues.instrument_label_control in args:
            self.rfq_extraction_request.extract_instrument_label_control(
                RFQPanelHeaderValues.instrument_label_control.value)
        if RFQPanelHeaderValues.currency_value_label_control in args:
            self.rfq_extraction_request.extract_currency_value_label_control(
                RFQPanelHeaderValues.currency_value_label_control.value)
        if RFQPanelHeaderValues.near_tenor_label in args:
            self.rfq_extraction_request.extract_near_tenor_label(RFQPanelHeaderValues.near_tenor_label.value)
        if RFQPanelHeaderValues.far_tenor_label in args:
            self.rfq_extraction_request.extract_far_tenor_label(RFQPanelHeaderValues.far_tenor_label.value)
        if RFQPanelHeaderValues.near_settl_date_label in args:
            self.rfq_extraction_request.extract_near_settl_date_label(RFQPanelHeaderValues.near_settl_date_label.value)
        if RFQPanelHeaderValues.far_settl_date_label in args:
            self.rfq_extraction_request.extract_far_settl_date_label(RFQPanelHeaderValues.far_settl_date_label.value)
        if RFQPanelHeaderValues.party_value_label_control in args:
            self.rfq_extraction_request.extract_party_value_label_control(
                RFQPanelHeaderValues.party_value_label_control.value)
        if RFQPanelHeaderValues.request_side_value_label_control in args:
            self.rfq_extraction_request.extract_request_side_value_label_control(
                RFQPanelHeaderValues.request_side_value_label_control.value)
        if RFQPanelHeaderValues.request_side in args:
            self.rfq_extraction_request.extract_request_side(
                RFQPanelHeaderValues.request_side.value)
        if RFQPanelHeaderValues.request_state in args:
            self.rfq_extraction_request.extract_request_state(RFQPanelHeaderValues.request_state.value)
        if RFQPanelHeaderValues.quote_state_value_label_control in args:
            self.rfq_extraction_request.extract_quote_state_value_label_control(
                RFQPanelHeaderValues.quote_state_value_label_control.value)
        if RFQPanelHeaderValues.fill_side_value_label_control in args:
            self.rfq_extraction_request.extract_fill_side_value_label_control(
                RFQPanelHeaderValues.fill_side_value_label_control.value)
        if RFQPanelHeaderValues.case_state_value_label_control in args:
            self.rfq_extraction_request.extract_case_state_value_label_control(
                RFQPanelHeaderValues.case_state_value_label_control.value)
        if RFQPanelHeaderValues.creation_value_label_control in args:
            self.rfq_extraction_request.extract_creation_value_label_control(
                RFQPanelHeaderValues.creation_value_label_control.value)
        response = call(self.getRFQDetail_call, self.rfq_extraction_request.build())
        self.clear_details([self.rfq_extraction_request])
        self.set_default_params()
        return response

    def extract_qty_from_di_panel(self, *args: RFQPanelQty):
        """
        Extract  NearLegQty, FarLegQty, NearQty, FarQty,NearOppositeQty, FarOppositeQty from DI panel
        -----Example of usage-----
        near_leg_quantity = RFQPanelQty.near_leg_quantity
        extracted_values = self.dealer_intervention.extract_qty_from_di_panel(near_leg_quantity)
        to receive extracted value-----> value = extracted_values[instrument.value]
        """
        if RFQPanelQty.near_leg_quantity in args:
            self.rfq_extraction_request.extract_near_leg_quantity(RFQPanelQty.near_leg_quantity.value)
        if RFQPanelQty.far_leg_quantity in args:
            self.rfq_extraction_request.extract_far_leg_quantity(RFQPanelQty.far_leg_quantity.value)
        if RFQPanelQty.opposite_near_bid_qty_value_label in args:
            self.rfq_extraction_request.extract_opposite_near_bid_qty_value_label(
                RFQPanelQty.opposite_near_bid_qty_value_label.value)
        if RFQPanelQty.opposite_far_bid_qty_value_label in args:
            self.rfq_extraction_request.extract_opposite_far_bid_qty_value_label(
                RFQPanelQty.opposite_far_bid_qty_value_label.value)
        if RFQPanelQty.opposite_near_ask_qty_value_label in args:
            self.rfq_extraction_request.extract_opposite_near_ask_qty_value_label(
                RFQPanelQty.opposite_near_ask_qty_value_label.value)
        if RFQPanelQty.opposite_far_ask_qty_value_label in args:
            self.rfq_extraction_request.extract_opposite_far_ask_qty_value_label(
                RFQPanelQty.opposite_far_ask_qty_value_label.value)
        response = call(self.getRFQDetail_call, self.rfq_extraction_request.build())
        # self.clear_details([self.rfq_extraction_request])
        # self.set_default_params()
        return response

    def extract_px_and_pts_from_di_panel(self, *args: RFQPanelPtsAndPx):
        """
        Extract  NearLegQty, FarLegQty, NearQty, FarQty,NearOppositeQty, FarOppositeQty from DI panel
        -----Example of usage-----
        bid_swap_pts = RFQPanelPtsAndPx.bid_value_label
        extracted_values = self.dealer_intervention.extract_px_and_pts_from_di_panel(bid_swap_pts)
        to receive extracted value-----> value = extracted_values[bid_swap_pts.value]
        """
        if RFQPanelPtsAndPx.bid_value_label in args:
            self.rfq_extraction_request.extract_bid_value_label(RFQPanelPtsAndPx.bid_value_label.value)
        if RFQPanelPtsAndPx.ask_value_label in args:
            self.rfq_extraction_request.extract_ask_value_label(RFQPanelPtsAndPx.ask_value_label.value)
        if RFQPanelPtsAndPx.ask_near_points_value_label in args:
            self.rfq_extraction_request.extract_ask_near_points_value_label(
                RFQPanelPtsAndPx.ask_near_points_value_label.value)
        if RFQPanelPtsAndPx.ask_far_points_value_label in args:
            self.rfq_extraction_request.extract_ask_far_points_value_label(
                RFQPanelPtsAndPx.ask_far_points_value_label.value)
        if RFQPanelPtsAndPx.bid_near_points_value_label in args:
            self.rfq_extraction_request.extract_bid_near_points_value_label(
                RFQPanelPtsAndPx.bid_near_points_value_label.value)
        if RFQPanelPtsAndPx.bid_far_points_value_label in args:
            self.rfq_extraction_request.extract_bid_far_points_value_label(
                RFQPanelPtsAndPx.bid_far_points_value_label.value)
        if RFQPanelPtsAndPx.bid_near_price_value_label in args:
            self.rfq_extraction_request.extract_bid_near_price_value_label(
                RFQPanelPtsAndPx.bid_near_price_value_label.value)
        if RFQPanelPtsAndPx.bid_far_price_value_label in args:
            self.rfq_extraction_request.extract_bid_far_price_value_label(
                RFQPanelPtsAndPx.bid_far_price_value_label.value)
        if RFQPanelPtsAndPx.ask_near_price_value_label in args:
            self.rfq_extraction_request.extract_ask_near_price_value_label(
                RFQPanelPtsAndPx.ask_near_price_value_label.value)
        if RFQPanelPtsAndPx.ask_far_price_value_label in args:
            self.rfq_extraction_request.extract_ask_far_price_value_label(
                RFQPanelPtsAndPx.ask_far_price_value_label.value)
        response = call(self.getRFQDetail_call, self.rfq_extraction_request.build())
        self.clear_details([self.rfq_extraction_request])
        self.set_default_params()
        return response

    def extract_state_from_di_panel(self, *args: RFQPanelValues):
        """
        Extract  state of price`s and qty`s fields from DI panel
        -----Example of usage-----
        text = RFQPanelValues.button_text
        extracted_values = self.dealer_intervention.extract_state_from_di_panel(text)
        to receive extracted value-----> value = extracted_values[text.value]
        """
        if RFQPanelValues.button_text in args:
            self.rfq_extraction_request.extract_button_text(
                RFQPanelValues.button_text.value)
        if RFQPanelValues.is_bid_price_pips_enabled in args:
            self.rfq_extraction_request.extract_is_bid_price_pips_enabled(
                RFQPanelValues.is_bid_price_pips_enabled.value)
        if RFQPanelValues.is_ask_price_pips_enabled in args:
            self.rfq_extraction_request.extract_is_ask_price_pips_enabled(
                RFQPanelValues.is_ask_price_pips_enabled.value)
        if RFQPanelValues.is_near_leg_quantity_enabled in args:
            self.rfq_extraction_request.extract_is_near_leg_quantity_enabled(
                RFQPanelValues.is_near_leg_quantity_enabled.value)
        if RFQPanelValues.is_far_leg_quantity_enabled in args:
            self.rfq_extraction_request.extract_is_far_leg_quantity_enabled(
                RFQPanelValues.is_far_leg_quantity_enabled.value)
        if RFQPanelValues.is_price_spread_enabled in args:
            self.rfq_extraction_request.extract_is_price_spread_enabled(
                RFQPanelValues.is_price_spread_enabled.value)
        if RFQPanelValues.is_bid_price_large_enabled in args:
            self.rfq_extraction_request.extract_is_bid_price_large_enabled(
                RFQPanelValues.is_bid_price_large_enabled.value)
        if RFQPanelValues.is_ask_price_large_enabled in args:
            self.rfq_extraction_request.extract_is_ask_price_large_enabled(
                RFQPanelValues.is_ask_price_large_enabled.value)
        response = call(self.getRFQDetail_call, self.rfq_extraction_request.build())
        self.clear_details([self.rfq_extraction_request])
        self.set_default_params()
        return response

    # endregion

    # region Close window
    def close_window(self):
        call(self.service.closeWindow, self.base_request)
    # endregion
