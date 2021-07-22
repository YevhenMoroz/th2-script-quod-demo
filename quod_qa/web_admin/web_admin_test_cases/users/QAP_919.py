import time

from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.pages.users.users.users_account_groups_sub_wizard import \
    UsersAccountGroupsSubWizard
from quod_qa.web_admin.web_admin_core.pages.users.users.users_page import UsersPage
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_919(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm02"
        self.password = "adm02"
        self.client = "ANDclient"
        self.type = "Holder"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_users_page()
        users_page = UsersPage(self.web_driver_container)
        users_page.click_on_more_actions()
        time.sleep(2)
        users_page.click_on_edit_at_more_actions()
        time.sleep(2)
        account_groups_sub_wizard = UsersAccountGroupsSubWizard(self.web_driver_container)
        account_groups_sub_wizard.click_on_plus_button()
        time.sleep(2)
        account_groups_sub_wizard.set_client(self.client)
        account_groups_sub_wizard.set_type(self.type)
        account_groups_sub_wizard.click_on_checkmark_button()
        time.sleep(2)
        account_groups_sub_wizard.click_on_plus_button()
        time.sleep(2)
        account_groups_sub_wizard.set_client(self.client)
        account_groups_sub_wizard.set_type(self.type)
        account_groups_sub_wizard.click_on_checkmark_button()
        time.sleep(2)

    def test_context(self):
        self.precondition()
        account_groups_sub_wizard = UsersAccountGroupsSubWizard(self.web_driver_container)
        self.verify("Is 'Such record already exist' exception displayed", True,
                    account_groups_sub_wizard.is_such_record_already_exist())
