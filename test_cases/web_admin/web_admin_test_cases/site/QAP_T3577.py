import time

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
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.desk_name = "QAP-T3577"
        self.desk_mode = "Collaborative"
        self.location = self.data_set.get_location("location_1")

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
