import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.users.users.users_page import UsersPage
from test_framework.web_admin_core.pages.users.users.users_wizard import UsersWizard
from test_framework.web_admin_core.pages.users.users.users_values_sub_wizard import UsersValuesSubWizard
from test_framework.web_admin_core.pages.users.users.users_user_details_sub_wizard import UsersUserDetailsSubWizard
from test_framework.web_admin_core.pages.users.users.users_assignments_sub_wizard import UsersAssignmentsSubWizard

from test_framework.web_admin_core.pages.general.common.common_page import CommonPage
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_5534(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)

        self.test_data = {
            "adm_user": {
                "login": "adm03",
                "password": "adm03"
            },
            "location_user": {
                "login": "adm_loca",
                "password": "adm_loca"
            },
            "user": {
                "user_id": 'QAP5534',
                "ext_id_client": ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6)),
                "email": '2@2',
                "desk": 'DESK A'
            }
        }

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.test_data['adm_user']['login'], self.test_data['adm_user']['password'])
        time.sleep(2)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_users_page()
        time.sleep(2)
        user_page = UsersPage(self.web_driver_container)
        user_page.set_user_id(self.test_data['user']['user_id'])
        time.sleep(2)
        if not user_page.is_searched_user_found(self.test_data['user']['user_id']):
            user_page.click_on_new_button()
            time.sleep(2)
            user_values_tab = UsersValuesSubWizard(self.web_driver_container)
            user_values_tab.set_user_id(self.test_data['user']['user_id'])
            user_values_tab.set_ext_id_client(self.test_data['user']['ext_id_client'])
            user_details_tab = UsersUserDetailsSubWizard(self.web_driver_container)
            user_details_tab.set_mail(self.test_data['user']['email'])
            user_assignments_tab = UsersAssignmentsSubWizard(self.web_driver_container)
            user_assignments_tab.set_desks([self.test_data['user']['desk']])
            user_wizard = UsersWizard(self.web_driver_container)
            user_wizard.click_on_save_changes()
            time.sleep(2)

        common_act = CommonPage(self.web_driver_container)
        common_act.click_on_user_icon()
        time.sleep(1)
        common_act.click_on_logout()
        time.sleep(2)

    def test_context(self):
        try:
            self.precondition()

            login_page = LoginPage(self.web_driver_container)
            login_page.login_to_web_admin(self.test_data['location_user']['login'],
                                          self.test_data['location_user']['password'])
            time.sleep(2)
            side_menu = SideMenu(self.web_driver_container)
            side_menu.open_users_page()
            time.sleep(2)
            user_page = UsersPage(self.web_driver_container)
            user_page.set_user_id(self.test_data['user']['user_id'])
            time.sleep(1)
            user_page.click_on_more_actions()
            time.sleep(1)
            user_page.click_on_edit_at_more_actions()
            time.sleep(2)
            user_assignments_tab = UsersAssignmentsSubWizard(self.web_driver_container)
            self.verify("Location field is disable", True, user_assignments_tab.is_location_field_enabled())

            user_assignments_tab.clear_assignments_tab()
            user_wizard = UsersWizard(self.web_driver_container)
            self.verify("User did not save with empty Assignments tab", True, user_wizard.is_warning_displayed())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
