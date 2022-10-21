from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.market_making.auto_hedger.auto_hedger_constants import \
    AutoHedgerConstants

from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class AutoHedgerInstrumentsSubWizard(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def click_on_plus_button(self):
        self.find_by_xpath(AutoHedgerConstants.INSTRUMENTS_TAB_PLUS_BUTTON_XPATH).click()

    def click_on_checkmark_button(self):
        self.find_by_xpath(AutoHedgerConstants.INSTRUMENTS_TAB_CHECKMARK_BUTTON_XPATH).click()

    def click_on_cancel_button(self):
        self.find_by_xpath(AutoHedgerConstants.INSTRUMENTS_TAB_CANCEL_BUTTON_XPATH).click()

    def click_on_edit_button(self):
        self.find_by_xpath(AutoHedgerConstants.INSTRUMENTS_TAB_EDIT_BUTTON_XPATH).click()

    def click_on_delete_button(self):
        self.find_by_xpath(AutoHedgerConstants.INSTRUMENTS_TAB_DELETE_BUTTON_XPATH).click()

    def set_symbol(self, value):
        self.set_combobox_value(AutoHedgerConstants.INSTRUMENTS_TAB_SYMBOL_FIELD_XPATH, value)

    def get_symbol(self):
        return self.get_text_by_xpath(AutoHedgerConstants.INSTRUMENTS_TAB_SYMBOL_FIELD_XPATH)

    def set_hedging_strategy(self, value):
        self.set_combobox_value(AutoHedgerConstants.INSTRUMENTS_TAB_HEDGING_STRATEGY_FIELD_XPATH, value)

    def get_hedging_strategy(self):
        return self.get_text_by_xpath(AutoHedgerConstants.INSTRUMENTS_TAB_HEDGING_STRATEGY_FIELD_XPATH)

    def set_long_threshold_qty(self, value):
        self.set_text_by_xpath(AutoHedgerConstants.INSTRUMENTS_TAB_LONG_THRESHOLD_QTY_FIELD_XPATH, value)

    def get_long_threshold_qty(self):
        return self.get_text_by_xpath(AutoHedgerConstants.INSTRUMENTS_TAB_LONG_THRESHOLD_QTY_FIELD_XPATH)

    def set_long_residual_qty(self, value):
        self.set_text_by_xpath(AutoHedgerConstants.INSTRUMENTS_TAB_LONG_RESIDUAL_QTY_FIELD_XPATH, value)

    def get_long_residual_qty(self):
        return self.get_text_by_xpath(AutoHedgerConstants.INSTRUMENTS_TAB_LONG_RESIDUAL_QTY_FIELD_XPATH)

    def set_short_threshold_qty(self, value):
        self.set_text_by_xpath(AutoHedgerConstants.INSTRUMENTS_TAB_SHORT_THRESHOLD_QTY_FIELD_XPATH, value)

    def get_short_threshold_qty(self):
        return self.get_text_by_xpath(AutoHedgerConstants.INSTRUMENTS_TAB_SHORT_THRESHOLD_QTY_FIELD_XPATH)

    def set_short_residual_qty(self, value):
        self.set_text_by_xpath(AutoHedgerConstants.INSTRUMENTS_TAB_SHORT_RESIDUAL_QTY_FIELD_XPATH, value)

    def get_short_residual_qty(self):
        return self.get_text_by_xpath(AutoHedgerConstants.INSTRUMENTS_TAB_SHORT_RESIDUAL_QTY_FIELD_XPATH)

    # checkboxes

    def click_on_use_long_quantities_as_both_long_and_short_checkbox(self):
        self.find_by_xpath(
            AutoHedgerConstants.INSTRUMENTS_TAB_USE_LONG_QUANTITIES_AS_BOTH_LONG_AND_SHORT_CHECKBOX_XPATH).click()

    def click_on_maintain_hedge_positions_checkbox(self):
        self.find_by_xpath(AutoHedgerConstants.INSTRUMENTS_TAB_MAINTAIN_HEDGE_POSITIONS_CHECKBOX_XPATH).click()

    def click_on_send_hedge_order_checkbox(self):
        self.find_by_xpath(AutoHedgerConstants.INSTRUMENTS_TAB_SEND_HEDGE_ORDER_CHECKBOX_XPATH).click()

    def set_send_hedge_order(self, value):
        self.set_combobox_value(AutoHedgerConstants.INSTRUMENTS_TAB_SEND_HEDGE_ORDER_FIELD_XPATH, value)

    def get_send_hedge_order(self):
        return self.get_text_by_xpath(AutoHedgerConstants.INSTRUMENTS_TAB_SEND_HEDGE_ORDER_FIELD_XPATH)

    def set_synthetic_combination_to_auto_hedge(self, value):
        self.set_combobox_value(AutoHedgerConstants.INSTRUMENTS_TAB_SYNTHETIC_COMBINATION_TO_AUTO_HEDGE_FIELD_XPATH,
                                value)

    def get_synthetic_combination_to_auto_hedge(self):
        return self.get_text_by_xpath(
            AutoHedgerConstants.INSTRUMENTS_TAB_SYNTHETIC_COMBINATION_TO_AUTO_HEDGE_FIELD_XPATH)

    def set_hedging_execution_strategy(self, value):
        self.set_combobox_value(AutoHedgerConstants.INSTRUMENTS_TAB_HEDGING_EXECUTION_STRATEGY_FIELD_XPATH, value)

    def get_hedging_execution_strategy(self):
        return self.get_text_by_xpath(AutoHedgerConstants.INSTRUMENTS_TAB_HEDGING_EXECUTION_STRATEGY_FIELD_XPATH)

    def set_execution_strategy_type(self, value):
        self.set_combobox_value(AutoHedgerConstants.INSTRUMENTS_TAB_EXECUTION_STRATEGY_TYPE_XPATH, value)

    def get_execution_strategy_type(self):
        return self.get_text_by_xpath(AutoHedgerConstants.INSTRUMENTS_TAB_EXECUTION_STRATEGY_TYPE_XPATH)

    def set_hedging_execution_strategy_tif(self, value):
        self.set_combobox_value(AutoHedgerConstants.INSTRUMENTS_TAB_HEDGING_EXECUTION_STRATEGY_TIF_FIELD_XPATH, value)

    def get_hedging_execution_strategy_tif(self):
        return self.get_text_by_xpath(AutoHedgerConstants.INSTRUMENTS_TAB_HEDGING_EXECUTION_STRATEGY_TIF_FIELD_XPATH)

    def set_hedging_execution_strategy_max_duration(self, value):
        self.set_text_by_xpath(AutoHedgerConstants.INSTRUMENTS_TAB_HEDGING_EXECUTION_STRATEGY_MAX_DURATION_FIELD_XPATH,
                               value)

    def get_hedging_execution_strategy_max_duration(self):
        return self.get_text_by_xpath(
            AutoHedgerConstants.INSTRUMENTS_TAB_HEDGING_EXECUTION_STRATEGY_MAX_DURATION_FIELD_XPATH)

    def is_default_execution_strategy_has_italic_font(self, value):
        self.find_by_xpath(AutoHedgerConstants.INSTRUMENTS_TAB_HEDGING_EXECUTION_STRATEGY_FIELD_XPATH).click()
        self.set_text_by_xpath(AutoHedgerConstants.INSTRUMENTS_TAB_HEDGING_EXECUTION_STRATEGY_FIELD_XPATH, value)
        attribute_value = self.find_by_xpath(AutoHedgerConstants.DROP_DOWN_MENU_XPATH).get_attribute("class")
        return True if 'italic' in attribute_value else False
