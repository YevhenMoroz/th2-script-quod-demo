from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_framework.web_trading.web_trading_core.pages.main_page.workspace.account_summary.account_summary_constants import \
    AccountSummaryConstants


class AccountSummaryPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    # region Filter values in main page
    def get_cash_account(self):
        return self.find_by_xpath(AccountSummaryConstants.USER_CASH_ACCOUNT_COLUMN_XPATH).text

    def get_currency(self):
        return self.find_by_xpath(AccountSummaryConstants.USER_CURRENCY_COLUMN_XPATH).text

    def get_cash_balance(self):
        return self.find_by_xpath(AccountSummaryConstants.USER_CURRENCY_CASH_BALANCE_XPATH).text

    def get_available_cash(self):
        return self.find_by_xpath(AccountSummaryConstants.USER_AVAILABLE_CASH_COLUMN_XPATH).text

    def get_transaction_holding_amount(self):
        return self.find_by_xpath(AccountSummaryConstants.USER_TRANSACTION_HOLDING_AMOUNT_COLUMN_XPATH).text

    def get_reserved_amount(self):
        return self.find_by_xpath(AccountSummaryConstants.USER_RESERVED_AMOUNT_COLUMN_XPATH).text

    def get_buying_power(self):
        return self.find_by_xpath(AccountSummaryConstants.USER_BUYING_POWER_COLUMN_XPATH).text

    def get_security_account(self):
        return self.find_by_xpath(AccountSummaryConstants.USER_SECURITY_ACCOUNT_XPATH).text

    def get_total_security_value(self):
        return self.find_by_xpath(AccountSummaryConstants.USER_TOTAL_SECURITY_VALUE_XPATH).text

    # endregion

    # region Visible columns
    def click_on_field_chooser_button(self):
        self.find_by_xpath(AccountSummaryConstants.FIELD_CHOOSER_XPATH).click()

    def select_visible_columns(self, value):
        self.set_checkbox_list(AccountSummaryConstants.COLUMNS_LIST_CHECKBOX_XPATH, value)

    def click_on_hide_all(self):
        self.find_by_xpath(AccountSummaryConstants.HIDE_ALL_BUTTON_XPATH).click()

    def click_on_show_all(self):
        self.find_by_xpath(AccountSummaryConstants.SHOW_ALL_BUTTON_XPATH).click()

    # endregion

    # region Advanced filtering
    def click_on_advanced_filtering_button(self):
        self.find_by_xpath(AccountSummaryConstants.ADVANCED_FILTERING_BUTTON_XPATH).click()

    # endregion

    def click_on_copy_panel_button(self):
        self.find_by_xpath(AccountSummaryConstants.COPY_PANEL_BUTTON_XPATH).click()

    def click_on_maximize_button(self):
        self.find_element_in_shadow_root(AccountSummaryConstants.MAXIMIZE_BUTTON_CSS)

    def click_on_minimize_button(self):
        self.find_element_in_shadow_root(AccountSummaryConstants.MINIMIZE_BUTTON_CSS)

    def click_on_close_button(self):
        self.find_element_in_shadow_root(AccountSummaryConstants.CLOSE_BUTTON_CSS)
