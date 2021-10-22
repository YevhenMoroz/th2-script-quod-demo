import time

from quod_qa.web_admin.web_admin_core.pages.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.reference_data.instr_symbol_info.instr_symbol_info_constants import \
    InstrSymbolInfoConstants

from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer


class InstrSymbolInfoWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_close(self):
        self.find_by_xpath(InstrSymbolInfoConstants.CLOSE_WIZARD_XPATH).click()

    def click_on_save_changes(self):
        self.find_by_xpath(InstrSymbolInfoConstants.SAVE_CHANGES_BUTTON_XPATH).click()

    def click_on_revert_changes(self):
        self.find_by_xpath(InstrSymbolInfoConstants.REVERT_CHANGES_XPATH).click()

    def click_on_go_back(self):
        self.find_by_xpath(InstrSymbolInfoConstants.GO_BACK_BUTTON_XPATH).click()

    def click_download_pdf_entity_button_and_check_pdf(self, value):
        self.clear_download_directory()
        self.find_by_xpath(InstrSymbolInfoConstants.DOWNLOAD_PDF_BUTTON_XPATH).click()
        time.sleep(2)
        return self.is_pdf_contains_value(value)

    def set_instr_symbol(self, value):
        self.set_combobox_value(InstrSymbolInfoConstants.WIZARD_INSTR_SYMBOL_XPATH, value)

    def get_instr_symbol(self):
        return self.get_text_by_xpath(InstrSymbolInfoConstants.WIZARD_INSTR_SYMBOL_XPATH)

    def set_cum_trading_limit_percentage(self, value):
        self.set_text_by_xpath(InstrSymbolInfoConstants.WIZARD_CUM_TRADING_LIMIT_PERCENTAGE_XPATH, value)

    def get_cum_trading_limit_percentage(self):
        return self.get_text_by_xpath(InstrSymbolInfoConstants.WIZARD_CUM_TRADING_LIMIT_PERCENTAGE_XPATH)

    def set_md_max_spread(self, value):
        self.set_text_by_xpath(InstrSymbolInfoConstants.WIZARD_MD_MAX_SPREAD_XPATH, value)

    def get_md_max_spread(self):
        return self.get_text_by_xpath(InstrSymbolInfoConstants.WIZARD_MD_MAX_SPREAD_XPATH)

    def click_on_cross_through_eur_checkbox(self):
        self.find_by_xpath(InstrSymbolInfoConstants.WIZARD_CROSS_THROUGH_EUR_CHECKBOX_XPATH).click()

    def click_on_cross_through_usd_checkbox(self):
        self.find_by_xpath(InstrSymbolInfoConstants.WIZARD_CROSS_THROUGH_USD_CHECKBOX_XPATH).click()

    def click_on_cross_through_usd_to_eur(self):
        self.find_by_xpath(InstrSymbolInfoConstants.WIZARD_CROSS_THROUGH_USD_TO_EUR_CHECKBOX_XPATH)

    def click_on_cross_through_eur_to_usd(self):
        self.find_by_xpath(InstrSymbolInfoConstants.WIZARD_CROSS_THROUGH_EUR_TO_USD_CHECKBOX_XPATH)
