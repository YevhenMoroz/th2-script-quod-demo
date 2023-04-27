import time

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.positions.wash_book_rules.wash_book_rules_constants import \
    WashBookRulesConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class WashBookRulesPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_more_actions(self):
        self.find_by_xpath(WashBookRulesConstants.MORE_ACTIONS_BUTTON_XPATH).click()

    def click_on_edit_at_more_actions(self):
        self.find_by_xpath(WashBookRulesConstants.EDIT_AT_MORE_ACTIONS_XPATH).click()

    def click_on_clone_at_more_actions(self):
        self.find_by_xpath(WashBookRulesConstants.CLONE_AT_MORE_ACTIONS_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(WashBookRulesConstants.DOWNLOAD_PDF_AT_MORE_ACTIONS_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_on_pin_row_at_more_actions(self):
        self.find_by_xpath(WashBookRulesConstants.PIN_TO_ROW_AT_MORE_ACTIONS_XPATH).click()

    def click_on_delete_and_confirmation(self, confirmation):
        self.find_by_xpath(WashBookRulesConstants.DELETE_AT_MORE_ACTIONS_XPATH).click()
        if confirmation:
            time.sleep(2)
            self.find_by_xpath(WashBookRulesConstants.OK_BUTTON_XPATH).click()
        else:
            self.find_by_xpath(WashBookRulesConstants.CANCEL_BUTTON_XPATH).click()

    def click_on_ok_button(self):
        self.find_by_xpath(WashBookRulesConstants.OK_BUTTON_XPATH).click()

    def click_on_no_button(self):
        self.find_by_xpath(WashBookRulesConstants.NO_BUTTON_XPATH).click()

    def click_on_cancel_button(self):
        self.find_by_xpath(WashBookRulesConstants.CANCEL_BUTTON_XPATH).click()

    def click_on_download_csv_button(self):
        self.find_by_xpath(WashBookRulesConstants.DOWNLOAD_CSV_BUTTON_XPATH).click()

    def click_on_refresh_button(self):
        self.find_by_xpath(WashBookRulesConstants.REFRESH_PAGE_BUTTON_XPATH).click()

    def click_on_new_button(self):
        self.find_by_xpath(WashBookRulesConstants.NEW_BUTTON_XPATH).click()

    # --setters--
    def set_name_at_filter(self, value):
        self.set_text_by_xpath(WashBookRulesConstants.MAIN_PAGE_NAME_FILTER_XPATH, value)

    def set_client_at_filter(self, value):
        self.set_text_by_xpath(WashBookRulesConstants.MAIN_PAGE_CLIENT_FILTER_XPATH, value)

    def set_instr_type_at_filter(self, value):
        self.set_text_by_xpath(WashBookRulesConstants.MAIN_PAGE_INSTR_TYPE_FILTER_XPATH, value)

    def set_execution_policy_at_filter(self, value):
        self.set_text_by_xpath(WashBookRulesConstants.MAIN_PAGE_EXECUTION_POLICY_FILTER_XPATH, value)

    def set_wash_book_account_at_filter(self, value):
        self.set_text_by_xpath(WashBookRulesConstants.MAIN_PAGE_WASH_BOOK_ACCOUNT_FILTER_XPATH, value)

    def set_user_at_filter(self, value):
        self.set_text_by_xpath(WashBookRulesConstants.MAIN_PAGE_USER_FILTER_XPATH, value)

    def set_desk_at_filter(self, value):
        self.set_text_by_xpath(WashBookRulesConstants.MAIN_PAGE_DESK_FILTER_XPATH, value)

    # --getters--
    def get_name(self):
        return self.find_by_xpath(WashBookRulesConstants.MAIN_PAGE_NAME_XPATH).text

    def get_client(self):
        return self.find_by_xpath(WashBookRulesConstants.MAIN_PAGE_CLIENT_XPATH).text

    def get_instr_type(self):
        return self.find_by_xpath(WashBookRulesConstants.MAIN_PAGE_INSTR_TYPE_XPATH).text

    def get_execution_policy(self):
        return self.find_by_xpath(WashBookRulesConstants.MAIN_PAGE_EXECUTION_POLICY_XPATH).text

    def get_wash_book_account(self):
        return self.find_by_xpath(WashBookRulesConstants.MAIN_PAGE_WASH_BOOK_ACCOUNT_XPATH).text

    def get_user(self):
        return self.find_by_xpath(WashBookRulesConstants.MAIN_PAGE_USER_XPATH).text

    def get_desk(self):
        return self.find_by_xpath(WashBookRulesConstants.MAIN_PAGE_DESK_XPATH).text

    def is_searched_entity_found(self, value):
        return self.is_element_present(WashBookRulesConstants.SEARCHED_ENTITY_XPATH.format(value))

    def get_page_icon_attributes(self):
        page_icon = self.find_elements_by_xpath(WashBookRulesConstants.PAGE_ICON)
        return [_.get_attribute('d') for _ in page_icon]
