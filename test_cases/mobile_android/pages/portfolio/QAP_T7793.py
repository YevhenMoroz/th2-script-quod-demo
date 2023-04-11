from datetime import datetime, timedelta

from test_cases.mobile_android.common_test_case import CommonTestCase
from test_framework.mobile_android_core.pages.login.login_page import LoginPage

from test_framework.mobile_android_core.pages.main_page.main_page_constants import MainPageConstants
from test_framework.mobile_android_core.pages.main_page.main_page import MainPage

from test_framework.mobile_android_core.pages.menu.menu_page import MenuPage
from test_framework.mobile_android_core.pages.portfolio.account_summary.account_summary_constants import \
    AccountSummaryConstants
from test_framework.mobile_android_core.pages.portfolio.account_summary.account_summary_page import AccountSummaryPage

from test_framework.mobile_android_core.utils.driver import AppiumDriver

from pathlib import Path
from test_framework.mobile_android_core.utils.decorators.try_except_decorator_mobile import try_except

class QAP_T7793(CommonTestCase):

    def __init__(self, driver: AppiumDriver, second_lvl_id=None, data_set=None, environment=None):
        super().__init__(driver, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.client1_1 = self.data_set.get_client("client1_1")
        self.cash_acc1_c1_1 = self.data_set.get_cash_account_by_name("cash_account1_c1_1")

    @try_except(test_id=Path(__file__).name[:-3])
    def test_context(self):
        # region - preconditions
        login_page = LoginPage(self.appium_driver)
        main_page = MainPage(self.appium_driver)
        menu_page = MenuPage(self.appium_driver)
        account_summary_page = AccountSummaryPage(self.appium_driver)

        login_page.login_to_mobile_trading(self.login, self.password)
        self.verify("Preconditions - Login successful", None, main_page.wait_element_presence(MainPageConstants.PORTFOLIO_BUTTON))
        # endregion

        # region - test details

        # Step 1
        main_page.click_on_menu()
        menu_page.click_on_preferences()
        menu_page.set_default_client(self.client1_1)
        self.verify(f"Step 1 - {self.client1_1} is set as default client", self.client1_1, menu_page.get_default_client())
        # endregion

        # Step 2
        menu_page.go_back()
        menu_page.click_pd_go_back()
        main_page.click_on_portfolio()
        account_summary_page.click_on_account_summary()
        self.verify("Step 2 - Account Summary is opened", "true", account_summary_page.get_attribute_of_element_by_xpath(AccountSummaryConstants.ACCOUNT_SUMMARY_TITLE, "selected"))
        # endregion

        # Step 3
        account_summary_page.swipe_cash_account(self.cash_acc1_c1_1)
        self.verify("Step 3 - Statement button is shown", True, account_summary_page.get_element_exists_by_xpath(AccountSummaryConstants.STATEMENT_BUTTON))
        # endregion

        # Step 4
        account_summary_page.click_statement_button()
        self.verify("Step 4 - Cash Balance Statement pop-up is displayed", True, account_summary_page.get_element_exists_by_xpath(AccountSummaryConstants.STATEMENT_TITLE))
        # endregion

        # Step 5
        self.verify("Step 5 - Title Cash Balance Statement", True,
                    account_summary_page.get_element_exists_by_xpath(AccountSummaryConstants.STATEMENT_TITLE))
        self.verify(f"Step 5 - Cash Account = {self.cash_acc1_c1_1}", True, True)
        self.verify(f"Step 5 - From Date = {(datetime.now() - timedelta(hours = 3)).strftime('%Y/%m/01')}",
                    f"{(datetime.now() - timedelta(hours = 3)).strftime('%Y/%m/01')}, From Date",
                    account_summary_page.find_by_xpath(AccountSummaryConstants.FROM_DATE).text)
        self.verify(f"Step 5 - To Date = {(datetime.now() - timedelta(hours = 3)).strftime('%Y/%m/%d')}",
                    f"{(datetime.now() - timedelta(hours = 3)).strftime('%Y/%m/%d')}, To Date",
                    account_summary_page.find_by_xpath(AccountSummaryConstants.TO_DATE).text)
        self.verify("Step 5 - PDF radiobutton exists", True,
                    account_summary_page.get_element_exists_by_xpath(AccountSummaryConstants.PDF_RADIOBUTTON))
        self.verify("Step 5 - PDF radiobutton is checked", "true",
                    account_summary_page.get_attribute_of_element_by_xpath(AccountSummaryConstants.PDF_RADIOBUTTON, "checked"))
        self.verify("Step 5 - CSV radiobutton exists", True,
                    account_summary_page.get_element_exists_by_xpath(AccountSummaryConstants.CSV_RADIOBUTTON))
        self.verify("Step 5 - CSV radiobutton is unchecked", "false",
                    account_summary_page.get_attribute_of_element_by_xpath(AccountSummaryConstants.CSV_RADIOBUTTON, "checked"))
        self.verify("Step 5 - Retrieve button exists", True,
                    account_summary_page.get_element_exists_by_xpath(AccountSummaryConstants.STATEMENT_RETRIEVE))
        # endregion

        # Step 6
        account_summary_page.click_statement_back()
        self.verify("Step 6 - Account Summary is opened", "true",
                    account_summary_page.get_attribute_of_element_by_xpath(AccountSummaryConstants.ACCOUNT_SUMMARY_TITLE, "selected"))
        # endregion

        # Step 7
        account_summary_page.open_cash_balance_statement(self.cash_acc1_c1_1)
        self.verify("Step 7 - Cash Balance Statement pop-up is displayed", True,
                    account_summary_page.get_element_exists_by_xpath(AccountSummaryConstants.STATEMENT_TITLE))
        # endregion

        # Step 8
        account_summary_page.swipe_left_to_right()
        self.verify("Step 8 - Account Summary is opened", "true",
                    account_summary_page.get_attribute_of_element_by_xpath(AccountSummaryConstants.ACCOUNT_SUMMARY_TITLE, "selected"))
        # endregion

        # region - postconditions
        # endregion