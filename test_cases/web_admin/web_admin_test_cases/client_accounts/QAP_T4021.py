import sys
import time
import traceback
import string
import random

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.client_accounts.client_groups.client_groups_page \
    import ClientGroupsPage
from test_framework.web_admin_core.pages.client_accounts.client_groups.client_groups_wizard import ClientGroupsWizard
from test_framework.web_admin_core.pages.client_accounts.client_groups.client_groups_values_sub_wizard \
    import ClientGroupsValuesSubWizard
from test_framework.web_admin_core.pages.general.common.common_page import CommonPage

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T4021(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = 'QAP_T4021'
        self.description = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        side_menu = SideMenu(self.web_driver_container)
        main_page = ClientGroupsPage(self.web_driver_container)
        wizard = ClientGroupsWizard(self.web_driver_container)
        values_tab = ClientGroupsValuesSubWizard(self.web_driver_container)

        login_page.login_to_web_admin(self.login, self.password)
        side_menu.open_client_groups_page()
        main_page.click_on_new()
        values_tab.set_name(self.name)
        values_tab.set_description(self.description)
        wizard.click_on_save_changes()

    def test_context(self):
        main_page = ClientGroupsPage(self.web_driver_container)
        common_act = CommonPage(self.web_driver_container)

        try:
            self.precondition()

            main_page.set_name(self.name)
            time.sleep(1)
            main_page.click_on_more_actions()
            main_page.click_on_delete(True)
            time.sleep(1)
            common_act.refresh_page(True)
            time.sleep(1)
            main_page.set_name(self.name)
            time.sleep(1)
            self.verify("Client Group deleted and not displayed", False,
                        main_page.is_searched_client_group_found_by_name(self.name))
            
        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
