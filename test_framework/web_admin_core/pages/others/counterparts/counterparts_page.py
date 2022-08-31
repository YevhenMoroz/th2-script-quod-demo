import time

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.others.counterparts.counterparts_constants import CounterpartsConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


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

    def click_on_delete_and_confirmation(self, confirmation):
        self.find_by_xpath(CounterpartsConstants.DELETE_AT_MORE_ACTIONS_XPATH).click()
        if confirmation:
            time.sleep(2)
            self.find_by_xpath(CounterpartsConstants.OK_BUTTON_XPATH).click()
        else:
            self.find_by_xpath(CounterpartsConstants.CANCEL_BUTTON_XPATH).click()

    def click_on_new(self):
        self.find_by_xpath(CounterpartsConstants.NEW_BUTTON_XPATH).click()

    def click_on_refresh_page(self):
        self.find_by_xpath(CounterpartsConstants.REFRESH_BUTTON_XPATH).click()

    def set_name_filter_value(self, name):
        self.set_text_by_xpath(CounterpartsConstants.NAME_FILTER_XPATH, name)

    def get_name_value(self):
        return self.find_by_xpath(CounterpartsConstants.NAME_VALUE_XPATH).text

    def is_counterpart_present_by_name(self, value):
        return self.is_element_present(CounterpartsConstants.COUNTERPARTS_NAME_AT_MAIN_PAGE_XPATH.format(value))

    def click_download_pdf_at_more_actions_and_check_pdf(self, value):
        self.clear_download_directory()
        self.click_on_more_actions()
        time.sleep(1)
        self.find_by_xpath(CounterpartsConstants.DOWNLOAD_PDF_AT_MORE_ACTIONS_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)
