import random
import string
import time
import traceback

from custom import basic_custom_actions
from test_cases.web_admin.web_admin_core.pages.login.login_page import LoginPage
from test_cases.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from test_cases.web_admin.web_admin_core.pages.site.zones.zones_assignments_sub_wizard import ZonesAssignmentsSubWizard
from test_cases.web_admin.web_admin_core.pages.site.zones.zones_page import ZonesPage
from test_cases.web_admin.web_admin_core.pages.site.zones.zones_values_sub_wizard import ZonesValuesSubWizard
from test_cases.web_admin.web_admin_core.pages.site.zones.zones_wizard import ZonesWizard
from test_cases.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_4712(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm02"
        self.password = "adm02"
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.institution = "LOAD"
        self.new_institution = "QUOD FINANCIAL"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_zones_page()
        time.sleep(2)
        page = ZonesPage(self.web_driver_container)
        assignments_sub_wizard = ZonesAssignmentsSubWizard(self.web_driver_container)
        values_sub_wizard = ZonesValuesSubWizard(self.web_driver_container)
        wizard = ZonesWizard(self.web_driver_container)
        page.click_on_new()
        time.sleep(2)
        values_sub_wizard.set_name(self.name)
        time.sleep(2)
        assignments_sub_wizard.set_institution(self.institution)
        time.sleep(1)
        wizard.click_on_save_changes()
        time.sleep(2)
        page.set_name(self.name)
        time.sleep(2)
        page.click_on_more_actions()
        time.sleep(2)
        page.click_on_edit()
        time.sleep(2)
        assignments_sub_wizard.set_institution(self.new_institution)
        time.sleep(2)
        wizard.click_on_save_changes()
        time.sleep(2)
        page.set_name(self.name)
        time.sleep(2)
        page.click_on_more_actions()
        time.sleep(2)
        page.click_on_clone()
        time.sleep(2)
        wizard.click_on_close()
        time.sleep(2)
        wizard.click_on_ok_button()
        time.sleep(2)

    def test_context(self):
        try:
            self.precondition()
            page = ZonesPage(self.web_driver_container)
            try:
                page.click_on_enable_disable_button()
                time.sleep(2)
                page.click_on_enable_disable_button()
                time.sleep(2)

                self.verify("Enable / disable button works correctly", True, True)
            except Exception as e:
                self.verify("Enable / disable button works incorrectly", True, e.__class__.__name__)

            page.set_name(self.name)
            time.sleep(2)
            page.click_on_more_actions()
            time.sleep(2)

            expected_pdf_content = [self.name,
                                    self.new_institution]

            self.verify("is pdf contains correctly values", True,
                        page.click_download_pdf_entity_button_and_check_pdf(
                            expected_pdf_content))

            try:
                page.click_on_download_csv()
                self.verify("Download csv button works correctly", True, True)

            except Exception as e:
                self.verify("Download csv button works incorrectly", True, e.__class__.__name__)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
