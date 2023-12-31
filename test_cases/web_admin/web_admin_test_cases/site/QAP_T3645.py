import random
import string
import time

from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.pages.site.zones.zones_assignments_sub_wizard import ZonesAssignmentsSubWizard
from test_framework.web_admin_core.pages.site.zones.zones_page import ZonesPage
from test_framework.web_admin_core.pages.site.zones.zones_values_sub_wizard import ZonesValuesSubWizard
from test_framework.web_admin_core.pages.site.zones.zones_wizard import ZonesWizard
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3645(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = self.data_set.get_user("user_1")
        self.password = self.data_set.get_password("password_1")
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.institution = self.data_set.get_institution("institution_1")

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_zones_page()
        time.sleep(2)
        zone_page = ZonesPage(self.web_driver_container)
        zone_page.click_on_new()
        time.sleep(1)
        values_tab = ZonesValuesSubWizard(self.web_driver_container)
        values_tab.set_name(self.name)
        assignments_tab = ZonesAssignmentsSubWizard(self.web_driver_container)
        assignments_tab.set_institution(self.institution)

    def test_context(self):
        self.precondition()
        zone_wizard = ZonesWizard(self.web_driver_container)
        zone_page = ZonesPage(self.web_driver_container)
        values_tab = ZonesValuesSubWizard(self.web_driver_container)
        zone_wizard.click_on_save_changes()
        time.sleep(2)
        zone_page.set_name(self.name)
        time.sleep(2)
        zone_page.click_on_more_actions()
        time.sleep(2)
        zone_page.click_on_edit()
        time.sleep(2)
        self.verify("Is entity saved correctly", self.name, values_tab.get_name())
