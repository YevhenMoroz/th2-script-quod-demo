import time
import traceback

from custom import basic_custom_actions
from quod_qa.web_admin.web_admin_core.pages.general.common.common_page import CommonPage
from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.pages.site.institution.institutions_page import InstitutionsPage
from quod_qa.web_admin.web_admin_core.pages.site.institution.institutions_wizard import InstitutionsWizard
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_5840(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm02"
        self.password = "adm02"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_institutions_page()
        time.sleep(3)

    def test_context(self):

        try:
            self.precondition()
            common_page = CommonPage(self.web_driver_container)
            side_menu = SideMenu(self.web_driver_container)
            institution_wizard = InstitutionsWizard(self.web_driver_container)
            institution_page = InstitutionsPage(self.web_driver_container)
            institution_wizard = InstitutionsWizard(self.web_driver_container)
            common_page.click_on_full_screen_button()
            time.sleep(2)
            common_page.click_on_exit_full_screen_button()
            self.verify("Full screen button works correctly at institution", True, True)
            time.sleep(2)
            side_menu.open_zones_page()
            time.sleep(2)
            common_page.click_on_full_screen_button()
            time.sleep(2)
            common_page.click_on_exit_full_screen_button()
            time.sleep(2)
            self.verify("Full screen button works correctly at zones", True, True)
            time.sleep(2)
            side_menu.open_locations_page()
            time.sleep(2)
            common_page.click_on_full_screen_button()
            time.sleep(2)
            common_page.click_on_exit_full_screen_button()
            self.verify("Full screen button works correctly at location", True, True)
            time.sleep(2)
            side_menu.open_desks_page()
            time.sleep(2)
            common_page.click_on_full_screen_button()
            time.sleep(2)
            common_page.click_on_exit_full_screen_button()
            self.verify("Full screen button works correctly at desks", True, True)
            side_menu.open_institutions_page()
            time.sleep(2)
            common_page.click_on_full_screen_button()
            time.sleep(2)
            institution_page.click_on_new()
            time.sleep(2)
            institution_wizard.click_on_close()
            time.sleep(2)
            institution_wizard.click_on_no_button()
            time.sleep(2)
            side_menu.open_institutions_page()
            time.sleep(2)
            common_page.click_on_full_screen_button()
            time.sleep(2)
            institution_page.click_on_more_actions()
            time.sleep(2)
            institution_page.click_on_edit()
            time.sleep(2)
            institution_wizard.click_on_close()
            time.sleep(2)
            institution_wizard.click_on_ok_button()
            time.sleep(2)
            side_menu.open_institutions_page()
            time.sleep(2)
            common_page.click_on_full_screen_button()
            time.sleep(2)
            institution_page.click_on_more_actions()
            time.sleep(2)
            institution_page.click_on_clone()
            self.verify("All works correctly", True, True)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
