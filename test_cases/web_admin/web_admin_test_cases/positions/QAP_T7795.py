import random
import string

from test_framework.web_admin_core.pages.positions.cash_positions.main_page import *
from test_framework.web_admin_core.pages.positions.cash_positions.wizards import *

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T7795(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")

        self.name = [''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6)) for _ in range(2)]
        self.client_cash_account_id = [''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
                                       for _ in range(2)]
        self.venue_cash_account_id = [''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
                                      for _ in range(2)]

        self.currency = 'EUR'
        self.client = 'CLIENT1'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_cash_positions_page()

    def test_context(self):
        self.precondition()

        cash_positions_page = MainPage(self.web_driver_container)
        cash_positions_page.click_on_new()
        values_tab = ValuesTab(self.web_driver_container)
        values_tab.set_name(self.name[0])
        values_tab.set_client_cash_account_id(self.client_cash_account_id[0])
        values_tab.set_venue_cash_account_id(self.venue_cash_account_id[0])
        values_tab.set_currency(self.currency)
        values_tab.set_client(self.client)
        wizard = MainWizard(self.web_driver_container)
        wizard.click_on_save_changes()

        cash_positions_page.click_on_new()
        values_tab.set_name(self.name[1])
        values_tab.set_client_cash_account_id(self.client_cash_account_id[1])
        values_tab.set_venue_cash_account_id(self.venue_cash_account_id[1])
        values_tab.set_currency(self.currency)
        values_tab.set_client(self.client)
        wizard.click_on_save_changes()

        cash_positions_page.set_name(self.name[0])
        time.sleep(1)
        self.verify("Firs entity has been saved", True,
                    cash_positions_page.is_searched_cash_account_found(self.name[0]))

        cash_positions_page.set_name(self.name[1])
        time.sleep(1)
        self.verify("Second entity has been saved", True,
                    cash_positions_page.is_searched_cash_account_found(self.name[1]))
