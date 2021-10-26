import time
import traceback

from custom import basic_custom_actions
from quod_qa.web_admin.web_admin_core.pages.login.login_page import LoginPage
from quod_qa.web_admin.web_admin_core.pages.root.side_menu import SideMenu
from quod_qa.web_admin.web_admin_core.pages.site.zones.zones_page import ZonesPage
from quod_qa.web_admin.web_admin_core.pages.site.zones.zones_wizard import ZonesWizard
from quod_qa.web_admin.web_admin_core.utils.web_driver_container import WebDriverContainer
from quod_qa.web_admin.web_admin_test_cases.common_test_case import CommonTestCase


class QAP_4724(CommonTestCase):

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
        page.click_on_new()
        time.sleep(2)

    def test_context(self):
        try:
            self.precondition()
            page = ZonesPage(self.web_driver_container)
            wizard = ZonesWizard(self.web_driver_container)
            wizard.click_on_save_changes()
            time.sleep(2)
            self.verify("Is incorrect or missing values message displayed", True,
                        wizard.is_incorrect_or_missing_value_message_displayed())
            try:
                page.click_on_more_actions()
            except Exception:
                self.verify("Entiy is not created (normal)", True, True)

        except Exception:
            basic_custom_actions.create_event("TEST FAILED before or after verifier", self.test_case_id,
                                              status='FAILED')
            print(traceback.format_exc() + " Search in ->  " + self.__class__.__name__)
