import time

from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.pages.site.institution.institutions_constants import InstitutionsConstants
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class InstitutionsPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_more_actions(self):
        self.find_by_xpath(InstitutionsConstants.MORE_ACTIONS_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(InstitutionsConstants.EDIT_XPATH).click()

    def click_on_clone(self):
        self.find_by_xpath(InstitutionsConstants.CLONE_XPATH).click()

    def click_on_delete(self, confirmation):
        self.find_by_xpath(InstitutionsConstants.DELETE_XPATH).click()
        if confirmation:
            time.sleep(2)
            self.find_by_xpath(InstitutionsConstants.OK_BUTTON_XPATH).click()
        else:
            self.find_by_xpath(InstitutionsConstants.CANCEL_BUTTON_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(InstitutionsConstants.DOWNLOAD_PDF_BUTTON_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_on_pin_row(self):
        self.find_by_xpath(InstitutionsConstants.PIN_ROW_XPATH).click()

    def click_on_new(self):
        self.find_by_xpath(InstitutionsConstants.NEW_BUTTON_XPATH).click()

    def click_on_user_icon(self):
        self.find_by_xpath(InstitutionsConstants.USER_ICON_AT_RIGHT_CORNER).click()

    def click_on_logout(self):
        self.find_by_xpath(InstitutionsConstants.LOGOUT_BUTTON_XPATH).click()

    def click_on_enable_disable_button(self):
        return self.find_by_xpath(InstitutionsConstants.ENABLE_DISABLE_TOGGLE_BUTTON_XPATH).click()

    def set_institution_name(self, value):
        self.set_text_by_xpath(InstitutionsConstants.MAIN_PAGE_INSTITUTION_NAME_FILTER_XPATH, value)

    def get_institution_name(self):
        return self.find_by_xpath(InstitutionsConstants.MAIN_PAGE_INSTITUTION_NAME_XPATH).text

    def set_lei(self, value):
        self.set_text_by_xpath(InstitutionsConstants.MAIN_PAGE_LEI_FILTER_XPATH, value)

    def get_lei(self):
        return self.find_by_xpath(InstitutionsConstants.MAIN_PAGE_LEI_XPATH).text

    def set_ctm_bic(self, value):
        self.set_text_by_xpath(InstitutionsConstants.MAIN_PAGE_CTM_BIC_FILTER_XPATH, value)

    def get_ctm_bic(self):
        return self.find_by_xpath(InstitutionsConstants.MAIN_PAGE_CTM_BIC_XPATH).text

    def set_counterpart(self, value):
        self.set_text_by_xpath(InstitutionsConstants.MAIN_PAGE_COUNTERPART_FILTER_XPATH, value)

    def get_counterpart(self):
        return self.find_by_xpath(InstitutionsConstants.MAIN_PAGE_COUNTERPART_XPATH).text

    def set_enabled(self, value):
        self.select_value_from_dropdown_list(InstitutionsConstants.MAIN_PAGE_ENABLED_FILTER_XPATH, value)

    def is_enable_disable_toggle_enabled(self):
        return self.find_by_xpath(InstitutionsConstants.ENABLE_DISABLE_TOGGLE_INPUT_XPATH).is_enabled()
