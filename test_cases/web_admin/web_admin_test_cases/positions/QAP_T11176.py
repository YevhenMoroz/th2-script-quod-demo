import random
import string

from test_framework.web_admin_core.pages.positions.cash_positions.main_page import *
from test_framework.web_admin_core.pages.positions.cash_positions.wizards import *
from test_framework.web_admin_core.pages.general.common.common_page import CommonPage

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T11176(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None,
                 db_manager=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.db_manager = db_manager

        self.name = self.__class__.__name__
        self.client_cash_account_id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.venue_cash_account_id = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.currency = 'EUR'
        self.client = ''

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        side_menu = SideMenu(self.web_driver_container)
        cash_positions_page = MainPage(self.web_driver_container)
        values_tab = ValuesTab(self.web_driver_container)
        wizard = MainWizard(self.web_driver_container)
        common_act = CommonPage(self.web_driver_container)

        login_page.login_to_web_admin(self.login, self.password)
        side_menu.open_cash_positions_page()
        cash_positions_page.set_name(self.name)
        time.sleep(1)
        if not cash_positions_page.is_searched_cash_account_found(self.name):
            cash_positions_page.click_on_new()
            values_tab.set_name(self.name)
            values_tab.set_client_cash_account_id(self.client_cash_account_id)
            values_tab.set_venue_cash_account_id(self.venue_cash_account_id)
            values_tab.set_currency(self.currency)
            self.client = random.choice(values_tab.get_all_client_from_drop_menu_by_patter('client'))
            values_tab.set_client(self.client)
            wizard.click_on_save_changes()
            time.sleep(1)

        self.db_manager.my_db.execute(f"UPDATE cashaccount SET alive = 'N' WHERE cashaccountname = '{self.name}'")
        common_act.refresh_page(True)
        time.sleep(2)

    def test_context(self):
        cash_positions_page = MainPage(self.web_driver_container)
        common_act = CommonPage(self.web_driver_container)

        self.precondition()

        cash_positions_page.set_name(self.name)
        time.sleep(1)
        cash_positions_page.click_on_enable_disable_button()
        cash_positions_page.click_on_ok_button()
        time.sleep(2)
        self.verify("Cash Position has been enabled", True, cash_positions_page.is_cash_position_enabled())
        cash_positions_page.click_on_refresh_page()
        time.sleep(2)
        self.verify("After click on 'Refresh' button, Cash Position still enabled",
                    True, cash_positions_page.is_cash_position_enabled())
        common_act.refresh_page(True)
        time.sleep(2)
        cash_positions_page.set_name(self.name)
        time.sleep(1)
        self.verify("After refreshing page via browser, Cash Position still enabled",
                    True, cash_positions_page.is_cash_position_enabled())
