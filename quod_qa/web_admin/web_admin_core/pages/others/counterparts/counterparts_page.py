import time

from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.others.counterparts.counterparts_constants import CounterpartsConstants
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class CounterpartsPage(CommonPage):
    """
    Class was created for interactions with Counterparts page components
    """

    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_others(self):
        self.find_by_xpath(CounterpartsConstants.OTHERS_PAGE_XPATH).click()

    def click_on_counterparts(self):
        self.find_by_xpath(CounterpartsConstants.COUNTERPARTS_PAGE_TITLE_XPATH).click()

    def click_on_more_actions(self):
        self.find_by_xpath(CounterpartsConstants.MORE_ACTIONS_XPATH).click()

    def click_on_cancel(self):
        self.find_by_xpath(CounterpartsConstants.CANCEL_BUTTON_XPATH).click()

    def click_on_ok_xpath(self):
        self.find_by_xpath(CounterpartsConstants.OK_BUTTON_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(CounterpartsConstants.EDIT_AT_MORE_ACTIONS_XPATH).click()

    def click_on_clone(self):
        self.find_by_xpath(CounterpartsConstants.CLONE_AT_MORE_ACTIONS_XPATH).click()

    def click_on_delete(self):
        self.find_by_xpath(CounterpartsConstants.DELETE_AT_MORE_ACTIONS_XPATH).click()
        time.sleep(2)
        self.find_by_xpath(CounterpartsConstants.OK_BUTTON_XPATH).click()

    def click_on_new(self):
        self.find_by_xpath(CounterpartsConstants.NEW_BUTTON_XPATH).click()

    def click_on_refresh_page(self):
        self.find_by_xpath(CounterpartsConstants.REFRESH_BUTTON_XPATH).click()

    def set_name_filter_value(self, name):
        self.set_text_by_xpath(CounterpartsConstants.NAME_FILTER_XPATH, name)

    def get_name_value(self):
        return self.find_by_xpath(CounterpartsConstants.NAME_VALUE_XPATH).text

    def check_that_name_value_row_is_not_exist(self):
        """
        The method will return the name of the exception that was thrown because the row with the value is empty
        """
        try:
            self.get_name_value()
        except Exception as e:
            actual_exception = type(e).__name__
            return str(actual_exception)
