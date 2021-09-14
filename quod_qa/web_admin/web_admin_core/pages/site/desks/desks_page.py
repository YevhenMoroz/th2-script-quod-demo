import time

from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.site.desks.desks_constants import DesksConstants
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class DesksPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_more_actions(self):
        self.find_by_xpath(DesksConstants.MORE_ACTIONS_XPATH).click()

    def click_on_cancel(self):
        self.find_by_xpath(DesksConstants.CANCEL_BUTTON_XPATH).click()

    def click_on_ok_xpath(self):
        self.find_by_xpath(DesksConstants.OK_BUTTON_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(DesksConstants.EDIT_AT_MORE_ACTIONS_XPATH).click()

    def click_on_clone(self):
        self.find_by_xpath(DesksConstants.CLONE_AT_MORE_ACTIONS_XPATH).click()

    def click_on_delete(self):
        self.find_by_xpath(DesksConstants.DELETE_AT_MORE_ACTIONS_XPATH).click()
        time.sleep(2)
        self.find_by_xpath(DesksConstants.OK_BUTTON_XPATH).click()

    def click_on_new(self):
        self.find_by_xpath(DesksConstants.NEW_BUTTON_XPATH).click()


    def set_name_filter(self , value):
        self.set_text_by_xpath(DesksConstants.NAME_FILTER_AT_MAIN_PAGE_XPATH, value)

    def set_mode_filter(self, value):
        self.set_text_by_xpath(DesksConstants.MODE_FILTER_AT_MAIN_PAGE_XPATH, value)

    def set_location_filter(self, value):
        self.set_text_by_xpath(DesksConstants.LOCATION_FILTER_AT_MAIN_PAGE_XPATH, value)

















