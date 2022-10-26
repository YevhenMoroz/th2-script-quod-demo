import time

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.markets.instrument_symbols.constants import \
    InstrumentSymbolsConstants

from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class InstrumentSymbolsMainPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_more_actions(self):
        self.find_by_xpath(InstrumentSymbolsConstants.MORE_ACTIONS_XPATH).click()

    def click_on_edit(self):
        self.find_by_xpath(InstrumentSymbolsConstants.EDIT_XPATH).click()

    def click_on_clone(self):
        self.find_by_xpath(InstrumentSymbolsConstants.CLONE_XPATH).click()

    def click_on_delete(self, confirmation):
        self.find_by_xpath(InstrumentSymbolsConstants.DELETE_XPATH).click()
        if confirmation:
            time.sleep(2)
            self.find_by_xpath(InstrumentSymbolsConstants.OK_BUTTON_XPATH).click()
        else:
            self.find_by_xpath(InstrumentSymbolsConstants.CANCEL_BUTTON_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(InstrumentSymbolsConstants.DOWNLOAD_PDF_BUTTON_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def click_on_pin_row(self):
        self.find_by_xpath(InstrumentSymbolsConstants.PIN_ROW_XPATH).click()

    def click_on_new(self):
        self.find_by_xpath(InstrumentSymbolsConstants.NEW_BUTTON_XPATH).click()

    def click_on_user_icon(self):
        self.find_by_xpath(InstrumentSymbolsConstants.USER_ICON_AT_RIGHT_CORNER).click()

    def click_on_logout(self):
        self.find_by_xpath(InstrumentSymbolsConstants.LOGOUT_BUTTON_XPATH).click()

    def set_instr_symbol(self, value):
        self.set_text_by_xpath(InstrumentSymbolsConstants.MAIN_PAGE_INSTR_SYMBOL_FILTER_XPATH, value)

    def set_cum_trading_limit_percentage(self, value):
        self.set_text_by_xpath(InstrumentSymbolsConstants.MAIN_PAGE_CUM_TRADING_LIMIT_FILTER_XPATH, value)

    def set_md_max_spread(self, value):
        self.set_text_by_xpath(InstrumentSymbolsConstants.MAIN_PAGE_MD_MAX_SPREAD_FILTER_XPATH, value)

    def set_cross_through_usd(self, value):
        self.set_text_by_xpath(InstrumentSymbolsConstants.MAIN_PAGE_CROSS_THROUGH_USD_FILTER_XPATH, value)

    def set_cross_through_eur(self, value):
        self.set_text_by_xpath(InstrumentSymbolsConstants.MAIN_PAGE_CROSS_THROUGH_EUR_FILTER_XPATH, value)

    def set_cross_through_eur_to_usd(self, value):
        self.set_text_by_xpath(InstrumentSymbolsConstants.MAIN_PAGE_CROSS_THROUGH_EUR_TO_USD_FILTER_XPATH, value)

    def set_cross_through_usd_to_eur(self, value):
        self.set_text_by_xpath(InstrumentSymbolsConstants.MAIN_PAGE_CROSS_THROUGH_USD_TO_EUR_FILTER_XPATH, value)

    def get_instr_symbol(self):
        return self.find_by_xpath(InstrumentSymbolsConstants.MAIN_PAGE_INSTR_SYMBOL_XPATH).text

    def get_cum_trading_limit_percentage(self):
        return self.find_by_xpath(InstrumentSymbolsConstants.MAIN_PAGE_CUM_TRADING_LIMIT_XPATH).text

    def get_md_max_spread(self):
        return self.find_by_xpath(InstrumentSymbolsConstants.MAIN_PAGE_MD_MAX_SPREAD_XPATH).text

    def get_cross_through_usd(self):
        return self.is_checkbox_selected(InstrumentSymbolsConstants.MAIN_PAGE_CROSS_THROUGH_USD_XPATH)

    def get_cross_through_eur(self):
        return self.is_checkbox_selected(InstrumentSymbolsConstants.MAIN_PAGE_CROSS_THROUGH_EUR_XPATH)

    def get_cross_through_eur_to_usd(self):
        return self.is_checkbox_selected(InstrumentSymbolsConstants.MAIN_PAGE_CROSS_THROUGH_EUR_TO_USD_XPATH)

    def get_cross_through_usd_to_eur(self):
        return self.is_checkbox_selected(InstrumentSymbolsConstants.MAIN_PAGE_CROSS_THROUGH_USD_TO_EUR_XPATH)

    def is_incorrect_or_missing_value_message_displayed(self):
        if self.find_by_xpath(
                InstrumentSymbolsConstants.INCORRECT_OR_MISSING_VALUES_XPATH).text == "Incorrect or missing values":
            return True
        else:
            return False

    def is_instr_symbol_present(self):
        return self.is_element_present(InstrumentSymbolsConstants.MAIN_PAGE_INSTR_SYMBOL_XPATH)