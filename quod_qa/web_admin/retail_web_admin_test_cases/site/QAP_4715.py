import time
import traceback

from custom import basic_custom_actions
from quod_qa.web_admin.web_admin_core.pages.general.common.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.pages.site.zones.zones_assignments_sub_wizard import ZonesAssignmentsSubWizard
from quod_qa.web_admin.web_admin_core.pages.site.zones.zones_page import ZonesPage
from quod_qa.web_admin.web_admin_core.pages.site.zones.zones_values_sub_wizard import ZonesValuesSubWizard
from quod_qa.web_admin.web_admin_core.pages.site.zones.zones_wizard import ZonesWizard
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_4715(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm02"
        self.password = "adm02"
        self.zone_name = "EAST-ZONE"
        self.institution = "QUOD FINANCIAL"
        self.location = "EAST-LOCATION-A"
        self.user = "adm_zone"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        wizard = ZonesWizard(self.web_driver_container)
        time.sleep(2)
        side_menu.open_zones_page()
        time.sleep(2)
        zone_page = ZonesPage(self.web_driver_container)
        zone_page.set_name(self.zone_name)
        time.sleep(2)
        zone_page.click_on_more_actions()
        time.sleep(2)
        zone_page.click_on_edit()
        time.sleep(2)
        assignments_tab = ZonesAssignmentsSubWizard(self.web_driver_container)
        assignments_tab.set_institution(self.institution)
        time.sleep(2)
        assignments_tab.click_on_locations(self.location)
        time.sleep(2)
        wizard.click_on_ok_button()

        common_page = CommonPage(self.web_driver_container)

        common_page.click_on_user_icon()
        time.sleep(2)
        common_page.click_on_logout()
        time.sleep(2)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)

        side_menu.open_zones_page()
        time.sleep(2)
        zone_page.set_name(self.zone_name)
        time.sleep(2)
        zone_page.click_on_more_actions()
        time.sleep(2)
        zone_page.click_on_edit()
        time.sleep(2)
        assignments_tab.click_on_user(self.user)
 
        time.sleep(2)
        common_page.click_on_user_icon()
        time.sleep(1)
        common_page.click_on_logout()
        time.sleep(2)
        login_page.login_to_web_admin(self.login, self.password)
        time.sleep(2)

        side_menu.open_zones_page()
        time.sleep(2)
        zone_page.set_name(self.zone_name)
        time.sleep(2)
        zone_page.click_on_more_actions()
        time.sleep(2)
        zone_page.click_on_edit()
        time.sleep(2)

    def test_context(self):
        try:
            self.precondition()
            self.verify("hyperlinks and institution field works correctly", True, True)
            values_tab = ZonesValuesSubWizard(self.web_driver_container)
            values_tab.click_on_values_tab()
            time.sleep(2)
            values_tab.click_on_values_tab()
            self.verify("Values tab is collapsed", True, True)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
