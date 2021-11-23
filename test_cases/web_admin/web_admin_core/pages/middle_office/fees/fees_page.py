import time

from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.pages.middle_office.fees.fees_constants import FeesConstants

from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class FeesPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_more_actions(self):
        self.find_by_xpath(FeesConstants.MORE_ACTIONS_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(FeesConstants.EDIT_XPATH).click()

    def click_on_clone(self):
        self.find_by_xpath(FeesConstants.CLONE_XPATH).click()

    def click_on_delete(self, confirmation):
        self.find_by_xpath(FeesConstants.DELETE_XPATH).click()
        if confirmation:
            time.sleep(2)
            self.find_by_xpath(FeesConstants.OK_BUTTON_XPATH).click()
        else:
            self.find_by_xpath(FeesConstants.CANCEL_BUTTON_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(FeesConstants.DOWNLOAD_PDF_BUTTON_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_on_pin_row(self):
        self.find_by_xpath(FeesConstants.PIN_ROW_XPATH).click()

    def click_on_new(self):
        self.find_by_xpath(FeesConstants.NEW_BUTTON_XPATH).click()

    def click_on_user_icon(self):
        self.find_by_xpath(FeesConstants.USER_ICON_AT_RIGHT_CORNER).click()

    def click_on_logout(self):
        self.find_by_xpath(FeesConstants.LOGOUT_BUTTON_XPATH).click()

    def set_description(self, value):
        self.set_text_by_xpath(FeesConstants.MAIN_PAGE_DESCRIPTION_FILTER_XPATH, value)

    def set_misc_fee_type(self, value):
        self.set_text_by_xpath(FeesConstants.MAIN_PAGE_MISC_FEE_TYPE_FILTER_XPATH, value)

    def set_charge_type(self, value):
        self.set_text_by_xpath(FeesConstants.MAIN_PAGE_CHANGE_TYPE_FILTER_XPATH, value)

    def set_exec_scope(self, value):
        self.set_text_by_xpath(FeesConstants.MAIN_PAGE_EXEC_COMMISSION_PROFILE_FILTER_XPATH, value)
