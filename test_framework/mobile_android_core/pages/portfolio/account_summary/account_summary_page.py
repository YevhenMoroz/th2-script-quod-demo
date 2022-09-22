from test_framework.mobile_android_core.pages.portfolio.account_summary.account_summary_constants import AccountSummaryConstants
from test_framework.mobile_android_core.utils.common_page import CommonPage
from test_framework.mobile_android_core.utils.driver import AppiumDriver


class AccountSummaryPage(CommonPage):
    def __init__(self, driver: AppiumDriver):
        super().__init__(driver)

    # region account_summary
    def click_on_account_summary(self):
        self.find_by_xpath(AccountSummaryConstants.ACCOUNT_SUMMARY_TITLE).click()

    def swipe_cash_account(self, name):
        cash_account = self.find_by_xpath(self.set_cash_account_xpath(name))
        cash_account_params = cash_account.rect
        self.swipe_by_coordinates(cash_account_params['x']+cash_account_params['width']/4,
                                  cash_account_params['y']+ cash_account_params['height']/2,
                                   cash_account_params['width']/2 + cash_account_params['x'] - 1,
                                   cash_account_params['height']/2 + cash_account_params['y'] - 1)

    def set_cash_account_xpath(self, name):
        return AccountSummaryConstants.CASH_ACCOUNT_START+name+AccountSummaryConstants.CASH_ACCOUNT_END
    # endregion

    # region cash_withdrawal
    # endregion

    # region statement
    def click_statement_back(self):
        self.find_by_xpath(AccountSummaryConstants.STATEMENT_GO_BACK).click()

    def click_statement_button(self):
        self.find_by_xpath(AccountSummaryConstants.STATEMENT_BUTTON).click()

    def open_cash_balance_statement(self, name):
        self.swipe_cash_account(name)
        self.click_statement_button()
    # endregion
