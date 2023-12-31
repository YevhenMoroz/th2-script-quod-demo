import time

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.middle_office.settlement_models.constants import \
    SettlementModelsConstants

from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class SettlementModelsPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_more_actions(self):
        self.find_by_xpath(SettlementModelsConstants.MORE_ACTIONS_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(SettlementModelsConstants.EDIT_XPATH).click()

    def click_on_clone(self):
        self.find_by_xpath(SettlementModelsConstants.CLONE_XPATH).click()

    def click_on_delete(self, confirmation):
        self.find_by_xpath(SettlementModelsConstants.DELETE_XPATH).click()
        if confirmation:
            time.sleep(2)
            self.find_by_xpath(SettlementModelsConstants.OK_BUTTON_XPATH).click()
        else:
            self.find_by_xpath(SettlementModelsConstants.CANCEL_BUTTON_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(SettlementModelsConstants.DOWNLOAD_PDF_BUTTON_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_on_pin_row(self):
        self.find_by_xpath(SettlementModelsConstants.PIN_ROW_XPATH).click()

    def click_on_new(self):
        self.find_by_xpath(SettlementModelsConstants.NEW_BUTTON_XPATH).click()

    def click_on_user_icon(self):
        self.find_by_xpath(SettlementModelsConstants.USER_ICON_AT_RIGHT_CORNER).click()

    def click_on_logout(self):
        self.find_by_xpath(SettlementModelsConstants.LOGOUT_BUTTON_XPATH).click()

    def set_description(self, value):
        self.set_text_by_xpath(SettlementModelsConstants.MAIN_PAGE_DESCRIPTION_FILTER_XPATH, value)

    def set_name(self, value):
        self.set_text_by_xpath(SettlementModelsConstants.MAIN_PAGE_NAME_FILTER_XPATH, value)

    def set_country_code(self, value):
        self.set_text_by_xpath(SettlementModelsConstants.MAIN_PAGE_COUNTRY_CODE_FILTER_XPATH, value)

    def set_instr_type(self, value):
        self.set_text_by_xpath(SettlementModelsConstants.MAIN_PAGE_INSTR_TYPE_FILTER_XPATH, value)

    def set_settl_location_bic(self, value):
        self.set_text_by_xpath(SettlementModelsConstants.MAIN_PAGE_SETTL_LOCATION_BIC_FILTER_XPATH, value)

    def get_description(self):
        return self.find_by_xpath(SettlementModelsConstants.MAIN_PAGE_DESCRIPTION_XPATH).text

    def get_name(self):
        return self.find_by_xpath(SettlementModelsConstants.MAIN_PAGE_NAME_XPATH).text

    def get_country_code(self):
        return self.find_by_xpath(SettlementModelsConstants.MAIN_PAGE_COUNTRY_CODE_XPATH).text

    def get_instr_type(self):
        return self.find_by_xpath(SettlementModelsConstants.MAIN_PAGE_INSTR_TYPE_XPATH).text

    def get_settl_location_bic(self):
        return self.find_by_xpath(SettlementModelsConstants.MAIN_PAGE_SETTL_LOCATION_BIC_XPATH).text

    def is_searched_entity_found(self, value):
        return self.is_element_present(SettlementModelsConstants.DISPLAYED_ENTITY_XPATH.format(value))