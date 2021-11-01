import time

from selenium.webdriver.common.keys import Keys

from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.site.desks.desks_constants import DesksConstants
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class DesksAssignmentsSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_location_at_description_tab(self, value):
        self.set_combobox_value(DesksConstants.LOCATION_AT_ASSIGNMENTS_TAB_XPATH, value)

    def get_location_at_description_tab(self):
        return self.get_text_by_xpath(DesksConstants.LOCATION_AT_ASSIGNMENTS_TAB_XPATH)

    def click_on_location(self, location_name):
        self.find_by_xpath(DesksConstants.ASSIGNMENTS_TAB_LOCATION_LINK_XPATH.format(location_name)).click()

    def click_on_user(self, user_name):
        self.find_by_xpath(DesksConstants.ASSIGNMENTS_TAB_USER_LINK_XPATH.format(user_name)).click()
        time.sleep(2)
        self.find_by_xpath(DesksConstants.OK_BUTTON_XPATH).click()

    def is_user_link_exist(self, user_link):
        return user_link == self.find_by_xpath(DesksConstants.ASSIGNMENTS_TAB_USER_LINK_XPATH.format(user_link)).text

    def clear_location_field(self):
        self.find_by_xpath(DesksConstants.LOCATION_AT_ASSIGNMENTS_TAB_XPATH).send_keys(Keys.CONTROL + 'a', Keys.DELETE)
