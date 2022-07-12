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


class QAP_5452(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)

        self.test_data = {
            "adm_user": {
                "login": "adm03",
                "password": "adm03"
            },
            "test_user": {
                "login": "adm_inst",
                "password": "adm_inst"
            },
            "user": {
                "user_id": 'QAP5452',
                "ext_id_client": ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6)),
                "email": '2@2',
                "institution": 'TEST'
            },
            "desk_user": "adm_desk",
            "zone_user": "adm_zone",
            "location_user": "adm_loca"
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
            user_assignments_tab.set_institution(self.test_data['user']['institution'])
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
            login_page.login_to_web_admin(self.test_data['test_user']['login'], self.test_data['test_user']['password'])
            time.sleep(2)
            side_menu = SideMenu(self.web_driver_container)
            side_menu.open_users_page()
            time.sleep(2)
            user_page = UsersPage(self.web_driver_container)
            user_page.set_user_id(self.test_data['user']['user_id'])
            time.sleep(1)

            self.verify("User from different Institution is not displayed", False,
                        user_page.is_searched_user_found(self.test_data['user']['user_id']))

            user_page.set_user_id(self.test_data['desk_user'])
            time.sleep(1)
            self.verify("User assignee to Desk is not displayed", False,
                        user_page.is_searched_user_found(self.test_data['desk_user']))

            user_page.set_user_id(self.test_data['zone_user'])
            time.sleep(1)
            self.verify("User assignee to Zone is not displayed", False,
                        user_page.is_searched_user_found(self.test_data['zone_user']))

            user_page.set_user_id(self.test_data['location_user'])
            time.sleep(1)
            self.verify("User assignee to Location is not displayed", False,
                        user_page.is_searched_user_found(self.test_data['location_user']))

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
