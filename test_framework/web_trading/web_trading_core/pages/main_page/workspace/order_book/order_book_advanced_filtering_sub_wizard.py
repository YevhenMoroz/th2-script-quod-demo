import time

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_framework.web_trading.web_trading_core.pages.main_page.workspace.order_book.order_book_constants import \
    OrderBookConstants


class OrderBookAdvancedFilteringSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    # TODO: implement methods, if something changed in FE part, please take a look


    def click_on_and_group_button(self):
        self.find_by_xpath(OrderBookConstants.AND_GROUP_BUTTON_XPATH).click()

    def click_on_or_group_button(self):
        self.find_by_xpath(OrderBookConstants.OR_GROUP_BUTTON_XPATH).click()

    def click_on_clear_filter_button(self):
        self.find_by_xpath(OrderBookConstants.CLEAR_FILTER_BUTTON_XPATH).click()

    def click_on_cancel_button(self):
        self.find_by_xpath(OrderBookConstants.CANCEL_BUTTON_XPATH).click()

    def click_on_apply_button(self):
        self.find_by_xpath(OrderBookConstants.APPLY_BUTTON_XPATH).click()

    def select_column(self, value):
        self.find_by_xpath(OrderBookConstants.SELECT_COLUMN_FIELD_XPATH).click()
        time.sleep(2)
        self.select_value_from_dropdown_list(OrderBookConstants.SELECT_COLUMN_LIST_XPATH.format(value))

    def select_filter(self, value):
        self.find_by_xpath(OrderBookConstants.SELECT_FILTER_FIELD_XPATH).click()
        time.sleep(2)
        self.select_value_from_dropdown_list(OrderBookConstants.SELECT_FILTER_LIST_XPATH.format(value))

    def set_value(self, value):
        self.set_text_by_xpath(OrderBookConstants.VALUE_FIELD_XPATH, value)

    def click_on_checkmark_button(self):
        self.find_by_xpath(OrderBookConstants.CHECK_AF_BUTTON_XPATH).click()

    def click_on_close_button(self):
        self.find_by_xpath(OrderBookConstants.CLOSE_AF_BUTTON_XPATH).click()

    def click_on_condition_button(self):
        self.find_by_xpath(OrderBookConstants.CONDITION_BUTTON_XPATH).click()



