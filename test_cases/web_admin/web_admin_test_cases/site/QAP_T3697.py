import random
import string
import sys
import time
import traceback

from custom import basic_custom_actions
from test_framework.web_admin_core.pages.login.login_page import LoginPage
from test_framework.web_admin_core.pages.root.side_menu import SideMenu
from test_framework.web_admin_core.pages.site.zones.zones_assignments_sub_wizard import ZonesAssignmentsSubWizard
from test_framework.web_admin_core.pages.site.zones.zones_page import ZonesPage
from test_framework.web_admin_core.pages.site.zones.zones_values_sub_wizard import ZonesValuesSubWizard
from test_framework.web_admin_core.pages.site.zones.zones_wizard import ZonesWizard
from test_framework.web_admin_core.utils.web_driver_container import WebDriverContainer
from test_cases.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_T3697(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id, data_set=None, environment=None):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id, data_set=data_set,
                         environment=environment)
        self.login = "adm03"
        self.password = "adm03"
        self.name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.new_name = ''.join(random.sample((string.ascii_uppercase + string.digits) * 6, 6))
        self.institution = "LOAD"
        self.new_institution = "QUOD FINANCIAL"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        side_menu.open_zones_page()
        page = ZonesPage(self.web_driver_container)
        assignments_sub_wizard = ZonesAssignmentsSubWizard(self.web_driver_container)
        values_sub_wizard = ZonesValuesSubWizard(self.web_driver_container)
        wizard = ZonesWizard(self.web_driver_container)
        page.click_on_new()
        values_sub_wizard.set_name(self.name)
        assignments_sub_wizard.set_institution(self.institution)
        wizard.click_on_save_changes()

    def test_context(self):
        page = ZonesPage(self.web_driver_container)
        assignments_sub_wizard = ZonesAssignmentsSubWizard(self.web_driver_container)
        wizard = ZonesWizard(self.web_driver_container)
        values_sub_wizard = ZonesValuesSubWizard(self.web_driver_container)

        try:
            self.precondition()

            page.set_name(self.name)
            time.sleep(1)
            page.click_on_more_actions()
            page.click_on_edit()
            values_sub_wizard.set_name(self.new_name)
            assignments_sub_wizard.set_institution(self.new_institution)
            wizard.click_on_save_changes()
            page.set_name(self.new_name)
            time.sleep(1)
            self.verify("Zone has been change", True, page.is_searched_zone_found(self.new_name))

            page.click_on_more_actions()
            page.click_on_clone()
            values_sub_wizard.set_name(self.name)
            assignments_sub_wizard.set_institution(self.institution)
            wizard.click_on_save_changes()
            page.set_name(self.name)
            time.sleep(1)
            self.verify("Zone has been clone", True, page.is_searched_zone_found(self.name))

            page.click_on_enable_disable_button()
            time.sleep(1)
            self.verify("Zone disabled", False, page.is_zone_enable())
            page.click_on_enable_disable_button()
            time.sleep(1)
            self.verify("Zone disabled", True, page.is_zone_enable())

            expected_pdf_content = [self.name, self.institution]
            self.verify("is pdf contains correctly values", True, page.click_download_pdf_entity_button_and_check_pdf(
                            expected_pdf_content))

            csv_content = page.click_on_download_csv_button_and_get_content()
            actual_result = self.name and self.name and self.institution and self.new_institution in csv_content

            self.verify("CSV file contains created and cloned entities", True, actual_result)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=2, file=sys.stdout)
            print(" Search in ->  " + self.__class__.__name__)
