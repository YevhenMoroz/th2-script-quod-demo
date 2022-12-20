import time

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.markets.instrument_symbols.constants import \
    InstrumentSymbolsConstants

from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class InstrumentSymbolsWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_close(self):
        self.find_by_xpath(InstrumentSymbolsConstants.CLOSE_WIZARD_XPATH).click()

    def click_on_save_changes(self):
        self.find_by_xpath(InstrumentSymbolsConstants.SAVE_CHANGES_BUTTON_XPATH).click()

    def click_on_revert_changes(self):
        self.find_by_xpath(InstrumentSymbolsConstants.REVERT_CHANGES_XPATH).click()

    def click_on_go_back(self):
        self.find_by_xpath(InstrumentSymbolsConstants.GO_BACK_BUTTON_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(InstrumentSymbolsConstants.DOWNLOAD_PDF_BUTTON_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def set_instr_symbol(self, value):
        self.set_combobox_value(InstrumentSymbolsConstants.WIZARD_INSTR_SYMBOL_XPATH, value)

    def get_instr_symbol(self):
        return self.get_text_by_xpath(InstrumentSymbolsConstants.WIZARD_INSTR_SYMBOL_XPATH)

    def get_all_instr_symbols_from_drop_menu(self):
        self.set_text_by_xpath(InstrumentSymbolsConstants.WIZARD_INSTR_SYMBOL_XPATH, "")
        time.sleep(1)
        return self.get_all_items_from_drop_down(InstrumentSymbolsConstants.DROP_DOWN_MENU_XPATH)

    def set_cum_trading_limit_percentage(self, value):
        self.set_text_by_xpath(InstrumentSymbolsConstants.WIZARD_CUM_TRADING_LIMIT_PERCENTAGE_XPATH, value)

    def get_cum_trading_limit_percentage(self):
        return self.get_text_by_xpath(InstrumentSymbolsConstants.WIZARD_CUM_TRADING_LIMIT_PERCENTAGE_XPATH)

    def set_md_max_spread(self, value):
        self.set_text_by_xpath(InstrumentSymbolsConstants.WIZARD_MD_MAX_SPREAD_XPATH, value)

    def get_md_max_spread(self):
        return self.get_text_by_xpath(InstrumentSymbolsConstants.WIZARD_MD_MAX_SPREAD_XPATH)

    def click_on_cross_through_eur_checkbox(self):
        self.find_by_xpath(InstrumentSymbolsConstants.WIZARD_CROSS_THROUGH_EUR_CHECKBOX_XPATH).click()

    def click_on_cross_through_usd_checkbox(self):
        self.find_by_xpath(InstrumentSymbolsConstants.WIZARD_CROSS_THROUGH_USD_CHECKBOX_XPATH).click()

    def click_on_cross_through_usd_to_eur(self):
        self.find_by_xpath(InstrumentSymbolsConstants.WIZARD_CROSS_THROUGH_USD_TO_EUR_CHECKBOX_XPATH)

    def click_on_cross_through_eur_to_usd(self):
        self.find_by_xpath(InstrumentSymbolsConstants.WIZARD_CROSS_THROUGH_EUR_TO_USD_CHECKBOX_XPATH)

    def is_instrsymbol_field_enabled(self):
        return self.is_field_enabled(InstrumentSymbolsConstants.WIZARD_INSTR_SYMBOL_XPATH)

    def is_error_message_displayed(self):
        return self.is_element_present(InstrumentSymbolsConstants.WIZARD_ERROR_MESSAGE_XPATH)

    def click_on_error_message_pop_up(self):
        self.find_by_xpath(InstrumentSymbolsConstants.WIZARD_ERROR_MESSAGE_XPATH).click()
