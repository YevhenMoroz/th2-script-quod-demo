import random
import string
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.pages.site.desks.desks_assignments_sub_wizard import DesksAssignmentsSubWizard
from test_framework.web_admin_core.pages.site.desks.desks_page import DesksPage
from test_framework.web_admin_core.pages.site.desks.desks_values_sub_wizard import DesksValuesSubWizard
from test_framework.web_admin_core.pages.site.desks.desks_wizard import DesksWizard
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T8698(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.desk_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.desk_mode = "Collaborative"
        self.ctm_bic = '12'

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_desks_page()
        main_page = DesksPage(self.web_driver_container)
        main_page.click_on_new()
        values_tab = DesksValuesSubWizard(self.web_driver_container)
        values_tab.set_name(self.desk_name)
        values_tab.set_desk_mode(self.desk_mode)
        assignments_tab = DesksAssignmentsSubWizard(self.web_driver_container)
        assignments_tab.set_location(random.choice(assignments_tab.get_all_locations_from_drop_menu()))
        wizard = DesksWizard(self.web_driver_container)
        wizard.click_on_save_changes()

    def test_context(self):
        try:
            self.precondition()

            main_page = DesksPage(self.web_driver_container)
            main_page.set_name_filter(self.desk_name)
            time.sleep(1)
            main_page.click_on_more_actions()
            main_page.click_on_edit()

            values_tab = DesksValuesSubWizard(self.web_driver_container)
            values_tab.set_ctm_bic(self.ctm_bic)

            wizard = DesksWizard(self.web_driver_container)
            wizard.click_on_save_changes()

            main_page.set_name_filter(self.desk_name)
            time.sleep(1)
            expected_result = [True, self.ctm_bic]
            actual_result = [main_page.is_desk_enable_disable(), main_page.get_ctm_bic()]
            self.verify("Desk is enabled and changes are saved", actual_result, expected_result)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
