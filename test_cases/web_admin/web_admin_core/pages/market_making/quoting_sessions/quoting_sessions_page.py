import time

from test_cases.web_admin.web_admin_core.pages.common_page import CommonPage
from test_cases.web_admin.web_admin_core.pages.market_making.quoting_sessions.quoting_sessions_constants import \
    QuotingSessionsConstants
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class QuotingSessionsPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_name_filter(self, value):
        self.set_text_by_xpath(QuotingSessionsConstants.MAIN_PAGE_NAME_FILTER_XPATH, value)

    def set_concurrently_active_quotes(self, value):
        self.set_text_by_xpath(QuotingSessionsConstants.MAIN_PAGE_CONCURRENTLY_ACTIVE_QUOTES_FILTER_XPATH, value)

    def set_quote_update_interval(self, value):
        self.set_text_by_xpath(QuotingSessionsConstants.MAIN_PAGE_QUOTE_UPDATE_INTERVAL_FILTER_XPATH, value)

    def set_published_quote_id_format(self, value):
        self.set_text_by_xpath(QuotingSessionsConstants.MAIN_PAGE_PUBLISHED_QUOTE_ID_FORMAT_FILTER_XPATH, value)

    def click_on_more_actions(self):
        self.find_by_xpath(QuotingSessionsConstants.MORE_ACTIONS_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(QuotingSessionsConstants.EDIT_XPATH).click()

    def click_on_clone(self):
        self.find_by_xpath(QuotingSessionsConstants.CLONE_XPATH).click()

    def click_on_delete(self, confirmation):
        self.find_by_xpath(QuotingSessionsConstants.DELETE_XPATH).click()
        if confirmation:
            time.sleep(2)
            self.find_by_xpath(QuotingSessionsConstants.OK_BUTTON_XPATH).click()
        else:
            self.find_by_xpath(QuotingSessionsConstants.CANCEL_BUTTON_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(QuotingSessionsConstants.DOWNLOAD_PDF_BUTTON_AT_MORE_ACTIONS_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_on_pin_row(self):
        self.find_by_xpath(QuotingSessionsConstants.PIN_ROW_XPATH).click()

    def click_on_new(self):
        self.find_by_xpath(QuotingSessionsConstants.NEW_BUTTON_XPATH).click()


    def click_on_user_icon(self):
        self.find_by_xpath(QuotingSessionsConstants.USER_ICON_AT_RIGHT_CORNER).click()

    def click_on_logout(self):
        self.find_by_xpath(QuotingSessionsConstants.LOGOUT_BUTTON_XPATH).click()
