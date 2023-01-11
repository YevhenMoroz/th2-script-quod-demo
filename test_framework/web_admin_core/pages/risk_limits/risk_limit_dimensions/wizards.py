import time

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.risk_limits.risk_limit_dimensions.constants import Constants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class MainWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_close(self):
        self.find_by_xpath(Constants.Wizard.CLOSE_WIZARD_BUTTON).click()

    def click_on_ok_button(self):
        self.find_by_xpath(Constants.Wizard.OK_BUTTON).click()

    def click_on_cancel_button(self):
        self.find_by_xpath(Constants.Wizard.CANCEL_BUTTON).click()

    def click_on_save_changes(self):
        self.find_by_xpath(Constants.Wizard.SAVE_CHANGES_BUTTON).click()

    def click_on_revert_changes(self):
        self.find_by_xpath(Constants.Wizard.REVERT_CHANGES).click()

    def click_on_clear_changes(self):
        self.find_by_xpath(Constants.Wizard.CLEAR_CHANGES_BUTTON).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(Constants.Wizard.DOWNLOAD_PDF_BUTTON).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def is_dimensions_limit_info_message_appears(self):
        return self.is_element_present(Constants.Wizard.DIMENSIONS_LIMIT_INFO_MESSAGE)


class ValuesTab(CommonPage):
    def set_name(self, value):
        self.set_text_by_xpath(Constants.Wizard.ValuesTab.NAME, value)

    def get_name(self):
        return self.get_text_by_xpath(Constants.Wizard.ValuesTab.NAME)

    def set_description(self, value):
        self.set_text_by_xpath(Constants.Wizard.ValuesTab.DESCRIPTION, value)

    def get_description(self):
        return self.get_text_by_xpath(Constants.Wizard.ValuesTab.DESCRIPTION)

    def set_trading_limits(self, values: list):
        self.set_checkbox_list(Constants.Wizard.ValuesTab.TRADING_LIMITS, values)

    def get_trading_limits(self):
        return self.get_text_by_xpath(Constants.Wizard.ValuesTab.TRADING_LIMITS)

    def set_cum_trading_limits(self, values: list):
        self.set_checkbox_list(Constants.Wizard.ValuesTab.CUM_TRADING_LIMITS, values)

    def get_cum_trading_limits(self):
        return self.get_text_by_xpath(Constants.Wizard.ValuesTab.CUM_TRADING_LIMITS)

    def get_all_cum_trading_limits_from_drop_menu(self):
        if not self.is_element_present(Constants.Wizard.CHECKBOX_DROP_DOWN_MENU):
            self.find_by_xpath(Constants.Wizard.ValuesTab.CUM_TRADING_LIMITS).click()
        time.sleep(1)
        return self.get_all_items_from_drop_down(Constants.Wizard.CHECKBOX_DROP_DOWN_MENU)

    def set_position_limits(self, values: list):
        self.set_checkbox_list(Constants.Wizard.ValuesTab.POSITION_LIMITS, values)

    def get_position_limits(self):
        return self.get_text_by_xpath(Constants.Wizard.ValuesTab.POSITION_LIMITS)

    def get_all_position_limits_from_drop_menu(self):
        if not self.is_element_present(Constants.Wizard.CHECKBOX_DROP_DOWN_MENU):
            self.find_by_xpath(Constants.Wizard.ValuesTab.POSITION_LIMITS).click()
        time.sleep(1)
        return self.get_all_items_from_drop_down(Constants.Wizard.CHECKBOX_DROP_DOWN_MENU)

    def is_position_limit_field_displayed(self):
        return self.is_element_present(Constants.Wizard.DimensionsTab.POSITION_LIMITS)

    def set_buying_powers(self, values: list):
        self.set_checkbox_list(Constants.Wizard.ValuesTab.BUYING_POWERS, values)

    def get_buying_powers(self):
        return self.get_text_by_xpath(Constants.Wizard.ValuesTab.BUYING_POWERS)

    def get_all_buying_powers_from_drop_menu(self):
        if not self.is_element_present(Constants.Wizard.CHECKBOX_DROP_DOWN_MENU):
            self.find_by_xpath(Constants.Wizard.ValuesTab.BUYING_POWERS).click()
        time.sleep(1)
        return self.get_all_items_from_drop_down(Constants.Wizard.CHECKBOX_DROP_DOWN_MENU)


