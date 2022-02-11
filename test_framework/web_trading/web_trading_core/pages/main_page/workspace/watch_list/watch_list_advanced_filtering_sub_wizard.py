import time

from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_framework.web_trading.web_trading_core.pages.main_page.workspace.watch_list.watch_list_constants import \
    WatchListConstants


class WatchListAdvancedFilteringSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    # TODO: implement methods, if something changed in FE part, please take a look


    def click_on_and_group_button(self):
        self.find_by_xpath(WatchListConstants.AND_GROUP_BUTTON_XPATH).click()

    def click_on_or_group_button(self):
        self.find_by_xpath(WatchListConstants.OR_GROUP_BUTTON_XPATH).click()

    def click_on_clear_filter_button(self):
        self.find_by_xpath(WatchListConstants.CLEAR_FILTER_BUTTON_XPATH).click()

    def click_on_cancel_button(self):
        self.find_by_xpath(WatchListConstants.CANCEL_BUTTON_XPATH).click()

    def click_on_apply_button(self):
        self.find_by_xpath(WatchListConstants.APPLY_BUTTON_XPATH).click()

    def select_column(self, value):
        self.find_by_xpath(WatchListConstants.SELECT_COLUMN_FIELD_XPATH).click()
        time.sleep(2)
        self.select_value_from_dropdown_list(WatchListConstants.SELECT_COLUMN_LIST_XPATH.format(value))

    def select_filter(self, value):
        self.find_by_xpath(WatchListConstants.SELECT_FILTER_FIELD_XPATH).click()
        time.sleep(2)
        self.select_value_from_dropdown_list(WatchListConstants.SELECT_FILTER_LIST_XPATH.format(value))

    def set_value(self, value):
        self.set_text_by_xpath(WatchListConstants.VALUE_FIELD_XPATH, value)

    def click_on_checkmark_button(self):
        self.find_by_xpath(WatchListConstants.CHECK_AF_BUTTON_XPATH).click()

    def click_on_close_button(self):
        self.find_by_xpath(WatchListConstants.CLOSE_AF_BUTTON_XPATH).click()

    def click_on_condition_button(self):
        self.find_by_xpath(WatchListConstants.CONDITION_BUTTON_XPATH).click()



