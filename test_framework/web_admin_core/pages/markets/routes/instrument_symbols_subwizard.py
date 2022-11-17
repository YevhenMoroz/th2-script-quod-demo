from selenium.webdriver import ActionChains

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.markets.routes.constants import RoutesConstants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class RoutesInstrumentSymbolsSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_plus_button_at_instr_symbols_tab(self):
        """
        ActionChains helps to avoid falling test when adding several quantities at once.
        (The usual "click" method fails because after adding the first entry, the cursor remains on the "edit" button
        and the pop-up of edit btn covers half of the "+" button)
        """
        element = self.find_by_xpath(RoutesConstants.PLUS_BUTTON_AT_INSTR_SYMBOLS_TAB_XPATH)
        action = ActionChains(self.web_driver_container.get_driver())
        action.move_to_element(element)
        action.click()
        action.perform()

    def click_on_checkmark_button_at_instr_symbols_tab(self):
        self.find_by_xpath(RoutesConstants.CHECK_MARK_BUTTON_AT_INSTR_SYMBOLS_TAB_XPATH).click()

    def click_on_close_button_at_instr_symbols_tab(self):
        self.find_by_xpath(RoutesConstants.CLOSE_BUTTON_AT_INSTR_SYMBOLS_TAB_XPATH).click()

    def click_on_edit_button_at_instr_symbols_tab(self):
        self.find_by_xpath(RoutesConstants.EDIT_BUTTON_AT_INSTR_SYMBOLS_TAB_XPATH).click()

    def click_on_delete_button_at_instr_symbol_tab(self):
        self.find_by_xpath(RoutesConstants.DELETE_BUTTON_AT_INSTR_SYMBOLS_TAB_XPATH).click()

    # setters
    def set_instr_symbol_at_instr_symbols_tab(self, value):
        self.set_combobox_value(RoutesConstants.INSTR_SYMBOL_AT_INSTR_SYMBOLS_TAB_XPATH, value)

    def set_price_multiplier_at_instr_symbols_tab(self, value):
        self.set_text_by_xpath(RoutesConstants.PRICE_MULTIPLIER_AT_INSTR_SYMBOLS_TAB_XPATH, value)

    def set_instr_symbol_filter_at_instr_symbols_tab(self, value):
        self.set_text_by_xpath(RoutesConstants.INSTR_SYMBOL_FILTER_AT_INSTR_SYMBOLS_TAB_XPATH, value)

    def set_price_multiplier_filter_at_instr_symbols_tab(self, value):
        self.set_text_by_xpath(RoutesConstants.PRICE_MULTIPLIER_FILTER_AT_INSTR_SYMBOLS_TAB_XPATH, value)

    # getters
    def get_instr_symbol_value_at_instr_symbols_tab(self):
        return self.get_text_by_xpath(RoutesConstants.INSTR_SYMBOL_AT_INSTR_SYMBOLS_TAB_XPATH)

    def get_price_multiplier_value_at_instr_symbols_tab(self):
        return self.get_text_by_xpath(RoutesConstants.PRICE_MULTIPLIER_AT_INSTR_SYMBOLS_TAB_XPATH)
