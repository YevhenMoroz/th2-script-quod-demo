import time

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.site.desks.desks_constants import DesksConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


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

    def click_on_disable_enable_button(self):
        self.find_by_xpath(DesksConstants.ENABLE_DISABLE_BUTTON_XPATH).click()
        time.sleep(1)
        self.click_on_ok_xpath()

    def set_name_filter(self, value):
        self.set_text_by_xpath(DesksConstants.NAME_FILTER_AT_MAIN_PAGE_XPATH, value)

    def set_mode_filter(self, value):
        self.set_text_by_xpath(DesksConstants.MODE_FILTER_AT_MAIN_PAGE_XPATH, value)

    def set_location_filter(self, value):
        self.set_text_by_xpath(DesksConstants.LOCATION_FILTER_AT_MAIN_PAGE_XPATH, value)

    def is_desk_enable_disable(self):
        return self.is_toggle_button_enabled(DesksConstants.ENABLE_DISABLE_BUTTON_XPATH)

    def is_searched_desk_found(self, value):
        return self.is_element_present(DesksConstants.DISPLAYED_DESK_XPATH.format(value))

    def get_list_of_all_locations(self):
        return self.get_all_items_from_table_column(DesksConstants.LOCATIONS_COLUMN_XPATH)

    def get_list_of_all_desks_name(self):
        return self.get_all_items_from_table_column(DesksConstants.DESKS_NAME_COLUMN_XPATH)

    def get_ctm_bic(self):
        return self.find_by_xpath(DesksConstants.CTM_BIC_AT_MAIN_PAGE).text
