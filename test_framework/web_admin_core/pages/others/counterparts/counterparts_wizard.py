import time

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.others.counterparts.counterparts_constants import CounterpartsConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class CounterpartsWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_name_value_at_values_tab(self, new_name):
        self.set_text_by_xpath(CounterpartsConstants.NAME_AT_VALUES_TAB_XPATH, new_name)

    def get_name_at_values_tab(self):
        return self.get_text_by_xpath(CounterpartsConstants.NAME_AT_VALUES_TAB_XPATH)

    def click_on_plus_sub_counterparts(self):
        self.find_by_xpath(CounterpartsConstants.PLUS_AT_SUB_COUNTERPARTS_TAB_XPATH).click()

    def click_on_plus_party_roles(self):
        self.find_by_xpath(CounterpartsConstants.PLUS_BUTTON_AT_PARTY_ROLES_TAB_XPATH).click()

    def click_on_pdf_button(self):
        self.find_by_xpath(CounterpartsConstants.DOWNLOAD_PDF_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(CounterpartsConstants.DOWNLOAD_PDF_IN_EDIT_WIZARD_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_on_check_mark(self):
        self.find_by_xpath(CounterpartsConstants.CHECK_MARK_XPATH).click()

    def click_on_close_changes(self):
        self.find_by_xpath(CounterpartsConstants.CLOSE_CHANGES_AT_COUNTERPARTS_TABS_XPATH).click()

    def click_on_close(self):
        self.find_by_xpath(CounterpartsConstants.CLOSE_COUNTERPARTS_WIZARD_XPATH).click()

    def click_on_edit_at_sub_counterparts_tab(self):
        self.find_by_xpath(CounterpartsConstants.EDIT_AT_SUB_COUNTERPARTS_TAB_XPATH).click()

    def click_on_edit_at_party_roles_tab(self):
        self.find_by_xpath(CounterpartsConstants.EDIT_AT_PARTY_ROLES_TAB_XPATH).click()

    def click_on_delete_at_sub_counterparts_tab(self):
        self.find_by_xpath(CounterpartsConstants.DELETE_AT_COUNTERPARTS_TABS_XPATH).click()

    def click_on_delete_at_party_roles_tab(self):
        self.find_by_xpath(CounterpartsConstants.DELETE_AT_PARTY_ROLES_TABS_XPATH).click()

    def click_on_clear_changes(self):
        self.find_by_xpath(CounterpartsConstants.CLEAR_CHANGES_XPATH).click()

    def click_on_revert_changes(self):
        self.find_by_xpath(CounterpartsConstants.REVERT_CHANGES_AT_COUNTERPARTS_TAB_XPATH).click()

    def click_on_save_changes(self):
        self.find_by_xpath(CounterpartsConstants.SAVE_CHANGES_XPATH).click()

    def is_warning_message_displayed(self):
        return self.is_element_present(CounterpartsConstants.FOOTER_WARNING_XPATH)
