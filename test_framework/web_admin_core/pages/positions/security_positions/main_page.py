import time

from test_framework.web_admin_core.pages.common_page import CommonPage
from test_framework.web_admin_core.pages.positions.security_positions.constants import Constants
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer


class MainPage(CommonPage):
    def __init__(self, web_driver_container: WebDriverContainer):
        super().__init__(web_driver_container)

    def set_account_search_pattern(self, acc_name):
        self.set_text_by_xpath(Constants.MainPage.ACCOUNTS_FIELD, acc_name)

    def select_account(self, acc_name):
        self.select_value_from_dropdown_list(Constants.MainPage.ACCOUNTS_FIELD, acc_name)

    def get_all_accounts_from_drop_down_by_entered_pattern(self, acc_name):
        self.set_account_search_pattern(acc_name)
        time.sleep(1)
        return self.get_all_items_from_drop_down(Constants.MainPage.DROP_DOWN_MENU)

    def is_searched_account_in_drop_down(self, acc_name):
        self.set_account_search_pattern(acc_name)
        time.sleep(1)
        return self.is_element_present(Constants.MainPage.DISPLAYED_ACCOUNT_IN_DROP_MENU.format(acc_name))
