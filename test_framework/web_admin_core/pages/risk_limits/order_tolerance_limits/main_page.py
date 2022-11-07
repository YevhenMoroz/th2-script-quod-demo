import time

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.risk_limits.order_tolerance_limits.constants import \
    OrderToleranceLimitsConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class OrderToleranceLimitsPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_more_actions(self):
        self.find_by_xpath(OrderToleranceLimitsConstants.MORE_ACTIONS_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(OrderToleranceLimitsConstants.EDIT_XPATH).click()

    def click_on_clone(self):
        self.find_by_xpath(OrderToleranceLimitsConstants.CLONE_XPATH).click()

    def click_on_delete(self, confirmation):
        self.find_by_xpath(OrderToleranceLimitsConstants.DELETE_XPATH).click()
        if confirmation:
            time.sleep(2)
            self.find_by_xpath(OrderToleranceLimitsConstants.OK_BUTTON_XPATH).click()
        else:
            self.find_by_xpath(OrderToleranceLimitsConstants.CANCEL_BUTTON_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(OrderToleranceLimitsConstants.DOWNLOAD_PDF_BUTTON_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_download_csv_entity_button_and_check_csv(self):
        self.clear_download_directory()
        self.find_by_xpath(OrderToleranceLimitsConstants.MAIN_PAGE_DOWNLOAD_CSV_BUTTON_XPATH).click()
        time.sleep(2)
        return self.get_csv_context()

    def click_on_pin_row(self):
        self.find_by_xpath(OrderToleranceLimitsConstants.PIN_ROW_XPATH).click()

    def click_on_new(self):
        self.find_by_xpath(OrderToleranceLimitsConstants.NEW_BUTTON_XPATH).click()

    def click_on_user_icon(self):
        self.find_by_xpath(OrderToleranceLimitsConstants.USER_ICON_AT_RIGHT_CORNER).click()

    def click_on_logout(self):
        self.find_by_xpath(OrderToleranceLimitsConstants.LOGOUT_BUTTON_XPATH).click()

    def set_name(self, value):
        self.set_text_by_xpath(OrderToleranceLimitsConstants.MAIN_PAGE_NAME_FILTER_XPATH, value)

    def set_id(self, value):
        self.set_text_by_xpath(OrderToleranceLimitsConstants.MAIN_PAGE_ID_FILTER_XPATH, value)

    def set_client(self, value):
        self.set_text_by_xpath(OrderToleranceLimitsConstants.MAIN_PAGE_CLIENT_FILTER_XPATH, value)

    def set_user(self, value):
        self.set_text_by_xpath(OrderToleranceLimitsConstants.MAIN_PAGE_USER_FILTER_XPATH, value)

    def set_venue(self, value):
        self.set_text_by_xpath(OrderToleranceLimitsConstants.MAIN_PAGE_VENUE_FILTER_XPATH, value)

    def set_client_group(self, value):
        self.set_text_by_xpath(OrderToleranceLimitsConstants.MAIN_PAGE_CLIENT_GROUP_FILTER_XPATH, value)

    def set_listing_group(self, value):
        self.set_text_by_xpath(OrderToleranceLimitsConstants.MAIN_PAGE_LISTING_GROUP_FILTER_XPATH, value)

    def get_name(self):
        return self.find_by_xpath(OrderToleranceLimitsConstants.MAIN_PAGE_NAME_XPATH).text

    def get_id(self):
        return self.find_by_xpath(OrderToleranceLimitsConstants.MAIN_PAGE_ID_XPATH).text

    def get_client(self):
        return self.find_by_xpath(OrderToleranceLimitsConstants.MAIN_PAGE_CLIENT_XPATH).text

    def get_user(self):
        return self.find_by_xpath(OrderToleranceLimitsConstants.MAIN_PAGE_USER_XPATH).text

    def get_venue(self):
        return self.find_by_xpath(OrderToleranceLimitsConstants.MAIN_PAGE_VENUE_XPATH).text

    def get_client_group(self):
        return self.find_by_xpath(OrderToleranceLimitsConstants.MAIN_PAGE_CLIENT_GROUP_XPATH).text

    def get_listing_group(self):
        return self.find_by_xpath(OrderToleranceLimitsConstants.MAIN_PAGE_LISTING_GROUP_XPATH).text

    def is_searched_entity_found_by_name(self, value):
        return self.is_element_present(OrderToleranceLimitsConstants.SEARCHED_VALUE_XPATH.format(value))
