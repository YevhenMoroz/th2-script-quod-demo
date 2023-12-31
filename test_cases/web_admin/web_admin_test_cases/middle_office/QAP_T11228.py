import time

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.middle_office.allocation_matching_profiles.main_page import MainPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T11228(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

        self.main_page_filters = ['Instrument', 'Client', 'Quantity', 'Avg Price', 'Currency', 'Side']

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)

    def test_context(self):
        side_menu = SideMenu(self.web_driver_container)
        main_page = MainPage(self.web_driver_container)

        self.precondition()

        side_menu.open_allocation_matching_profiles_page()
        time.sleep(1)
        expected_result = [False for _ in range(len(self.main_page_filters))]
        actual_result = [main_page.is_instrument_column_displayed(), main_page.is_client_column_displayed(),
                         main_page.is_quantity_column_displayed(), main_page.is_avg_price_column_displayed(),
                         main_page.is_currency_column_displayed(), main_page.is_side_column_displayed()]
        self.verify("Required fields are not displayed", expected_result, actual_result)
