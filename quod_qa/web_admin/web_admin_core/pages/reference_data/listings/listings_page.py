import time

from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.reference_data.listings.listings_constants import ListingsConstants
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class ListingsPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_more_actions(self):
        self.find_by_xpath(ListingsConstants.MORE_ACTIONS_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(ListingsConstants.EDIT_XPATH).click()

    def click_on_clone(self):
        self.find_by_xpath(ListingsConstants.CLONE_XPATH).click()

    def click_on_enable_disable_button(self):
        self.find_by_xpath(ListingsConstants.ENABLE_DISABLE_BUTTON_XPATH).click()
        time.sleep(2)
        self.find_by_xpath(ListingsConstants.OK_BUTTON_XPATH).click()


    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(ListingsConstants.DOWNLOAD_PDF_BUTTON_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_on_delete(self, confirmation):
        self.find_by_xpath(ListingsConstants.DELETE_XPATH).click()
        if confirmation:
            time.sleep(2)
            self.find_by_xpath(ListingsConstants.OK_BUTTON_XPATH).click()
        else:
            self.find_by_xpath(ListingsConstants.CANCEL_BUTTON_XPATH).click()

    def click_on_pin_row(self):
        self.find_by_xpath(ListingsConstants.PIN_ROW_XPATH).click()

    def click_on_new(self):
        self.find_by_xpath(ListingsConstants.NEW_BUTTON_XPATH).click()

    def click_on_user_icon(self):
        self.find_by_xpath(ListingsConstants.USER_ICON_AT_RIGHT_CORNER).click()

    def click_on_logout(self):
        self.find_by_xpath(ListingsConstants.LOGOUT_BUTTON_XPATH).click()

    def set_venue(self, value):
        self.set_text_by_xpath(ListingsConstants.MAIN_PAGE_VENUE_FILTER_XPATH, value)

    def get_venue(self):
        return self.find_by_xpath(ListingsConstants.MAIN_PAGE_VENUE_XPATH).text

    def set_sub_venue(self, value):
        self.set_text_by_xpath(ListingsConstants.MAIN_PAGE_SUB_VENUE_FILTER_XPATH, value)

    def get_sub_venue(self):
        return self.find_by_xpath(ListingsConstants.MAIN_PAGE_SUB_VENUE_XPATH).text

    def set_symbol(self, value):
        self.set_text_by_xpath(ListingsConstants.MAIN_PAGE_SYMBOL_FILTER_XPATH, value)

    def get_symbol(self):
        return self.find_by_xpath(ListingsConstants.MAIN_PAGE_SYMBOL_XPATH).text

    def set_instrument(self, value):
        self.set_text_by_xpath(ListingsConstants.MAIN_PAGE_INSTRUMENT_FILTER_XPATH, value)

    def get_instrument(self):
        return self.find_by_xpath(ListingsConstants.MAIN_PAGE_INSTRUMENT_XPATH).text

    def set_currency(self, value):
        self.set_text_by_xpath(ListingsConstants.MAIN_PAGE_CURRENCY_FILTER_XPATH, value)

    def get_currency(self):
        return self.find_by_xpath(ListingsConstants.MAIN_PAGE_CURRENCY_XPATH).text

    def set_instr_type(self, value):
        self.set_text_by_xpath(ListingsConstants.MAIN_PAGE_INSTR_TYPE_FILTER_XPATH, value)

    def get_instr_type(self):
        return self.find_by_xpath(ListingsConstants.MAIN_PAGE_INSTR_TYPE_XPATH).text

    def set_tenor(self, value):
        self.set_text_by_xpath(ListingsConstants.MAIN_PAGE_TENOR_FILTER_XPATH, value)

    def get_tenor(self):
        return self.find_by_xpath(ListingsConstants.MAIN_PAGE_TENOR_XPATH).text


    def set_listing_in_global_filter(self,value):
        self.set_text_by_xpath(ListingsConstants.MAIN_PAGE_LISTING_GLOBAL_FILTER_XPATH,value)

    def click_on_load(self):
        self.find_by_xpath(ListingsConstants.MAIN_PAGE_LOAD_BUTTON_XPATH).click()
        time.sleep(2)
