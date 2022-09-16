import time
import traceback
import random
import string

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.client_accounts.accounts.accounts_page import AccountsPage
from test_framework.web_admin_core.pages.client_accounts.accounts.accounts_wizard import AccountsWizard
from test_framework.web_admin_core.pages.client_accounts.accounts.accounts_routes_subwizard \
    import AccountsRoutesSubWizard
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3356(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = "adm03"
        self.password = "adm03"
        self.account_id = ''
        self.route_account_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.route = 'Credit Suisse'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_accounts_page()

    def test_context(self):
        try:
            self.precondition()

            main_page = AccountsPage(self.web_driver_container)
            main_page.click_more_actions_button()
            main_page.click_edit_entity_button()
            values_sub_wizard = AccountsWizard(self.web_driver_container)
            self.account_id = values_sub_wizard.get_id()

            routes_tab = AccountsRoutesSubWizard(self.web_driver_container)
            routes_tab.click_on_plus_button()
            routes_tab.set_route_account_name(self.route_account_name)
            routes_tab.set_route(self.route)
            routes_tab.select_agent_fee_exemption_checkbox()
            routes_tab.click_on_checkmark_button()

            wizard = AccountsWizard(self.web_driver_container)
            wizard.click_save_button()

            main_page.set_id(self.account_id)
            time.sleep(1)
            main_page.click_more_actions_button()
            main_page.click_edit_entity_button()

            routes_tab.filter_routes(self.route_account_name)
            time.sleep(1)
            routes_tab.click_edit_button()
            self.verify("Agent fee exemption is selected", True, routes_tab.is_agent_fee_exemption_selected())

            routes_tab.click_discard_entity_button()
            routes_tab.click_delete_button()

            wizard.click_save_button()

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