class DimensionsTab(CommonPage):
    def set_accounts_dimension(self, value):
        self.set_combobox_value(Constants.Wizard.DimensionsTab.ACCOUNT_DIMENSIONS, value)

    def get_accounts_dimension(self):
        return self.get_text_by_xpath(Constants.Wizard.DimensionsTab.ACCOUNT_DIMENSIONS)

    def is_accounts_dimension_enabled(self):
        return self.is_field_enabled(Constants.Wizard.DimensionsTab.ACCOUNT_DIMENSIONS)

    def set_accounts(self, value: list):
        self.set_checkbox_list(Constants.Wizard.DimensionsTab.ACCOUNTS, value)

    def get_accounts(self):
        return self.get_text_by_xpath(Constants.Wizard.DimensionsTab.ACCOUNTS)

    def get_all_accounts_from_drop_menu(self):
        if not self.is_element_present(Constants.Wizard.CHECKBOX_DROP_DOWN_MENU):
            self.find_by_xpath(Constants.Wizard.DimensionsTab.ACCOUNTS).click()
        time.sleep(1)
        return self.get_all_items_from_drop_down(Constants.Wizard.CHECKBOX_DROP_DOWN_MENU)

    def is_accounts_enabled(self):
        return self.is_field_enabled(Constants.Wizard.DimensionsTab.ACCOUNTS)

    def set_clients(self, value):
        self.set_checkbox_list(Constants.Wizard.DimensionsTab.CLIENTS, value)

    def get_clients(self):
        return self.get_text_by_xpath(Constants.Wizard.DimensionsTab.CLIENTS)

    def get_all_clients_from_drop_menu(self):
        if not self.is_element_present(Constants.Wizard.CHECKBOX_DROP_DOWN_MENU):
            self.find_by_xpath(Constants.Wizard.DimensionsTab.CLIENTS).click()
        time.sleep(1)
        return self.get_all_items_from_drop_down(Constants.Wizard.CHECKBOX_DROP_DOWN_MENU)

    def is_clients_enabled(self):
        return self.is_field_enabled(Constants.Wizard.DimensionsTab.CLIENTS)

    def set_client_list(self, value):
        self.set_combobox_value(Constants.Wizard.DimensionsTab.CLIENT_LIST, value)

    def get_client_list(self):
        return self.get_text_by_xpath(Constants.Wizard.DimensionsTab.CLIENT_LIST)

    def get_all_client_list_from_drop_menu(self):
        if not self.is_element_present(Constants.Wizard.DROP_DOWN_MENU):
            self.find_by_xpath(Constants.Wizard.DimensionsTab.CLIENT_LIST).click()
        time.sleep(1)
        return self.get_all_items_from_drop_down(Constants.Wizard.DROP_DOWN_MENU)

    def is_client_list_enabled(self):
        return self.is_field_enabled(Constants.Wizard.DimensionsTab.CLIENT_LIST)

    def set_users_dimension(self, value):
        self.set_combobox_value(Constants.Wizard.DimensionsTab.USER_DIMENSIONS, value)

    def get_users_dimension(self):
        return self.get_text_by_xpath(Constants.Wizard.DimensionsTab.USER_DIMENSIONS)

    def is_users_dimension_enabled(self):
        return self.is_field_enabled(Constants.Wizard.DimensionsTab.USER_DIMENSIONS)

    def set_desks(self, value):
        self.set_checkbox_list(Constants.Wizard.DimensionsTab.DESKS, value)

    def get_desks(self):
        return self.get_text_by_xpath(Constants.Wizard.DimensionsTab.DESKS)

    def get_all_desks_from_drop_menu(self):
        if not self.is_element_present(Constants.Wizard.CHECKBOX_DROP_DOWN_MENU):
            self.find_by_xpath(Constants.Wizard.DimensionsTab.DESKS).click()
        time.sleep(1)
        return self.get_all_items_from_drop_down(Constants.Wizard.CHECKBOX_DROP_DOWN_MENU)

    def is_desks_enabled(self):
        return self.is_field_enabled(Constants.Wizard.DimensionsTab.DESKS)

    def set_user(self, value: list):
        self.set_checkbox_list(Constants.Wizard.DimensionsTab.USERS, value)

    def get_user(self):
        return self.get_text_by_xpath(Constants.Wizard.DimensionsTab.USERS)

    def get_all_user_from_drop_menu(self):
        if not self.is_element_present(Constants.Wizard.CHECKBOX_DROP_DOWN_MENU):
            self.find_by_xpath(Constants.Wizard.DimensionsTab.USERS).click()
        time.sleep(1)
        return self.get_all_items_from_drop_down(Constants.Wizard.CHECKBOX_DROP_DOWN_MENU)

    def is_user_enabled(self):
        return self.is_field_enabled(Constants.Wizard.DimensionsTab.USERS)

    def set_reference_data_dimension(self, value):
        self.set_combobox_value(Constants.Wizard.DimensionsTab.REFERENCE_DATA_DIMENSIONS, value)

    def get_reference_data_dimension(self):
        return self.get_text_by_xpath(Constants.Wizard.DimensionsTab.REFERENCE_DATA_DIMENSIONS)

    def get_all_reference_data_dimension_from_drop_menu(self):
        self.find_by_xpath(Constants.Wizard.DimensionsTab.REFERENCE_DATA_DIMENSIONS).click()
        time.sleep(1)
        return self.get_all_items_from_drop_down(Constants.Wizard.DROP_DOWN_MENU)

    def is_reference_data_enabled(self):
        return self.is_field_enabled(Constants.Wizard.DimensionsTab.REFERENCE_DATA_DIMENSIONS)

    def set_venue(self, value):
        self.set_combobox_value(Constants.Wizard.DimensionsTab.VENUES, value)

    def get_venue(self):
        return self.get_text_by_xpath(Constants.Wizard.DimensionsTab.VENUES)

    def get_all_venues_from_drop_menu(self):
        self.find_by_xpath(Constants.Wizard.DimensionsTab.VENUES).click()
        time.sleep(1)
        return self.get_all_items_from_drop_down(Constants.Wizard.DROP_DOWN_MENU)

    def is_venue_enabled(self):
        return self.is_field_enabled(Constants.Wizard.DimensionsTab.VENUES)

    def set_sub_venue(self, value):
        self.set_combobox_value(Constants.Wizard.DimensionsTab.SUB_VENUE, value)

    def get_sub_venue(self):
        return self.get_text_by_xpath(Constants.Wizard.DimensionsTab.SUB_VENUE)

    def get_all_sub_venues_from_drop_menu(self):
        self.find_by_xpath(Constants.Wizard.DimensionsTab.SUB_VENUE).click()
        time.sleep(1)
        return self.get_all_items_from_drop_down(Constants.Wizard.DROP_DOWN_MENU)

    def is_sub_venue_enabled(self):
        return self.is_field_enabled(Constants.Wizard.DimensionsTab.SUB_VENUE)

    def set_listing_group(self, value):
        self.set_combobox_value(Constants.Wizard.DimensionsTab.LISTING_GROUP, value)

    def get_listing_group(self):
        return self.get_text_by_xpath(Constants.Wizard.DimensionsTab.LISTING_GROUP)

    def get_all_listing_group_from_drop_menu(self):
        self.find_by_xpath(Constants.Wizard.DimensionsTab.LISTING_GROUP).click()
        time.sleep(1)
        return self.get_all_items_from_drop_down(Constants.Wizard.DROP_DOWN_MENU)

    def is_listing_group_enabled(self):
        return self.is_field_enabled(Constants.Wizard.DimensionsTab.LISTING_GROUP)

    def set_listing(self, value):
        self.set_combobox_value(Constants.Wizard.DimensionsTab.LISTING, value)

    def get_listing(self):
        return self.get_text_by_xpath(Constants.Wizard.DimensionsTab.LISTING)

    def is_listing_enabled(self):
        return self.is_field_enabled(Constants.Wizard.DimensionsTab.LISTING)

    def set_instrument_type(self, value):
        self.set_combobox_value(Constants.Wizard.DimensionsTab.INSTRUMENT_TYPE, value)

    def get_instrument_type(self):
        return self.get_text_by_xpath(Constants.Wizard.DimensionsTab.INSTRUMENT_TYPE)

    def is_instrument_type_enabled(self):
        return self.is_field_enabled(Constants.Wizard.DimensionsTab.INSTRUMENT_TYPE)

    def is_instrument_type_field_displayed(self):
        return self.is_element_present(Constants.Wizard.DimensionsTab.INSTRUMENT_TYPE)

    def set_trading_phase(self, value):
        self.set_combobox_value(Constants.Wizard.DimensionsTab.TRADING_PHASE, value)

    def get_trading_phase(self):
        return self.get_text_by_xpath(Constants.Wizard.DimensionsTab.TRADING_PHASE)

    def is_trading_phase_field_displayed(self):
        return self.is_element_present(Constants.Wizard.DimensionsTab.TRADING_PHASE)

    def is_trading_phase_enabled(self):
        return self.is_field_enabled(Constants.Wizard.DimensionsTab.TRADING_PHASE)

    def set_route(self, value):
        self.set_combobox_value(Constants.Wizard.DimensionsTab.ROUTE, value)

    def get_route(self):
        return self.get_text_by_xpath(Constants.Wizard.DimensionsTab.ROUTE)

    def is_route_field_displayed(self):
        return self.is_element_present(Constants.Wizard.DimensionsTab.ROUTE)

    def is_route_enabled(self):
        return self.is_field_enabled(Constants.Wizard.DimensionsTab.ROUTE)

    def set_execution_policy(self, value):
        self.set_combobox_value(Constants.Wizard.DimensionsTab.EXECUTION_POLICY, value)

    def get_execution_policy(self):
        return self.get_text_by_xpath(Constants.Wizard.DimensionsTab.EXECUTION_POLICY)

    def is_execution_policy_field_displayed(self):
        return self.is_element_present(Constants.Wizard.DimensionsTab.EXECUTION_POLICY)

    def is_execution_policy_enabled(self):
        return self.is_field_enabled(Constants.Wizard.DimensionsTab.EXECUTION_POLICY)

    def set_position_type(self, value):
        self.set_combobox_value(Constants.Wizard.DimensionsTab.POSITION_TYPE, value)

    def get_position_type(self):
        return self.get_text_by_xpath(Constants.Wizard.DimensionsTab.POSITION_TYPE)

    def get_all_position_type_from_drop_menu(self):
        self.find_by_xpath(Constants.Wizard.DimensionsTab.POSITION_TYPE).click()
        time.sleep(1)
        return self.get_all_items_from_drop_down(Constants.Wizard.DROP_DOWN_MENU)

    def is_position_type_enabled(self):
        return self.is_field_enabled(Constants.Wizard.DimensionsTab.POSITION_TYPE)

    def is_position_type_field_displayed(self):
        return self.is_element_present(Constants.Wizard.DimensionsTab.POSITION_TYPE)

    def set_position_validity(self, value):
        self.set_combobox_value(Constants.Wizard.DimensionsTab.POSITION_VALIDITY, value)

    def get_position_validity(self):
        return self.get_text_by_xpath(Constants.Wizard.DimensionsTab.POSITION_VALIDITY)

    def is_position_validity_field_displayed(self):
        return self.is_element_present(Constants.Wizard.DimensionsTab.POSITION_VALIDITY)

    def is_position_validity_enabled(self):
        return self.is_field_enabled(Constants.Wizard.DimensionsTab.POSITION_VALIDITY)

    def set_settlement_period(self, value):
        self.set_combobox_value(Constants.Wizard.DimensionsTab.SETTLEMENT_PERIOD, value)

    def get_settlement_period(self):
        return self.get_text_by_xpath(Constants.Wizard.DimensionsTab.SETTLEMENT_PERIOD)

    def is_settlement_period_field_displayed(self):
        return self.is_element_present(Constants.Wizard.DimensionsTab.SETTLEMENT_PERIOD)

    def is_settlement_period_enabled(self):
        return self.is_field_enabled(Constants.Wizard.DimensionsTab.SETTLEMENT_PERIOD)

    def set_side(self, value):
        self.set_combobox_value(Constants.Wizard.DimensionsTab.SIDE, value)

    def get_side(self):
        return self.get_text_by_xpath(Constants.Wizard.DimensionsTab.SIDE)

    def is_side_field_displayed(self):
        return self.is_element_present(Constants.Wizard.DimensionsTab.SIDE)

    def is_side_enabled(self):
        return self.is_field_enabled(Constants.Wizard.DimensionsTab.SIDE)


class AssignmentsTab(CommonPage):
    def set_institution(self, value):
        self.set_combobox_value(Constants.Wizard.AssignmentsTab.INSTITUTION, value)

    def clear_institution_field(self):
        self.set_text_by_xpath(Constants.Wizard.AssignmentsTab.INSTITUTION, "")

    def get_institution(self):
        return self.get_text_by_xpath(Constants.Wizard.AssignmentsTab.INSTITUTION)

    def is_institution_field_enable(self):
        return self.is_field_enabled(Constants.Wizard.AssignmentsTab.INSTITUTION)
