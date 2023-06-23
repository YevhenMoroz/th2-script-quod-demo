import time

from test_framework.web_admin_core.pages.clients_accounts.client_lists.main_page import ClientListsPage
from test_framework.web_admin_core.pages.general.common.common_page import CommonPage
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T8433(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = "adm03"
        self.password = "adm03"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_client_list_page()

    def test_context(self):
        self.precondition()

        main_page = ClientListsPage(self.web_driver_container)
        main_page.click_on_more_actions()
        main_page.click_on_edit()

        time.sleep(1)
        common_act = CommonPage(self.web_driver_container)
        self.verify("Such record already exists displayed", False, common_act.is_error_message_displayed())
