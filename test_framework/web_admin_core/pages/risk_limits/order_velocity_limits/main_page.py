import time

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.risk_limits.order_velocity_limits.constants import \
    OrderVelocityLimitsConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class OrderVelocityLimitsPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_more_actions(self):
        self.find_by_xpath(OrderVelocityLimitsConstants.MORE_ACTIONS_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(OrderVelocityLimitsConstants.EDIT_XPATH).click()

    def click_on_clone(self):
        self.find_by_xpath(OrderVelocityLimitsConstants.CLONE_XPATH).click()

    def click_on_delete(self, confirmation):
        self.find_by_xpath(OrderVelocityLimitsConstants.DELETE_XPATH).click()
        if confirmation:
            time.sleep(2)
            self.find_by_xpath(OrderVelocityLimitsConstants.OK_BUTTON_XPATH).click()
        else:
            self.find_by_xpath(OrderVelocityLimitsConstants.CANCEL_BUTTON_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(OrderVelocityLimitsConstants.DOWNLOAD_PDF_BUTTON_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_download_csv_entity_button_and_check_csv(self):
        self.clear_download_directory()
        self.find_by_xpath(OrderVelocityLimitsConstants.MAIN_PAGE_DOWNLOAD_CSV_BUTTON_XPATH).click()
        time.sleep(2)
        return self.get_csv_context()

    def click_on_pin_row(self):
        self.find_by_xpath(OrderVelocityLimitsConstants.PIN_ROW_XPATH).click()

    def click_on_new(self):
        self.find_by_xpath(OrderVelocityLimitsConstants.NEW_BUTTON_XPATH).click()

    def click_on_user_icon(self):
        self.find_by_xpath(OrderVelocityLimitsConstants.USER_ICON_AT_RIGHT_CORNER).click()

    def click_on_logout(self):
        self.find_by_xpath(OrderVelocityLimitsConstants.LOGOUT_BUTTON_XPATH).click()

    def set_name(self, value):
        self.set_text_by_xpath(OrderVelocityLimitsConstants.MAIN_PAGE_NAME_FILTER_XPATH, value)

    def set_client(self, value):
        self.set_text_by_xpath(OrderVelocityLimitsConstants.MAIN_PAGE_CLIENT_FILTER_XPATH, value)

    def set_side(self, value):
        self.set_text_by_xpath(OrderVelocityLimitsConstants.MAIN_PAGE_SIDE_FILTER_XPATH, value)

    def set_instr_symbol(self, value):
        self.set_text_by_xpath(OrderVelocityLimitsConstants.MAIN_PAGE_INSTR_SYMBOL_FILTER_XPATH, value)

    def set_listing(self, value):
        self.set_text_by_xpath(OrderVelocityLimitsConstants.MAIN_PAGE_LISTING_FILTER_XPATH, value)

    def set_moving_time_window(self, value):
        self.set_text_by_xpath(OrderVelocityLimitsConstants.MAIN_PAGE_MOVING_TIME_WINDOW_FILTER_XPATH, value)

    def set_max_quantity(self, value):
        self.set_text_by_xpath(OrderVelocityLimitsConstants.MAIN_PAGE_MAX_QUANTITY_FILTER_XPATH, value)

    def get_name(self):
        return self.find_by_xpath(OrderVelocityLimitsConstants.MAIN_PAGE_NAME_XPATH).text

    def get_client(self):
        return self.find_by_xpath(OrderVelocityLimitsConstants.MAIN_PAGE_CLIENT_XPATH).text

    def get_side(self):
        return self.find_by_xpath(OrderVelocityLimitsConstants.MAIN_PAGE_SIDE_XPATH).text

    def get_instr_symbol(self):
        return self.find_by_xpath(OrderVelocityLimitsConstants.MAIN_PAGE_INSTR_SYMBOL_XPATH).text

    def get_listing(self):
        return self.find_by_xpath(OrderVelocityLimitsConstants.MAIN_PAGE_LISTING_XPATH).text

    def get_moving_time_window(self):
        return self.find_by_xpath(OrderVelocityLimitsConstants.MAIN_PAGE_MOVING_TIME_WINDOW_XPATH).text

    def get_max_quantity(self):
        return self.find_by_xpath(OrderVelocityLimitsConstants.MAIN_PAGE_MAX_QUANTITY_XPATH).text

    def is_searched_entity_found_by_name(self, value):
        return self.is_element_present(OrderVelocityLimitsConstants.SEARCHED_VALUE_XPATH.format(value))
