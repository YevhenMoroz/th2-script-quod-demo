import time

from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.site.zones.zones_constants import ZonesConstants

from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class ZonesPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_more_actions(self):
        self.find_by_xpath(ZonesConstants.MORE_ACTIONS_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(ZonesConstants.EDIT_XPATH).click()

    def click_on_clone(self):
        self.find_by_xpath(ZonesConstants.CLONE_XPATH).click()

    def click_on_delete(self, confirmation):
        self.find_by_xpath(ZonesConstants.DELETE_XPATH).click()
        if confirmation:
            time.sleep(2)
            self.find_by_xpath(ZonesConstants.OK_BUTTON_XPATH).click()
        else:
            self.find_by_xpath(ZonesConstants.CANCEL_BUTTON_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(ZonesConstants.DOWNLOAD_PDF_BUTTON_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_on_pin_row(self):
        self.find_by_xpath(ZonesConstants.PIN_ROW_XPATH).click()

    def click_on_new(self):
        self.find_by_xpath(ZonesConstants.NEW_BUTTON_XPATH).click()

    def click_on_user_icon(self):
        self.find_by_xpath(ZonesConstants.USER_ICON_AT_RIGHT_CORNER).click()

    def click_on_logout(self):
        self.find_by_xpath(ZonesConstants.LOGOUT_BUTTON_XPATH).click()

    def set_name(self, value):
        self.set_text_by_xpath(ZonesConstants.MAIN_PAGE_NAME_FILTER_XPATH, value)

    def set_institution(self, value):
        self.set_text_by_xpath(ZonesConstants.MAIN_PAGE_INSTITUTION_FILTER_XPATH, value)

    def set_enabled(self, value):
        self.select_value_from_dropdown_list(ZonesConstants.MAIN_PAGE_ENABLED_FILTER_XPATH, value)
