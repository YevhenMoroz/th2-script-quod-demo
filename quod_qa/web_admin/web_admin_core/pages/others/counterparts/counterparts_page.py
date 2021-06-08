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
        self.find_by_xpath(CounterpartsConstants.OTHERS_PAGE).click()

    def click_on_counterparts(self):
        self.find_by_xpath(CounterpartsConstants.COUNTERPARTS_PAGE_TITLE_XPATH).click()

    def click_on_more_actions(self):
        self.find_by_xpath(CounterpartsConstants.MORE_ACTIONS).click()

    def click_on_edit(self):
        self.find_by_xpath(CounterpartsConstants.EDIT_AT_MORE_ACTIONS).click()

    def click_on_clone(self):
        self.find_by_xpath(CounterpartsConstants.CLONE_AT_MORE_ACTIONS).click()

    def click_on_delete(self):
        self.find_by_xpath(CounterpartsConstants.DELETE_AT_MORE_ACTIONS).click()

    def click_on_new(self):
        self.find_by_xpath(CounterpartsConstants.NEW_BUTTON).click()

    def click_on_refresh_page(self):
        self.find_by_xpath(CounterpartsConstants.REFRESH_BUTTON).click()

    def set_name_filter_value(self, name):
        self.set_text_by_xpath(CounterpartsConstants.NAME_FILTER_XPATH, name)

    def get_name_value(self):
        return self.find_by_xpath(CounterpartsConstants.NAME_VALUE).text
