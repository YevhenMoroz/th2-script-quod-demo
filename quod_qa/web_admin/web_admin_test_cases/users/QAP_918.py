import time

from selenium.common.exceptions import TimeoutException

from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.pages.users.users.users_constants import UsersConstants
from quod_qa.web_admin.web_admin_core.pages.users.users.users_page import UsersPage
from quod_qa.web_admin.web_admin_core.pages.users.users.users_role_sub_wizard import UsersRoleSubWizard
from quod_qa.web_admin.web_admin_core.pages.users.users.users_wizard import UsersWizard
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase

#TODO: Must be edit context in Jira (for assignements tab)
class QAP_918(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm02"
        self.password = "adm02"
        self.role_id_first_input = "HeadOfInstitution"
        self.role_id_second_input = "HeadOfLocation"
        self.desks = ("Desk Market Marking FX", "Desk of Dealers 1")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_users_page()
        time.sleep(2)
        users_page = UsersPage(self.web_driver_container)
        users_page.click_on_new_button()
        time.sleep(2)
        users_wizard = UsersWizard(self.web_driver_container)
        users_wizard.click_on_save_changes()
        time.sleep(2)

    def test_context(self):

        self.precondition()
        users_wizard = UsersWizard(self.web_driver_container)
        self.verify("After click on save changes with empty values", "Incorrect or missing values",
                    users_wizard.get_incorrect_or_missing_values_exception())
        users_role_sub_wizard = UsersRoleSubWizard(self.web_driver_container)
        users_role_sub_wizard.set_role_id(self.role_id_first_input)
        time.sleep(3)
        self.verify("After set RoleID to HeadOfInstitution, desk field is disabled", False,
                    users_role_sub_wizard.is_field_enabled(UsersConstants.DESKS_AT_ROLE_SUB_WIZARD))
        self.verify("After set RoleID to HeadOfInstitution,  location field is disabled", False,
                    users_role_sub_wizard.is_field_enabled(UsersConstants.LOCATION_AT_ROLE_SUB_WIZARD))
        users_role_sub_wizard.set_role_id(self.role_id_second_input)
        time.sleep(2)
        self.verify("After set RoleID to HeadOfLocation, desk field is disabled", False,
                    users_role_sub_wizard.is_field_enabled(UsersConstants.DESKS_AT_ROLE_SUB_WIZARD))
        self.verify("After set RoleID to HeadOfLocation,  location field is enabled", True,
                    users_role_sub_wizard.is_field_enabled(UsersConstants.LOCATION_AT_ROLE_SUB_WIZARD))
        # step 5, 6
        try:
            users_role_sub_wizard.set_group("something")
            users_role_sub_wizard.set_perm_role("something")
            users_role_sub_wizard.set_perm_op("something")
            users_role_sub_wizard.set_location("something")
            users_role_sub_wizard.set_desks(tuple("something"))
        except TimeoutException as e:
            exception = e.__class__.__name__
            self.verify("Verify that group, perm role, perm op, location, "
                        "desks field cannot kept text manually", "TimeoutException", exception)
        finally:
            # step 7
            users_role_sub_wizard.set_role_id("BuySideClient")
            time.sleep(2)
            users_role_sub_wizard.click_on_desks()
            users_role_sub_wizard.set_desks(self.desks)
            self.verify("Verify that location is disabled when desks selected, ",
                        False, users_role_sub_wizard.is_field_enabled(UsersConstants.LOCATION_AT_ROLE_SUB_WIZARD))
