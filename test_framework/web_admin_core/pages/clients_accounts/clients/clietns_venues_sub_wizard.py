import time

from test_framework.web_admin_core.pages.clients_accounts.clients.clients_constants import ClientsConstants
from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class ClientsVenuesSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_plus(self):
        self.find_by_xpath(ClientsConstants.VENUES_TAB_PLUS_BUTTON_XPATH).click()

    def click_on_checkmark(self):
        self.find_by_xpath(ClientsConstants.VENUES_TAB_CHECKMARK_BUTTON_XPATH).click()

    def click_on_cancel(self):
        self.find_by_xpath(ClientsConstants.VENUES_TAB_CANCEL_BUTTON_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(ClientsConstants.VENUES_TAB_EDIT_BUTTON_XPATH).click()

    def click_on_delete(self):
        self.find_by_xpath(ClientsConstants.VENUES_TAB_DELETE_BUTTON_XPATH).click()

    def set_venue(self, value):
        self.set_combobox_value(ClientsConstants.VENUES_TAB_VENUE_XPATH, value)

    # for future: get_venue_in_edit_mode
    def get_venue(self):
        return self.get_text_by_xpath(ClientsConstants.VENUES_TAB_VENUE_XPATH)

    def get_venue_in_table(self):
        return self.find_by_xpath(ClientsConstants.VENUES_TAB_VENUE_TABLE).text

    def get_all_venue_from_drop_menu(self):
        self.click_on_plus()
        self.set_text_by_xpath(ClientsConstants.VENUES_TAB_VENUE_XPATH, "")
        time.sleep(1)
        available_venues = self.get_all_items_from_drop_down(ClientsConstants.DROP_DOWN_MENU_XPATH)
        self.click_on_cancel()
        return available_venues

    def set_venue_filter(self, value):
        self.set_text_by_xpath(ClientsConstants.VENUES_TAB_VENUE_FILTER_XPATH, value)

    def set_venue_client_name(self, value):
        self.set_text_by_xpath(ClientsConstants.VENUES_TAB_VENUE_CLIENT_NAME_XPATH, value)

    def get_venue_client_name(self):
        return self.get_text_by_xpath(ClientsConstants.VENUES_TAB_VENUE_CLIENT_NAME_XPATH)

    def set_venue_client_name_filter(self, value):
        self.set_text_by_xpath(ClientsConstants.VENUES_TAB_VENUE_CLIENT_NAME_FILTER_XPATH, value)

    def set_venue_client_account(self, value):
        self.set_text_by_xpath(ClientsConstants.VENUES_TAB_VENUE_CLIENT_ACCOUNT_GROUP_NAME_XPATH, value)

    def get_venue_client_account(self):
        return self.get_text_by_xpath(ClientsConstants.VENUES_TAB_VENUE_CLIENT_ACCOUNT_GROUP_NAME_XPATH)

    def set_default_route(self, value):
        self.set_combobox_value(ClientsConstants.VENUES_TAB_DEFAULT_ROUTE_XPATH, value)

    def get_default_route(self):
        return self.get_text_by_xpath(ClientsConstants.VENUES_TAB_DEFAULT_ROUTE_XPATH)

    def set_default_route_filter(self, value):
        self.set_text_by_xpath(ClientsConstants.VENUES_TAB_DEFAULT_ROUTE_FILTER_XPATH, value)

    def set_routing_param_group(self, value):
        self.set_combobox_value(ClientsConstants.VENUES_TAB_ROUTING_PARAM_GROUP_XPATH, value)

    def get_routing_param_group(self):
        return self.get_text_by_xpath(ClientsConstants.VENUES_TAB_ROUTING_PARAM_GROUP_XPATH)

    def set_routing_param_group_filter(self, value):
        self.set_combobox_value(ClientsConstants.VENUES_TAB_ROUTING_PARAM_GROUP_FILTER_XPATH, value)

    def set_max_commission_type(self, value):
        self.select_value_from_dropdown_list(ClientsConstants.VENUES_TAB_MAX_COMMISSION_TYPE_XPATH, value)

    def get_max_commission_type(self):
        self.get_text_by_xpath(ClientsConstants.VENUES_TAB_MAX_COMMISSION_TYPE_XPATH)

    def set_max_commission_filter(self, value):
        self.set_text_by_xpath(ClientsConstants.VENUES_TAB_MAX_COMMISSION_TYPE_FILTER_XPATH, value)

    def set_max_commission_value(self, value):
        self.set_text_by_xpath(ClientsConstants.VENUES_TAB_MAX_COMMISSION_VALUE_XPATH,value)

    def get_max_commission_value(self):
        return self.get_text_by_xpath(ClientsConstants.VENUES_TAB_MAX_COMMISSION_VALUE_XPATH)

    def set_max_commission_value_filter(self, value):
        self.set_text_by_xpath(ClientsConstants.VENUES_TAB_MAX_COMMISSION_VALUE_XPATH, value)

    def set_price_precision(self, value):
        self.set_text_by_xpath(ClientsConstants.VENUES_TAB_PRICE_PRECISION_XPATH, value)

    def get_price_precision(self):
        return self.get_text_by_xpath(ClientsConstants.VENUES_TAB_PRICE_PRECISION_XPATH)

    def set_price_precision_filter(self, value):
        self.set_text_by_xpath(ClientsConstants.VENUES_TAB_PRICE_PRECISION_FILTER_XPATH, value)

    def click_on_stamp_fee_exemption_checkbox(self):
        self.find_by_xpath(ClientsConstants.VENUES_TAB_STAMP_FEE_EXEMPTION_CHECKBOX_XPATH).click()

    def is_stamp_fee_exemption_selected(self):
        return self.is_checkbox_selected(ClientsConstants.VENUES_TAB_STAMP_FEE_EXEMPTION_CHECKBOX_XPATH)

    def click_on_levy_fee_exemption(self):
        self.find_by_xpath(ClientsConstants.VENUES_TAB_LEVY_FEE_EXEMPTION_CHECKBOX_XPATH).click()

    def is_levy_fee_exemption_selected(self):
        return self.is_checkbox_selected(ClientsConstants.VENUES_TAB_LEVY_FEE_EXEMPTION_CHECKBOX_XPATH)

    def click_per_transac_fee_exemption(self):
        self.find_by_xpath(ClientsConstants.VENUES_TAB_PER_TRANSAC_FEE_EXEMPTION_CHECKBOX_XPATH).click()

    def is_per_transac_fee_exemption_selected(self):
        return self.is_checkbox_selected(ClientsConstants.VENUES_TAB_PER_TRANSAC_FEE_EXEMPTION_CHECKBOX_XPATH)

    def is_venue_present(self):
        return self.is_element_present(ClientsConstants.VENUES_TAB_DELETE_BUTTON_XPATH)

    def create_new_venue(self, venue, venue_client_name, venue_client_account):
        self.click_on_plus()
        time.sleep(1)
        self.set_venue(venue)
        self.set_venue_client_name(venue_client_name)
        self.set_venue_client_account(venue_client_account)
        time.sleep(1)
        self.click_on_checkmark()
        



















