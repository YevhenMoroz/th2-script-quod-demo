import time
import traceback

from custom import basic_custom_actions
from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.pages.site.zones.zones_assignments_sub_wizard import ZonesAssignmentsSubWizard
from quod_qa.web_admin.web_admin_core.pages.site.zones.zones_page import ZonesPage
from quod_qa.web_admin.web_admin_core.pages.site.zones.zones_values_sub_wizard import ZonesValuesSubWizard
from quod_qa.web_admin.web_admin_core.pages.site.zones.zones_wizard import ZonesWizard
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_4713(CommonTestCase):

    def __init__(self, web_driver_container: WebDriverContainer, second_lvl_id):
        super().__init__(web_driver_container, self.__class__.__name__, second_lvl_id)
        self.login = "adm02"
        self.password = "adm02"

    def precondition(self):
        login_page = LoginPage(self.web_driver_container)
        login_page.login_to_web_admin(self.login, self.password)
        side_menu = SideMenu(self.web_driver_container)
        time.sleep(2)
        side_menu.open_zones_page()
        time.sleep(2)
        page = ZonesPage(self.web_driver_container)
        page.click_on_more_actions()
        time.sleep(2)
        page.click_on_edit()
        time.sleep(2)
        values_sub_wizard = ZonesValuesSubWizard(self.web_driver_container)
        first_name = values_sub_wizard.get_name()
        assignments_sub_wizard = ZonesAssignmentsSubWizard(self.web_driver_container)
        first_institution = assignments_sub_wizard.get_institution()
        wizard = ZonesWizard(self.web_driver_container)
        wizard.click_on_save_changes()
        time.sleep(2)
        page.click_on_new()
        time.sleep(2)
        values_sub_wizard.set_name(first_name)
        time.sleep(2)
        assignments_sub_wizard.set_institution(first_institution)
        time.sleep(2)
        wizard.click_on_save_changes()
        time.sleep(2)


    def test_context(self):
        try:
            self.precondition()

            wizard = ZonesWizard(self.web_driver_container)
            self.verify("such record already exist message displayed",True,wizard.is_such_record_exists_massage_displayed())


        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
