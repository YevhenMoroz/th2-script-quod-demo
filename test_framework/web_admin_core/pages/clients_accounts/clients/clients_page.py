import time

from test_framework.web_admin_core.pages.clients_accounts.clients.clients_constants import ClientsConstants
from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class ClientsPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_enable_disable(self):
        self.find_by_xpath(ClientsConstants.ENABLE_DISABLE_TOGGLE_BUTTON_XPATH).click()
        self.find_by_xpath(ClientsConstants.OK_BUTTON_XPATH).click()

    def is_client_enable(self):
        return self.is_toggle_button_enabled(ClientsConstants.ENABLE_DISABLE_TOGGLE_BUTTON_XPATH)

    def click_on_more_actions(self):
        self.find_by_xpath(ClientsConstants.MORE_ACTIONS_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(ClientsConstants.EDIT_XPATH).click()

    def click_on_clone(self):
        self.find_by_xpath(ClientsConstants.CLONE_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(ClientsConstants.DOWNLOAD_PDF_BUTTON_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_on_pin_row(self):
        self.find_by_xpath(ClientsConstants.PIN_ROW_XPATH).click()

    def click_on_new(self):
        self.find_by_xpath(ClientsConstants.NEW_BUTTON_XPATH).click()

    def click_on_user_icon(self):
        self.find_by_xpath(ClientsConstants.USER_ICON_AT_RIGHT_CORNER).click()

    def click_on_logout(self):
        self.find_by_xpath(ClientsConstants.LOGOUT_BUTTON_XPATH).click()

    def click_on_load_button(self):
        self.find_by_xpath(ClientsConstants.LOAD_BUTTON).click()

    def set_name(self, value):
        self.set_text_by_xpath(ClientsConstants.MAIN_PAGE_NAME_FILTER_XPATH, value)

    def set_description(self, value):
        self.set_text_by_xpath(ClientsConstants.MAIN_PAGE_DESCRIPTION_FILTER_XPATH, value)

    def set_clearing_account_type(self, value):
        self.set_text_by_xpath(ClientsConstants.MAIN_PAGE_CLEARING_ACCOUNT_TYPE_FILTER_XPATH, value)

    def set_booking_ins(self, value):
        self.set_text_by_xpath(ClientsConstants.MAIN_PAGE_BOOKING_INS_FILTER_XPATH, value)

    def set_allocation_preference(self, value):
        self.set_text_by_xpath(ClientsConstants.MAIN_PAGE_ALLOCATION_PREFERENCE_FILTER_XPATH, value)

    def set_disclose_exec(self, value):
        self.set_text_by_xpath(ClientsConstants.MAIN_PAGE_DISCLOSE_EXEC_FILTER_XPATH, value)

    def set_client_group(self, value):
        self.set_text_by_xpath(ClientsConstants.MAIN_PAGE_CLIENT_GROUP_FILTER_XPATH, value)

    def set_client_name_for_load(self, value):
        self.set_text_by_xpath(ClientsConstants.CLIENT_LOAD_FILTER, value)

    def get_clearing_account_type(self):
        return self.find_by_xpath(ClientsConstants.MAIN_PAGE_CLEARING_ACCOUNT_TYPE_XPATH).text

    def get_client_name(self):
        return self.find_by_xpath(ClientsConstants.MAIN_PAGE_CLIENT_NAME).text

    def get_popup_text(self):
        popup = self.find_by_xpath(ClientsConstants.POPUP_TEXT_XPATH)
        text = popup.text

        popup.click()
        return text

    def load_client_from_global_filter(self, client):
        self.set_client_name_for_load(client)
        time.sleep(1)
        self.click_on_load_button()
        time.sleep(1)

    def is_client_lookup_displayed_in_header(self):
        return self.is_element_present(ClientsConstants.CLIENT_LOAD_FILTER)

    def is_searched_client_found(self, value):
        return self.is_element_present(ClientsConstants.DISPLAYED_CLIENT_XPATH.format(value))

    def set_global_filter(self, value):
        self.set_text_by_xpath(ClientsConstants.MAIN_PAGE_GLOBAL_FILTER_XPATH, value)

    def get_venue_names(self):
        self.horizontal_scroll(ClientsConstants.VENUE_NAMES_ROW)
        return self.find_by_xpath(ClientsConstants.VENUE_NAMES_ROW).text

    def get_route_names(self):
        self.horizontal_scroll(ClientsConstants.ROUTE_NAMES_ROW)
        return self.find_by_xpath(ClientsConstants.ROUTE_NAMES_ROW).text
