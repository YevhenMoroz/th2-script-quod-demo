import time

from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.market_making.auto_hedger.auto_hedger_constants import \
    AutoHedgerConstants

from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class AutoHedgerPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_name_filter(self, value):
        self.set_text_by_xpath(AutoHedgerConstants.MAIN_PAGE_NAME_FILTER_XPATH, value)

    def set_position_book_filter(self, value):
        self.set_text_by_xpath(AutoHedgerConstants.MAIN_PAGE_POSITION_BOOK_FILTER_XPATH, value)

    def set_client_group_filter(self, value):
        self.set_text_by_xpath(AutoHedgerConstants.MAIN_PAGE_CLIENT_GROUP_FILTER_XPATH, value)

    def set_enable_schedule_filter(self, value):
        self.set_text_by_xpath(AutoHedgerConstants.MAIN_PAGE_ENABLE_SCHEDULE_FILTER_XPATH, value)

    def click_on_more_actions(self):
        self.find_by_xpath(AutoHedgerConstants.MORE_ACTIONS_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(AutoHedgerConstants.EDIT_XPATH).click()

    def click_on_clone(self):
        self.find_by_xpath(AutoHedgerConstants.CLONE_XPATH).click()

    def click_on_delete(self, confirmation):
        self.find_by_xpath(AutoHedgerConstants.DELETE_XPATH).click()
        if confirmation:
            time.sleep(2)
            self.find_by_xpath(AutoHedgerConstants.OK_BUTTON_XPATH).click()
        else:
            self.find_by_xpath(AutoHedgerConstants.CANCEL_BUTTON_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(AutoHedgerConstants.DOWNLOAD_PDF_BUTTON_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_on_pin_row(self):
        self.find_by_xpath(AutoHedgerConstants.PIN_ROW_XPATH).click()

    def click_on_new(self):
        self.find_by_xpath(AutoHedgerConstants.NEW_BUTTON_XPATH).click()

    def click_on_user_icon(self):
        self.find_by_xpath(AutoHedgerConstants.USER_ICON_AT_RIGHT_CORNER).click()

    def click_on_logout(self):
        self.find_by_xpath(AutoHedgerConstants.LOGOUT_BUTTON_XPATH).click()
