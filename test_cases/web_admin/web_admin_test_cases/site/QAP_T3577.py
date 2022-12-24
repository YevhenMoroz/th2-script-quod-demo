import time
import traceback
import sys

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.pages.site.desks.desks_assignments_sub_wizard import DesksAssignmentsSubWizard
from test_framework.web_admin_core.pages.site.desks.desks_page import DesksPage
from test_framework.web_admin_core.pages.site.desks.desks_values_sub_wizard import DesksValuesSubWizard
from test_framework.web_admin_core.pages.site.desks.desks_wizard import DesksWizard
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3577(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = "adm03"
        self.password = "adm03"
        self.desk_name = "QAP5695"
        self.desk_mode = "Collaborative"
        self.location = "WEST-LOCATION-A"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)
        side_menu = SideMenu(self.web_driver_container)
        main_page = DesksPage(self.web_driver_container)
        side_menu.open_desks_page()
        time.sleep(2)
        main_page.set_name_filter(self.desk_name)
        time.sleep(1)
        if not main_page.is_searched_desk_found(self.desk_name):
            main_page.click_on_new()
            time.sleep(2)
            values_sub_wizard = DesksValuesSubWizard(self.web_driver_container)
            values_sub_wizard.set_name(self.desk_name)
            values_sub_wizard.set_desk_mode(self.desk_mode)
            assignments_sub_wizard = DesksAssignmentsSubWizard(self.web_driver_container)
            assignments_sub_wizard.set_location(self.location)
            wizard = DesksWizard(self.web_driver_container)
            wizard.click_on_save_changes()
            time.sleep(2)

    def test_context(self):
        assignments_sub_wizard = DesksAssignmentsSubWizard(self.web_driver_container)
        wizard = DesksWizard(self.web_driver_container)
        try:
            self.precondition()

            main_page = DesksPage(self.web_driver_container)
            main_page.click_on_more_actions()
            time.sleep(1)
            main_page.click_on_edit()
            time.sleep(2)
            assignments_sub_wizard.clear_location_field()
            wizard.click_on_save_changes()
            time.sleep(2)
            self.verify("Is incorrect or missing values message preloaded without location field(edit)", True,
                        wizard.is_incorrect_or_missing_value_message_displayed())

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
