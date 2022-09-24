from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.market_making.client_tier.client_tier_constants import \
    ClientTierConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class ClientTiersInstrumentTenorsSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_plus(self):
        self.find_by_xpath(
            ClientTierConstants.CLIENT_TIER_INSTRUMENTS_TENORS_TAB_PLUS_BUTTON_XPATH).click()

    def click_on_checkmark(self):
        self.find_by_xpath(
            ClientTierConstants.CLIENT_TIER_INSTRUMENTS_TENORS_TAB_CHECKMARK_BUTTON_XPATH).click()

    def click_on_close(self):
        self.find_by_xpath(
            ClientTierConstants.CLIENT_TIER_INSTRUMENTS_TENORS_TAB_CLOSE_BUTTON_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(
            ClientTierConstants.CLIENT_TIER_INSTRUMENTS_TENORS_TAB_EDIT_BUTTON_XPATH).click()

    def click_on_delete(self):
        self.find_by_xpath(
            ClientTierConstants.CLIENT_TIER_INSTRUMENTS_TENORS_TAB_DELETE_BUTTON_XPATH).click()

    def set_tenor(self, value):
        self.set_combobox_value(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_TENORS_TAB_TENOR_XPATH, value)

    def set_tenor_filter(self, value):
        self.set_text_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_TENORS_TAB_TENOR_FILTER_XPATH, value)

    def get_tenor(self):
        return self.get_text_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_TENORS_TAB_TENOR_XPATH)

    def click_on_created_tenor(self, value):
        self.find_by_xpath(ClientTierConstants
                           .CLIENT_TIER_INSTRUMENTS_TENORS_TAB_CREATED_TENOR_ENTITY_XPATH.format(value)).click()

    def set_min_spread(self, value: int):
        self.set_text_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_TENORS_TAB_MIN_SPREAD_XPATH, str(value))

    def get_min_spread(self):
        return self.get_text_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_TENORS_TAB_MIN_SPREAD_XPATH)

    def set_max_spread(self, value: int):
        self.set_text_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_TENORS_TAB_MAX_SPREAD_XPATH, str(value))

    def get_max_spread(self):
        return self.get_text_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_TENORS_TAB_MAX_SPREAD_XPATH)

    def set_margin_format(self, value):
        self.set_combobox_value(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_TENORS_TAB_MARGIN_FORMAT_XPATH, value)

    def get_margin_format(self):
        return self.get_text_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_TENORS_TAB_MARGIN_FORMAT_XPATH)

    def click_on_executable_checkbox(self):
        self.find_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_TENORS_TAB_EXECUTABLE_CHECKBOX_XPATH).click()

    def get_executable(self):
        return self.is_checkbox_selected(
            ClientTierConstants.CLIENT_TIER_INSTRUMENTS_TENORS_TAB_EXECUTABLE_CHECKBOX_XPATH)

    def click_on_pricing_checkbox(self):
        self.find_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_TENORS_TAB_PRICING_CHECKBOX_XPATH).click()

    def get_pricing(self):
        return self.is_checkbox_selected(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_TENORS_TAB_PRICING_CHECKBOX_XPATH)

    def click_on_client_price_slippage_range_checkbox(self):
        self.find_by_xpath(
            ClientTierConstants.CLIENT_TIER_INSTRUMENTS_TENORS_TAB_CLIENT_PRICE_SLIPPAGE_RANGE_CHECKBOX_XPATH).click()

    def set_client_price_slippage_range(self, value: int):
        self.set_text_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_TENORS_TAB_CLIENT_PRICE_SLIPPAGE_RANGE_XPATH,
                               str(value))

    def get_client_price_slippage_range(self):
        return self.get_text_by_xpath(
            ClientTierConstants.CLIENT_TIER_INSTRUMENTS_TENORS_TAB_CLIENT_PRICE_SLIPPAGE_RANGE_XPATH)

    def is_client_price_slippage_range_field_enabled(self):
        return self.is_field_enabled(ClientTierConstants.
                                     CLIENT_TIER_INSTRUMENTS_TENORS_TAB_CLIENT_PRICE_SLIPPAGE_RANGE_XPATH)

    def click_on_minimum_price_checkbox(self):
        self.find_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_TENORS_TAB_MINIMUM_PRICE_CHECKBOX_XPATH).click()

    def set_minimum_price(self, value: int):
        self.set_text_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_TENORS_TAB_MINIMUM_PRICE_XPATH, str(value))

    def get_minimum_price(self):
        return self.get_text_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_TENORS_TAB_MINIMUM_PRICE_XPATH)

    def click_on_maximum_price(self):
        self.find_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_TENORS_TAB_MAXIMUM_PRICE_CHECKBOX_XPATH).click()

    def set_maximum_price(self, value: int):
        self.set_text_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_TENORS_TAB_MAXIMUM_PRICE_XPATH, str(value))

    def get_maximum_price(self):
        return self.get_text_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_TENORS_TAB_MAXIMUM_PRICE_XPATH)

    def click_on_automated_margin_strategies_enabled_checkbox(self):
        self.find_by_xpath(
            ClientTierConstants.CLIENT_TIER_INSTRUMENTS_TENORS_TAB_AUTOMATED_MARGIN_STRATEGIES_ENABLED_CHECKBOX_XPATH).click()

    def get_automated_margin_strategies_enabled(self):
        return self.is_checkbox_selected(
            ClientTierConstants.CLIENT_TIER_INSTRUMENTS_TENORS_TAB_AUTOMATED_MARGIN_STRATEGIES_ENABLED_CHECKBOX_XPATH)

    def click_on_position_based_margins(self):
        self.find_by_xpath(
            ClientTierConstants.CLIENT_TIER_INSTRUMENTS_TENORS_TAB_POSITION_BASED_MARGINS_CHECKBOX_XPATH).click()

    def get_position_based_margins(self):
        return self.is_checkbox_selected(
            ClientTierConstants.CLIENT_TIER_INSTRUMENTS_TENORS_TAB_POSITION_BASED_MARGINS_CHECKBOX_XPATH)

    def set_position_book(self, value):
        self.set_combobox_value(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_TENORS_TAB_POSITION_BOOK_XPATH, value)

    def get_position_book(self):
        return self.get_text_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_TENORS_TAB_POSITION_BOOK_XPATH)

    # base margins tab

    def click_on_plus_button_at_base_margin_tab(self):
        self.find_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_BASE_MARGINS_SUB_TAB_PLUS_BUTTON_XPATH).click()

    def click_on_edit_at_base_margins_tab(self):
        self.find_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_BASE_MARGINS_SUB_TAB_EDIT_BUTTON_XPATH).click()

    def click_on_edit_at_base_margins_tab_by_values(self, value):
        self.find_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_BASE_MARGINS_SUB_TAB_EDIT_BUTTON_BY_VALUE_XPATH.
                           format(value)).click()

    def click_on_delete_at_base_margins_tab_by_values(self, value):
        self.find_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_BASE_MARGINS_SUB_TAB_DELETE_BUTTON_BY_VALUE_XPATH.
                           format(value)).click()

    def click_on_checkmark_at_base_margins_tab(self):
        self.find_by_xpath(
            ClientTierConstants.CLIENT_TIER_INSTRUMENTS_BASE_MARGINS_SUB_TAB_CHECKMARK_BUTTON_XPATH).click()

    def click_on_close_at_base_margins_tab(self):
        self.find_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_BASE_MARGINS_SUB_TAB_CLOSE_BUTTON_XPATH).click()

    def click_on_executable_checkbox_at_base_margins_tab(self):
        self.find_by_xpath(
            ClientTierConstants.CLIENT_TIER_INSTRUMENTS_BASE_MARGINS_SUB_TAB_EXECUTABLE_CHECKBOX_XPATH).click()

    def click_on_pricing_checkbox_at_base_margins_tab(self):
        self.find_by_xpath(
            ClientTierConstants.CLIENT_TIER_INSTRUMENTS_BASE_MARGINS_SUB_TAB_PRICING_CHECKBOX_XPATH).click()

    def click_on_publish_prices_checkbox_at_base_margins_tab(self):
        self.find_by_xpath(
            ClientTierConstants.CLIENT_TIER_INSTRUMENTS_BASE_MARGINS_SUB_TAB_PUBLISH_PRICES_CHECKBOX_XPATH).click()

    def is_publish_prices_checkbox_selected_at_base_margins_tab(self):
        return self.is_checkbox_selected(
            ClientTierConstants.CLIENT_TIER_INSTRUMENTS_BASE_MARGINS_SUB_TAB_PUBLISH_PRICES_CHECKBOX_XPATH)

    def set_quantity_at_base_margin_tab(self, value):
        self.set_text_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_BASE_MARGINS_SUB_TAB_QUANTITY_XPATH, value)

    def is_quantity_field_enable_at_base_margin_tab(self):
        return self.is_field_enabled(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_BASE_MARGINS_SUB_TAB_QUANTITY_XPATH)

    def get_quantity_at_base_margins_tab(self):
        return self.find_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_BASE_MARGINS_SUB_TAB_QUANTITY_XPATH).text

    def set_quantity_filter_at_base_margins_tab(self, value: int):
        self.set_text_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_BASE_MARGINS_SUB_TAB_QUANTITY_FILTER_XPATH,
                               str(value))

    def get_all_list_quantity_at_base_margin_tab(self):
        return self._get_all_items_from_table_column(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_BASE_MARGINS_SUB_TAB_QUANTITY_TABLE_ROW_XPATH)

    def set_bid_margin_at_base_margins_tab(self, value):
        self.set_text_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_BASE_MARGINS_SUB_TAB_BID_MARGIN_XPATH,value)

    def get_bid_margin_at_base_margins_tab(self):
        return self.find_by_xpath(
            ClientTierConstants.CLIENT_TIER_INSTRUMENTS_BASE_MARGINS_SUB_TAB_BID_MARGIN_XPATH).text

    def set_bid_margin_filter_at_base_margins_tab(self, value):
        self.set_text_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_BASE_MARGINS_SUB_TAB_BID_MARGIN_FILTER_XPATH,
                               value)

    def set_offer_margin_at_base_margins_tab(self, value):
        self.set_text_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_BASE_MARGINS_SUB_TAB_OFFER_MARGIN_XPATH,
                               value)

    def get_offer_margin_at_base_margins_tab(self):
        return self.find_by_xpath(
            ClientTierConstants.CLIENT_TIER_INSTRUMENTS_BASE_MARGINS_SUB_TAB_OFFER_MARGIN_XPATH).text

    def set_offer_margin_filter_at_base_margins_tab(self, value):
        self.set_text_by_xpath(
            ClientTierConstants.CLIENT_TIER_INSTRUMENTS_BASE_MARGINS_SUB_TAB_OFFER_MARGIN_FILTER_XPATH, value)

    def get_executable_at_base_margins_tab(self):
        return self.is_checkbox_selected(
            ClientTierConstants.CLIENT_TIER_INSTRUMENTS_BASE_MARGINS_SUB_TAB_EXECUTABLE_CHECKBOX_XPATH)

    def get_pricing_at_base_margins_tab(self):
        return self.is_checkbox_selected(
            ClientTierConstants.CLIENT_TIER_INSTRUMENTS_BASE_MARGINS_SUB_TAB_PRICING_CHECKBOX_XPATH)

    def set_executable_filter_at_base_margins_tab(self, value):
        self.set_text_by_xpath(
            ClientTierConstants.CLIENT_TIER_INSTRUMENTS_BASE_MARGINS_SUB_TAB_EXECUTABLE_MARGIN_FILTER_XPATH, value)

    def set_pricing_filter_at_base_margins_tab(self, value):
        self.set_text_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_BASE_MARGINS_SUB_TAB_PRICING_FILTER_XPATH,
                               value)

    # position levels tab

    def click_on_plus_button_at_position_levels_tab(self):
        self.find_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_POSITION_LEVELS_TAB_PLUS_BUTTON_XPATH).click()

    def click_on_checkmark_at_position_levels_tab(self):
        self.find_by_xpath(
            ClientTierConstants.CLIENT_TIER_INSTRUMENTS_POSITION_LEVELS_TAB_CHECKMARK_BUTTON_XPATH).click()

    def click_on_close_button_at_position_levels_tab(self):
        self.find_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_POSITION_LEVELS_TAB_CLOSE_BUTTON_XPATH).click()

    def click_on_delete_button_at_position_levels_tab(self):
        self.find_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_POSITION_LEVELS_TAB_DELETE_BUTTON_XPATH).click()

    def click_on_edit_button_at_position_levels_tab(self):
        self.find_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_POSITION_LEVELS_TAB_EDIT_BUTTON_XPATH).click()

    def set_position_at_position_levels_tab(self, value):
        self.set_text_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_POSITION_LEVELS_TAB_POSITION_XPATH,
                               str(value))

    def get_position_at_position_levels_tab(self):
        return self.get_text_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_POSITION_LEVELS_TAB_POSITION_XPATH)

    def set_position_filter_at_position_levels_tab(self, value):
        self.set_text_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_POSITION_LEVELS_TAB_POSITION_FILTER_XPATH,
                               value)

    def set_bid_margin_at_position_levels_tab(self, value):
        self.set_text_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_POSITION_LEVELS_TAB_BID_MARGIN_XPATH, value)

    def get_bid_margin_at_position_levels_tab(self):
        return self.get_text_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_POSITION_LEVELS_TAB_BID_MARGIN_XPATH)

    def set_bid_margin_filter_at_position_levels_tab(self, value):
        self.set_text_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_POSITION_LEVELS_TAB_BID_MARGIN_FILTER_XPATH,
                               value)

    def set_offer_margin_at_position_levels_tab(self, value):
        self.set_text_by_xpath(ClientTierConstants.CLIENT_TIER_INSTRUMENTS_POSITION_LEVELS_TAB_OFFER_MARGIN_XPATH,
                               value)

    def get_offer_margin_at_position_levels_tab(self):
        return self.get_text_by_xpath(
            ClientTierConstants.CLIENT_TIER_INSTRUMENTS_POSITION_LEVELS_TAB_OFFER_MARGIN_XPATH)

    def set_offer_margin_filter_at_position_levels_tab(self, value):
        self.set_text_by_xpath(
            ClientTierConstants.CLIENT_TIER_INSTRUMENTS_BASE_MARGINS_SUB_TAB_OFFER_MARGIN_FILTER_XPATH, value)

    def click_on_plus_for_tiered_quantity(self):
        self.find_by_xpath(ClientTierConstants.TIRED_QUANTITY_PLUS_BUTTON_AT_TENOR).click()

    def click_on_edit_for_tiered_quantity(self):
        self.find_by_xpath(ClientTierConstants.TIRED_QUANTITY_EDIT_BUTTON_AT_TENOR).click()

    def click_on_delete_for_tiered_quantity(self):
        self.find_by_xpath(ClientTierConstants.TIRED_QUANTITY_DELETE_BUTTON_AT_TENOR).click()

    def click_on_checkmark_for_tiered_quantity(self):
        self.find_by_xpath(ClientTierConstants.TIRED_QUANTITY_CHECKMARK_BUTTON_AT_TENOR).click()

    def click_on_cancel_for_tiered_quantity(self):
        self.find_by_xpath(ClientTierConstants.TIRED_QUANTITY_CANCEL_BUTTON_AT_TENOR).click()

    def set_quantity_for_tiered_quantity(self, value):
        self.set_text_by_xpath(ClientTierConstants.TIRED_QUANTITY_QUANTITY_INPUT_AT_TENOR, value)

    def get_quantity_for_tiered_quantity(self):
        self.get_text_by_xpath(ClientTierConstants.TIRED_QUANTITY_QUANTITY_INPUT_AT_TENOR)
