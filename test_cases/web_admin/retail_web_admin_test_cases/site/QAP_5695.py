import time
import traceback

from custom import basic_custom_actions
from test_cases.web_admin.web_admin_core.pages.login.login_page import LoginPage
from test_cases.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from test_cases.web_admin.web_admin_core.pages.site.desks.desks_assignments_sub_wizard import DesksAssignmentsSubWizard
from test_cases.web_admin.web_admin_core.pages.site.desks.desks_page import DesksPage
from test_cases.web_admin.web_admin_core.pages.site.desks.desks_values_sub_wizard import DesksValuesSubWizard
from test_cases.web_admin.web_admin_core.pages.site.desks.desks_wizard import DesksWizard
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_5695(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm02"
        self.password = "adm02"
        self.desk_name = "new desk"
        self.desk_mode = "Collaborative"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        main_page = DesksPage(self.web_driver_container)
        time.sleep(2)
        side_menu.open_desks_page()
        time.sleep(2)
        main_page.click_on_more_actions()
        time.sleep(2)
        main_page.click_on_edit()
        time.sleep(2)
        assignments_sub_wizard = DesksAssignmentsSubWizard(self.web_driver_container)
        values_sub_wizard = DesksValuesSubWizard(self.web_driver_container)
        assignments_sub_wizard.clear_location_field()
        time.sleep(2)
        values_sub_wizard.set_desk_mode(self.desk_mode)
        time.sleep(2)
        wizard = DesksWizard(self.web_driver_container)
        wizard.click_on_save_changes()
        time.sleep(2)

    def test_context(self):
        try:
            self.precondition()
            wizard = DesksWizard(self.web_driver_container)
            values_sub_wizard = DesksValuesSubWizard(self.web_driver_container)
            main_page = DesksPage(self.web_driver_container)
            self.verify("Is incorrect or missing values message preloaded without location field(edit)", True,
                        wizard.is_incorrect_or_missing_value_message_displayed())
            wizard.click_on_close_wizard()
            time.sleep(2)
            main_page.click_on_new()
            time.sleep(2)
            values_sub_wizard.set_name(self.desk_name)
            time.sleep(2)
            wizard.click_on_save_changes()
            self.verify("Is incorrect or missing values message preloaded without location field(new)", True,
                        wizard.is_incorrect_or_missing_value_message_displayed())



        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
