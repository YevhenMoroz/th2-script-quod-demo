import time

from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.pages.risk_limits.order_velocity_limit.order_velocity_limit_constants import \
    OrderVelocityLimitConstants
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class OrderVelocityLimitPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_more_actions(self):
        self.find_by_xpath(OrderVelocityLimitConstants.MORE_ACTIONS_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(OrderVelocityLimitConstants.EDIT_XPATH).click()

    def click_on_clone(self):
        self.find_by_xpath(OrderVelocityLimitConstants.CLONE_XPATH).click()

    def click_on_delete(self, confirmation):
        self.find_by_xpath(OrderVelocityLimitConstants.DELETE_XPATH).click()
        if confirmation:
            time.sleep(2)
            self.find_by_xpath(OrderVelocityLimitConstants.OK_BUTTON_XPATH).click()
        else:
            self.find_by_xpath(OrderVelocityLimitConstants.CANCEL_BUTTON_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(OrderVelocityLimitConstants.DOWNLOAD_PDF_BUTTON_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_download_csv_entity_button_and_check_csv(self):
        self.clear_download_directory()
        self.find_by_xpath(OrderVelocityLimitConstants.MAIN_PAGE_DOWNLOAD_CSV_BUTTON_XPATH).click()
        time.sleep(2)
        return self.get_csv_context()

    def click_on_pin_row(self):
        self.find_by_xpath(OrderVelocityLimitConstants.PIN_ROW_XPATH).click()

    def click_on_new(self):
        self.find_by_xpath(OrderVelocityLimitConstants.NEW_BUTTON_XPATH).click()

    def click_on_user_icon(self):
        self.find_by_xpath(OrderVelocityLimitConstants.USER_ICON_AT_RIGHT_CORNER).click()

    def click_on_logout(self):
        self.find_by_xpath(OrderVelocityLimitConstants.LOGOUT_BUTTON_XPATH).click()

    def set_name(self, value):
        self.set_text_by_xpath(OrderVelocityLimitConstants.MAIN_PAGE_NAME_FILTER_XPATH, value)

    def set_client(self, value):
        self.set_text_by_xpath(OrderVelocityLimitConstants.MAIN_PAGE_CLIENT_FILTER_XPATH, value)

    def set_side(self, value):
        self.set_text_by_xpath(OrderVelocityLimitConstants.MAIN_PAGE_SIDE_FILTER_XPATH, value)

    def set_instr_symbol(self, value):
        self.set_text_by_xpath(OrderVelocityLimitConstants.MAIN_PAGE_INSTR_SYMBOL_FILTER_XPATH, value)

    def set_listing(self, value):
        self.set_text_by_xpath(OrderVelocityLimitConstants.MAIN_PAGE_LISTING_FILTER_XPATH, value)

    def set_moving_time_window(self, value):
        self.set_text_by_xpath(OrderVelocityLimitConstants.MAIN_PAGE_MOVING_TIME_WINDOW_FILTER_XPATH, value)

    def set_max_quantity(self, value):
        self.set_text_by_xpath(OrderVelocityLimitConstants.MAIN_PAGE_MAX_QUANTITY_FILTER_XPATH, value)

    def get_name(self):
        return self.find_by_xpath(OrderVelocityLimitConstants.MAIN_PAGE_NAME_XPATH).text

    def get_client(self):
        return self.find_by_xpath(OrderVelocityLimitConstants.MAIN_PAGE_CLIENT_XPATH).text

    def get_side(self):
        return self.find_by_xpath(OrderVelocityLimitConstants.MAIN_PAGE_SIDE_XPATH).text

    def get_instr_symbol(self):
        return self.find_by_xpath(OrderVelocityLimitConstants.MAIN_PAGE_INSTR_SYMBOL_XPATH).text

    def get_listing(self):
        return self.find_by_xpath(OrderVelocityLimitConstants.MAIN_PAGE_LISTING_XPATH).text

    def get_moving_time_window(self):
        return self.find_by_xpath(OrderVelocityLimitConstants.MAIN_PAGE_MOVING_TIME_WINDOW_XPATH).text

    def get_max_quantity(self):
        return self.find_by_xpath(OrderVelocityLimitConstants.MAIN_PAGE_MAX_QUANTITY_XPATH).text
